"""
data/cards_buildings.py
========================
All building Card instances — 11 buildings.

Sources: Building Statistical Dataset (Level 11) in reference.md.

NOTE: Furnace is NOT here. It was reclassified as a TROOP (CardType.TROOP)
in the August 2025 update (per reference.md) and lives in cards_troops.py.

Role flag notes:
  - is_defensive_building: True for all (they kite building-targeting units).
  - is_investment: Spawner buildings (Barbarian Hut) that generate long-term value.
  - is_win_condition: X-Bow and Mortar are siege win conditions.
  - is_anti_air: Buildings that can hit air (Tesla, Bomb Tower, Inferno Tower, X-Bow).
  - DPS for spawners = spawn_unit_damage / spawn_interval.
"""

from models.card import Card, CardType, SlotType, TargetType, SpeedTier, Rarity


def _bldg(
    id, name, rarity, elixir,
    hp, damage, hit_speed, lifetime,
    targets=TargetType.BOTH,
    spawn_hp=0, spawn_interval=0,
    is_defensive_building=True,   # explicit — Elixir Collector overrides to False
    is_win_condition=False,
    is_anti_air=False,
    is_investment=False,
    is_pump_response=False,
    is_splash=False,
    is_anti_ground_swarm=False,
    counters_win_conditions=None,
    counters_defenders=None,
    anti_air_strength=0.0,
    meta_weight=1.0,
    confidence=1.0,
    **kw,
) -> Card:
    dps = round(damage / hit_speed, 1) if hit_speed > 0 else 0.0
    return Card(
        id=id, name=name,
        rarity=rarity, card_type=CardType.BUILDING, slot_type=SlotType.BASE,
        elixir=elixir, hp=hp, damage=damage,
        dps=dps, hit_speed=hit_speed, lifetime=lifetime,
        targets=targets, spawn_hp=spawn_hp,
        range=5.5,  # typical building range (~5-6 tiles)
        is_defensive_building=is_defensive_building,
        is_win_condition=is_win_condition,
        is_anti_air=is_anti_air,
        is_investment=is_investment,
        is_pump_response=is_pump_response,
        is_splash=is_splash,
        is_anti_ground_swarm=is_anti_ground_swarm,
        anti_air_strength=anti_air_strength,
        tank_strength=round(min(1.0, hp / 5120), 2),
        cycle_strength=round(max(0.0, (7 - elixir) / 6), 2),
        counters_win_conditions=counters_win_conditions or [],
        counters_defenders=counters_defenders or [],
        meta_weight=meta_weight, confidence=confidence,
        last_verified="2026-03-23",
        **kw,
    )


# ===========================================================================
# BUILDINGS
# ===========================================================================

CANNON = _bldg(
    id="cannon", name="Cannon",
    rarity=Rarity.COMMON, elixir=3,
    hp=896, damage=212, hit_speed=0.8, lifetime=30,
    targets=TargetType.GROUND,  # Cannon targets ground only in-game
    # High DPS cheap distraction; pulls building-targeting units (stated)
    is_anti_air=False,
    anti_air_strength=0.0,
    counters_win_conditions=["hog_rider", "battle_ram", "ram_rider",
                             "giant", "goblin_drill"],
    meta_weight=1.4,
)

BOMB_TOWER = _bldg(
    id="bomb_tower", name="Bomb Tower",
    rarity=Rarity.RARE, elixir=4,
    hp=1354, damage=225, hit_speed=1.6, lifetime=30,
    is_anti_air=True, is_splash=True, is_anti_ground_swarm=True,
    anti_air_strength=0.65,
    # High AoE splash; death bomb on destruction (stated)
    counters_win_conditions=["royal_hogs", "goblin_barrel", "graveyard",
                             "battle_ram", "hog_rider"],
    counters_defenders=["skeleton_army", "goblins", "minions",
                        "spear_goblins", "goblin_gang"],
    meta_weight=1.2,
)

TESLA = _bldg(
    id="tesla", name="Tesla",
    rarity=Rarity.COMMON, elixir=4,
    hp=1152, damage=230, hit_speed=1.1, lifetime=35,
    is_anti_air=True,
    anti_air_strength=0.60,
    # Submerges when inactive → spell immune; 0.2s micro-stun per hit (stated)
    counters_win_conditions=["hog_rider", "balloon", "battle_ram",
                             "goblin_drill", "ram_rider"],
    meta_weight=1.3,
)

INFERNO_TOWER = _bldg(
    id="inferno_tower", name="Inferno Tower",
    rarity=Rarity.RARE, elixir=5,
    hp=1748, damage=40, hit_speed=0.4, lifetime=30,  # 40 base → ramps to 800
    is_anti_air=True,
    anti_air_strength=0.80,
    # Focal ramp: 40→800 DPS over ~2.5s; melts heavy tanks (stated)
    # Reset by Zap/Freeze/Electro Wizard
    counters_win_conditions=["giant", "golem", "lava_hound", "electro_giant",
                             "p_e_k_k_a", "goblin_giant", "mega_knight",
                             "balloon", "hero_giant"],
    meta_weight=1.4,
)

MORTAR = _bldg(
    id="mortar", name="Mortar",
    rarity=Rarity.COMMON, elixir=4,
    hp=1472, damage=266, hit_speed=5.0, lifetime=30,
    targets=TargetType.GROUND,
    is_win_condition=True,  # siege win condition (stated in plan)
    is_pump_response=True,  # forces opponent to react when placed in back
    # Blind spot prevents close-proximity targeting (stated)
    win_condition_strength=0.60,
    counters_win_conditions=[],  # not a counter, it's offensive
    meta_weight=1.0,
)

X_BOW = _bldg(
    id="x_bow", name="X-Bow",
    rarity=Rarity.EPIC, elixir=6,
    hp=1600, damage=34, hit_speed=0.25, lifetime=40,
    targets=TargetType.GROUND,
    is_win_condition=True,   # siege win condition (stated in plan)
    is_investment=True,       # placed in back, forces opponent to respond
    # Extreme range; 0.25s fire rate = 34×4=136 DPS (stated)
    win_condition_strength=0.70,
    is_pump_response=True,
    meta_weight=1.1,
)

BARBARIAN_HUT = _bldg(
    id="barbarian_hut", name="Barbarian Hut",
    rarity=Rarity.RARE, elixir=7,
    hp=1650, damage=192, hit_speed=11.0, lifetime=40,
    targets=TargetType.GROUND, spawn_hp=670,
    is_investment=True,  # high spatial commitment, generates 2 Barbs/wave (stated)
    is_pump_response=False,
    # Very expensive; spawns 2 Barbarians per wave at 11s interval
    meta_weight=0.7,
)

GOBLIN_HUT = _bldg(
    id="goblin_hut", name="Goblin Hut",
    rarity=Rarity.RARE, elixir=5,
    hp=920, damage=81, hit_speed=4.0, lifetime=28,
    targets=TargetType.BOTH, spawn_hp=132,
    is_investment=True,  # generates consistent lane pressure via Spear Goblins (stated)
    meta_weight=0.8,
)

TOMBSTONE = _bldg(
    id="tombstone", name="Tombstone",
    rarity=Rarity.RARE, elixir=3,
    hp=532, damage=81, hit_speed=3.3, lifetime=30,
    targets=TargetType.GROUND, spawn_hp=81,
    # Rapidly spawns skeletons; swarm on destruction (stated)
    counters_win_conditions=["hog_rider", "golem", "giant",
                             "battle_ram", "ram_rider"],
    is_anti_ground_swarm=False,  # it spawns swarm, doesn't counter swarm
    meta_weight=1.2,
)

GOBLIN_CAGE = _bldg(
    id="goblin_cage", name="Goblin Cage",
    rarity=Rarity.RARE, elixir=4,
    hp=853, damage=318, hit_speed=0.0, lifetime=15,  # cage itself doesn't attack
    targets=TargetType.GROUND, spawn_hp=0,
    # Pulls aggro; Goblin Brawler (318 damage) unleashed on destruction (stated)
    counters_win_conditions=["hog_rider", "battle_ram", "ram_rider",
                             "giant", "goblin_drill"],
    confidence=0.9,
    meta_weight=1.1,
)

ELIXIR_COLLECTOR = _bldg(
    id="elixir_collector", name="Elixir Collector",
    rarity=Rarity.RARE, elixir=6,
    hp=1063, damage=0, hit_speed=8.5, lifetime=65,
    targets=TargetType.GROUND,
    is_investment=True,  # generates +1 elixir per 8.5s while alive (in-game mechanics)
    is_defensive_building=False,  # NOT a kiting building (doesn't pull troops)
    is_pump_response=False,
    # Generates elixir advantage if defended; punishes unaddressed by Fireball/EQ (stated)
    meta_weight=1.0,
    confidence=0.95,
)


# ===========================================================================
# Aggregated export
# ===========================================================================

ALL_BUILDINGS: list[Card] = [
    CANNON,
    BOMB_TOWER,
    TESLA,
    INFERNO_TOWER,
    MORTAR,
    X_BOW,
    BARBARIAN_HUT,
    GOBLIN_HUT,
    TOMBSTONE,
    GOBLIN_CAGE,
    ELIXIR_COLLECTOR,
]
