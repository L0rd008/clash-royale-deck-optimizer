"""
data/cards_troops.py
=====================
All 79 core base troop Card instances.
Stats from Core Troop Matrix (Level 11) in reference.md.
Continuous strengths derived analytically from raw stats.

Simulation note — continuous strengths are computed as:
  tank_strength      = min(1.0, hp / 5120)
  anti_air_strength  = (dps / 218) * range_factor if targets BOTH/AIR else 0
  win_cond_strength  = (dps / 320) * (hp / 2000) * speed_factor if targets BUILDINGS
  cycle_strength     = max(0, (7 - elixir) / 6)
  bridge_spam_str    = speed_factor * (dps / 320) if is_bridge_spam
where speed_factor: SLOW=0.4, MEDIUM=0.7, FAST=0.9, VERY_FAST=1.0
"""

from models.card import Card, CardType, SlotType, TargetType, SpeedTier, Rarity

# Speed factor used in simulated strength calcs
_SF = {SpeedTier.SLOW: 0.4, SpeedTier.MEDIUM: 0.7,
       SpeedTier.FAST: 0.9, SpeedTier.VERY_FAST: 1.0}

def _t(id, name, rarity, elixir, hp, damage, dps, hit_speed, speed, tgt, rng=0.0,
       wc=False, aa=False, tank=False, sup=False, bs=False, pun=False,
       inv=False, ka=False, bait=False, splash=False, ags=False, aas=False,
       pump=False, li=False, so=False, wu=False,
       bait_s=None, cwc=None, cdf=None, cswc=None,
       wcs=None, aas_=None, puns=None, bss=None, tanks=None, sups=None,
       cys=None, sps=None, meta=1.0, conf=1.0, death_damage=0, spawn_hp=0,
       sp=None, sc=None, **kw) -> Card:
    sf = _SF.get(speed, 0.7)
    ts = tanks if tanks is not None else round(min(1.0, hp / 5120), 2)
    cs = cys if cys is not None else round(max(0.0, (7 - elixir) / 6), 2)
    # Simulated anti_air_strength
    if aas_ is None:
        if tgt in (TargetType.BOTH, TargetType.AIR) and aa:
            rf = min(1.0, rng / 6.0) if rng > 0 else 0.5
            aas_ = round(min(1.0, (dps / 218) * rf), 2)
        else:
            aas_ = 0.0
    # Simulated win_condition_strength
    if wcs is None:
        if wc and tgt == TargetType.BUILDINGS:
            wcs = round(min(1.0, (dps / 320) * (hp / 3000) * sf), 2)
        elif wc:
            wcs = round(min(1.0, (dps / 320) * sf * 0.8), 2)
        else:
            wcs = 0.0
    # Simulated bridge_spam_strength
    if bss is None:
        bss = round(min(1.0, (dps / 320) * sf), 2) if bs else 0.0
    if puns is None:
        puns = round(min(1.0, (dps / 320) * sf * 0.9), 2) if pun else 0.0
    if sups is None:
        sups = 0.0
    if sps is None:
        sps = 0.0
    return Card(
        id=id, name=name, rarity=rarity, card_type=CardType.TROOP,
        slot_type=SlotType.BASE, elixir=elixir, hp=hp, damage=damage,
        dps=dps, hit_speed=hit_speed, speed=speed, range=rng, targets=tgt,
        death_damage=death_damage, spawn_hp=spawn_hp,
        is_win_condition=wc, is_anti_air=aa, is_tank=tank, is_support=sup,
        is_bridge_spam=bs, is_punishment=pun, is_investment=inv,
        is_king_activator=ka, is_bait_card=bait, is_splash=splash,
        is_anti_ground_swarm=ags, is_anti_air_swarm=aas, is_pump_response=pump,
        is_level_independent=li, is_strong_overleveled=so, is_weak_underleveled=wu,
        bait_spells=bait_s or [],
        win_condition_strength=wcs, anti_air_strength=aas_, punish_strength=puns,
        bridge_spam_strength=bss, tank_strength=ts, support_strength=sups,
        cycle_strength=cs, splash_strength=sps,
        counters_win_conditions=cwc or [], counters_defenders=cdf or [],
        counters_secondary_wc=cswc or [],
        state_profiles=sp or {}, state_condition=sc,
        meta_weight=meta, confidence=conf, last_verified="2026-03-23", **kw)


C=Rarity.COMMON; R=Rarity.RARE; E=Rarity.EPIC; L=Rarity.LEGENDARY
G=TargetType.GROUND; A=TargetType.BOTH; B=TargetType.BUILDINGS

# ===========================================================================
# 79 CORE TROOPS  (alphabetical per reference.md Core Troop Matrix)
# ===========================================================================

ARCHERS = _t("archers","Archers",C,3,304,112,124,0.9,SpeedTier.MEDIUM,A,5.0,
    aa=True, bait=True, bait_s=["arrows","zap"],
    cwc=["balloon","lava_hound"], meta=1.2)

BABY_DRAGON = _t("baby_dragon","Baby Dragon",E,4,1152,161,107,1.5,SpeedTier.FAST,A,3.5,
    aa=True, splash=True, ags=True, aas=True, sup=True, sps=0.65,
    cwc=["goblin_barrel","graveyard"], meta=1.1)

BALLOON = _t("balloon","Balloon",E,5,1679,640,320,2.0,SpeedTier.MEDIUM,B,0.0,
    wc=True, tank=True, cwc=[], death_damage=200,
    meta=1.5)

BANDIT = _t("bandit","Bandit",L,3,906,194,194,1.0,SpeedTier.FAST,G,0.0,
    bs=True, pun=True, meta=1.3)

BARBARIANS = _t("barbarians","Barbarians",C,5,670,192,147,1.3,SpeedTier.MEDIUM,G,0.0,
    pun=True, meta=0.9)

BATS = _t("bats","Bats",C,2,81,81,67,1.2,SpeedTier.VERY_FAST,A,0.0,
    aa=True, aas=True, bait=True, bait_s=["arrows","zap"],
    cys=0.85, meta=1.2)

BATTLE_HEALER = _t("battle_healer","Battle Healer",R,4,1717,148,98,1.5,SpeedTier.MEDIUM,G,0.0,
    tank=True, sup=True, sups=0.60, meta=0.9)

BATTLE_RAM = _t("battle_ram","Battle Ram",R,4,967,286,0,0.0,SpeedTier.MEDIUM,B,0.0,
    wc=True, bs=True, pun=True, wcs=0.80, bss=0.85, puns=0.80,
    cwc=[], cdf=["cannon","tesla","mini_pekka","goblin_cage"], meta=1.3)

BERSERKER = _t("berserker","Berserker",C,2,896,102,170,0.6,SpeedTier.FAST,G,0.8,
    li=True, cys=0.85, meta=0.9)

BOMBER = _t("bomber","Bomber",C,2,304,225,125,1.8,SpeedTier.MEDIUM,G,4.5,
    splash=True, ags=True, sps=0.65, cys=0.85, meta=0.9)

BOWLER = _t("bowler","Bowler",E,5,2081,289,115,2.5,SpeedTier.SLOW,G,4.0,
    tank=True, splash=True, ags=True, sps=0.75,
    cdf=["skeleton_army","goblins","goblin_gang"], meta=1.0)

CANNON_CART = _t("cannon_cart","Cannon Cart",E,5,896,212,176,1.2,SpeedTier.FAST,G,5.5,
    bs=True, bss=0.50, meta=0.8)

DARK_PRINCE = _t("dark_prince","Dark Prince",E,4,1180,240,184,1.3,SpeedTier.MEDIUM,G,0.0,
    bs=True, splash=True, ags=True, bait=True, bait_s=["the_log"],
    sps=0.60, bss=0.55, meta=1.1)

DART_GOBLIN = _t("dart_goblin","Dart Goblin",R,3,260,131,187,0.7,SpeedTier.VERY_FAST,A,7.0,
    aa=True, bait=True, bait_s=["arrows","zap"],
    cwc=["balloon"], meta=0.9)

ELECTRO_DRAGON = _t("electro_dragon","Electro Dragon",E,5,944,192,91,2.1,SpeedTier.MEDIUM,A,3.5,
    aa=True, aas=True, sup=True, sups=0.55, aas_=0.60, meta=1.0)

ELECTRO_GIANT = _t("electro_giant","Electro Giant",E,7,3840,192,91,2.1,SpeedTier.SLOW,B,0.0,
    wc=True, tank=True, wcs=0.72, meta=1.0)

ELECTRO_SPIRIT = _t("electro_spirit","Electro Spirit",C,1,230,99,0,0.0,SpeedTier.VERY_FAST,A,2.5,
    aa=True, aas=True, splash=True, li=True,
    cdf=["sparky","inferno_tower","inferno_dragon"],
    cys=1.0, aas_=0.55, meta=1.4)

ELECTRO_WIZARD = _t("electro_wizard","Electro Wizard",L,4,720,93,103,1.8,SpeedTier.FAST,A,5.0,
    aa=True, sup=True, sups=0.80,
    cdf=["sparky","inferno_tower","inferno_dragon"],
    aas_=0.70, meta=1.2)

ELITE_BARBARIANS = _t("elite_barbarians","Elite Barbarians",C,6,1341,318,212,1.5,SpeedTier.VERY_FAST,G,0.0,
    pun=True, bs=True, puns=0.70, bss=0.65, meta=0.9)

ELIXIR_GOLEM = _t("elixir_golem","Elixir Golem",R,3,1424,254,195,1.3,SpeedTier.SLOW,B,0.0,
    tank=True, wcs=0.0,  # NOT a win condition — high-risk liability card
    meta=0.8)

EXECUTIONER = _t("executioner","Executioner",E,5,1210,168,140,2.4,SpeedTier.MEDIUM,A,4.5,
    aa=True, splash=True, ags=True, aas=True, sps=0.70,
    cdf=["skeleton_army","goblins","minion_horde"], meta=1.1)

FIRE_SPIRIT = _t("fire_spirit","Fire Spirit",C,1,230,207,0,0.0,SpeedTier.VERY_FAST,A,2.0,
    aa=True, splash=True, aas=True,
    aas_=0.25,  # contacts air units on impact despite dps=0 (collision card)
    cys=1.0, sps=0.65, meta=1.0)

FIRECRACKER = _t("firecracker","Firecracker",C,3,304,64,106,3.0,SpeedTier.FAST,A,6.0,
    aa=True, bait=True, bait_s=["the_log","arrows"],
    aas_=0.55, meta=1.1)

FISHERMAN = _t("fisherman","Fisherman",L,3,871,190,126,1.5,SpeedTier.MEDIUM,G,0.0,
    cwc=["hog_rider","balloon","battle_ram"],
    cdf=["hog_rider","battle_ram"], meta=1.0)

FLYING_MACHINE = _t("flying_machine","Flying Machine",R,4,615,170,154,1.1,SpeedTier.FAST,A,6.0,
    aa=True, aas_=0.75, meta=1.1)

GIANT = _t("giant","Giant",R,5,3968,254,169,1.5,SpeedTier.SLOW,B,0.0,
    wc=True, tank=True, inv=True, wcs=0.72, meta=1.2)

GIANT_SKELETON = _t("giant_skeleton","Giant Skeleton",E,6,3424,271,180,1.5,SpeedTier.MEDIUM,G,0.0,
    wc=True, tank=True, death_damage=1000,
    wcs=0.60, meta=0.9)

GOBLIN_DEMOLISHER = _t("goblin_demolisher","Goblin Demolisher",R,4,1211,186,124,1.5,SpeedTier.MEDIUM,A,4.0,
    aa=True, aas_=0.55, meta=0.8)

GOBLIN_GANG = _t("goblin_gang","Goblin Gang",C,3,202,0,0,0,SpeedTier.VERY_FAST,A,0.0,
    bait=True, bait_s=["the_log","arrows","zap"],
    cys=0.65, meta=1.0, conf=0.85)  # mixed unit, stats vary

GOBLIN_GIANT = _t("goblin_giant","Goblin Giant",E,6,3024,176,103,1.7,SpeedTier.MEDIUM,B,0.0,
    wc=True, tank=True, spawn_hp=132, wcs=0.60, meta=0.9)

GOBLIN_MACHINE = _t("goblin_machine","Goblin Machine",E,5,2423,212,141,1.5,SpeedTier.MEDIUM,G,0.0,
    tank=True, pun=True, meta=0.9)

GOBLINS = _t("goblins","Goblins",C,2,202,120,109,1.1,SpeedTier.VERY_FAST,G,0.0,
    bait=True, bait_s=["the_log","zap","arrows"],
    cys=0.85, li=True, meta=1.1)

GOLEM = _t("golem","Golem",E,8,5120,310,124,2.5,SpeedTier.SLOW,B,0.0,
    wc=True, tank=True, inv=True, wcs=1.0, tanks=1.0, meta=1.1)

GUARDS = _t("guards","Guards",E,3,811,81,108,1.0,SpeedTier.FAST,G,0.0,
    bait=True, bait_s=["the_log","arrows"],
    cwc=["hog_rider","prince"], cys=0.65, meta=0.9)

HEAL_SPIRIT = _t("heal_spirit","Heal Spirit",R,1,230,109,0,0.0,SpeedTier.VERY_FAST,A,2.5,
    aa=True, sup=True, sups=0.50,
    aas_=0.20,  # contacts air units on impact despite dps=0 (collision card)
    cys=1.0, meta=0.9)

HOG_RIDER = _t("hog_rider","Hog Rider",R,4,1696,318,198,1.6,SpeedTier.VERY_FAST,B,0.0,
    wc=True, bs=True, pun=True, li=True,
    wcs=0.90, bss=0.95, puns=0.90, meta=1.9)

HUNTER = _t("hunter","Hunter",E,4,838,84,381,2.2,SpeedTier.MEDIUM,A,4.0,
    aa=True, splash=True, sps=0.65,
    cwc=["balloon","lava_hound","giant"], meta=1.0)

ICE_GOLEM = _t("ice_golem","Ice Golem",R,2,1190,84,33,2.5,SpeedTier.SLOW,B,0.0,
    tank=True, li=True,
    cwc=["hog_rider","battle_ram"], cys=0.85, meta=1.3)

ICE_SPIRIT = _t("ice_spirit","Ice Spirit",C,1,230,109,0,0.0,SpeedTier.VERY_FAST,A,2.5,
    aa=True, li=True, cys=1.0, aas_=0.45, meta=1.3)

ICE_WIZARD = _t("ice_wizard","Ice Wizard",L,3,720,90,52,1.7,SpeedTier.MEDIUM,A,5.5,
    aa=True, sup=True, sups=0.70, aas_=0.50, meta=1.1)

INFERNO_DRAGON = _t("inferno_dragon","Inferno Dragon",L,4,1294,35,0,0.4,SpeedTier.MEDIUM,A,4.0,
    aa=True, aas_=0.80,
    cwc=["giant","golem","balloon","electro_giant","mega_knight","lava_hound"],
    cdf=[], meta=1.3)

KNIGHT = _t("knight","Knight",C,3,1650,202,168,1.2,SpeedTier.MEDIUM,G,0.0,
    tank=True, li=True,
    cwc=["hog_rider","battle_ram"], cys=0.65, meta=1.5)

LAVA_HOUND = _t("lava_hound","Lava Hound",L,7,3800,54,41,1.3,SpeedTier.SLOW,B,2.0,
    wc=True, tank=True, inv=True, wcs=0.65, meta=1.1)

LUMBERJACK = _t("lumberjack","Lumberjack",L,4,1270,240,300,0.8,SpeedTier.VERY_FAST,G,0.0,
    bs=True, pun=True, sup=True, sups=0.70, bss=0.85, puns=0.80, meta=1.2)

MAGIC_ARCHER = _t("magic_archer","Magic Archer",L,4,532,111,100,1.1,SpeedTier.MEDIUM,A,7.0,
    aa=True, aas_=0.60, meta=1.0)

MEGA_KNIGHT = _t("mega_knight","Mega Knight",L,7,3993,268,157,1.7,SpeedTier.MEDIUM,G,0.0,
    tank=True, splash=True, ags=True, sps=0.80, meta=1.2)

MEGA_MINION = _t("mega_minion","Mega Minion",R,3,840,315,196,1.6,SpeedTier.MEDIUM,A,2.0,
    aa=True, cwc=["balloon","battle_ram"], aas_=0.80, cys=0.65, meta=1.4)

MINER = _t("miner","Miner",L,3,1210,192,160,1.2,SpeedTier.FAST,G,0.0,
    wc=True, bs=True, pun=True, ka=True,
    wcs=0.70, bss=0.85, puns=0.80, meta=1.4)

MINI_PEKKA = _t("mini_pekka","Mini P.E.K.K.A.",R,4,1361,598,373,1.6,SpeedTier.FAST,G,0.0,
    pun=True, puns=0.85,
    cwc=["hog_rider","battle_ram","ram_rider"],
    cdf=["hog_rider","battle_ram","ram_rider"], meta=1.3)

MINION_HORDE = _t("minion_horde","Minion Horde",C,5,230,102,85,1.2,SpeedTier.FAST,A,2.0,
    aa=True, aas=True, bait=True, bait_s=["arrows","fireball"],
    cwc=["balloon","lava_hound"], aas_=0.60, meta=1.0)

MINIONS = _t("minions","Minions",C,3,230,102,85,1.2,SpeedTier.FAST,A,2.0,
    aa=True, aas=True, bait=True, bait_s=["arrows","zap"],
    cwc=["balloon"], aas_=0.55, cys=0.65, meta=1.1)

MOTHER_WITCH = _t("mother_witch","Mother Witch",L,4,532,132,120,1.1,SpeedTier.MEDIUM,A,5.5,
    aa=True, sup=True, sups=0.55, aas_=0.55, meta=0.9)

MUSKETEER = _t("musketeer","Musketeer",R,4,720,218,218,1.0,SpeedTier.MEDIUM,A,6.0,
    aa=True, cwc=["balloon","lava_hound","electro_dragon"],
    aas_=0.95, meta=1.4)

NIGHT_WITCH = _t("night_witch","Night Witch",L,4,1081,313,208,1.5,SpeedTier.MEDIUM,A,0.0,
    aa=True, sup=True, spawn_hp=81, sups=0.65, aas_=0.60, meta=1.1)

P_E_K_K_A = _t("p_e_k_k_a","P.E.K.K.A.",E,7,3760,816,453,1.8,SpeedTier.SLOW,G,0.0,
    tank=True, pun=True, puns=0.65,
    cwc=["hog_rider","battle_ram","prince"], meta=1.1)

PHOENIX = _t("phoenix","Phoenix",L,4,1244,212,235,0.9,SpeedTier.FAST,A,0.0,
    wc=True, aa=True, bs=True, wcs=0.60, aas_=0.60, bss=0.65, meta=1.2)

PRINCE = _t("prince","Prince",E,5,1919,392,280,1.4,SpeedTier.MEDIUM,G,0.0,
    wc=True, bs=True, wcs=0.55, bss=0.65, meta=1.0)

PRINCESS = _t("princess","Princess",L,3,261,169,56,3.0,SpeedTier.MEDIUM,A,9.0,
    aa=True, bait=True, bait_s=["the_log","arrows"],
    aas_=0.45, li=True, cys=0.65, meta=1.3)

RAM_RIDER = _t("ram_rider","Ram Rider",L,5,1775,266,147,1.8,SpeedTier.MEDIUM,B,0.0,
    wc=True, bs=True, wcs=0.65, bss=0.55, meta=1.0)

RASCALS = _t("rascals","Rascals",C,5,1804,131,87,1.5,SpeedTier.MEDIUM,G,0.0,
    bait=True, bait_s=["fireball","arrows"], meta=0.9)

ROYAL_GHOST = _t("royal_ghost","Royal Ghost",L,3,1210,261,145,1.8,SpeedTier.FAST,G,0.0,
    bs=True, pun=True, bss=0.40, puns=0.45, cys=0.65, meta=1.0)

ROYAL_GIANT = _t("royal_giant","Royal Giant",C,6,3061,254,141,1.8,SpeedTier.SLOW,B,5.0,
    wc=True, tank=True, bs=True, wcs=0.70, meta=1.1)

ROYAL_HOGS = _t("royal_hogs","Royal Hogs",R,5,838,72,60,1.2,SpeedTier.VERY_FAST,B,0.0,
    wc=True, bs=True, pun=True, wcs=0.55, bss=0.60, puns=0.55, meta=1.0)

ROYAL_RECRUITS = _t("royal_recruits","Royal Recruits",C,7,532,133,102,1.3,SpeedTier.MEDIUM,G,0.0,
    meta=0.8)

RUNE_GIANT = _t("rune_giant","Rune Giant",E,4,2662,120,80,1.5,SpeedTier.MEDIUM,B,1.2,
    wc=False, tank=True, sup=True, sups=0.85,
    # 8.5-tile enchantment aura: every 3rd attack of enchanted allies = bonus dmg (stated)
    # Pairs exceptionally with high-hit-speed units like Berserker (0.6s) (stated)
    meta=1.0)

SKELETON_BARREL = _t("skeleton_barrel","Skeleton Barrel",C,3,532,132,0,0.0,SpeedTier.FAST,B,0.0,
    wc=True, bs=True, wcs=0.45, bss=0.55, death_damage=180,
    # Drops skeletons on burst; barrel itself targets buildings
    cys=0.65, meta=1.0)

SKELETON_DRAGONS = _t("skeleton_dragons","Skeleton Dragons",C,4,532,170,94,1.8,SpeedTier.FAST,A,3.5,
    aa=True, aas_=0.55, meta=0.9)

SKELETONS = _t("skeletons","Skeletons",C,1,81,81,81,1.0,SpeedTier.FAST,G,0.0,
    bait=True, bait_s=["zap","arrows","the_log"],
    li=True, cys=1.0, meta=1.4)

SPARKY = _t("sparky","Sparky",L,6,1440,1331,332,4.0,SpeedTier.SLOW,G,4.5,
    pun=True, splash=True, ags=True, sps=0.90, puns=0.55,
    wu=True,  # very weak when underleveled (Zap interaction)
    meta=0.9)

SPEAR_GOBLINS = _t("spear_goblins","Spear Goblins",C,2,132,81,47,1.7,SpeedTier.VERY_FAST,A,5.0,
    aa=True, bait=True, bait_s=["the_log","arrows","zap"],
    cys=0.85, aas_=0.35, meta=1.0)

# Spirit Empress — state-switching card (stated in reference.md)
SPIRIT_EMPRESS = _t("spirit_empress","Spirit Empress",L,3,1152,307,279,1.1,SpeedTier.FAST,G,0.0,
    # Ground form (<6 elixir): 3e, 1152 HP, 279 DPS, ground, Fast (stated)
    # Air form (≥6 elixir): 6e, 1152 HP, 307 DPS, both, Fast (stated)
    #   Use ground profile for role flags and cycle_elixir
    wc=True, aa=False, bs=True,
    wcs=0.65, bss=0.55,
    sp={"ground": {"elixir": 3, "hp": 1152, "dps": 279, "targets": "ground", "speed": "fast"},
        "air":    {"elixir": 6, "hp": 1152, "dps": 307, "targets": "both",   "speed": "fast"}},
    sc="elixir_at_deploy >= 6",
    meta=1.2, conf=0.9)

SUSPICIOUS_BUSH = _t("suspicious_bush","Suspicious Bush",R,2,81,0,0,0.0,SpeedTier.SLOW,B,0.0,
    wc=True, bs=True, wcs=0.45, bss=0.50,
    # 81 HP (stated); spawn 2 Bush Goblins (304 HP, combined DPS 324) on death (stated)
    spawn_hp=304, cys=0.85, meta=0.9)

THREE_MUSKETEERS = _t("three_musketeers","Three Musketeers",R,9,720,218,167,1.3,SpeedTier.MEDIUM,A,6.0,
    wc=True, aa=True, inv=True,
    wcs=0.70, aas_=0.80,
    pump=True,  # punishes Elixir Collector by generating elixir lead when split
    meta=0.8)

VALKYRIE = _t("valkyrie","Valkyrie",R,4,1908,266,177,1.5,SpeedTier.MEDIUM,G,0.0,
    tank=True, splash=True, ags=True, sps=0.85,
    cwc=["goblin_barrel","graveyard"],
    cdf=["skeleton_army","goblins","goblin_gang","bats"],
    meta=1.4)

WALL_BREAKERS = _t("wall_breakers","Wall Breakers",E,2,329,391,0,0.0,SpeedTier.VERY_FAST,B,0.0,
    bs=True, pun=True, bait=True, bait_s=["the_log"],
    bss=0.85, puns=0.80, death_damage=258,  # post-nerf (stated)
    cys=0.85, meta=1.2)

WITCH = _t("witch","Witch",E,5,838,134,121,1.1,SpeedTier.MEDIUM,A,5.5,
    aa=True, sup=True, splash=True, spawn_hp=81,
    sups=0.60, sps=0.60, aas_=0.55, meta=1.0)

WIZARD = _t("wizard","Wizard",R,5,720,281,200,1.4,SpeedTier.MEDIUM,A,5.5,
    aa=True, splash=True, ags=True, aas=True,
    sps=0.85, aas_=0.80, meta=1.1)

ZAPPIES = _t("zappies","Zappies",R,4,532,84,40,2.1,SpeedTier.MEDIUM,A,4.5,
    aa=True, aas=True, aas_=0.45,
    cdf=["sparky","inferno_tower","inferno_dragon"],
    meta=0.8)

# --- Furnace (reclassified from BUILDING to TROOP, Aug 2025, stated) ---
FURNACE = _t("furnace","Furnace",R,4,1000,0,0,0.0,SpeedTier.SLOW,G,0.0,
    # NOTE: NOT a defensive building — cannot kite Hog Rider or Balloon (stated)
    spawn_hp=230, sup=True, sups=0.40,
    meta=0.7, conf=0.80)

# --- Goblin Drill (Epic troop, 4e, targets buildings) ---
GOBLIN_DRILL = _t("goblin_drill","Goblin Drill",E,4,1100,120,100,1.2,SpeedTier.FAST,B,0.0,
    wc=True, bs=True, pun=True, ka=True,
    wcs=0.65, bss=0.70, puns=0.65,
    meta=1.0, conf=0.80)


# ===========================================================================
# Aggregated export
# ===========================================================================

ALL_TROOPS: list[Card] = [
    ARCHERS, BABY_DRAGON, BALLOON, BANDIT, BARBARIANS, BATS,
    BATTLE_HEALER, BATTLE_RAM, BERSERKER, BOMBER, BOWLER, CANNON_CART,
    DARK_PRINCE, DART_GOBLIN, ELECTRO_DRAGON, ELECTRO_GIANT,
    ELECTRO_SPIRIT, ELECTRO_WIZARD, ELITE_BARBARIANS, ELIXIR_GOLEM,
    EXECUTIONER, FIRE_SPIRIT, FIRECRACKER, FISHERMAN, FLYING_MACHINE,
    GIANT, GIANT_SKELETON, GOBLIN_DEMOLISHER, GOBLIN_GANG, GOBLIN_GIANT,
    GOBLIN_MACHINE, GOBLINS, GOLEM, GUARDS, HEAL_SPIRIT, HOG_RIDER,
    HUNTER, ICE_GOLEM, ICE_SPIRIT, ICE_WIZARD, INFERNO_DRAGON,
    KNIGHT, LAVA_HOUND, LUMBERJACK, MAGIC_ARCHER, MEGA_KNIGHT,
    MEGA_MINION, MINER, MINI_PEKKA, MINION_HORDE, MINIONS,
    MOTHER_WITCH, MUSKETEER, NIGHT_WITCH, P_E_K_K_A, PHOENIX,
    PRINCE, PRINCESS, RAM_RIDER, RASCALS, ROYAL_GHOST, ROYAL_GIANT,
    ROYAL_HOGS, ROYAL_RECRUITS, RUNE_GIANT, SKELETON_BARREL,
    SKELETON_DRAGONS, SKELETONS, SPARKY, SPEAR_GOBLINS, SPIRIT_EMPRESS,
    SUSPICIOUS_BUSH, THREE_MUSKETEERS, VALKYRIE, WALL_BREAKERS,
    WITCH, WIZARD, ZAPPIES, FURNACE, GOBLIN_DRILL,
]
