"""
scoring/versatility_scorer.py
==============================
Versatility Score — Section 4.4 of final_hybrid_plan.md.

Formula (verbatim from plan):
  # Cycle speed
  cycle_cost = cheapest_four_elixir
  cycle_points = max(0, 16 - cycle_cost) * 5
  versatility_score += min(cycle_points, 35)

  # Elixir balance (ideal: 3.5–4.2 → centred at 3.85)
  avg = avg_elixir
  balance_points = max(0, 10 - abs(avg - 3.85) * 6)
  versatility_score += balance_points

  # Role coverage breadth (unique true boolean flags)
  roles_covered = len({flag for c in deck for flag in c.active_role_flags()})
  versatility_score += min(roles_covered * 2.5, 25)

  # Investment card bonus
  investment_count = count(card for card in deck if card.is_investment)
  versatility_score += 10 if investment_count >= 1 else 0
  versatility_score += 5  if investment_count >= 2 else 0

  # Level independence (ladder viability)
  level_indep = count(card for card in deck if card.is_level_independent)
  versatility_score += min(level_indep * 2, 10)

  # Dual-lane pressure
  if bridge_spam >= 1 and punishment_count >= 1:
      versatility_score += 5

  # Tower troop synergy (folded in)
  versatility_score += min(tower_synergy_score * 0.1, 10)

  versatility_score = min(versatility_score, 100)
"""

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.deck import Deck

# All boolean role flag names that count toward role coverage breadth
_ROLE_FLAGS = [
    "is_win_condition", "is_damage_spell", "is_anti_air",
    "is_defensive_building", "is_investment", "is_tank", "is_support",
    "is_punishment", "is_pump_response", "is_bridge_spam",
    "is_king_activator", "is_bait_card", "is_anti_air_swarm",
    "is_anti_ground_swarm", "is_splash", "is_level_independent",
]


class VersatilityScorer:
    """Computes the Versatility component score for a Deck (0–100)."""

    def score(self, deck: "Deck", tower_synergy_score: float = 50.0) -> float:
        cards = deck.cards
        s = 0.0

        # ── Cycle Speed ───────────────────────────────────────────────────────
        # cheapest_four_elixir = sum of 4 cheapest cycle_elixir values
        cycle_cost = deck.cheapest_four_elixir
        cycle_points = max(0, 16 - cycle_cost) * 5
        s += min(cycle_points, 35.0)

        # ── Elixir Balance (ideal centred at 3.85) ────────────────────────────
        avg = deck.avg_elixir
        balance_points = max(0.0, 10.0 - abs(avg - 3.85) * 6.0)
        s += balance_points

        # ── Role Coverage Breadth ─────────────────────────────────────────────
        # Unique role flags that are True across any card in the deck
        active_flags: set[str] = set()
        for c in cards:
            for flag in _ROLE_FLAGS:
                if getattr(c, flag, False):
                    active_flags.add(flag)
        roles_covered = len(active_flags)
        s += min(roles_covered * 2.5, 25.0)

        # ── Investment Card Bonus ─────────────────────────────────────────────
        investment_count = sum(1 for c in cards if c.is_investment)
        if investment_count >= 1:
            s += 10.0
        if investment_count >= 2:
            s += 5.0

        # ── Level Independence (ladder viability) ─────────────────────────────
        level_indep = sum(1 for c in cards if c.is_level_independent)
        s += min(level_indep * 2.0, 10.0)

        # ── Dual-Lane Pressure ────────────────────────────────────────────────
        bs_count = sum(1 for c in cards if c.is_bridge_spam)
        pun_count = sum(1 for c in cards if c.is_punishment)
        if bs_count >= 1 and pun_count >= 1:
            s += 5.0

        # ── Tower Troop Synergy folded in (up to 10 bonus pts) ───────────────
        s += min(tower_synergy_score * 0.1, 10.0)

        return min(s, 100.0)
