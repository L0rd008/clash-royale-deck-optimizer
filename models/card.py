"""
models/card.py
==============
Core Card dataclass for the Clash Royale Deck Optimizer.
Architecture: Final Hybrid Plan v2.0 — Q1 2026 Meta, Mid-March balance.

Design rules:
  - All role flags are HARDCODED per card (never auto-inferred from stats).
  - Continuous strength fields (0.0–1.0) layer nuance ON TOP of boolean flags.
  - cycle_elixir always uses base elixir only (Hero ability cost is separate).
  - state_profiles handles Spirit-Empress-style state-switching cards.
  - ct_damage is pre-computed from base_damage × ct_modifier for spells.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class CardType(Enum):
    TROOP       = "troop"
    SPELL       = "spell"
    BUILDING    = "building"
    TOWER_TROOP = "tower_troop"


class SlotType(Enum):
    BASE       = "base"        # Occupies a standard deck slot
    EVOLUTION  = "evolution"   # Requires the Evolution slot (or Wild slot as Evo)
    HERO       = "hero"        # Requires the Hero slot (only ONE Hero allowed)


class TargetType(Enum):
    GROUND    = "ground"
    AIR       = "air"
    BOTH      = "both"
    BUILDINGS = "buildings"


class SpeedTier(Enum):
    SLOW      = 1
    MEDIUM    = 2
    FAST      = 3
    VERY_FAST = 4


class Rarity(Enum):
    COMMON    = "common"
    RARE      = "rare"
    EPIC      = "epic"
    LEGENDARY = "legendary"


# ---------------------------------------------------------------------------
# Card Dataclass
# ---------------------------------------------------------------------------

@dataclass
class Card:
    """
    Represents a single Clash Royale card at Level 11 Tournament Standard.

    Fields are grouped as:
      1. Identity
      2. Core Stats
      3. Derived properties (via @property)
      4. Boolean Role Flags  — hardcoded, human-verified
      5. Continuous Strengths — 0.0–1.0 nuance scores
      6. Interaction Tags
      7. Spell-specific fields
      8. State profiles (Spirit Empress, etc.)
      9. Meta & Provenance
    """

    # -----------------------------------------------------------------------
    # 1. Identity
    # -----------------------------------------------------------------------
    id: str                         # Unique slug, e.g. "hog_rider"
    name: str                       # Display name, e.g. "Hog Rider"
    rarity: Rarity
    card_type: CardType
    slot_type: SlotType             # BASE, EVOLUTION, or HERO
    elixir: int                     # Base deployment cost
    ability_elixir: int = 0         # Hero/Champ ability cost (separate from base)
    base_card_id: Optional[str] = None  # Evo/Hero → slug of the base card it replaces

    # -----------------------------------------------------------------------
    # 2. Core Stats (Level 11 Tournament Standard)
    # -----------------------------------------------------------------------
    hp: int = 0                     # Hitpoints (0 for spells)
    damage: int = 0                 # Damage per hit
    dps: float = 0.0                # Damage per second
    hit_speed: float = 0.0          # Attack period in seconds
    speed: SpeedTier = SpeedTier.MEDIUM
    range: float = 0.0              # 0.0 = melee
    targets: TargetType = TargetType.GROUND
    lifetime: int = 0               # Seconds alive (buildings only)
    spawn_hp: int = 0               # HP of spawned units (spawners)
    death_damage: int = 0           # On-death damage (e.g. Giant Skeleton bomb)

    # -----------------------------------------------------------------------
    # 3. Derived Properties
    # -----------------------------------------------------------------------

    @property
    def cycle_elixir(self) -> int:
        """
        Elixir cost for cycle/average calculations — always base elixir only.
        Hero ability cost is NEVER included here.
        """
        return self.elixir

    @property
    def ability_total_elixir(self) -> int:
        """
        Total cost if ability is always used. Used ONLY for ability-budget
        analysis, never for deck average or cycle calculations.
        """
        return self.elixir + self.ability_elixir

    @property
    def is_melee(self) -> bool:
        return self.range == 0.0

    # -----------------------------------------------------------------------
    # 4. Boolean Role Flags (hardcoded per card — NO auto-inference)
    # -----------------------------------------------------------------------

    # --- Defensive roles ---
    is_anti_air: bool = False           # Can attack air units
    is_defensive_building: bool = False # Building that kites building-targeting units
    is_investment: bool = False         # Played in back to force opponent to react
    is_tank: bool = False               # High-HP frontline absorber
    is_support: bool = False            # Supports and empowers other cards

    # --- Offensive roles ---
    is_win_condition: bool = False      # Independently threatens towers
    is_damage_spell: bool = False       # Deals direct damage
    is_punishment: bool = False         # Immediate response to opponent's back-line play
    is_pump_response: bool = False      # Good vs Elixir Collector
    is_bridge_spam: bool = False        # Can be dropped at bridge for immediate pressure
    is_king_activator: bool = False     # Activates King Tower when placed/pulled correctly

    # --- Swarm roles ---
    is_bait_card: bool = False          # Baits specific spells (see bait_spells)
    is_anti_air_swarm: bool = False     # Counters air swarms (e.g. Bats, Minion Horde)
    is_anti_ground_swarm: bool = False  # Counters ground swarms (splash/AoE)
    is_splash: bool = False             # Deals area-of-effect damage

    # --- Ladder flags ---
    is_level_independent: bool = False  # Key stats unaffected by level differences
    is_strong_overleveled: bool = False # Key interactions change when overleveled
    is_weak_underleveled: bool = False  # Key interactions change when underleveled

    # -----------------------------------------------------------------------
    # 5. Continuous Role Strengths (0.0–1.0, independent of boolean flags)
    #    Set even when the boolean flag is False to allow gradient scoring.
    # -----------------------------------------------------------------------
    anti_air_strength: float = 0.0      # How effective vs air threats
    win_condition_strength: float = 0.0 # Tower-threatening capability
    punish_strength: float = 0.0        # How well it punishes back-line commits
    bridge_spam_strength: float = 0.0   # Effectiveness as bridge pressure
    tank_strength: float = 0.0          # HP-absorbing capability (0=spell,1=Golem)
    support_strength: float = 0.0       # How much it amplifies allies
    cycle_strength: float = 0.0         # Usefulness in pure cycle/cheap decks
    splash_strength: float = 0.0        # AoE radius/damage effectiveness

    # -----------------------------------------------------------------------
    # 6. Interaction Tags
    # -----------------------------------------------------------------------
    bait_spells: list[str] = field(default_factory=list)
    # ^ Spell slugs this card baits, e.g. ["log", "arrows"] for Princess

    hard_countered_by: list[str] = field(default_factory=list)
    # ^ Card slugs that hard-counter this card (effectiveness 0.8–1.0)

    soft_countered_by: list[str] = field(default_factory=list)
    # ^ Card slugs that soft-counter this card (effectiveness 0.4–0.79)

    counters_win_conditions: list[str] = field(default_factory=list)
    # ^ Win condition slugs this card can defend against

    counters_defenders: list[str] = field(default_factory=list)
    # ^ Defending unit/building slugs this card can remove offensively
    # e.g. Lightning counters Inferno Tower → "inferno_tower"

    counters_secondary_wc: list[str] = field(default_factory=list)
    # ^ Secondary win condition slugs this card counters
    # e.g. Poison counters Graveyard → "graveyard"

    # -----------------------------------------------------------------------
    # 7. Spell-Specific Fields
    # -----------------------------------------------------------------------
    ct_modifier: float = 0.0
    # ^ Crown Tower damage modifier:
    #   The Log / Void (single-target focal): 0.15
    #   Arrows / Poison / Goblin Curse / Void (5+ targets): 0.25
    #   Fireball / Lightning / Zap / Giant Snowball / Rage / Freeze / Tornado: 0.30
    #   Earthquake: variable (extra multiplier vs structures)

    ct_damage: int = 0
    # ^ Pre-computed Crown Tower damage = base_damage × ct_modifier.
    # Set explicitly in cards_spells.py. Used for spell pressure scoring.

    # -----------------------------------------------------------------------
    # 8. State Profiles (for mechanics like Spirit Empress dual-state)
    # -----------------------------------------------------------------------
    state_profiles: dict = field(default_factory=dict)
    # ^ Dict of named stat profiles, keyed by state name.
    # Example for Spirit Empress:
    # {
    #   "ground": {"elixir": 3, "hp": 1152, "dps": 279, "targets": "ground", "speed": "fast"},
    #   "air":    {"elixir": 6, "hp": 1152, "dps": 307, "targets": "both",   "speed": "fast"},
    # }

    state_condition: Optional[str] = None
    # ^ Human-readable trigger, e.g. "elixir_at_deploy >= 6"
    # Role flags and cycle_elixir always use the PRIMARY (lowest-cost) state.

    # -----------------------------------------------------------------------
    # 9. Meta & Provenance
    # -----------------------------------------------------------------------
    meta_weight: float = 1.0
    # ^ Usage/win-rate multiplier [0.0–2.0]. 1.0 = average meta presence.

    meta_weight_source: str = "manual"
    # ^ Source of meta weight: "royaleapi" | "tier_list" | "manual"

    patch_version: str = "Q1-2026-mid-march"
    # ^ Patch this card's stats/flags were last verified against.

    last_verified: str = ""
    # ^ ISO date string of last manual review, e.g. "2026-03-23"

    confidence: float = 1.0
    # ^ Data confidence [0.0–1.0]. <1.0 for estimated or partially-sourced stats.

    # -----------------------------------------------------------------------
    # 10. Utility Methods
    # -----------------------------------------------------------------------

    def active_role_flags(self) -> list[str]:
        """Returns a list of role flag names that are True for this card."""
        flags = [
            "is_anti_air", "is_defensive_building", "is_investment",
            "is_tank", "is_support", "is_win_condition", "is_damage_spell",
            "is_punishment", "is_pump_response", "is_bridge_spam",
            "is_king_activator", "is_bait_card", "is_anti_air_swarm",
            "is_anti_ground_swarm", "is_splash", "is_level_independent",
            "is_strong_overleveled", "is_weak_underleveled",
        ]
        return [f for f in flags if getattr(self, f)]

    def role_count(self) -> int:
        """Number of distinct roles this card fulfils."""
        return len(self.active_role_flags())

    def __repr__(self) -> str:
        flags = ", ".join(self.active_role_flags())
        return (
            f"Card({self.id!r}, {self.elixir}e, "
            f"{self.slot_type.value}, [{flags}])"
        )

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Card):
            return NotImplemented
        return self.id == other.id
