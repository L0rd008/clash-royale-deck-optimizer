"""
optimizer/constraint_checker.py
================================
Constraint Checker — wraps SlotValidator for use inside the beam search.
Section 8, Stage 3 of final_hybrid_plan.md.

Provides:
  can_add(card, partial_deck_cards) → bool
  is_complete_valid(deck) → bool
"""

from __future__ import annotations
from models.card import Card
from models.slot_validator import SlotValidator


class ConstraintChecker:
    """Delegates to SlotValidator for deck slot/base-card exclusion rules."""

    def __init__(self) -> None:
        self._validator = SlotValidator()

    def can_add(self, card: Card, current_cards: list[Card]) -> bool:
        """Return True if card can legally be added to the current partial deck."""
        return self._validator.can_add(card, current_cards)

    def is_complete_valid(self, cards: list[Card]) -> bool:
        """Return True if a complete 8-card deck satisfies all hard constraints."""
        return (
            len(cards) == 8 and
            self._validator.validate(cards).valid
        )

    def has_win_condition(self, cards: list[Card]) -> bool:
        """Return True if at least one card is a win condition (plan Stage 3 hard filter)."""
        return any(c.is_win_condition for c in cards)
