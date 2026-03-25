"""
optimizer/partial_scorer.py
============================
Partial Deck Scorer — Section 8, Stage 3 of final_hybrid_plan.md.

Used by beam search to estimate quality of incomplete decks.
Applies an optimism_buffer (0.8×) on role-gap bonuses so that
expensive early cards are not over-committed to (plan fix §8).

partial_score(cards, depth) = actual_score_of_partial +
    optimism_buffer × estimated_remaining_bonus
"""

from __future__ import annotations
from typing import TYPE_CHECKING

import config
from models.card import Card, CardType
from data.synergy_matrix import SYNERGY_MATRIX
from itertools import combinations

if TYPE_CHECKING:
    pass

# Maximum per-role bonus we optimistically hope remaining cards add
_ROLE_BONUS = {
    "has_wc":        35.0,
    "has_aa":        25.0,
    "has_spell":     20.0,
    "has_def_bldg":  20.0,
    "has_splash":    15.0,
    "has_tank":       8.0,
}

_STRUCT_BONUS = 35.0   # max structural synergy estimate per remaining card


class PartialScorer:
    """
    Scores an incomplete deck with an optimistic estimate of what remaining
    cards could contribute.  Returns a float suitable for beam ranking.
    """

    def score(self, cards: list[Card], depth: int) -> float:
        """
        Args:
            cards: list of Card objects already chosen (len == depth).
            depth: number of cards chosen so far (1–8).

        Returns:
            Estimated final score (higher = better candidate).
        """
        buf = config.OPTIMISM_BUFFER  # 0.8 per plan

        # ── Actual earned points from chosen cards ────────────────────────────
        earned = self._earned_score(cards)

        # ── Optimistic bonus for what remaining slots could contribute ────────
        remaining = 8 - depth
        if remaining <= 0:
            return earned

        # Identify which key roles are still MISSING from partial deck
        missing_bonus = 0.0
        if not any(c.is_win_condition for c in cards):
            missing_bonus += _ROLE_BONUS["has_wc"]
        if sum(1 for c in cards if c.is_anti_air) < 2:
            aa_deficit = 2 - sum(1 for c in cards if c.is_anti_air)
            missing_bonus += _ROLE_BONUS["has_aa"] * min(aa_deficit, remaining) / 2
        if not any(c.is_damage_spell for c in cards):
            missing_bonus += _ROLE_BONUS["has_spell"]
        if not any(c.is_defensive_building for c in cards):
            missing_bonus += _ROLE_BONUS["has_def_bldg"]
        if not any(c.is_splash for c in cards):
            missing_bonus += _ROLE_BONUS["has_splash"]
        if not any(c.is_tank for c in cards):
            missing_bonus += _ROLE_BONUS["has_tank"]

        # Structural synergy optimistic estimate (per remaining slot)
        synergy_est = remaining * (_STRUCT_BONUS / 8.0)

        return earned + buf * (missing_bonus + synergy_est)

    def _earned_score(self, cards: list[Card]) -> float:
        """Compute actual attack + defense + synergy contribution so far."""
        s = 0.0

        # WC contribution
        wc = sum(1 for c in cards if c.is_win_condition)
        s += 35 if wc >= 1 else 0
        s += 10 if wc >= 2 else 0
        s += min(sum(c.win_condition_strength for c in cards) * 5, 10)

        # CT damage (spell pressure)
        ct = sum(c.ct_damage for c in cards if c.is_damage_spell)
        s += min((ct / 500.0) * 20.0, 20.0)

        # Anti-air
        aa = sum(1 for c in cards if c.is_anti_air)
        s += 25 if aa >= 2 else (12 if aa == 1 else 0)
        s += min(sum(c.anti_air_strength for c in cards) * 3, 8)

        # Defensive buildings
        db = sum(1 for c in cards if c.is_defensive_building)
        s += 20 if db >= 1 else 0

        # Pairwise synergy earned so far
        for c1, c2 in combinations(cards, 2):
            key = (c1.id, c2.id) if c1.id < c2.id else (c2.id, c1.id)
            s += SYNERGY_MATRIX.get(key, 0.0) * 10.0

        # HP buffer (proportional of target 20000)
        total_hp = sum(c.hp for c in cards if c.hp and c.card_type != CardType.SPELL)
        s += min((total_hp / 20000.0) * 15.0, 15.0)

        return s
