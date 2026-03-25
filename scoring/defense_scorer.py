"""
scoring/defense_scorer.py
==========================
Defense Score — Section 4.2 of final_hybrid_plan.md.

Formula (verbatim from plan):
  defense_score = 0.0

  # Anti-air (hard threshold + continuous strength)
  anti_air_hard = count(card for card in deck if card.is_anti_air)
  defense_score += 25 if anti_air_hard >= 2 else 12 if anti_air_hard == 1 else 0
  anti_air_strength_sum = sum(c.anti_air_strength for c in deck)
  defense_score += min(anti_air_strength_sum * 3, 8)   # up to 8 bonus pts

  # Defensive buildings
  def_bldg = count(card for card in deck if card.is_defensive_building)
  defense_score += 20 if def_bldg >= 1 else 0

  # Anti-ground swarm + splash
  anti_gs = count(card for card in deck if card.is_anti_ground_swarm)
  defense_score += 12 if anti_gs >= 2 else 6 if anti_gs == 1 else 0
  anti_as = count(card for card in deck if card.is_anti_air_swarm)
  defense_score += 8 if anti_as >= 1 else 0
  splash = count(card for card in deck if card.is_splash)
  defense_score += min(splash * 5, 15)

  # HP buffer (troops/buildings only)
  total_hp = sum(c.hp for c in deck if c.hp and c.card_type != CardType.SPELL)
  hp_score = min((total_hp / 20000) * 15, 15)
  defense_score += hp_score

  # King Tower activation bonus
  king_act = count(card for card in deck if card.is_king_activator)
  defense_score += min(king_act * 5, 10)

  defense_score = min(defense_score, 100)
"""

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.deck import Deck

from models.card import CardType


class DefenseScorer:
    """Computes the Defense component score for a Deck (0–100)."""

    def score(self, deck: "Deck") -> float:
        cards = deck.cards
        s = 0.0

        # ── Anti-Air ──────────────────────────────────────────────────────────
        anti_air_hard = sum(1 for c in cards if c.is_anti_air)
        if anti_air_hard >= 2:
            s += 25
        elif anti_air_hard == 1:
            s += 12

        anti_air_strength_sum = sum(c.anti_air_strength for c in cards)
        s += min(anti_air_strength_sum * 3.0, 8.0)

        # ── Defensive Buildings ───────────────────────────────────────────────
        def_bldg = sum(1 for c in cards if c.is_defensive_building)
        s += 20 if def_bldg >= 1 else 0

        # ── Anti-Ground Swarm + Splash ────────────────────────────────────────
        anti_gs = sum(1 for c in cards if c.is_anti_ground_swarm)
        if anti_gs >= 2:
            s += 12
        elif anti_gs == 1:
            s += 6

        anti_as = sum(1 for c in cards if c.is_anti_air_swarm)
        s += 8 if anti_as >= 1 else 0

        splash = sum(1 for c in cards if c.is_splash)
        s += min(splash * 5.0, 15.0)

        # ── HP Buffer (troops & buildings only — spells contribute 0 HP) ──────
        total_hp = sum(
            c.hp for c in cards
            if c.hp and c.card_type != CardType.SPELL
        )
        hp_score = min((total_hp / 20000.0) * 15.0, 15.0)
        s += hp_score

        # ── King Tower Activation (was dead code in approach_3 — now live) ───
        king_act = sum(1 for c in cards if c.is_king_activator)
        s += min(king_act * 5.0, 10.0)

        return min(s, 100.0)
