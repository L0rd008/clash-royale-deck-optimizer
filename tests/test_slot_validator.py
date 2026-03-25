"""
tests/test_slot_validator.py
============================
Unit tests for SlotValidator.

Covers:
  - Max 1 Hero hard lock (problem_description.md constraint)
  - Max 2 Evolutions
  - Special slot total cap (Evo + Hero ≤ 3)
  - Base card / Evo / Hero coexistence exclusion
  - Duplicate card detection
  - can_add() fast path used by beam search
  - Valid configuration acceptance

Run with:  python -m pytest tests/test_slot_validator.py -v
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from models.card import Card, CardType, SlotType, TargetType, SpeedTier, Rarity
from models.slot_validator import SlotValidator


# ---------------------------------------------------------------------------
# Helpers — minimal throwaway cards for testing
# ---------------------------------------------------------------------------

def _base(id: str, elixir: int = 3) -> Card:
    return Card(
        id=id, name=id.replace("_", " ").title(),
        rarity=Rarity.COMMON, card_type=CardType.TROOP,
        slot_type=SlotType.BASE, elixir=elixir,
    )


def _evo(id: str, base_id: str, elixir: int = 3) -> Card:
    return Card(
        id=id, name=id.replace("_", " ").title(),
        rarity=Rarity.COMMON, card_type=CardType.TROOP,
        slot_type=SlotType.EVOLUTION, elixir=elixir,
        base_card_id=base_id,
    )


def _hero(id: str, base_id: str = None, elixir: int = 4) -> Card:
    return Card(
        id=id, name=id.replace("_", " ").title(),
        rarity=Rarity.LEGENDARY, card_type=CardType.TROOP,
        slot_type=SlotType.HERO, elixir=elixir,
        base_card_id=base_id,
    )


def _make_deck(*cards: Card, pad_to: int = 8) -> list[Card]:
    """Pad with unique base cards to reach pad_to total cards."""
    deck = list(cards)
    i = 0
    while len(deck) < pad_to:
        cid = f"filler_{i}"
        if not any(c.id == cid for c in deck):
            deck.append(_base(cid, elixir=3))
        i += 1
    return deck


# ---------------------------------------------------------------------------
# VALID CONFIGURATIONS
# ---------------------------------------------------------------------------

class TestValidConfigs:

    def test_config_H_all_base(self):
        """8 base cards — should always be valid."""
        cards = [_base(f"card_{i}") for i in range(8)]
        result = SlotValidator.validate(cards)
        assert result.valid, result.errors

    def test_config_F_one_hero(self):
        """0 Evos + 1 Hero + 7 base = valid."""
        cards = _make_deck(_hero("hero_knight", "knight"))
        result = SlotValidator.validate(cards)
        assert result.valid, result.errors

    def test_config_G_one_evo(self):
        """1 Evo + 0 Heroes + 7 base = valid."""
        cards = _make_deck(_evo("evo_knight", "knight"))
        result = SlotValidator.validate(cards)
        assert result.valid, result.errors

    def test_config_A_one_evo_one_hero(self):
        """1 Evo + 1 Hero + 6 base = valid."""
        cards = _make_deck(
            _evo("evo_knight", "knight"),
            _hero("hero_giant", "giant"),
        )
        result = SlotValidator.validate(cards)
        assert result.valid, result.errors

    def test_config_B_two_evos_one_hero(self):
        """2 Evos + 1 Hero + 5 base = valid."""
        cards = _make_deck(
            _evo("evo_knight", "knight"),
            _evo("evo_skeletons", "skeletons", elixir=1),
            _hero("hero_giant", "giant"),
        )
        result = SlotValidator.validate(cards)
        assert result.valid, result.errors

    def test_config_D_two_evos_no_hero(self):
        """2 Evos + 0 Heroes + 6 base = valid."""
        cards = _make_deck(
            _evo("evo_knight", "knight"),
            _evo("evo_skeletons", "skeletons", elixir=1),
        )
        result = SlotValidator.validate(cards)
        assert result.valid, result.errors


# ---------------------------------------------------------------------------
# HERO CONSTRAINT (most critical)
# ---------------------------------------------------------------------------

class TestHeroConstraint:

    def test_two_heroes_rejected(self):
        """2 Heroes must be rejected — hard lock from problem_description.md."""
        cards = _make_deck(
            _hero("hero_knight", "knight", elixir=3),
            _hero("hero_giant", "giant", elixir=5),
        )
        result = SlotValidator.validate(cards)
        assert not result.valid
        assert any("hero" in e.lower() or "Hero" in e for e in result.errors)

    def test_two_heroes_no_evos_rejected(self):
        """Config E (0 Evos + 2 Heroes) explicitly disabled."""
        cards = _make_deck(
            _hero("hero_musketeer", "musketeer", elixir=4),
            _hero("hero_mini_pekka", "mini_pekka", elixir=4),
        )
        result = SlotValidator.validate(cards)
        assert not result.valid

    def test_one_hero_one_evo_one_hero_rejected(self):
        """1 Evo + 2 Heroes → special slot total = 3 AND hero count = 2 → rejected."""
        cards = _make_deck(
            _evo("evo_skeletons", "skeletons", elixir=1),
            _hero("hero_knight", "knight", elixir=3),
            _hero("hero_giant", "giant", elixir=5),
        )
        result = SlotValidator.validate(cards)
        assert not result.valid


# ---------------------------------------------------------------------------
# EVOLUTION CONSTRAINT
# ---------------------------------------------------------------------------

class TestEvoConstraint:

    def test_three_evos_rejected(self):
        """3 Evos exceeds max of 2."""
        cards = _make_deck(
            _evo("evo_knight", "knight"),
            _evo("evo_skeletons", "skeletons", elixir=1),
            _evo("evo_archers", "archers"),
        )
        result = SlotValidator.validate(cards)
        assert not result.valid

    def test_two_evos_accepted(self):
        """2 Evos without Hero is valid."""
        cards = _make_deck(
            _evo("evo_knight", "knight"),
            _evo("evo_skeletons", "skeletons", elixir=1),
        )
        result = SlotValidator.validate(cards)
        assert result.valid, result.errors


# ---------------------------------------------------------------------------
# BASE CARD EXCLUSION
# ---------------------------------------------------------------------------

class TestBaseExclusion:

    def test_evo_with_base_card_rejected(self):
        """Evo Knight + base Knight in same deck → invalid."""
        cards = _make_deck(
            _evo("evo_knight", "knight"),
            _base("knight"),
        )
        result = SlotValidator.validate(cards)
        assert not result.valid
        assert any("knight" in e for e in result.errors)

    def test_hero_with_base_card_rejected(self):
        """Hero Giant + base Giant in same deck → invalid."""
        cards = _make_deck(
            _hero("hero_giant", "giant"),
            _base("giant"),
        )
        result = SlotValidator.validate(cards)
        assert not result.valid

    def test_evo_without_base_card_accepted(self):
        """Evo Knight without base Knight → valid."""
        cards = _make_deck(_evo("evo_knight", "knight"))
        result = SlotValidator.validate(cards)
        assert result.valid, result.errors

    def test_hero_no_base_card_id_no_conflict(self):
        """Hero with no base_card_id (standalone hero) → no exclusion conflict."""
        cards = _make_deck(_hero("boss_bandit", base_id=None))
        result = SlotValidator.validate(cards)
        assert result.valid, result.errors


# ---------------------------------------------------------------------------
# DUPLICATE DETECTION
# ---------------------------------------------------------------------------

class TestDuplicates:

    def test_duplicate_base_cards_rejected(self):
        """Two copies of the same card → invalid."""
        cards = _make_deck(_base("hog_rider"), _base("hog_rider"))
        result = SlotValidator.validate(cards)
        assert not result.valid
        assert any("hog_rider" in e for e in result.errors)


# ---------------------------------------------------------------------------
# DECK SIZE
# ---------------------------------------------------------------------------

class TestDeckSize:

    def test_incomplete_deck_rejected(self):
        """7-card deck rejected when require_complete=True."""
        cards = [_base(f"card_{i}") for i in range(7)]
        result = SlotValidator.validate(cards, require_complete=True)
        assert not result.valid

    def test_incomplete_deck_accepted_when_not_required(self):
        """Partial deck accepted when require_complete=False."""
        cards = [_base(f"card_{i}") for i in range(4)]
        result = SlotValidator.validate(cards, require_complete=False)
        assert result.valid, result.errors

    def test_nine_card_deck_rejected(self):
        """9-card deck always rejected."""
        cards = [_base(f"card_{i}") for i in range(9)]
        result = SlotValidator.validate(cards)
        assert not result.valid


# ---------------------------------------------------------------------------
# CAN_ADD (Beam Search Fast Path)
# ---------------------------------------------------------------------------

class TestCanAdd:

    def test_can_add_first_hero(self):
        """Adding the first hero to a base-only partial deck → allowed."""
        existing = [_base(f"card_{i}") for i in range(4)]
        candidate = _hero("hero_knight", "knight")
        assert SlotValidator.can_add(candidate, existing)

    def test_cannot_add_second_hero(self):
        """Adding a second hero when one already exists → blocked."""
        existing = [_base(f"card_{i}") for i in range(4)]
        existing.append(_hero("hero_knight", "knight"))
        candidate = _hero("hero_giant", "giant")
        assert not SlotValidator.can_add(candidate, existing)

    def test_can_add_first_evo(self):
        """Adding first evo → allowed."""
        existing = [_base(f"card_{i}") for i in range(4)]
        candidate = _evo("evo_knight", "knight")
        assert SlotValidator.can_add(candidate, existing)

    def test_can_add_second_evo(self):
        """Adding second evo when one already exists → allowed."""
        existing = [_base(f"card_{i}") for i in range(4)]
        existing.append(_evo("evo_knight", "knight"))
        candidate = _evo("evo_skeletons", "skeletons")
        assert SlotValidator.can_add(candidate, existing)

    def test_cannot_add_third_evo(self):
        """Adding third evo → blocked."""
        existing = [_base(f"card_{i}") for i in range(3)]
        existing.append(_evo("evo_knight", "knight"))
        existing.append(_evo("evo_skeletons", "skeletons"))
        candidate = _evo("evo_archers", "archers")
        assert not SlotValidator.can_add(candidate, existing)

    def test_cannot_add_evo_if_base_present(self):
        """Adding Evo Knight when base Knight is already in deck → blocked."""
        existing = [_base(f"card_{i}") for i in range(3)]
        existing.append(_base("knight"))
        candidate = _evo("evo_knight", "knight")
        assert not SlotValidator.can_add(candidate, existing)

    def test_cannot_add_duplicate(self):
        """Adding a card already present → blocked."""
        existing = [_base("hog_rider")] + [_base(f"card_{i}") for i in range(3)]
        candidate = _base("hog_rider")
        assert not SlotValidator.can_add(candidate, existing)


# ---------------------------------------------------------------------------
# SLOT CONFIG NAME
# ---------------------------------------------------------------------------

class TestSlotConfigName:

    def test_config_name_0e0h(self):
        cards = [_base(f"c{i}") for i in range(8)]
        assert SlotValidator.slot_config_name(cards) == "0E0H"

    def test_config_name_1e1h(self):
        cards = _make_deck(_evo("evo_k", "k"), _hero("hero_g", "g"))
        assert SlotValidator.slot_config_name(cards) == "1E1H"

    def test_config_name_2e0h(self):
        cards = _make_deck(_evo("evo_k", "k"), _evo("evo_s", "s"))
        assert SlotValidator.slot_config_name(cards) == "2E0H"


# ---------------------------------------------------------------------------
# Run directly
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
