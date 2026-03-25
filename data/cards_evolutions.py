"""
data/cards_evolutions.py
=========================
All 39 Evolution Card instances.

Sources: Comprehensive Evolution Dataset (Level 11) in reference.md.
All evolved cards have the same base elixir as their base form.
The `base_card_id` field links to the base card slug for exclusion enforcement.
The `cycles` field records how many turns of base-card deployment are required.

Key balance notes from reference.md (March 2026):
  - Evo Royal Hogs landing damage: 115→84 (-27%); can no longer 1-shot Goblins (stated)
  - Evo Royal Giant hit speed: 1.7s→1.8s; medium melee can now land a strike in knockback gap (stated)
  - Evo Witch HP regen: 60→53 per skeleton (-11%) (stated)
  - Evo Skeleton Barrel death damage: 238→220 (-8%); can no longer 1-shot Minions (stated)
  - Evo Wall Breakers death damage: 291→258 (-11%); defensive nuke no longer viable (stated)
"""

from models.card import Card, CardType, SlotType, TargetType, SpeedTier, Rarity


def _evo(
    id, name, rarity, elixir,
    hp, damage, hit_speed, speed,
    targets, cycles,
    range=0.0,
    dps=None,
    base_card_id=None,
    stat_boost_notes="",
    evo_mechanic="",
    is_win_condition=False,
    is_anti_air=False,
    is_tank=False,
    is_support=False,
    is_bridge_spam=False,
    is_punishment=False,
    is_investment=False,
    is_king_activator=False,
    is_damage_spell=False,
    is_defensive_building=False,
    is_splash=False,
    is_anti_ground_swarm=False,
    is_anti_air_swarm=False,
    is_bait_card=False,
    is_pump_response=False,
    is_level_independent=False,
    bait_spells=None,
    win_condition_strength=0.0,
    anti_air_strength=0.0,
    punish_strength=0.0,
    bridge_spam_strength=0.0,
    tank_strength=None,
    support_strength=0.0,
    cycle_strength=None,
    splash_strength=0.0,
    ct_modifier=0.0, ct_damage=0,
    counters_win_conditions=None,
    counters_defenders=None,
    death_damage=0,
    spawn_hp=0,
    meta_weight=1.0,
    confidence=1.0,
    **kw,
) -> Card:
    computed_dps = round(damage / hit_speed, 1) if hit_speed > 0 else 0.0
    ts = tank_strength if tank_strength is not None else round(min(1.0, hp / 5120), 2)
    cs = cycle_strength if cycle_strength is not None else round(max(0.0, (7 - elixir) / 6), 2)
    return Card(
        id=id, name=name,
        rarity=rarity, card_type=CardType.TROOP, slot_type=SlotType.EVOLUTION,
        elixir=elixir, base_card_id=base_card_id or id.replace("evo_", ""),
        hp=hp, damage=damage, dps=dps or computed_dps,
        hit_speed=hit_speed, speed=speed, range=range,
        targets=targets, death_damage=death_damage, spawn_hp=spawn_hp,
        is_win_condition=is_win_condition,
        is_anti_air=is_anti_air, is_tank=is_tank, is_support=is_support,
        is_bridge_spam=is_bridge_spam, is_punishment=is_punishment,
        is_investment=is_investment, is_king_activator=is_king_activator,
        is_damage_spell=is_damage_spell, is_defensive_building=is_defensive_building,
        is_splash=is_splash, is_anti_ground_swarm=is_anti_ground_swarm,
        is_anti_air_swarm=is_anti_air_swarm, is_bait_card=is_bait_card,
        is_pump_response=is_pump_response, is_level_independent=is_level_independent,
        bait_spells=bait_spells or [],
        win_condition_strength=win_condition_strength,
        anti_air_strength=anti_air_strength, punish_strength=punish_strength,
        bridge_spam_strength=bridge_spam_strength, tank_strength=ts,
        support_strength=support_strength, cycle_strength=cs,
        splash_strength=splash_strength,
        ct_modifier=ct_modifier, ct_damage=ct_damage,
        counters_win_conditions=counters_win_conditions or [],
        counters_defenders=counters_defenders or [],
        meta_weight=meta_weight, confidence=confidence,
        last_verified="2026-03-23",
        **kw,
    )


# ===========================================================================
# EVOLUTIONS  (sorted by base elixir cost, then name)
# ===========================================================================

# --- 1-elixir Evolutions ---

EVO_SKELETONS = _evo(
    id="evo_skeletons", name="Evo Skeletons",
    base_card_id="skeletons",
    rarity=Rarity.COMMON, elixir=1, cycles=2,
    hp=81, damage=81, hit_speed=1.0, speed=SpeedTier.FAST,
    targets=TargetType.GROUND, range=0.0,
    # Spawns extra skeleton on every successful strike (up to 8 total) (stated)
    is_bait_card=True, bait_spells=["zap", "arrows", "the_log"],
    cycle_strength=1.0,
    meta_weight=1.4,
)

EVO_ICE_SPIRIT = _evo(
    id="evo_ice_spirit", name="Evo Ice Spirit",
    base_card_id="ice_spirit",
    rarity=Rarity.COMMON, elixir=1, cycles=2,
    hp=230, damage=109, hit_speed=0.0, speed=SpeedTier.VERY_FAST,
    targets=TargetType.BOTH,
    # +33% splash radius; applies 1.1s freeze then secondary 1.1s after 3s delay (stated)
    is_splash=True, is_anti_air=True, is_anti_ground_swarm=True, is_anti_air_swarm=True,
    splash_strength=0.65,
    cycle_strength=1.0,
    meta_weight=1.3,
)

# --- 2-elixir Evolutions ---

EVO_BATS = _evo(
    id="evo_bats", name="Evo Bats",
    base_card_id="bats",
    rarity=Rarity.COMMON, elixir=2, cycles=2,
    hp=81, damage=81, hit_speed=1.2, speed=SpeedTier.VERY_FAST,
    targets=TargetType.BOTH,
    # +50% HP; heals 2 pulses/sec on strike up to 2× max HP (stated)
    is_anti_air=True, is_anti_air_swarm=True, is_bait_card=True,
    bait_spells=["arrows", "zap"],
    anti_air_strength=0.50,
    cycle_strength=0.85,
    meta_weight=1.1,
)

EVO_ZAP = _evo(
    id="evo_zap", name="Evo Zap",
    base_card_id="zap",
    rarity=Rarity.COMMON, elixir=2, cycles=2,
    hp=0, damage=192, hit_speed=0.0, speed=SpeedTier.VERY_FAST,
    targets=TargetType.BOTH, range=3.5,
    is_damage_spell=True, is_splash=True, is_anti_air=True,
    is_anti_ground_swarm=True, is_anti_air_swarm=True,
    ct_modifier=0.30, ct_damage=58,
    # Emits secondary expanding concentric shockwaves, re-applying stun (stated)
    cycle_strength=0.85,
    meta_weight=1.4,
    confidence=0.95,
)

EVO_BOMBER = _evo(
    id="evo_bomber", name="Evo Bomber",
    base_card_id="bomber",
    rarity=Rarity.COMMON, elixir=2, cycles=2,
    hp=304, damage=225, hit_speed=1.8, speed=SpeedTier.MEDIUM,
    targets=TargetType.GROUND, range=4.5,
    # Projectile bounces twice, traversing immense linear distance (stated)
    is_splash=True, is_anti_ground_swarm=True,
    splash_strength=0.70,
    cycle_strength=0.85,
    meta_weight=1.0,
)

EVO_WALL_BREAKERS = _evo(
    id="evo_wall_breakers", name="Evo Wall Breakers",
    base_card_id="wall_breakers",
    rarity=Rarity.EPIC, elixir=2, cycles=2,
    hp=329, damage=391, hit_speed=0.0, speed=SpeedTier.VERY_FAST,
    targets=TargetType.BUILDINGS,
    death_damage=258,  # nerfed from 291→258 (stated)
    # Survives initial barrel; continues running for 50% impact damage (stated)
    # Death damage 258 — can no longer 1-shot Minions defensively (stated)
    is_bridge_spam=True, is_punishment=True, is_bait_card=True,
    bridge_spam_strength=0.85, punish_strength=0.80,
    bait_spells=["the_log"],
    cycle_strength=0.85,
    meta_weight=1.2,
)

EVO_BARBARIAN_BARREL = _evo(
    id="evo_barbarian_barrel", name="Evo Barbarian Barrel",
    base_card_id="barbarian_barrel",
    rarity=Rarity.EPIC, elixir=2, cycles=2,
    hp=0, damage=0, hit_speed=0.0, speed=SpeedTier.VERY_FAST,
    targets=TargetType.GROUND,
    is_damage_spell=True, is_splash=True, is_anti_ground_swarm=True,
    is_bait_card=True, bait_spells=["the_log"],
    # Distinct from Hero variant; applies radically enhanced physical knockback (stated)
    cycle_strength=0.85,
    meta_weight=1.0,
)

EVO_GIANT_SNOWBALL = _evo(
    id="evo_giant_snowball", name="Evo Giant Snowball",
    base_card_id="giant_snowball",
    rarity=Rarity.COMMON, elixir=2, cycles=2,
    hp=0, damage=192, hit_speed=0.0, speed=SpeedTier.VERY_FAST,
    targets=TargetType.BOTH, range=3.5,
    is_damage_spell=True, is_splash=True, is_anti_air=True,
    is_anti_ground_swarm=True, is_anti_air_swarm=True,
    ct_modifier=0.30, ct_damage=54,
    # Expanded radius; permanently applies movement freeze to center targets (stated)
    cycle_strength=0.85,
    meta_weight=1.1,
)

# --- 3-elixir Evolutions ---

EVO_KNIGHT = _evo(
    id="evo_knight", name="Evo Knight",
    base_card_id="knight",
    rarity=Rarity.COMMON, elixir=3, cycles=2,
    hp=1650, damage=202, hit_speed=1.2, speed=SpeedTier.MEDIUM,
    targets=TargetType.GROUND,
    # 60% damage reduction shield while moving/deploying (stated)
    is_tank=True, is_level_independent=True,
    tank_strength=0.45,  # effectively doubled HP while shield active
    cycle_strength=0.65,
    counters_win_conditions=["hog_rider", "battle_ram"],
    meta_weight=1.5,
)

EVO_ARCHERS = _evo(
    id="evo_archers", name="Evo Archers",
    base_card_id="archers",
    rarity=Rarity.COMMON, elixir=3, cycles=2,
    hp=304, damage=112, hit_speed=0.9, speed=SpeedTier.MEDIUM,
    targets=TargetType.BOTH, range=5.0,
    # +20% range; 50% bonus damage to targets 4-6 tiles away (stated)
    is_anti_air=True,
    anti_air_strength=0.65,
    cycle_strength=0.65,
    meta_weight=1.1,
)

EVO_FIRECRACKER = _evo(
    id="evo_firecracker", name="Evo Firecracker",
    base_card_id="firecracker",
    rarity=Rarity.COMMON, elixir=3, cycles=2,
    hp=304, damage=64, hit_speed=3.0, speed=SpeedTier.FAST,
    targets=TargetType.BOTH, range=6.0,
    # Projectiles leave lingering AoE incendiary sparks + 15% move slow (stated)
    is_anti_air=True, is_splash=True, is_bait_card=True,
    bait_spells=["the_log", "arrows"],
    anti_air_strength=0.55, splash_strength=0.55,
    cycle_strength=0.65,
    meta_weight=1.1,
)

EVO_ROYAL_GHOST = _evo(
    id="evo_royal_ghost", name="Evo Royal Ghost",
    base_card_id="royal_ghost",
    rarity=Rarity.LEGENDARY, elixir=3, cycles=2,
    hp=1210, damage=261, hit_speed=1.8, speed=SpeedTier.FAST,
    targets=TargetType.GROUND,
    # Drastically enhanced invisibility; strikes without immediate reveal (stated)
    is_bridge_spam=True, is_punishment=True,
    bridge_spam_strength=0.70, punish_strength=0.65,
    cycle_strength=0.65,
    meta_weight=1.0,
)

EVO_SKELETON_ARMY = _evo(
    id="evo_skeleton_army", name="Evo Skeleton Army",
    base_card_id="skeleton_army",
    rarity=Rarity.EPIC, elixir=3, cycles=1,
    hp=81, damage=81, hit_speed=1.0, speed=SpeedTier.FAST,
    targets=TargetType.GROUND,
    is_bait_card=True, bait_spells=["fireball", "arrows", "the_log", "poison"],
    # Immortal Skeleton General; fallen skeletons return as medium-speed ghosts (stated)
    cycle_strength=0.65,
    meta_weight=1.0,
)

EVO_DART_GOBLIN = _evo(
    id="evo_dart_goblin", name="Evo Dart Goblin",
    base_card_id="dart_goblin",
    rarity=Rarity.RARE, elixir=3, cycles=2,
    hp=260, damage=131, hit_speed=0.7, speed=SpeedTier.VERY_FAST,
    targets=TargetType.BOTH, range=7.0,
    # Blowdarts apply continuous poison (25% CT dmg) (stated)
    is_anti_air=True, is_bait_card=True,
    bait_spells=["arrows", "zap"],
    anti_air_strength=0.70,
    cycle_strength=0.65,
    meta_weight=0.9,
)

EVO_SKELETON_BARREL = _evo(
    id="evo_skeleton_barrel", name="Evo Skeleton Barrel",
    base_card_id="skeleton_barrel",
    rarity=Rarity.COMMON, elixir=3, cycles=2,
    hp=532, damage=132, hit_speed=0.0, speed=SpeedTier.FAST,
    targets=TargetType.BUILDINGS,
    death_damage=220,  # nerfed from 238→220 (stated); cannot 1-shot Minions
    # Massive kinetic drop-damage on burst (stated)
    is_bridge_spam=True, is_win_condition=True,
    win_condition_strength=0.55, bridge_spam_strength=0.65,
    cycle_strength=0.65,
    meta_weight=1.0,
)

EVO_CANNON = _evo(
    id="evo_cannon", name="Evo Cannon",
    base_card_id="cannon",
    rarity=Rarity.COMMON, elixir=3, cycles=2,
    hp=896, damage=212, hit_speed=0.8, speed=SpeedTier.SLOW,
    targets=TargetType.GROUND,
    # Operates as rapid-fire battery, tracking targets dynamically across lanes (stated)
    is_defensive_building=True,
    counters_win_conditions=["hog_rider", "battle_ram", "ram_rider"],
    cycle_strength=0.65,
    meta_weight=1.1,
)

EVO_GOBLIN_BARREL = _evo(
    id="evo_goblin_barrel", name="Evo Goblin Barrel",
    base_card_id="goblin_barrel",
    rarity=Rarity.EPIC, elixir=3, cycles=2,
    hp=0, damage=0, hit_speed=0.0, speed=SpeedTier.VERY_FAST,
    targets=TargetType.GROUND,
    # Deploys deceptive decoy barrels alongside primary payload (stated)
    is_win_condition=True, is_bridge_spam=True, is_bait_card=True,
    bait_spells=["arrows", "zap", "the_log"],
    win_condition_strength=0.80, bridge_spam_strength=0.85,
    is_king_activator=True,
    cycle_strength=0.65,
    meta_weight=1.3,
)

# --- 4-elixir Evolutions ---

EVO_VALKYRIE = _evo(
    id="evo_valkyrie", name="Evo Valkyrie",
    base_card_id="valkyrie",
    rarity=Rarity.RARE, elixir=4, cycles=2,
    hp=1908, damage=266, hit_speed=1.5, speed=SpeedTier.MEDIUM,
    targets=TargetType.GROUND,
    # Axe generates 5.5-tile cyclonic tornado pulling units inward (stated)
    is_splash=True, is_anti_ground_swarm=True, is_tank=True,
    splash_strength=0.85, tank_strength=0.37,
    counters_win_conditions=["goblin_barrel", "graveyard"],
    counters_defenders=["skeleton_army", "goblins", "goblin_gang"],
    meta_weight=1.2,
)

EVO_MUSKETEER = _evo(
    id="evo_musketeer", name="Evo Musketeer",
    base_card_id="musketeer",
    rarity=Rarity.RARE, elixir=4, cycles=2,
    hp=720, damage=218, hit_speed=1.0, speed=SpeedTier.MEDIUM,
    targets=TargetType.BOTH, range=6.0,
    # Firearm projectiles pierce targets, extended linear distance (stated)
    is_anti_air=True, is_support=True,
    anti_air_strength=0.90,
    counters_win_conditions=["balloon", "lava_hound"],
    meta_weight=1.1,
)

EVO_BATTLE_RAM = _evo(
    id="evo_battle_ram", name="Evo Battle Ram",
    base_card_id="battle_ram",
    rarity=Rarity.RARE, elixir=4, cycles=2,
    hp=967, damage=286, hit_speed=0.0, speed=SpeedTier.MEDIUM,
    targets=TargetType.BUILDINGS,
    # Tremendous charge velocity; spawned Barbarians arrive pre-evolved (stated)
    is_win_condition=True, is_bridge_spam=True, is_punishment=True,
    win_condition_strength=0.80,
    bridge_spam_strength=0.90, punish_strength=0.85,
    meta_weight=1.3,
)

EVO_MORTAR = _evo(
    id="evo_mortar", name="Evo Mortar",
    base_card_id="mortar",
    rarity=Rarity.COMMON, elixir=4, cycles=2,
    hp=1472, damage=266, hit_speed=4.0, speed=SpeedTier.SLOW,  # -20% attack period (stated)
    targets=TargetType.GROUND,
    # -20% attack period (4.0s not 5.0s); impact spawns aggressive Goblin (stated)
    is_win_condition=True, is_investment=True, is_defensive_building=True,
    win_condition_strength=0.65,
    meta_weight=1.0,
)

EVO_LUMBERJACK = _evo(
    id="evo_lumberjack", name="Evo Lumberjack",
    base_card_id="lumberjack",
    rarity=Rarity.LEGENDARY, elixir=4, cycles=2,
    hp=1270, damage=240, hit_speed=0.8, speed=SpeedTier.VERY_FAST,
    targets=TargetType.GROUND,
    # On death: expanded high-potency "super-rage" spell (stated)
    is_bridge_spam=True, is_punishment=True, is_support=True,
    bridge_spam_strength=0.80, punish_strength=0.75, support_strength=0.75,
    meta_weight=1.1,
)

EVO_HUNTER = _evo(
    id="evo_hunter", name="Evo Hunter",
    base_card_id="hunter",
    rarity=Rarity.EPIC, elixir=4, cycles=1,
    hp=838, damage=84, hit_speed=2.2, speed=SpeedTier.MEDIUM,
    targets=TargetType.BOTH, range=4.0, dps=381.0,
    # Widened shotgun spread + heavy unit knockback (stated)
    is_anti_air=True, is_splash=True,
    anti_air_strength=0.75, splash_strength=0.70,
    counters_win_conditions=["balloon", "lava_hound", "giant"],
    meta_weight=1.0,
)

EVO_BABY_DRAGON = _evo(
    id="evo_baby_dragon", name="Evo Baby Dragon",
    base_card_id="baby_dragon",
    rarity=Rarity.EPIC, elixir=4, cycles=2,
    hp=1152, damage=161, hit_speed=1.5, speed=SpeedTier.FAST,
    targets=TargetType.BOTH, range=3.5,
    # Expanded blast radius, exponential damage to clustered units (stated)
    is_anti_air=True, is_splash=True, is_anti_ground_swarm=True, is_anti_air_swarm=True,
    anti_air_strength=0.60, splash_strength=0.70,
    meta_weight=1.0,
)

EVO_INFERNO_DRAGON = _evo(
    id="evo_inferno_dragon", name="Evo Inferno Dragon",
    base_card_id="inferno_dragon",
    rarity=Rarity.LEGENDARY, elixir=4, cycles=1,
    hp=1294, damage=35, hit_speed=0.4, speed=SpeedTier.MEDIUM,
    targets=TargetType.BOTH, range=4.0,
    # Ramping damage targets multiple distinct units simultaneously in cone (stated)
    is_anti_air=True,
    anti_air_strength=0.85,
    counters_win_conditions=["giant", "golem", "balloon", "electro_giant",
                             "lava_hound", "mega_knight"],
    meta_weight=1.2,
)

EVO_TESLA = _evo(
    id="evo_tesla", name="Evo Tesla",
    base_card_id="tesla",
    rarity=Rarity.COMMON, elixir=4, cycles=2,
    hp=1152, damage=230, hit_speed=1.1, speed=SpeedTier.SLOW,
    targets=TargetType.BOTH,
    is_anti_air=True, is_defensive_building=True,
    anti_air_strength=0.65,
    # Massive radial electro-pulse on submerge/emerge, resetting targets (stated)
    counters_win_conditions=["hog_rider", "balloon", "battle_ram"],
    meta_weight=1.1,
)

EVO_GOBLIN_DRILL = _evo(
    id="evo_goblin_drill", name="Evo Goblin Drill",
    base_card_id="goblin_drill",
    rarity=Rarity.EPIC, elixir=4, cycles=2,
    hp=1100, damage=120, hit_speed=1.2, speed=SpeedTier.FAST,
    targets=TargetType.BUILDINGS,
    # Secondary resurface event, additional Goblin output post-destruction (stated)
    is_win_condition=True, is_bridge_spam=True, is_king_activator=True,
    win_condition_strength=0.70, bridge_spam_strength=0.75,
    meta_weight=1.0, confidence=0.85,
)

EVO_FURNACE = _evo(
    id="evo_furnace", name="Evo Furnace",
    base_card_id="furnace",
    rarity=Rarity.RARE, elixir=4, cycles=1,
    hp=1000, damage=0, hit_speed=0.0, speed=SpeedTier.SLOW,
    targets=TargetType.GROUND,
    # Evolution mechanics undergoing structural overhaul (stated)
    # Furnace base is a TROOP (reclassified); evo maintains troop classification
    meta_weight=0.6, confidence=0.70,
)

# --- 5-elixir Evolutions ---

EVO_BARBARIANS = _evo(
    id="evo_barbarians", name="Evo Barbarians",
    base_card_id="barbarians",
    rarity=Rarity.COMMON, elixir=5, cycles=1,
    hp=670, damage=192, hit_speed=1.3, speed=SpeedTier.MEDIUM,
    targets=TargetType.GROUND,
    # +10% HP; successful attacks stack +35% move/attack speed for 3s (stated)
    is_punishment=True, is_anti_ground_swarm=False,
    punish_strength=0.60,
    meta_weight=0.9,
)

EVO_WIZARD = _evo(
    id="evo_wizard", name="Evo Wizard",
    base_card_id="wizard",
    rarity=Rarity.RARE, elixir=5, cycles=1,
    hp=720, damage=281, hit_speed=1.4, speed=SpeedTier.MEDIUM,
    targets=TargetType.BOTH, range=5.5,
    # Fireballs apply continuous burn, negating heal mechanics (stated)
    is_anti_air=True, is_splash=True, is_anti_ground_swarm=True, is_anti_air_swarm=True,
    anti_air_strength=0.80, splash_strength=0.85,
    meta_weight=1.0,
)

EVO_EXECUTIONER = _evo(
    id="evo_executioner", name="Evo Executioner",
    base_card_id="executioner",
    rarity=Rarity.EPIC, elixir=5, cycles=1,
    hp=1210, damage=168, hit_speed=2.4, speed=SpeedTier.MEDIUM,
    targets=TargetType.BOTH, range=4.5, dps=140.0,
    # Extended axe throw; return velocity manipulated for maximum dwell time (stated)
    is_anti_air=True, is_splash=True, is_anti_ground_swarm=True, is_anti_air_swarm=True,
    anti_air_strength=0.70, splash_strength=0.75,
    meta_weight=0.9,
)

EVO_WITCH = _evo(
    id="evo_witch", name="Evo Witch",
    base_card_id="witch",
    rarity=Rarity.EPIC, elixir=5, cycles=1,
    hp=838, damage=134, hit_speed=1.1, speed=SpeedTier.MEDIUM,
    targets=TargetType.BOTH, range=5.5,
    spawn_hp=81,
    # HP regen per spawned/killed skeleton: 60→53 HP (-11%) (stated)
    # Now susceptible to secondary spell chip damage after Fireball
    is_anti_air=True, is_splash=True, is_support=True,
    anti_air_strength=0.55, splash_strength=0.60, support_strength=0.65,
    meta_weight=0.9,
)

EVO_ROYAL_HOGS = _evo(
    id="evo_royal_hogs", name="Evo Royal Hogs",
    base_card_id="royal_hogs",
    rarity=Rarity.RARE, elixir=5, cycles=1,
    hp=838, damage=72, hit_speed=1.2, speed=SpeedTier.VERY_FAST,
    targets=TargetType.BUILDINGS,
    # Landing damage nerfed 115→84 (-27%); no longer 1-shots Goblins/Spear Goblins (stated)
    is_win_condition=True, is_bridge_spam=True, is_punishment=True,
    win_condition_strength=0.65,
    bridge_spam_strength=0.75, punish_strength=0.70,
    meta_weight=1.0,
)

EVO_ELECTRO_DRAGON = _evo(
    id="evo_electro_dragon", name="Evo Electro Dragon",
    base_card_id="electro_dragon",
    rarity=Rarity.EPIC, elixir=5, cycles=1,
    hp=944, damage=192, hit_speed=2.1, speed=SpeedTier.MEDIUM,
    targets=TargetType.BOTH, range=3.5,
    # Lightning chain capacity infinite if targets within rigid proximity (stated)
    is_anti_air=True, is_splash=True,
    anti_air_strength=0.65,
    meta_weight=0.9,
)

# --- 6-elixir Evolutions ---

EVO_ROYAL_GIANT = _evo(
    id="evo_royal_giant", name="Evo Royal Giant",
    base_card_id="royal_giant",
    rarity=Rarity.COMMON, elixir=6, cycles=1,
    hp=3061, damage=254, hit_speed=1.8, speed=SpeedTier.SLOW,  # 1.7→1.8s (stated)
    targets=TargetType.BUILDINGS, range=5.0,
    # Cannon blasts generate 2.5-tile physical knockback shockwave (stated)
    # Hit speed 1.7→1.8s (stated): medium melee can now land a strike in gap
    is_win_condition=True, is_tank=True,
    win_condition_strength=0.75, tank_strength=0.60,
    meta_weight=1.1,
)

EVO_GOBLIN_GIANT = _evo(
    id="evo_goblin_giant", name="Evo Goblin Giant",
    base_card_id="goblin_giant",
    rarity=Rarity.EPIC, elixir=6, cycles=1,
    hp=3024, damage=176, hit_speed=1.7, speed=SpeedTier.MEDIUM,
    targets=TargetType.BUILDINGS,
    spawn_hp=132,
    # Backpack Spear Goblins throw highly potent, accelerated projectiles (stated)
    is_win_condition=True, is_tank=True,
    win_condition_strength=0.75, tank_strength=0.59,
    meta_weight=0.9,
)

# --- 7-elixir Evolutions ---

EVO_P_E_K_K_A = _evo(
    id="evo_p_e_k_k_a", name="Evo P.E.K.K.A.",
    base_card_id="p_e_k_k_a",
    rarity=Rarity.EPIC, elixir=7, cycles=1,
    hp=3760, damage=816, hit_speed=1.8, speed=SpeedTier.SLOW,
    targets=TargetType.GROUND, dps=453.0,
    # Restores HP % upon securing fatal blow on enemy troop (stated)
    is_tank=True, is_punishment=True,
    tank_strength=0.73,
    punish_strength=0.70,
    counters_win_conditions=["hog_rider", "battle_ram", "prince"],
    meta_weight=1.1,
)

EVO_MEGA_KNIGHT = _evo(
    id="evo_mega_knight", name="Evo Mega Knight",
    base_card_id="mega_knight",
    rarity=Rarity.LEGENDARY, elixir=7, cycles=1,
    hp=3993, damage=268, hit_speed=1.7, speed=SpeedTier.MEDIUM,
    targets=TargetType.GROUND,
    # Deployment jump + subsequent leaps apply secondary disruptive shockwave (stated)
    is_tank=True, is_splash=True, is_anti_ground_swarm=True,
    tank_strength=0.78, splash_strength=0.80,
    meta_weight=1.2,
)

EVO_ROYAL_RECRUITS = _evo(
    id="evo_royal_recruits", name="Evo Royal Recruits",
    base_card_id="royal_recruits",
    rarity=Rarity.COMMON, elixir=7, cycles=1,
    hp=532, damage=133, hit_speed=1.3, speed=SpeedTier.MEDIUM,
    targets=TargetType.GROUND,
    # Shield shed → Very Fast charge, 2× impact damage (stated)
    is_tank=False, is_punishment=True,
    punish_strength=0.55,
    meta_weight=0.8,
)


# ===========================================================================
# Aggregated export
# ===========================================================================

ALL_EVOLUTIONS: list[Card] = [
    EVO_SKELETONS, EVO_ICE_SPIRIT,
    EVO_BATS, EVO_ZAP, EVO_BOMBER, EVO_WALL_BREAKERS,
    EVO_BARBARIAN_BARREL, EVO_GIANT_SNOWBALL,
    EVO_KNIGHT, EVO_ARCHERS, EVO_FIRECRACKER, EVO_ROYAL_GHOST,
    EVO_SKELETON_ARMY, EVO_DART_GOBLIN, EVO_SKELETON_BARREL,
    EVO_CANNON, EVO_GOBLIN_BARREL,
    EVO_VALKYRIE, EVO_MUSKETEER, EVO_BATTLE_RAM, EVO_MORTAR,
    EVO_LUMBERJACK, EVO_HUNTER, EVO_BABY_DRAGON, EVO_INFERNO_DRAGON,
    EVO_TESLA, EVO_GOBLIN_DRILL, EVO_FURNACE,
    EVO_BARBARIANS, EVO_WIZARD, EVO_EXECUTIONER, EVO_WITCH,
    EVO_ROYAL_HOGS, EVO_ELECTRO_DRAGON,
    EVO_ROYAL_GIANT, EVO_GOBLIN_GIANT,
    EVO_P_E_K_K_A, EVO_MEGA_KNIGHT, EVO_ROYAL_RECRUITS,
]
