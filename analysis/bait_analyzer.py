"""
analysis/bait_analyzer.py
==========================
Bait Analyzer — Section 9.3 of final_hybrid_plan.md.

A bait deck exploits spell mismatches so opponent wastes big spells on
small threats (or has no answer for key threats).

Metrics computed:
  bait_chains:   dict mapping spell_id → count of cards that bait it
  bait_score:    graduated (plan fix §4.3): single-bait=5pts, double=14pts
  bait_spells:   set of spells the deck baits (which opponent needs to cycle)
  all_bait:      True if deck baits every major meta spell (arrows, log, zap, fireball)
"""

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.deck import Deck

_META_SPELLS = {"arrows", "the_log", "zap", "fireball", "snowball", "giant_snowball"}


class BaitAnalyzer:
    """Analyzes spell-bait chains in a deck."""

    def analyze(self, deck: "Deck") -> dict:
        cards = deck.cards

        # Collect all unique spells present in deck (for bait chain checking)
        spell_ids_in_deck = {c.id for c in cards if c.is_damage_spell}

        # Build bait chain: how many cards bait each spell
        chains: dict[str, list[str]] = {}
        for card in cards:
            for spell_id in card.bait_spells:
                chains.setdefault(spell_id, []).append(card.id)

        # Bait score (graduated — plan fix §4.3)
        bait_score = 0.0
        for spell_id, baiters in chains.items():
            n = len(baiters)
            if n == 1:
                bait_score += 5.0
            elif n >= 2:
                bait_score += 14.0

        # Which meta spells does the deck bait?
        baited_meta = {s for s in chains if s in _META_SPELLS}

        # Classic bait deck: baits arrows + log (or zap)
        is_bait_deck = (
            "arrows" in chains and
            ("the_log" in chains or "zap" in chains) and
            len(chains) >= 3
        )

        return {
            "bait_chains":    {k: len(v) for k, v in chains.items()},
            "bait_score":     round(bait_score, 1),
            "baited_spells":  list(chains.keys()),
            "baited_meta":    list(baited_meta),
            "is_bait_deck":   is_bait_deck,
            "all_meta_baited": baited_meta.issuperset(
                {"arrows", "the_log", "zap", "fireball"}
            ),
        }
