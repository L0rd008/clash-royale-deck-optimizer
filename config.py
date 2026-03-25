"""
config.py
=========
All tunable constants for the Clash Royale Deck Optimizer.
Change values here — never hardcode them inside scoring or search modules.
"""

# ---------------------------------------------------------------------------
# Patch & Data Versioning
# ---------------------------------------------------------------------------

PATCH_VERSION = "Q1-2026-mid-march"
# ^ Must match Card.patch_version. On change, combo_cache.pkl is auto-invalidated.

# ---------------------------------------------------------------------------
# Optimizer Settings
# ---------------------------------------------------------------------------

BEAM_WIDTH = 500_000
# ^ Near-exhaustive beam width. With a 48-card pool:
#   C(48,5) = 1.7M   → depth 1–5 covered completely
#   C(48,6) = 12.3M  → ~4% sampled at depth 6 (highest-scoring 500K kept)
#   C(48,7) = 73.6M  → elite frontier preserved
# At 500K states the beam is effectively exhaustive for the quality-critical middle depths.

CANDIDATE_POOL_GLOBAL_TOP = 80
# ^ Include top-80 cards by individual score. Wider than the default 40 to ensure
# no viable card archetype is pre-filtered before the beam evaluates combinations.

CANDIDATE_POOL_WC_TOP      = 20  # Include all meta win conditions
CANDIDATE_POOL_AA_TOP      = 15  # Include all meaningful anti-air options
CANDIDATE_POOL_SPELL_TOP   = 12  # Include all playable damage spells
CANDIDATE_POOL_COUNTER_TOP = 12  # Include all meta-counter specialists

HILL_CLIMBER_PASSES = 20
# ^ Exhaustive card-swap refinement. 20 passes ensures convergence to a local
# optimum with overwhelming probability — beam search may miss near-optimal swaps
# that the climber finds when given enough iterations.

OPTIMISM_BUFFER = 1.0
# ^ Full optimism — no deflation of partial-deck estimates.
# With a 500K-wide beam, we no longer need conservative deflation to avoid
# pruning good states early. Full optimism lets the beam explore globally.

# ---------------------------------------------------------------------------
# Scoring Weights
# ---------------------------------------------------------------------------

WEIGHTS = {
    "attack":      0.30,
    "defense":     0.30,
    "synergy":     0.25,
    "versatility": 0.15,
}
# ^ Must sum to 1.0. Tower synergy is folded into versatility (bonus ≤10 pts).

# ---------------------------------------------------------------------------
# Ladder Mode
# ---------------------------------------------------------------------------

LADDER_MODE = False
# ^ True  → apply level_penalty/bonus after normalization (real-level ladder play)
# ^ False → pure Tournament Standard Level 11 evaluation (default)

LADDER_PENALTY_UNDERLEVELED = -5   # pts per is_weak_underleveled card
LADDER_BONUS_LEVEL_INDEP    = +3   # pts per is_level_independent card

# ---------------------------------------------------------------------------
# Tower Troops
# ---------------------------------------------------------------------------

TOWER_TROOPS = ["princess", "cannoneer", "dagger_duchess", "royal_chef"]
# ^ Optimizer runs once per tower troop and ranks (deck, tower) pairs.

# ---------------------------------------------------------------------------
# Combo Cache
# ---------------------------------------------------------------------------

COMBO_CACHE_PATH = "cache/combo_cache.pkl"
# ^ Relative to project root. Auto-generated on first run.

# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

OUTPUT_PATH      = "output/top_decks.json"
TOP_N_PER_TOWER  = 15          # Top decks extracted per tower before cross-tower dedup
TOP_N_DECKS      = 3           # Final number of unique decks to output
