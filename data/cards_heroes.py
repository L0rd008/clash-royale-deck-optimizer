"""
data/cards_heroes.py
=====================
All 18 Hero & Champion Card instances.

Sources: Hero and Champion Statistical Dataset (Level 11) in reference.md.
Balance notes: Boss Bandit nerfed 268→245 dmg; Hero Giant HP 3% reduction to 3,968;
Hero Magic Archer and Hero Barbarian Barrel are new Q1 2026 additions.

Hero vs Champion distinction was merged in late 2025 (stated) — all use
slot_type=SlotType.HERO and occupy the single Hero slot.

CRITICAL SLOT RULE: Max 1 Hero per deck. No double-hero configs.
"""

from models.card import Card, CardType, SlotType, TargetType, SpeedTier, Rarity


def _hero(
    id, name, rarity, elixir, ability_elixir,
    hp, damage, hit_speed, speed,
    range=0.0,
    targets=TargetType.GROUND,
    base_card_id=None,
    dps=None,
    is_win_condition=False,
    is_anti_air=False,
    is_support=False,
    is_tank=False,
    is_bridge_spam=False,
    is_punishment=False,
    is_investment=False,
    is_king_activator=False,
    is_defensive_building=False,
    is_pump_response=False,
    is_splash=False,
    is_anti_ground_swarm=False,
    is_anti_air_swarm=False,
    is_damage_spell=False,
    is_bait_card=False,
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
    counters_win_conditions=None,
    counters_defenders=None,
    counters_secondary_wc=None,
    meta_weight=1.0,
    confidence=1.0,
    **kw,
) -> Card:
    computed_dps = round(damage / hit_speed, 1) if hit_speed > 0 else 0.0
    ts = tank_strength if tank_strength is not None else round(min(1.0, hp / 5120), 2)
    cs = cycle_strength if cycle_strength is not None else round(max(0.0, (7 - elixir) / 6), 2)
    return Card(
        id=id, name=name,
        rarity=rarity, card_type=CardType.TROOP, slot_type=SlotType.HERO,
        elixir=elixir, ability_elixir=ability_elixir,
        base_card_id=base_card_id,
        hp=hp, damage=damage, dps=dps or computed_dps,
        hit_speed=hit_speed, speed=speed, range=range,
        targets=targets,
        is_win_condition=is_win_condition,
        is_anti_air=is_anti_air,
        is_support=is_support,
        is_tank=is_tank,
        is_bridge_spam=is_bridge_spam,
        is_punishment=is_punishment,
        is_investment=is_investment,
        is_king_activator=is_king_activator,
        is_defensive_building=is_defensive_building,
        is_pump_response=is_pump_response,
        is_splash=is_splash,
        is_anti_ground_swarm=is_anti_ground_swarm,
        is_anti_air_swarm=is_anti_air_swarm,
        is_damage_spell=is_damage_spell,
        is_bait_card=is_bait_card,
        is_level_independent=is_level_independent,
        bait_spells=bait_spells or [],
        win_condition_strength=win_condition_strength,
        anti_air_strength=anti_air_strength,
        punish_strength=punish_strength,
        bridge_spam_strength=bridge_spam_strength,
        tank_strength=ts,
        support_strength=support_strength,
        cycle_strength=cs,
        splash_strength=splash_strength,
        counters_win_conditions=counters_win_conditions or [],
        counters_defenders=counters_defenders or [],
        counters_secondary_wc=counters_secondary_wc or [],
        meta_weight=meta_weight, confidence=confidence,
        last_verified="2026-03-23",
        **kw,
    )


# ===========================================================================
# CHAMPIONS
# ===========================================================================

BOSS_BANDIT = _hero(
    id="boss_bandit", name="Boss Bandit",
    rarity=Rarity.LEGENDARY, elixir=6, ability_elixir=1,
    hp=2624, damage=245, hit_speed=1.1, speed=SpeedTier.FAST,
    # Getaway Grenade: dashes, deals 491 dash damage (stated)
    # Nerfed from 268→245 base damage (stated)
    is_win_condition=True, is_bridge_spam=True, is_punishment=True,
    win_condition_strength=0.80,
    bridge_spam_strength=0.85,
    punish_strength=0.80,
    counters_win_conditions=["hog_rider", "balloon"],
    meta_weight=1.3,
)

GOLDEN_KNIGHT = _hero(
    id="golden_knight", name="Golden Knight",
    rarity=Rarity.LEGENDARY, elixir=4, ability_elixir=1,
    hp=1800, damage=160, hit_speed=0.9, speed=SpeedTier.MEDIUM,
    base_card_id="knight",
    # Dashing Dash: chains attacks across multiple units; 12s cooldown (stated)
    is_bridge_spam=True, is_punishment=True,
    bridge_spam_strength=0.75,
    punish_strength=0.70,
    counters_win_conditions=["hog_rider"],
    meta_weight=1.2,
)

ARCHER_QUEEN = _hero(
    id="archer_queen", name="Archer Queen",
    rarity=Rarity.LEGENDARY, elixir=5, ability_elixir=1,
    hp=1000, damage=225, hit_speed=1.2, speed=SpeedTier.MEDIUM,
    range=5.0, targets=TargetType.BOTH,
    # Cloaking Cape: invisible + drastically increased fire rate (stated)
    is_anti_air=True, is_support=True,
    anti_air_strength=0.70,
    support_strength=0.65,
    meta_weight=1.3,
)

SKELETON_KING = _hero(
    id="skeleton_king", name="Skeleton King",
    rarity=Rarity.LEGENDARY, elixir=4, ability_elixir=2,
    hp=2300, damage=205, hit_speed=1.6, speed=SpeedTier.MEDIUM,
    base_card_id="skeleton_king",  # standalone, no base card in deck to conflict
    # Soul Summoning: collects souls of fallen troops → skeleton swarm (stated)
    is_support=True,
    support_strength=0.70,
    meta_weight=1.1,
)

MIGHTY_MINER = _hero(
    id="mighty_miner", name="Mighty Miner",
    rarity=Rarity.LEGENDARY, elixir=4, ability_elixir=1,
    hp=2400, damage=40, hit_speed=0.4, speed=SpeedTier.MEDIUM,
    targets=TargetType.GROUND,
    base_card_id="miner",
    # Explosive Escape: drops bomb + burrows to opposite lane (stated)
    # Variable damage: 40 min → 800 max per hit
    is_win_condition=True, is_bridge_spam=True, is_king_activator=True,
    win_condition_strength=0.75,
    bridge_spam_strength=0.80,
    punish_strength=0.75,
    meta_weight=1.2,
)

MONK = _hero(
    id="monk", name="Monk",
    rarity=Rarity.LEGENDARY, elixir=5, ability_elixir=1,
    hp=2000, damage=140, hit_speed=0.9, speed=SpeedTier.MEDIUM,
    # Pensive Protection: reduces incoming damage + reflects projectiles (stated)
    is_tank=True, is_support=True,
    tank_strength=0.39,
    support_strength=0.60,
    meta_weight=1.0,
)

LITTLE_PRINCE = _hero(
    id="little_prince", name="Little Prince",
    rarity=Rarity.LEGENDARY, elixir=3, ability_elixir=3,
    hp=700, damage=110, hit_speed=1.2, speed=SpeedTier.MEDIUM,
    range=6.0, targets=TargetType.BOTH,
    # Royal Rescue: summons Guardian who dashes forward, knocking back enemies
    # 1.2s → 0.4s (sped up attack after charge)
    is_anti_air=True,
    anti_air_strength=0.50,
    cycle_strength=0.65,  # 3 elixir
    meta_weight=1.2,
)

GOBLINSTEIN = _hero(
    id="goblinstein", name="Goblinstein",
    rarity=Rarity.LEGENDARY, elixir=5, ability_elixir=2,
    hp=2200, damage=150, hit_speed=1.5, speed=SpeedTier.MEDIUM,
    targets=TargetType.BUILDINGS,
    # Lightning Link: electrifies tether between monster and doctor (stated)
    # King Tower activator via Lightning Link path (per final plan Section 3.8)
    is_win_condition=True, is_tank=True, is_king_activator=True,
    win_condition_strength=0.70,
    tank_strength=0.43,
    meta_weight=1.1,
)


# ===========================================================================
# HEROES (merged class from late 2025)
# ===========================================================================

HERO_KNIGHT = _hero(
    id="hero_knight", name="Hero Knight",
    rarity=Rarity.LEGENDARY, elixir=3, ability_elixir=2,
    hp=1650, damage=167, hit_speed=1.2, speed=SpeedTier.MEDIUM,
    base_card_id="knight",
    # Triumphant Taunt: 6.5-tile taunt radius + 30% HP shield (stated)
    # Radius nerfed from 7.5→6.5 tiles (March 2026, stated)
    is_tank=True, is_support=True,
    tank_strength=0.32,
    support_strength=0.55,
    cycle_strength=0.65,  # 3 elixir
    counters_win_conditions=["hog_rider", "battle_ram"],      # kite via taunt
    meta_weight=1.2,
)

HERO_GIANT = _hero(
    id="hero_giant", name="Hero Giant",
    rarity=Rarity.LEGENDARY, elixir=5, ability_elixir=2,
    hp=3968, damage=254, hit_speed=1.5, speed=SpeedTier.SLOW,
    targets=TargetType.BUILDINGS,
    # Heroic Hurl: throws highest-HP enemy troop across arena (stated)
    # HP = 3968 (same as Giant per reference.md, 3% reduction applied)
    is_win_condition=True, is_tank=True, is_investment=True,
    win_condition_strength=0.85,
    tank_strength=0.78,
    support_strength=0.30,
    counters_win_conditions=["giant", "golem"],   # hurl removes biggest threats
    meta_weight=1.3,
)

HERO_MINI_PEKKA = _hero(
    id="hero_mini_pekka", name="Hero Mini P.E.K.K.A.",
    rarity=Rarity.LEGENDARY, elixir=4, ability_elixir=1,
    hp=1120, damage=598, hit_speed=1.6, speed=SpeedTier.FAST,
    base_card_id="mini_pekka",
    # Breakfast Boost: cooks pancakes to level up over 22s (stated)
    is_punishment=True, is_bridge_spam=True,
    punish_strength=0.80,
    bridge_spam_strength=0.70,
    counters_win_conditions=["hog_rider", "battle_ram", "ram_rider"],
    meta_weight=1.1,
)

HERO_MUSKETEER = _hero(
    id="hero_musketeer", name="Hero Musketeer",
    rarity=Rarity.LEGENDARY, elixir=4, ability_elixir=3,
    hp=720, damage=218, hit_speed=1.0, speed=SpeedTier.MEDIUM,
    range=6.0, targets=TargetType.BOTH,
    base_card_id="musketeer",
    # Trusty Turret: spawns automated turret at 4.0-tile reach (stated)
    is_anti_air=True, is_support=True,
    anti_air_strength=0.90,
    support_strength=0.65,
    counters_win_conditions=["balloon", "lava_hound", "electro_dragon"],
    meta_weight=1.1,
)

HERO_ICE_GOLEM = _hero(
    id="hero_ice_golem", name="Hero Ice Golem",
    rarity=Rarity.LEGENDARY, elixir=2, ability_elixir=2,
    hp=1190, damage=84, hit_speed=2.5, speed=SpeedTier.SLOW,
    targets=TargetType.BUILDINGS,
    base_card_id="ice_golem",
    # Snowstorm: freezes surrounding troops for 1.5s (nerfed from 2.0s, stated)
    # Now defensive-only evaluation weight (per final plan Section 8 special notes)
    # At 1.5s, heavy defenders thaw before win condition secures secondary swing (stated)
    is_tank=True, is_investment=True,
    tank_strength=0.23,
    cycle_strength=0.85,  # 2 elixir
    counters_win_conditions=["hog_rider", "battle_ram"],  # kite
    meta_weight=1.2,
)

HERO_WIZARD = _hero(
    id="hero_wizard", name="Hero Wizard",
    rarity=Rarity.LEGENDARY, elixir=5, ability_elixir=1,
    hp=720, damage=281, hit_speed=1.4, speed=SpeedTier.MEDIUM,
    range=5.5, targets=TargetType.BOTH,
    base_card_id="wizard",
    # Fiery Flight: airborne tornadoes pull units back; 43 Tower Dmg (stated)
    is_anti_air=True, is_support=True, is_splash=True,
    is_anti_ground_swarm=True, is_anti_air_swarm=True,
    anti_air_strength=0.75,
    support_strength=0.70,
    splash_strength=0.80,
    meta_weight=1.1,
)

HERO_GOBLINS = _hero(
    id="hero_goblins", name="Hero Goblins",
    rarity=Rarity.LEGENDARY, elixir=2, ability_elixir=1,
    hp=202, damage=120, hit_speed=1.1, speed=SpeedTier.VERY_FAST,
    base_card_id="goblins",
    # Banner Brigade: final goblin drops banner → 3 reinforcements over 5s (stated)
    # Nerfed from 4→3 brigade summons (stated)
    is_bait_card=True,
    bait_spells=["zap", "arrows", "the_log"],
    cycle_strength=0.85,  # 2 elixir
    meta_weight=0.9,
)

HERO_MEGA_MINION = _hero(
    id="hero_mega_minion", name="Hero Mega Minion",
    rarity=Rarity.LEGENDARY, elixir=3, ability_elixir=2,
    hp=840, damage=315, hit_speed=1.6, speed=SpeedTier.MEDIUM,
    range=2.0, targets=TargetType.BOTH,
    base_card_id="mega_minion",
    # Wounding Warp: teleports to lowest-HP unit, deals 412 warp damage (stated)
    # Nerfed from 468→412; no longer can 1-shot Musketeer/Flying Machine (stated)
    is_anti_air=True, is_punishment=True,
    anti_air_strength=0.80,
    punish_strength=0.65,
    counters_win_conditions=["balloon", "electro_dragon"],
    meta_weight=1.0,
)

HERO_BARBARIAN_BARREL = _hero(
    id="hero_barbarian_barrel", name="Hero Barbarian Barrel",
    rarity=Rarity.LEGENDARY, elixir=2, ability_elixir=1,
    hp=0, damage=241, hit_speed=0.0, speed=SpeedTier.VERY_FAST,
    targets=TargetType.GROUND,
    base_card_id="barbarian_barrel",
    # Rowdy Reroll: barrel rolls a 2nd time (4 tiles, 116 CT dmg) + spawns Barb (stated)
    # Total CT damage potential with ability = 116 (stated at Level 11)
    # This is a HERO SPELL card (Hero/Spell type in reference.md)
    is_damage_spell=True, is_bait_card=True,
    is_anti_ground_swarm=True,
    ct_damage=116,    # ability phase CT damage (stated)
    ct_modifier=0.48, # 116/241 ≈ 0.48 effective for ability phase
    bait_spells=["the_log"],
    cycle_strength=0.85,  # 2 elixir
    meta_weight=1.0,
    confidence=0.9,
)

HERO_MAGIC_ARCHER = _hero(
    id="hero_magic_archer", name="Hero Magic Archer",
    rarity=Rarity.LEGENDARY, elixir=4, ability_elixir=1,
    hp=532, damage=111, hit_speed=1.1, speed=SpeedTier.MEDIUM,
    range=7.0, targets=TargetType.BOTH,
    base_card_id="magic_archer",
    # Triple Threat: 5-tile retreat + stationary decoy + triple-arrow shot (stated)
    # Nullifies spell retaliation with perfect timing; very high skill ceiling (stated)
    is_anti_air=True, is_bridge_spam=True,
    anti_air_strength=0.60,
    bridge_spam_strength=0.60,
    meta_weight=1.0,
    confidence=0.9,  # new card, less meta data
)


# ===========================================================================
# Aggregated export
# ===========================================================================

ALL_HEROES: list[Card] = [
    # Champions
    BOSS_BANDIT,
    GOLDEN_KNIGHT,
    ARCHER_QUEEN,
    SKELETON_KING,
    MIGHTY_MINER,
    MONK,
    LITTLE_PRINCE,
    GOBLINSTEIN,
    # Heroes
    HERO_KNIGHT,
    HERO_GIANT,
    HERO_MINI_PEKKA,
    HERO_MUSKETEER,
    HERO_ICE_GOLEM,
    HERO_WIZARD,
    HERO_GOBLINS,
    HERO_MEGA_MINION,
    HERO_BARBARIAN_BARREL,
    HERO_MAGIC_ARCHER,
]
