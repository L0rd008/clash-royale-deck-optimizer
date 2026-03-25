"""
optimizer/card_filter.py
=========================
Stratified Card Filter — Section 8, Stage 1 of final_hybrid_plan.md.

Builds CANDIDATE_POOL via stratified pools:
  global_pool   = top 40 by individual_score
  wc_pool       = top 8 win conditions (role-guaranteed)
  anti_air_pool = top 6 anti-air cards
  spell_pool    = top 6 damage spells
  counter_pool  = top 5 counter-specialists for current meta

CANDIDATE_POOL = deduplicate(all pools)

individual_score(card) =
    sum(continuous strength fields) * 8
    + count(true bool flags) * 3
    + card.meta_weight * 15
    + elixir_efficiency(card)          # DPS / cycle_elixir, normalized
    + len(SYNERGY_MATRIX entries for card) * 0.5

Stage 2 — Constraint-Based Pruning (pool-level hard requirements):
  Pool must contain ≥ 1 win condition
  Pool must contain ≥ 2 anti-air cards
  Pool must contain ≥ 1 damage spell
  Pool must contain ≥ 1 defensive building
"""

from __future__ import annotations
from typing import TYPE_CHECKING

import config
from models.card import Card
from data.synergy_matrix import SYNERGY_MATRIX

if TYPE_CHECKING:
    pass

# All continuous-strength fields (plan §8 individual_score formula)
_STRENGTH_FIELDS = [
    "win_condition_strength", "anti_air_strength", "punish_strength",
    "bridge_spam_strength", "tank_strength", "support_strength",
    "cycle_strength", "splash_strength",
]

# All boolean role flags (for counting true flags)
_BOOL_FLAGS = [
    "is_win_condition", "is_damage_spell", "is_anti_air",
    "is_defensive_building", "is_investment", "is_tank", "is_support",
    "is_punishment", "is_pump_response", "is_bridge_spam",
    "is_king_activator", "is_bait_card", "is_anti_air_swarm",
    "is_anti_ground_swarm", "is_splash", "is_level_independent",
]


def individual_score(card: Card, synergy_degree: dict[str, int]) -> float:
    """
    Compute individual card score per plan §8:
      strengths * 8 + flag_count * 3 + meta_weight * 15
      + elixir_efficiency + synergy_degree * 0.5
    """
    strength_sum = sum(getattr(card, f, 0.0) for f in _STRENGTH_FIELDS)
    flag_count   = sum(1 for f in _BOOL_FLAGS if getattr(card, f, False))
    meta_pts     = card.meta_weight * 15.0

    # Elixir efficiency: DPS / cycle_elixir, normalized vs reference of 80 DPS/e
    if card.cycle_elixir > 0 and card.dps > 0:
        elixir_eff = min((card.dps / card.cycle_elixir) / 80.0 * 10.0, 10.0)
    else:
        elixir_eff = 0.0

    syn_deg = synergy_degree.get(card.id, 0)

    return (
        strength_sum * 8.0 +
        flag_count * 3.0 +
        meta_pts +
        elixir_eff +
        syn_deg * 0.5
    )


def _synergy_degree(cards: list[Card]) -> dict[str, int]:
    """Count how many SYNERGY_MATRIX entries each card ID appears in."""
    deg: dict[str, int] = {}
    for (a, b) in SYNERGY_MATRIX:
        deg[a] = deg.get(a, 0) + 1
        deg[b] = deg.get(b, 0) + 1
    return deg


def build_candidate_pool(all_cards: list[Card]) -> list[Card]:
    """
    Build stratified candidate pool per plan §8 Stage 1 + 2.
    Returns a deduplicated list of Card objects sorted by individual_score desc.

    Raises RuntimeError if Stage 2 hard constraints cannot be satisfied.
    """
    syn_deg = _synergy_degree(all_cards)
    scores  = {c.id: individual_score(c, syn_deg) for c in all_cards}

    by_score = sorted(all_cards, key=lambda c: scores[c.id], reverse=True)

    # ── Stratified pools ──────────────────────────────────────────────────────
    global_pool   = by_score[:config.CANDIDATE_POOL_GLOBAL_TOP]

    wc_pool = [c for c in by_score if c.is_win_condition
               ][:config.CANDIDATE_POOL_WC_TOP]

    aa_pool = [c for c in by_score if c.is_anti_air
               ][:config.CANDIDATE_POOL_AA_TOP]

    spell_pool = [c for c in by_score if c.is_damage_spell
                  ][:config.CANDIDATE_POOL_SPELL_TOP]

    # Counter specialists: highest meta_weight cards that counter many WCs
    counter_pool = sorted(
        [c for c in all_cards if c.counters_win_conditions],
        key=lambda c: (len(c.counters_win_conditions) * c.meta_weight),
        reverse=True
    )[:config.CANDIDATE_POOL_COUNTER_TOP]

    # ── Deduplicate (preserve order: global first, then role extras) ──────────
    seen: set[str] = set()
    pool: list[Card] = []
    for c in global_pool + wc_pool + aa_pool + spell_pool + counter_pool:
        if c.id not in seen:
            seen.add(c.id)
            pool.append(c)

    # ── Stage 2: Pool-level hard requirement checks ───────────────────────────
    if not any(c.is_win_condition for c in pool):
        raise RuntimeError(
            "CandidatePool violates Stage 2: no win condition cards in pool."
        )
    if sum(1 for c in pool if c.is_anti_air) < 2:
        raise RuntimeError(
            "CandidatePool violates Stage 2: < 2 anti-air cards in pool."
        )
    if not any(c.is_damage_spell for c in pool):
        raise RuntimeError(
            "CandidatePool violates Stage 2: no damage spells in pool."
        )
    if not any(c.is_defensive_building for c in pool):
        raise RuntimeError(
            "CandidatePool violates Stage 2: no defensive building in pool."
        )

    # Return sorted by score for display/debugging convenience
    return sorted(pool, key=lambda c: scores.get(c.id, 0.0), reverse=True)
