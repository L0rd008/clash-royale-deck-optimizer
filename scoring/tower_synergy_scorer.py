"""
scoring/tower_synergy_scorer.py
================================
Tower Synergy Score — Section 4.5 of final_hybrid_plan.md.

Computed from deck.tower_troop + deck composition using TOWER_SYNERGY_RULES.

Returns a score in [0, 100].
→ Folded into VersatilityScorer as: min(tower_synergy_score * 0.1, 10) bonus pts.
"""

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.deck import Deck

from data.tower_synergy_rules import TOWER_SYNERGY_RULES


class TowerSynergyScorer:
    """
    Computes how well a deck composition synergises with its chosen tower troop.
    Returns a float in [0.0, 100.0].
    """

    def score(self, deck: "Deck") -> float:
        tower_id = deck.tower_troop
        if not tower_id or tower_id not in TOWER_SYNERGY_RULES:
            return 50.0  # neutral default if unknown tower

        rules = TOWER_SYNERGY_RULES[tower_id]
        cards = deck.cards
        card_ids = {c.id for c in cards}

        raw = rules.get("base_score", 50.0)
        bonus_per_pref = rules.get("bonus_per_preferred", 5.0)
        penalty_per_anti = rules.get("penalty_per_anti", 4.0)

        # ── Preferred card bonuses ─────────────────────────────────────────────
        preferred = rules.get("preferred_cards", [])
        for card_id in preferred:
            if card_id in card_ids:
                raw += bonus_per_pref

        # ── Anti-card penalties ────────────────────────────────────────────────
        anti = rules.get("anti_cards", [])
        for card_id in anti:
            if card_id in card_ids:
                raw -= penalty_per_anti

        # ── Preferred role flag bonuses ────────────────────────────────────────
        preferred_flags = rules.get("preferred_role_flags", [])
        for flag in preferred_flags:
            count_flag = sum(1 for c in cards if getattr(c, flag, False))
            if count_flag >= 1:
                raw += bonus_per_pref * 0.5  # half bonus per matching role flag

        # ── Anti role flag penalties ───────────────────────────────────────────
        anti_flags = rules.get("anti_role_flags", [])
        for flag in anti_flags:
            count_flag = sum(1 for c in cards if getattr(c, flag, False))
            if count_flag >= 2:
                raw -= penalty_per_anti * 0.5

        # ── Preferred archetype bonus (rough check via deck composition) ───────
        preferred_arch = rules.get("preferred_archetype")
        if preferred_arch == "beatdown":
            tanks = sum(1 for c in cards if c.is_tank and c.is_investment)
            if tanks >= 1:
                raw += 5.0
        elif preferred_arch == "cycle":
            cheap = sum(1 for c in cards if c.cycle_elixir <= 2)
            if cheap >= 3:
                raw += 5.0
        elif preferred_arch == "control":
            splashers = sum(1 for c in cards if c.is_splash or c.is_defensive_building)
            if splashers >= 3:
                raw += 5.0
        elif preferred_arch == "bridge_spam":
            bs = sum(1 for c in cards if c.is_bridge_spam)
            if bs >= 3:
                raw += 5.0

        return max(0.0, min(100.0, raw))
