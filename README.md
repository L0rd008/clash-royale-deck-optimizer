# Clash Royale Deck Optimizer

A tournament-standard deck optimizer for Clash Royale (Q1-2026 meta). Given all 169 cards, it finds the highest-scoring 8-card decks per tower troop using beam search + hill climbing, scored across attack, defense, synergy, and versatility dimensions.

---

## Quick Start

```bash
python main.py
```

Output is written to `output/top_decks.json`. First run builds the combo cache (~30s); subsequent runs load it instantly.

---

## Updating Stats & Cards for Future Metas 🛠️

This optimizer is currently tuned for the Q1-2026 meta. As Clash Royale updates with new cards, balance changes, or tower troops, you will need to update the data layer. 

Please see the included **`reference.md`** file for the base stats and theoretical foundation. 
To update the optimizer for a new patch:
1. Update exact health, damage, and interaction parameters in the `data/cards_*.py` files.
2. Update the meta usage rates in `data/meta_weights.py`.
3. Update specific counter matchups in `data/wc_counters.py` and `data/def_counters.py`.
4. Bump the `PATCH_VERSION` in `config.py` to automatically invalidate the stale cache.

---

## Pipeline Overview

The pipeline executes these stages in order:

```
Stage 1 — Data Layer       →  169 cards, synergy matrix, meta weights, counter lists
Stage 2 — Candidate Pool   →  48-card filtered pool per tower troop
Stage 3 — Combo Cache      →  Pre-compute 2/3/4-card subset scores
Stage 4 — Beam Search      →  Build best partial decks (beam width 500k)
Stage 5 — Constraint Check →  Hard-filter: slot rules, ≥1 win condition
Stage 6 — Hill Climbing    →  Card-swap refinement (20 passes)
Stage 7 — Full Scoring     →  Final 5-component score on complete decks
Stage 8 — Analysis         →  Counter, cycle, bait reports
Stage 9 — Output           →  Deduplicate, rank, write top_decks.json
```

---

## Stage-by-Stage Detail

### Stage 1 — Data Layer (`data/`)

Provides all static data. No computation happens here — it is the authoritative source of truth loaded once at startup.

| File | Contents |
|---|---|
| `all_cards.py` | Aggregates all 169 cards into `ALL_CARDS` list + `CARD_BY_ID` dict |
| `cards_troops.py` | 79 base troop `Card` objects with simulated strengths |
| `cards_spells.py` | 21 spell `Card` objects with `ct_damage` / `ct_modifier` |
| `cards_buildings.py` | 18 defensive building `Card` objects |
| `cards_heroes.py` | 4 Hero cards (slot-typed `HERO`) |
| `cards_evolutions.py` | 47 Evolution cards (slot-typed `EVOLUTION`) |
| `cards_tower_troops.py` | 4 tower troop options (Princess, Cannoneer, Dagger Duchess, Royal Chef) |
| `synergy_matrix.py` | `SYNERGY_MATRIX` — dict of `(id_a, id_b) → float` pairwise synergy values |
| `meta_weights.py` | `META_WEIGHT` per card — ladder/tournament usage frequency multiplier |
| `wc_counters.py` | Which cards counter which win conditions |
| `def_counters.py` | Which cards counter which defensive buildings |
| `swc_counters.py` | Secondary win condition counter map |
| `tower_synergy_rules.py` | Per-tower-troop card affinity bonuses |

**Card strengths** are computed analytically from raw stats (HP, DPS, range, speed) in each `cards_*.py` helper, with manual overrides for special cards (e.g. spirits, evolutions).

---

### Stage 2 — Candidate Pool (`optimizer/card_filter.py`)

Reduces 169 cards to a filtered pool of **~89 cards** per tower troop.

**Why:** Beam search over all 169 cards would produce C(169,8) ≈ 1.2 × 10¹³ combinations. The pool applies role-quota constraints:

| Quota | Setting (`config.py`) | Default |
|---|---|---|
| Global top-N by individual score | `CANDIDATE_POOL_GLOBAL_TOP` | 80 |
| Win condition guaranteed slots | `CANDIDATE_POOL_WC_TOP` | 20 |
| Anti-air guaranteed slots | `CANDIDATE_POOL_AA_TOP` | 15 |
| Damage spell guaranteed slots | `CANDIDATE_POOL_SPELL_TOP` | 12 |
| Meta counter specialists | `CANDIDATE_POOL_COUNTER_TOP` | 5 |

Cards qualifying under multiple quotas are deduplicated. The resulting pool ensures role diversity regardless of individual score ranks.

---

### Stage 3 — Combo Cache (`optimizer/combo_cache.py`)

Pre-computes `ComboScore` objects for all card subsets of size 2, 3, and (role-valid) 4 in the candidate pool.

**Stored in:** `cache/combo_cache.pkl` — keyed by `PATCH_VERSION` and `config.WEIGHTS` hash; auto-invalidated on config change.

Each `ComboScore` (`models/combo_score.py`) contains:

| Field | Description |
|---|---|
| `card_ids` | Frozenset of card IDs in this combo |
| `elixir_total` / `avg_elixir` | Elixir cost metrics |
| `roles_covered` | Union of all role flags in the combo |
| `synergy_sum` | Sum of SYNERGY_MATRIX pairwise values |
| `bait_chains` | Dict of `spell_id → count` for bait interactions |
| `has_win_condition` | True if any combo card is a win condition |
| `spell_ct_damage_total` | Total CT damage potential from spells |
| `counter_wc_coverage` | Set of meta WCs this combo can counter |
| `attack_contribution` / `defense_contribution` | Partial scoring config-scaled estimates |

**4-card combos** are filtered to role-valid subsets only (≤2 win conditions, ≥1 anti-air) to keep cache size manageable.

---

### Stage 4 — Beam Search (`optimizer/beam_search.py`)

Builds 8-card decks card-by-card using beam search, guided by optimistic partial-deck scores.

**Algorithm:**
1. Start with an empty state (0 cards chosen).
2. At each depth step, expand every partial deck by every card in the pool.
3. Score each expanded partial deck via `PartialScorer` (Stage 4a).
4. Keep only the top `BEAM_WIDTH` (default: 500,000) states.
5. Repeat until states have 8 cards.
6. Return the top-N complete decks.

**Partial scoring** (`optimizer/partial_scorer.py`) uses combo cache lookups for sub-deck contributions plus an *optimism buffer* (`OPTIMISM_BUFFER = 1.0`) — a deflation factor that prevents over-estimating the value of unfilled slots.

---

### Stage 5 — Constraint Checking (`optimizer/constraint_checker.py`)

Hard filters applied at every beam expansion step and on complete decks.

**Slot rules** (delegated to `models/slot_validator.py`):

| Rule | Limit |
|---|---|
| Maximum Evolutions | 2 |
| Maximum Heroes | 1 (absolute hard lock) |
| Evo + Hero + Wild combined | ≤ 3 |
| Base card cannot coexist with its Evo/Hero variant | enforced |
| No duplicate card IDs | enforced |

**Win condition filter:** Every complete deck must contain **≥ 1 win condition** card. Decks without one are discarded regardless of score.

---

### Stage 6 — Hill Climbing (`optimizer/hill_climber.py`)

Applies 1-card-swap refinement to the beam search output to escape local optima.

**Algorithm (per deck, up to 20 passes):**
1. For each card in the deck (positions 0–7):
   - Try replacing it with every candidate pool card not already in the deck.
   - Validate the swap with `SlotValidator`.
   - Accept the swap if it raises `total_score` AND the deck still has ≥1 win condition.
2. Repeat until no improvement is found or `HILL_CLIMBER_PASSES` is exhausted.

---

### Stage 7 — Full Scoring (`scoring/`)

Scores complete 8-card decks across 5 components, combined into a weighted total.

```
total_score = 100 × (
    0.30 × attack_score    +
    0.30 × defense_score   +
    0.25 × synergy_score   +
    0.15 × versatility_score
) + tower_synergy_bonus (≤10 pts)
```

Weights are set in `config.py → WEIGHTS` and can be freely adjusted.

| Component | File | What it measures |
|---|---|---|
| **Attack** | `attack_scorer.py` | Win condition strength, spell CT damage, bridge-spam potential, punishment coverage |
| **Defense** | `defense_scorer.py` | Anti-air coverage, defensive buildings, tank-killing, counter score vs meta WCs |
| **Synergy** | `synergy_scorer.py` | Pairwise SYNERGY_MATRIX sum, bait chain bonus, structural role fit, anti-synergy penalty |
| **Versatility** | `versatility_scorer.py` | Role breadth, cycle speed, elixir balance, level-independence, ladder modifier |
| **Tower Synergy** | `tower_synergy_scorer.py` | Tower-troop-specific card affinity bonuses (additive, ≤10 pts) |

**Ladder mode** (`LADDER_MODE = False` by default): when enabled, applies a −5 pt penalty per underleveled card and a +3 pt bonus per level-independent card.

---

### Stage 8 — Analysis (`analysis/`)

Generates a structured breakdown of each top deck.

| Module | Output |
|---|---|
| `counter_analyzer.py` | WC coverage %, defensive coverage %, secondary WC coverage % |
| `cycle_analyzer.py` | Avg elixir, cheapest-4-card cycle cost, cycle speed score, elixir variance |
| `bait_analyzer.py` | Bait chains per spell, bait score, is_bait_deck flag |
| `deck_report.py` | Aggregates all analysis + component scores into a single report dict |

---

### Stage 9 — Output (`output/top_decks.json`)

The optimizer runs independently for each of the 4 tower troops, produces top-3 decks each, then cross-deduplicates to remove decks whose card sets are identical across towers. The remaining best decks are ranked globally and written to JSON.

**Output fields per deck:**

```jsonc
{
  "rank": 1,
  "tower_troop": "dagger_duchess",
  "total_score": 89.52,
  "component_scores": { "attack": 87.16, "defense": 96.14, ... },
  "counter_analysis": { "wc_coverage": 81.5, ... },
  "cycle_analysis":   { "avg_elixir": 3.12, "cheapest_four": 9, ... },
  "bait_analysis":    { "bait_chains": {"the_log": 2}, ... },
  "cards": [ { "id": "hog_rider", "name": "Hog Rider", "elixir": 4, "roles": [...] }, ... ]
}
```

---

## Configuration Reference (`config.py`)

| Setting | Default | Description |
|---|---|---|
| `PATCH_VERSION` | `"Q1-2026-mid-march"` | Card data version; changing it auto-invalidates the cache |
| `BEAM_WIDTH` | `500,000` | Beam search width — increase for better quality, higher runtime |
| `CANDIDATE_POOL_GLOBAL_TOP` | `80` | Top-N cards by score in the global pool |
| `CANDIDATE_POOL_WC_TOP` | `20` | Guaranteed win condition slots |
| `CANDIDATE_POOL_AA_TOP` | `15` | Guaranteed anti-air slots |
| `CANDIDATE_POOL_SPELL_TOP` | `12` | Guaranteed damage spell slots |
| `HILL_CLIMBER_PASSES` | `20` | Post-beam refinement passes |
| `OPTIMISM_BUFFER` | `1.0` | Partial deck optimism deflation (1.0 = fully optimistic) |
| `WEIGHTS` | `{atk:0.35, def:0.25, syn:0.25, ver:0.15}` | Score component weights (must sum to 1.0) |
| `LADDER_MODE` | `False` | Enable ladder-level penalties/bonuses |
| `TOWER_TROOPS` | all 4 | Tower troops to optimize for |
| `TOP_N_DECKS` | `3` | Top decks to output per tower before deduplication |

---

## Testing

```bash
python -m pytest tests/ -q
```

---

## Requirements

- Python 3.11+
- `pytest` (for tests only)
