"""
models/deck.py
==============
Deck dataclass for the Clash Royale Deck Optimizer.
Architecture: Final Hybrid Plan v2.0 — Q1 2026 Meta.

Key design decisions:
  - tower_troop is a first-class field (not external).
  - avg_elixir and cycle calculations always use card.cycle_elixir (base only).
  - No hero_wild_slot field — max 1 hero is an absolute constraint.
  - Scores are populated by DeckScorer after construction.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from models.card import Card, CardType, SlotType
from models.slot_validator import SlotValidator, ValidationResult


# ---------------------------------------------------------------------------
# Deck Dataclass
# ---------------------------------------------------------------------------

@dataclass
class Deck:
    """
    Represents a complete Clash Royale deck (exactly 8 cards).

    Slot fields track which card occupies each special slot.
    Score fields are populated externally by DeckScorer.
    """

    cards: list[Card]               # Always exactly 8 cards

    # --- Tower Troop (first-class, approach_2 + evaluation fix) ---
    tower_troop: Optional[str] = None
    # ^ One of: "princess" | "cannoneer" | "dagger_duchess" | "royal_chef"
    # The optimizer runs once per tower_troop and ranks (deck, tower) pairs.

    # --- Special Slot Tracking ---
    evo_slot: Optional[Card] = None
    # ^ Card in the primary Evolution slot (or None).

    evo_wild_slot: Optional[Card] = None
    # ^ Card in the Wild slot acting as a second Evolution (or None).

    hero_slot: Optional[Card] = None
    # ^ Card in the Hero slot (or None). This is the ONLY hero slot.
    # NOTE: There is intentionally NO hero_wild_slot — max 1 Hero hard constraint.

    # --- Score Cache (populated by DeckScorer) ---
    attack_score: float = 0.0
    defense_score: float = 0.0
    synergy_score: float = 0.0
    versatility_score: float = 0.0
    tower_synergy_score: float = 0.0   # New: tower troop compatibility
    total_score: float = 0.0

    # -----------------------------------------------------------------------
    # Derived Properties
    # -----------------------------------------------------------------------

    @property
    def avg_elixir(self) -> float:
        """Average elixir cost using cycle_elixir (base cost only)."""
        if not self.cards:
            return 0.0
        return sum(c.cycle_elixir for c in self.cards) / len(self.cards)

    @property
    def cheapest_four_elixir(self) -> int:
        """
        Sum of the 4 cheapest cards by cycle_elixir.
        Measures cycle potential — the lower, the faster the deck cycles.
        """
        return sum(sorted(c.cycle_elixir for c in self.cards)[:4])

    @property
    def slot_config(self) -> str:
        """
        Slot configuration code. E.g. '2E1H', '1E1H', '0E0H'.
        Derived from which special slot fields are populated.
        """
        evo_count  = sum(1 for x in [self.evo_slot, self.evo_wild_slot] if x)
        hero_count = sum(1 for x in [self.hero_slot] if x)
        return f"{evo_count}E{hero_count}H"

    @property
    def elixir_variance(self) -> float:
        """Variance of elixir costs. High variance = incoherent curve."""
        if not self.cards:
            return 0.0
        avg = self.avg_elixir
        return sum((c.cycle_elixir - avg) ** 2 for c in self.cards) / len(self.cards)

    @property
    def win_conditions(self) -> list[Card]:
        return [c for c in self.cards if c.is_win_condition]

    @property
    def damage_spells(self) -> list[Card]:
        return [c for c in self.cards if c.is_damage_spell]

    @property
    def anti_air_units(self) -> list[Card]:
        return [c for c in self.cards if c.is_anti_air]

    @property
    def defensive_buildings(self) -> list[Card]:
        return [c for c in self.cards if c.is_defensive_building]

    @property
    def bait_cards(self) -> list[Card]:
        return [c for c in self.cards if c.is_bait_card]

    @property
    def total_hp(self) -> int:
        """Sum of HP for all non-spell cards."""
        return sum(c.hp for c in self.cards if c.hp and c.card_type != CardType.SPELL)

    @property
    def unique_roles_covered(self) -> set[str]:
        """Union of all active role flags across all 8 cards."""
        roles: set[str] = set()
        for c in self.cards:
            roles.update(c.active_role_flags())
        return roles

    # -----------------------------------------------------------------------
    # Validation
    # -----------------------------------------------------------------------

    def validate(self) -> ValidationResult:
        """Full slot validation — calls SlotValidator.validate()."""
        return SlotValidator.validate(self.cards, require_complete=True)

    def is_valid(self) -> bool:
        return self.validate().valid

    # -----------------------------------------------------------------------
    # Utility
    # -----------------------------------------------------------------------

    def card_ids(self) -> list[str]:
        return [c.id for c in self.cards]

    def has_card(self, card_id: str) -> bool:
        return any(c.id == card_id for c in self.cards)

    def summary(self) -> str:
        """One-line human-readable deck summary."""
        card_names = ", ".join(c.name for c in self.cards)
        tt = self.tower_troop or "any tower"
        return (
            f"[{self.slot_config}] ({tt}) "
            f"Score={self.total_score:.1f} "
            f"Avg={self.avg_elixir:.2f}e | "
            f"{card_names}"
        )

    def __repr__(self) -> str:
        return self.summary()

    def __hash__(self) -> int:
        return hash(frozenset(c.id for c in self.cards))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Deck):
            return NotImplemented
        return set(c.id for c in self.cards) == set(c.id for c in other.cards)
