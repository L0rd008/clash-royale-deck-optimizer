"""
data/cards_tower_troops.py
===========================
The 4 Tower Troop Card instances.

Sources: Tower Troop Dataset (Level 11) in reference.md.

Tower troops are NOT added to the main 8-card deck — they are selected
as the `deck.tower_troop` field and assessed via TowerSynergyScorer.
They are stored here as Card objects for data consistency and to allow
property lookups during tower synergy scoring.

Stats (Level 11 Tournament Standard):
  - Tower Princess : 3,052 HP, 109 dmg, 0.8s, 136 DPS, 7.5 range, Air/Ground
  - Cannoneer      : 2,616 HP, 422 dmg, 2.4s, 175 DPS, 7.5 range, Air/Ground
  - Dagger Duchess : 2,768 HP, 107 dmg, 0.35s, 306/76 DPS (burst/sustained)
  - Royal Chef     : 2,703 HP, 109 dmg, 0.9s, 121 DPS (+ level buff mechanic)
"""

from models.card import Card, CardType, SlotType, TargetType, SpeedTier, Rarity


def _tower(
    id, name, rarity,
    hp, damage, hit_speed,
    dps=None,
    special_notes="",
    meta_weight=1.0,
    confidence=1.0,
    **kw,
) -> Card:
    computed_dps = round(damage / hit_speed, 1) if hit_speed > 0 else 0.0
    return Card(
        id=id, name=name,
        rarity=rarity,
        card_type=CardType.TOWER_TROOP,
        slot_type=SlotType.BASE,
        elixir=0,          # Tower troops have no elixir cost
        hp=hp, damage=damage,
        dps=dps if dps is not None else computed_dps,
        hit_speed=hit_speed,
        range=7.5,         # All tower troops have 7.5 tile range (stated)
        targets=TargetType.BOTH,
        meta_weight=meta_weight,
        confidence=confidence,
        last_verified="2026-03-23",
        **kw,
    )


# ===========================================================================
# TOWER TROOPS
# ===========================================================================

TOWER_PRINCESS = _tower(
    id="tower_princess", name="Tower Princess",
    rarity=Rarity.COMMON,
    hp=3052, damage=109, hit_speed=0.8, dps=136,
    # Standard consistent single-target defense (stated)
    # Balanced baseline — no specific structural penalty or bonus
    meta_weight=1.0,
)

CANNONEER = _tower(
    id="cannoneer", name="Cannoneer",
    rarity=Rarity.EPIC,
    hp=2616, damage=422, hit_speed=2.4, dps=175,
    # Extreme burst, 422 per shot; highly vulnerable to swarm attrition (stated)
    # Players must compensate with splash-damage utility in deck
    meta_weight=1.0,
)

DAGGER_DUCHESS = _tower(
    id="dagger_duchess", name="Dagger Duchess",
    rarity=Rarity.LEGENDARY,
    hp=2768, damage=107, hit_speed=0.35, dps=306,
    # Two DPS phases:
    #   Burst phase (8 daggers full): 306 DPS (107dmg / 0.35s)
    #   Sustained phase (daggers exhausted): 76 DPS
    # Depleted DPS drops to 76 (stated)
    # Rewards high-HP sponge cards and cheap spells that exploit burst-window timing
    meta_weight=1.0,
)

ROYAL_CHEF = _tower(
    id="royal_chef", name="Royal Chef",
    rarity=Rarity.LEGENDARY,
    hp=2703, damage=109, hit_speed=0.9, dps=121,
    # Passive: +1 Level buff (+10% stats) to highest-HP allied troop (stated)
    # HP reduced 7% to 2703 from 2921 (stated, March 2026 balance)
    # Synergizes with beatdown tanks: Golem, Giant, Hero Giant
    # Buff delayed under heavy offensive pressure (stated)
    meta_weight=1.0,
)


# ===========================================================================
# Aggregated export
# ===========================================================================

ALL_TOWER_TROOPS: list[Card] = [
    TOWER_PRINCESS,
    CANNONEER,
    DAGGER_DUCHESS,
    ROYAL_CHEF,
]
