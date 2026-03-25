"""
models/slot_validator.py
========================
Validates Clash Royale 2026 slot constraints for any deck or partial deck.

Hard rules (from final_hybrid_plan.md, Section 1):
  - Max 2 Evolutions total (Evo slot + Wild slot as Evo)
  - Max 1 Hero  ← ABSOLUTE HARD LOCK per problem_description.md
    (approach_3 Configs C and E — double Hero — are DISABLED)
  - Evo + Hero + Wild ≤ 3 special slots combined
  - If a card appears in Evo or Hero form, its base card ID cannot also appear
  - A complete deck has exactly 8 cards

Valid configurations:
  Config A: 1 Evo + 1 Hero + 6 base cards   (1E1H + wild as Evo → Config B)
  Config B: 2 Evos + 1 Hero + 5 base cards
  Config D: 2 Evos + 0 Heroes + 6 base cards
  Config F: 0 Evos + 1 Hero + 7 base cards
  Config G: 1 Evo + 0 Heroes + 7 base cards
  Config H: 0 Evos + 0 Heroes + 8 base cards
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from models.card import Card, SlotType


# ---------------------------------------------------------------------------
# Validation Result
# ---------------------------------------------------------------------------

@dataclass
class ValidationResult:
    valid: bool
    errors: list[str]

    def __bool__(self) -> bool:
        return self.valid

    def __repr__(self) -> str:
        if self.valid:
            return "ValidationResult(valid=True)"
        return f"ValidationResult(valid=False, errors={self.errors})"


# ---------------------------------------------------------------------------
# SlotValidator
# ---------------------------------------------------------------------------

class SlotValidator:
    """
    Stateless validator for Clash Royale 2026 slot constraints.

    Usage:
        result = SlotValidator.validate(cards)
        if not result:
            print(result.errors)

        # During beam search — check if adding one more card is still legal:
        ok = SlotValidator.can_add(candidate_card, existing_cards)
    """

    MAX_EVOLUTIONS: int = 2
    MAX_HEROES: int = 1       # Hard lock — problem_description.md constraint
    MAX_SPECIAL: int = 3      # Evo + Hero + Wild combined

    # -----------------------------------------------------------------------
    # Full Deck Validation
    # -----------------------------------------------------------------------

    @classmethod
    def validate(cls, cards: list[Card], require_complete: bool = True) -> ValidationResult:
        """
        Validate a full (or partial) list of cards against all slot rules.

        Args:
            cards: List of Card objects in the deck (should be 8 for a complete deck).
            require_complete: If True, also checks that len(cards) == 8.

        Returns:
            ValidationResult — .valid is True iff all constraints pass.
        """
        errors: list[str] = []

        evo_count  = sum(1 for c in cards if c.slot_type == SlotType.EVOLUTION)
        hero_count = sum(1 for c in cards if c.slot_type == SlotType.HERO)
        special    = evo_count + hero_count

        # --- Max Hero check (most critical) ---
        if hero_count > cls.MAX_HEROES:
            errors.append(
                f"Hero count {hero_count} exceeds maximum of {cls.MAX_HEROES}. "
                f"Double-Hero configurations (Configs C/E) are disabled."
            )

        # --- Max Evo check ---
        if evo_count > cls.MAX_EVOLUTIONS:
            errors.append(
                f"Evolution count {evo_count} exceeds maximum of {cls.MAX_EVOLUTIONS}."
            )

        # --- Special slot total ---
        if special > cls.MAX_SPECIAL:
            errors.append(
                f"Total special slots used ({special}) exceeds maximum of "
                f"{cls.MAX_SPECIAL} (Evo + Hero + Wild)."
            )

        # --- Base card exclusion ---
        exclusion_errors = cls._check_base_exclusions(cards)
        errors.extend(exclusion_errors)

        # --- Duplicate card check ---
        dup_errors = cls._check_duplicates(cards)
        errors.extend(dup_errors)

        # --- Complete deck size ---
        if require_complete and len(cards) != 8:
            errors.append(
                f"Deck has {len(cards)} cards; exactly 8 are required."
            )

        return ValidationResult(valid=len(errors) == 0, errors=errors)

    # -----------------------------------------------------------------------
    # Partial Deck Check (used during beam search)
    # -----------------------------------------------------------------------

    @classmethod
    def can_add(cls, candidate: Card, existing: list[Card]) -> bool:
        """
        Returns True if `candidate` can legally be added to `existing` cards
        without violating any slot constraint.

        Does NOT check for deck completeness (since the deck is partial).
        This is the fast path used in beam_search.py.
        """
        combined = existing + [candidate]

        evo_count  = sum(1 for c in combined if c.slot_type == SlotType.EVOLUTION)
        hero_count = sum(1 for c in combined if c.slot_type == SlotType.HERO)
        special    = evo_count + hero_count

        if hero_count > cls.MAX_HEROES:
            return False
        if evo_count > cls.MAX_EVOLUTIONS:
            return False
        if special > cls.MAX_SPECIAL:
            return False

        # Check base card exclusions for the new candidate specifically
        if cls._check_base_exclusions(combined):
            return False

        # Check for duplicate card ids
        if cls._check_duplicates(combined):
            return False

        return True

    # -----------------------------------------------------------------------
    # Config Name
    # -----------------------------------------------------------------------

    @classmethod
    def slot_config_name(cls, cards: list[Card]) -> str:
        """
        Returns the slot configuration code for a given card list.
        E.g. "2E1H", "1E0H", "0E0H"
        """
        evo_count  = sum(1 for c in cards if c.slot_type == SlotType.EVOLUTION)
        hero_count = sum(1 for c in cards if c.slot_type == SlotType.HERO)
        return f"{evo_count}E{hero_count}H"

    # -----------------------------------------------------------------------
    # Internal Helpers
    # -----------------------------------------------------------------------

    @classmethod
    def _check_base_exclusions(cls, cards: list[Card]) -> list[str]:
        """
        A card and its Evo/Hero variant cannot coexist in the same deck.

        Rule: for any Evo or Hero card with a base_card_id set,
        no card in the deck may have an id equal to that base_card_id.
        """
        errors: list[str] = []
        base_card_ids_in_deck = {c.id for c in cards if c.slot_type == SlotType.BASE}
        evo_hero_base_refs = {
            c.base_card_id for c in cards
            if c.slot_type in (SlotType.EVOLUTION, SlotType.HERO)
            and c.base_card_id is not None
        }

        conflicts = base_card_ids_in_deck & evo_hero_base_refs
        for conflict_id in sorted(conflicts):
            errors.append(
                f"Conflict: base card '{conflict_id}' is present alongside "
                f"its Evo/Hero variant."
            )
        return errors

    @classmethod
    def _check_duplicates(cls, cards: list[Card]) -> list[str]:
        """No two cards may share the same id."""
        errors: list[str] = []
        seen: dict[str, int] = {}
        for c in cards:
            seen[c.id] = seen.get(c.id, 0) + 1
        for card_id, count in seen.items():
            if count > 1:
                errors.append(f"Duplicate card: '{card_id}' appears {count} times.")
        return errors
