"""
data/cards_spells.py
====================
All spell Card instances — 21 spells.

Sources:
  - Spell Statistical Dataset (Level 11) in reference.md
  - CT modifier rules from reference.md Methodological Framework:
      15% : The Log, Void (single-target focal)
      20% : Goblin Curse, Void (5+ targets)
      25% : Arrows, Poison, Rocket, Vines, Void (2-4 targets), Skeleton Army (area)
      30% : Fireball, Lightning, Zap, Giant Snowball, Rage, Freeze, Tornado

CT damages are taken directly from the spell table in reference.md wherever stated;
otherwise computed as round(base_damage * ct_modifier).

Role flag notes:
  - is_anti_air: True for any AoE spell that can hit flying units.
  - is_damage_spell: True for spells that deal direct damage (not Clone, Graveyard).
  - is_pump_response: True for spells that efficiently destroy Elixir Collector.
  - is_king_activator: Tornado only (pulls units into King Tower range).
  - is_splash: True for all AoE spells.
  - is_bait_card / bait_spells: spells don't bait; that's on the troop side.
"""

from models.card import Card, CardType, SlotType, TargetType, Rarity

# ---------------------------------------------------------------------------
# Helper — build a spell Card
# ---------------------------------------------------------------------------

def _spell(
    id, name, rarity, elixir,
    base_damage, ct_modifier, ct_damage,
    hp=0,
    targets=TargetType.BOTH,   # explicit — allows ground-only override
    is_damage_spell=True,
    is_anti_air=False,
    is_splash=False,
    is_pump_response=False,
    is_king_activator=False,
    is_anti_ground_swarm=False,
    is_anti_air_swarm=False,
    counters_win_conditions=None,
    counters_defenders=None,
    counters_secondary_wc=None,
    meta_weight=1.0,
    confidence=1.0,
    **kw,
) -> Card:
    return Card(
        id=id, name=name,
        rarity=rarity, card_type=CardType.SPELL, slot_type=SlotType.BASE,
        elixir=elixir,
        damage=base_damage,
        ct_modifier=ct_modifier, ct_damage=ct_damage,
        targets=targets,
        is_damage_spell=is_damage_spell,
        is_anti_air=is_anti_air,
        is_splash=is_splash,
        is_pump_response=is_pump_response,
        is_king_activator=is_king_activator,
        is_anti_ground_swarm=is_anti_ground_swarm,
        is_anti_air_swarm=is_anti_air_swarm,
        cycle_strength=round(max(0.0, (7 - elixir) / 6), 2),
        counters_win_conditions=counters_win_conditions or [],
        counters_defenders=counters_defenders or [],
        counters_secondary_wc=counters_secondary_wc or [],
        meta_weight=meta_weight, confidence=confidence,
        last_verified="2026-03-23",
        **kw,
    )


# ===========================================================================
# SPELLS
# ===========================================================================

THE_LOG = _spell(
    id="the_log", name="The Log",
    rarity=Rarity.LEGENDARY, elixir=2,
    base_damage=290, ct_modifier=0.15, ct_damage=41,
    targets=TargetType.GROUND,   # override: ground only, linear knockback
    # The Log deals 15% to towers (stated), ground-only rolling knockback
    is_splash=True,
    is_anti_ground_swarm=True,
    # Great vs small ground units
    bait_spells=[],  # spells don't bait; this field not relevant for spells
    counters_win_conditions=["goblin_barrel", "prince"],  # rolls into prince charge
    counters_defenders=["skeleton_army", "goblins", "spear_goblins",
                        "goblin_gang", "bats", "minions"],
    counters_secondary_wc=["goblin_barrel"],
    meta_weight=1.7,
)

ARROWS = _spell(
    id="arrows", name="Arrows",
    rarity=Rarity.COMMON, elixir=3,
    base_damage=370, ct_modifier=0.25, ct_damage=93,
    # ↑ 370 total across 3 waves (stated), 25% CT modifier, 93 CT (stated)
    is_splash=True, is_anti_air=True, is_anti_air_swarm=True,
    is_anti_ground_swarm=True,
    counters_defenders=["minions", "bats", "minion_horde", "goblins",
                        "spear_goblins", "goblin_gang", "skeleton_army",
                        "witch", "mother_witch", "dark_prince",
                        "princess", "dart_goblin", "firecracker"],
    counters_secondary_wc=["goblin_barrel", "princess"],
    meta_weight=1.6,
)

GIANT_SNOWBALL = _spell(
    id="giant_snowball", name="Giant Snowball",
    rarity=Rarity.COMMON, elixir=2,
    base_damage=192, ct_modifier=0.30, ct_damage=54,  # stated as 54
    is_splash=True, is_anti_air=True,
    is_anti_ground_swarm=True, is_anti_air_swarm=True,
    # Radial knockback + 2.5s slow (stated)
    counters_defenders=["goblins", "spear_goblins", "bats",
                        "minions", "skeleton_army", "goblin_gang"],
    meta_weight=1.3,
)

ZAP = _spell(
    id="zap", name="Zap",
    rarity=Rarity.COMMON, elixir=2,
    base_damage=192, ct_modifier=0.30, ct_damage=58,  # stated as 58
    is_splash=True, is_anti_air=True,
    is_anti_ground_swarm=True, is_anti_air_swarm=True,
    # 0.5s stun; resets Inferno Tower ramp and Inferno Dragon ramp (stated)
    counters_defenders=["inferno_tower", "inferno_dragon",
                        "sparky", "goblins", "bats", "skeletons",
                        "spear_goblins", "minions"],
    counters_secondary_wc=["sparky"],
    meta_weight=1.7,
)

EARTHQUAKE = _spell(
    id="earthquake", name="Earthquake",
    rarity=Rarity.RARE, elixir=3,
    base_damage=207, ct_modifier=0.77,  # 159/207 ≈ 0.77 variable modifier vs structures
    ct_damage=159,
    targets=TargetType.GROUND,
    is_splash=True, is_pump_response=True, is_anti_ground_swarm=True,
    # Massive bonus vs structures (stated); slows ground troops
    counters_defenders=["cannon", "tombstone", "tesla", "bomb_tower",
                        "mortar", "x_bow", "inferno_tower",
                        "goblin_hut", "barbarian_hut", "goblin_cage",
                        "elixir_collector"],
    meta_weight=1.2,
)

FIREBALL = _spell(
    id="fireball", name="Fireball",
    rarity=Rarity.RARE, elixir=4,
    base_damage=689, ct_modifier=0.30, ct_damage=207,  # stated 207
    is_splash=True, is_anti_air=True,
    is_pump_response=True, is_anti_ground_swarm=True,
    # Kinetic knockback on medium-weight units (stated)
    counters_win_conditions=["three_musketeers", "royal_hogs"],
    counters_defenders=["musketeer", "barbarians", "valkyrie", "baby_dragon",
                        "wizard", "witch", "bomber", "night_witch",
                        "goblin_demolisher", "flying_machine", "executioner",
                        "rune_giant", "three_musketeers", "elixir_collector"],
    counters_secondary_wc=["royal_hogs", "three_musketeers"],
    meta_weight=1.7,
)

POISON = _spell(
    id="poison", name="Poison",
    rarity=Rarity.EPIC, elixir=4,
    base_damage=720, ct_modifier=0.25, ct_damage=180,  # stated 180
    is_splash=True, is_anti_air=True, is_anti_ground_swarm=True,
    is_pump_response=True,
    # 720 total over 8s + movement slow (stated)
    counters_win_conditions=["graveyard"],
    counters_defenders=["musketeer", "elixir_collector", "goblin_hut",
                        "witch", "night_witch", "skeleton_army",
                        "barbarians", "goblins", "goblin_gang"],
    counters_secondary_wc=["graveyard", "goblin_barrel"],
    meta_weight=1.5,
)

VOID = _spell(
    id="void", name="Void",
    rarity=Rarity.EPIC, elixir=3,
    base_damage=0,  # variable, scales down with cluster density (stated)
    ct_modifier=0.15, ct_damage=0,  # 15% focal, 20% multi — set dynamically
    is_splash=True, is_anti_air=True,
    # Single target 15%, 2-4 target 15%, 5+ target 20% (stated)
    # Damage scales dramatically downward with cluster density
    meta_weight=0.9, confidence=0.85,
)


FREEZE = _spell(
    id="freeze", name="Freeze",
    rarity=Rarity.EPIC, elixir=4,
    base_damage=115, ct_modifier=0.30, ct_damage=35,  # stated 35
    is_splash=True, is_anti_air=True,
    # Paralyzes all units 4.0s (stated); 115 base damage
    counters_win_conditions=["hog_rider", "giant", "golem",
                             "balloon", "graveyard"],
    meta_weight=1.1,
)

LIGHTNING = _spell(
    id="lightning", name="Lightning",
    rarity=Rarity.EPIC, elixir=6,
    base_damage=1056, ct_modifier=0.30, ct_damage=317,  # stated 317
    is_splash=False,  # single-hit per target (3 targets)
    is_anti_air=True, is_pump_response=True,
    # Strikes 3 highest-HP targets + 0.5s stun (stated)
    counters_win_conditions=["three_musketeers", "sparky"],
    counters_defenders=["inferno_tower", "three_musketeers",
                        "musketeer", "sparky", "goblin_machine",
                        "wizard", "executioner", "mega_minion",
                        "elixir_collector"],
    counters_secondary_wc=["three_musketeers", "sparky"],
    meta_weight=1.3,
)

ROCKET = _spell(
    id="rocket", name="Rocket",
    rarity=Rarity.RARE, elixir=6,
    base_damage=1484, ct_modifier=0.25, ct_damage=371,  # stated 371
    is_splash=True, is_anti_air=True, is_pump_response=True,
    # Highest localized burst; slow projectile (stated)
    counters_win_conditions=["three_musketeers"],
    counters_defenders=["three_musketeers", "elixir_collector",
                        "sparky", "goblin_machine", "musketeer"],
    meta_weight=1.2,
)

RAGE = _spell(
    id="rage", name="Rage",
    rarity=Rarity.EPIC, elixir=2,
    base_damage=192, ct_modifier=0.30, ct_damage=58,  # same as Zap CT (stated)
    is_splash=True, is_anti_air=True,
    # Boosts allied move/attack speed +35% + 192 drop damage (stated)
    is_damage_spell=True,  # deals 192 + buffs
    meta_weight=0.8,
)

TORNADO = _spell(
    id="tornado", name="Tornado",
    rarity=Rarity.EPIC, elixir=3,
    base_damage=280, ct_modifier=0.30, ct_damage=84,  # stated 84
    is_splash=True, is_anti_air=True, is_king_activator=True,
    # Physically drags all susceptible units to center (stated)
    # Primary king-tower activator — pulls units into king tower range
    counters_win_conditions=["hog_rider", "balloon", "graveyard",
                             "miner", "goblin_drill"],
    counters_defenders=["mini_pekka", "inferno_tower"],
    meta_weight=1.4,
)

CLONE = _spell(
    id="clone", name="Clone",
    rarity=Rarity.EPIC, elixir=3,
    base_damage=0, ct_modifier=0.0, ct_damage=0,
    is_damage_spell=False,  # no direct damage — duplicates troops at 1HP
    is_splash=False, is_anti_air=False,
    meta_weight=0.7,
)

GOBLIN_CURSE = _spell(
    id="goblin_curse", name="Goblin Curse",
    rarity=Rarity.EPIC, elixir=2,
    base_damage=160, ct_modifier=0.20, ct_damage=32,  # stated 32, 20%
    is_splash=True, is_anti_air=True,
    # Amplifies damage taken; defeated units spawn Goblins (stated)
    meta_weight=0.9,
)

ROYAL_DELIVERY = _spell(
    id="royal_delivery", name="Royal Delivery",
    rarity=Rarity.COMMON, elixir=3,
    base_damage=435, ct_modifier=0.0, ct_damage=0,  # stated N/A, restricted territory
    targets=TargetType.GROUND,
    is_damage_spell=False,  # lands in friendly territory; cannot damage crown tower directly
    is_splash=True,  # area impact
    is_anti_ground_swarm=True,
    # Drops Royal Recruit from sky + 435 impact damage, friendly territory only (stated)
    meta_weight=0.8,
)

VINES = _spell(
    id="vines", name="Vines",
    rarity=Rarity.EPIC, elixir=3,
    base_damage=280, ct_modifier=0.25, ct_damage=70,  # stated ~70
    is_splash=True, is_anti_air=True, is_anti_air_swarm=True,
    # Targets 3 highest HP units, pulls air to ground, 0.9s deploy delay (stated)
    # Ground-only high-DPS units can then finish them off
    counters_win_conditions=["balloon", "lava_hound", "electro_dragon",
                             "baby_dragon"],
    anti_air_strength=0.80,  # specialized vs air tanks (pulls them to ground)
    meta_weight=1.1,
)

GRAVEYARD = _spell(
    id="graveyard", name="Graveyard",
    rarity=Rarity.LEGENDARY, elixir=5,
    base_damage=0, ct_modifier=0.0, ct_damage=0,
    is_damage_spell=False,  # spawns skeletons, no direct damage
    is_win_condition=True,   # independently threatens towers via skeletons
    is_splash=False, is_anti_air=False,
    # Spawns skeletons over 10s (stated), modified spawn pattern
    win_condition_strength=0.85,
    counters_secondary_wc=[],
    meta_weight=1.5,
)

GOBLIN_BARREL = _spell(
    id="goblin_barrel", name="Goblin Barrel",
    rarity=Rarity.EPIC, elixir=3,
    base_damage=0, ct_modifier=0.0, ct_damage=0,  # spawns goblins
    is_damage_spell=False,
    is_win_condition=True,
    is_bridge_spam=True,
    is_king_activator=True,
    is_bait_card=True,
    bait_spells=["arrows", "zap", "the_log"],
    # Deploys goblins directly on tower — classic win condition
    win_condition_strength=0.75,
    bridge_spam_strength=0.80,
    counters_defenders=["skeleton_army", "goblins"],    # outbaits swarm responses
    counters_secondary_wc=[],
    meta_weight=1.6,
)

SKELETON_ARMY = _spell(
    id="skeleton_army", name="Skeleton Army",
    rarity=Rarity.EPIC, elixir=3,
    base_damage=0, ct_modifier=0.0, ct_damage=0,
    is_damage_spell=False,
    is_bait_card=True,
    is_splash=False,
    bait_spells=["fireball", "arrows", "the_log", "poison"],
    # Spawns 15 skeletons, collectively very high DPS, dies to any spell
    is_anti_ground_swarm=False,  # not splash
    meta_weight=1.1,
)

BARBARIAN_BARREL = _spell(
    id="barbarian_barrel", name="Barbarian Barrel",
    rarity=Rarity.EPIC, elixir=2,
    base_damage=0, ct_modifier=0.0, ct_damage=0,  # base barrel rolls
    targets=TargetType.GROUND,
    is_damage_spell=True,  # deals rolling impact damage
    is_splash=True,
    is_anti_ground_swarm=True,
    is_bait_card=True,
    bait_spells=["the_log", "zap"],
    # Base: Rolls forward, spawns 1 Barbarian on impact
    # Evo: Distinct enhanced knockback (approach_3 special notes)
    meta_weight=1.0,
)


# ===========================================================================
# Aggregated export
# ===========================================================================

ALL_SPELLS: list[Card] = [
    THE_LOG,
    ARROWS,
    GIANT_SNOWBALL,
    ZAP,
    EARTHQUAKE,
    FIREBALL,
    POISON,
    VOID,
    FREEZE,
    LIGHTNING,
    ROCKET,
    RAGE,
    TORNADO,
    CLONE,
    GOBLIN_CURSE,
    ROYAL_DELIVERY,
    VINES,
    GRAVEYARD,
    GOBLIN_BARREL,
    SKELETON_ARMY,
    BARBARIAN_BARREL,
]
