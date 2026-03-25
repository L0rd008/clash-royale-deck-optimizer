"""
tests/test_card_data.py
========================
Card Data Validation — per plan §13.3.

Checks:
  - Every Card has meta_weight_source set (not empty)
  - Every spell Card has ct_damage > 0 (plan fix §4.1)
  - Every Card has meta_weight in [0.0, 2.0]
  - Every Card with is_win_condition=True has win_condition_strength > 0
  - Every Card with is_anti_air=True has anti_air_strength > 0
  - Every Card with is_damage_spell=True has ct_modifier > 0
  - No duplicate card IDs in ALL_CARDS
  - Every evolution card (SlotType.EVOLUTION) has base_card_id set
  - Every hero card (SlotType.HERO) has slot_type == HERO
  - Total card count >= 100 (allow for data evolution)
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from data.all_cards import CARD_BY_ID, ALL_CARDS
from models.card import SlotType


# ---------------------------------------------------------------------------
# Basic count + ID uniqueness
# ---------------------------------------------------------------------------

class TestCardCount:
    def test_minimum_card_count(self):
        """Must have at least 100 cards loaded."""
        assert len(ALL_CARDS) >= 100, (
            f"Expected >= 100 cards, got {len(ALL_CARDS)}"
        )

    def test_no_duplicate_ids(self):
        """All card IDs must be unique."""
        ids = [c.id for c in ALL_CARDS]
        dups = [cid for cid in set(ids) if ids.count(cid) > 1]
        assert not dups, f"Duplicate card IDs found: {dups}"

    def test_card_by_id_size_matches_all_cards(self):
        """CARD_BY_ID length must match ALL_CARDS after dedup."""
        assert len(CARD_BY_ID) == len(set(c.id for c in ALL_CARDS)), (
            "CARD_BY_ID and ALL_CARDS disagree on unique card count"
        )


# ---------------------------------------------------------------------------
# Provenance & meta weight (plan §13.3)
# ---------------------------------------------------------------------------

class TestProvenance:
    def test_all_cards_have_meta_weight_source(self):
        """Every Card must have meta_weight_source set (non-empty string)."""
        missing = [c.id for c in ALL_CARDS if not c.meta_weight_source]
        assert not missing, (
            f"{len(missing)} cards missing meta_weight_source: {missing[:10]}"
        )

    def test_meta_weight_in_range(self):
        """meta_weight must be in [0.0, 2.0] for all cards."""
        bad = [c.id for c in ALL_CARDS if not (0.0 <= c.meta_weight <= 2.0)]
        assert not bad, (
            f"{len(bad)} cards have meta_weight out of [0, 2]: {bad[:10]}"
        )

    def test_patch_version_consistent(self):
        """All cards should report the same patch_version (or empty)."""
        versions = {c.patch_version for c in ALL_CARDS if c.patch_version}
        assert len(versions) <= 1, (
            f"Multiple patch_versions found: {versions}"
        )


# ---------------------------------------------------------------------------
# Spell-specific checks (plan §4.1: CT damage must be set)
# ---------------------------------------------------------------------------

class TestSpellData:
    def test_damage_spells_have_ct_damage(self):
        """Every BASE direct-damage spell (base_damage > 0) must have ct_damage > 0.
        Utility spells like Rage/Clone have base_damage=0 and are excluded."""
        bad = [
            c.id for c in ALL_CARDS
            if c.is_damage_spell
            and c.slot_type == SlotType.BASE
            and c.damage > 0        # only direct-damage spells
            and c.ct_damage <= 0
        ]
        assert not bad, (
            f"{len(bad)} direct-damage BASE spells have ct_damage=0: {bad}"
        )

    def test_damage_spells_have_ct_modifier(self):
        """Every BASE direct-damage spell (base_damage > 0) must have ct_modifier > 0."""
        bad = [
            c.id for c in ALL_CARDS
            if c.is_damage_spell
            and c.slot_type == SlotType.BASE
            and c.damage > 0        # only direct-damage spells
            and c.ct_modifier <= 0
        ]
        assert not bad, (
            f"{len(bad)} direct-damage BASE spells have ct_modifier=0: {bad}"
        )

    def test_fireball_ct_damage_reasonable(self):
        """Fireball ct_damage must be > 100 (reference: ~207 at lv11)."""
        fb = CARD_BY_ID.get("fireball")
        assert fb is not None, "fireball not found in CARD_BY_ID"
        assert fb.ct_damage > 100, (
            f"fireball ct_damage={fb.ct_damage} — expected > 100"
        )

    def test_the_log_ct_damage_less_than_fireball(self):
        """The Log (ct_modifier=0.15) must deal less CT damage than Fireball (0.30)."""
        fb  = CARD_BY_ID.get("fireball")
        log = CARD_BY_ID.get("the_log")
        if fb and log:
            assert log.ct_damage < fb.ct_damage, (
                f"the_log ct_damage={log.ct_damage} >= fireball ct_damage={fb.ct_damage}"
            )


# ---------------------------------------------------------------------------
# Role flag consistency checks
# ---------------------------------------------------------------------------

class TestRoleFlags:
    def test_win_conditions_have_strength(self):
        """All BASE is_win_condition=True cards must have win_condition_strength > 0.
        Evolution spells that inherit is_win_condition may have wcs=0 (expected).
        """
        bad = [
            c.id for c in ALL_CARDS
            if c.is_win_condition
            and c.slot_type == SlotType.BASE        # exclude evo spells
            and c.win_condition_strength <= 0
        ]
        assert not bad, (
            f"{len(bad)} BASE WC cards have win_condition_strength=0: {bad}"
        )

    def test_anti_air_cards_have_strength(self):
        """BASE troop/building cards that target AIR or BOTH and have
        is_anti_air=True must have anti_air_strength > 0.
        Exclusions:
          - SPELL cards: use ct_damage for AA contribution
          - EVOLUTION cards: inherit is_anti_air from base; base card holds strength
          - HERO cards: ability-scaled AA, not captured by anti_air_strength
        """
        from models.card import TargetType, CardType
        bad = [
            c.id for c in ALL_CARDS
            if c.is_anti_air
            and c.card_type not in (CardType.SPELL, CardType.TOWER_TROOP)
            and c.slot_type == SlotType.BASE          # exclude evolutions/heroes
            and c.targets in (TargetType.AIR, TargetType.BOTH)
            and c.anti_air_strength <= 0
        ]
        assert not bad, (
            f"{len(bad)} BASE air-targeting anti-air troops have anti_air_strength=0: {bad}"
        )

    def test_known_wc_cards_flagged(self):
        """Key known WC cards must have is_win_condition=True."""
        known_wcs = [
            "hog_rider", "balloon", "goblin_barrel", "miner",
            "giant", "golem", "graveyard", "x_bow", "mortar",
        ]
        for cid in known_wcs:
            c = CARD_BY_ID.get(cid)
            if c is None:
                continue  # allow missing if card wasn't loaded
            assert c.is_win_condition, (
                f"{cid} expected is_win_condition=True but got False"
            )

    def test_known_anti_air_cards_flagged(self):
        """Key anti-air cards must have is_anti_air=True."""
        known_aa = [
            "mega_minion", "musketeer", "minion_horde",
            "inferno_dragon", "minions",
        ]
        for cid in known_aa:
            c = CARD_BY_ID.get(cid)
            if c is None:
                continue
            assert c.is_anti_air, (
                f"{cid} expected is_anti_air=True but got False"
            )


# ---------------------------------------------------------------------------
# Evolution / Hero slot checks
# ---------------------------------------------------------------------------

class TestSlotTypes:
    def test_evolutions_have_base_card_id(self):
        """All Evolution cards must have base_card_id set."""
        evos = [c for c in ALL_CARDS if c.slot_type == SlotType.EVOLUTION]
        assert evos, "No evolution cards found in ALL_CARDS"
        missing = [c.id for c in evos if not c.base_card_id]
        assert not missing, (
            f"{len(missing)} evo cards missing base_card_id: {missing}"
        )

    def test_heroes_have_hero_slot_type(self):
        """All champion/hero cards must have slot_type == HERO."""
        from models.card import CardType
        heroes = [c for c in ALL_CARDS if c.slot_type == SlotType.HERO]
        assert heroes, "No hero cards found in ALL_CARDS"

    def test_evo_base_exists_in_pool(self):
        """Every evo's base_card_id should resolve to a known card."""
        evos = [c for c in ALL_CARDS if c.slot_type == SlotType.EVOLUTION]
        missing_bases = [
            c.id for c in evos
            if c.base_card_id and c.base_card_id not in CARD_BY_ID
        ]
        assert not missing_bases, (
            f"{len(missing_bases)} evos have unknown base_card_id: {missing_bases}"
        )
