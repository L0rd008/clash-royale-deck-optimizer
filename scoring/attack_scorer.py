"""
scoring/attack_scorer.py
=========================
Attack Score — Section 4.1 of final_hybrid_plan.md.

Formula (verbatim from plan):
  attack_score = 0.0

  # Win conditions (hard flag)
  wc_hard = count(card for card in deck if card.is_win_condition)
  attack_score += 35 if wc_hard >= 1 else 0
  attack_score += 10 if wc_hard >= 2 else 0

  # Win condition quality (continuous strength)
  wc_strength_sum = sum(c.win_condition_strength for c in deck)
  attack_score += min(wc_strength_sum * 5, 10)   # up to 10 bonus pts

  # Damage spells — weighted by actual CT damage, not flat count
  spell_ct_total = sum(c.ct_damage for c in deck if c.is_damage_spell)
  ct_score = min((spell_ct_total / 500) * 20, 20)
  attack_score += ct_score

  # Punishment potential
  punish_score = sum(c.punish_strength for c in deck if c.is_punishment)
  attack_score += min(punish_score * 4, 10)

  # Bridge spam
  bridge_score = sum(c.bridge_spam_strength for c in deck if c.is_bridge_spam)
  attack_score += min(bridge_score * 3, 9)

  # Pump response
  pump = count(card for card in deck if card.is_pump_response)
  attack_score += min(pump * 2, 6)

  attack_score = min(attack_score, 100)
"""

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.deck import Deck


class AttackScorer:
    """Computes the Attack component score for a Deck (0–100)."""

    def score(self, deck: "Deck") -> float:
        cards = deck.cards
        s = 0.0

        # ── Win Conditions (hard flag) ─────────────────────────────────────────
        wc_hard = sum(1 for c in cards if c.is_win_condition)
        s += 35 if wc_hard >= 1 else 0
        s += 10 if wc_hard >= 2 else 0

        # ── Win-condition quality (continuous strength) ────────────────────────
        wc_strength_sum = sum(c.win_condition_strength for c in cards)
        s += min(wc_strength_sum * 5, 10)

        # ── Damage Spells — CT-damage weighted (plan fix §4.1) ────────────────
        # Fireball=207, Log=41, Zap=58, Earthquake=159, Poison=180, Lightning=317
        # Budget reference ≈ 500 CT dmg → normalized over that
        spell_ct_total = sum(c.ct_damage for c in cards if c.is_damage_spell)
        ct_score = min((spell_ct_total / 500.0) * 20.0, 20.0)
        s += ct_score

        # ── Punishment potential ───────────────────────────────────────────────
        punish_score = sum(
            c.punish_strength for c in cards if c.is_punishment
        )
        s += min(punish_score * 4.0, 10.0)

        # ── Bridge spam ────────────────────────────────────────────────────────
        bridge_score = sum(
            c.bridge_spam_strength for c in cards if c.is_bridge_spam
        )
        s += min(bridge_score * 3.0, 9.0)

        # ── Pump response ──────────────────────────────────────────────────────
        pump = sum(1 for c in cards if c.is_pump_response)
        s += min(pump * 2.0, 6.0)

        return min(s, 100.0)
