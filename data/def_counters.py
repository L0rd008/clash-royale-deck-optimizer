"""
data/def_counters.py
====================
Defense Counters — Layer 2 of 3-layer counter model (Section 5.2, plan).

These are dangerous DEFENDING units/buildings that commonly shut down pushes.
Format: { defender_id: [(counter_card_id, effectiveness), ...] }

Used by: CounterAnalyzer, to flag whether a deck can handle key defensive structures.
Source: reference.md mechanics + Q1 2026 meta knowledge.
"""

DEF_COUNTERS: dict[str, list[tuple[str, float]]] = {

    # ── Inferno Tower (focal ramp 40→800 DPS, hard counters tanks) ──
    "inferno_tower": [
        ("lightning",           1.0),
        ("zap",                 1.0),  # resets ramp
        ("electro_wizard",      0.9),  # resets ramp + ongoing stun
        ("freeze",              0.9),  # buys whole push window
        ("electro_spirit",      0.9),
        ("earthquake",          0.8),
        ("rocket",              0.8),
        ("poison",              0.7),
        ("giant_snowball",      0.6),
        ("zappies",             0.5),
    ],

    # ── Inferno Dragon (focal ramp, same weakness but air-mobile) ──
    "inferno_dragon": [
        ("zap",                 1.0),
        ("electro_wizard",      0.9),
        ("electro_spirit",      0.9),
        ("freeze",              0.9),
        ("lightning",           0.8),
        ("musketeer",           0.7),
        ("mega_minion",         0.7),
        ("minions",             0.7),
        ("arrows",              0.6),
    ],

    # ── Sparky (devastating AoE, reset-able) ──
    "sparky": [
        ("zap",                 1.0),  # insta-reset
        ("electro_wizard",      0.9),  # reset + stun chain
        ("electro_spirit",      0.9),
        ("lightning",           0.8),
        ("freeze",              0.7),
        ("zappies",             0.7),  # chain reset
        ("ice_spirit",          0.5),
    ],

    # ── Tesla (submerges, spell-immune while buried) ──
    "tesla": [
        ("earthquake",          1.0),
        ("lightning",           0.9),
        ("rocket",              0.8),
        ("goblin_barrel",       0.7),
        ("miner",               0.7),
        ("goblin_drill",        0.7),
    ],

    # ── Cannon (premium Hog counter, ground only) ──
    "cannon": [
        ("earthquake",          1.0),
        ("lightning",           0.8),
        ("rocket",              0.7),
        ("goblin_barrel",       0.6),
        ("miner",               0.6),
        ("goblin_drill",        0.6),
    ],

    # ── Bomb Tower (ground-targeting splash nuke) ──
    "bomb_tower": [
        ("earthquake",          1.0),
        ("lightning",           0.9),
        ("rocket",              0.8),
        ("goblin_barrel",       0.7),
        ("miner",               0.7),
        ("goblin_drill",        0.7),
        ("giant",               0.6),
    ],

    # ── Tombstone (swarms on death, kites building-targeters) ──
    "tombstone": [
        ("earthquake",          0.9),
        ("poison",              0.9),  # clears spawned skeletons continuously
        ("arrows",              0.8),
        ("fireball",            0.8),
        ("lightning",           0.7),
        ("valkyrie",            0.7),
    ],

    # ── Goblin Cage (pulls aggro; Brawler on destruction) ──
    "goblin_cage": [
        ("earthquake",          1.0),
        ("goblin_barrel",       0.8),  # deploys behind cage
        ("miner",               0.8),
        ("rocket",              0.7),
        ("lightning",           0.7),
    ],

    # ── P.E.K.K.A (melee anti-pushback, can be air-kited) ──
    "p_e_k_k_a": [
        ("mini_pekka",          0.7),
        ("balloon",             0.9),  # floats past PEKKA entirely
        ("miner",               0.8),
        ("goblin_barrel",       0.8),
        ("lava_hound",          0.7),
        ("baby_dragon",         0.6),
    ],

    # ── Mini P.E.K.K.A (great vs hog/ram) ──
    "mini_pekka": [
        ("valkyrie",            0.9),
        ("miner",               0.8),
        ("balloon",             0.8),
        ("goblin_barrel",       0.8),
        ("fireball",            0.7),
        ("lumberjack",          0.7),
    ],

    # ── Mega Knight (jump splash on deploy) ──
    "mega_knight": [
        ("inferno_tower",       0.9),
        ("inferno_dragon",      0.9),
        ("pekka",               0.8),
        ("mini_pekka",          0.7),
        ("miner",               0.8),
        ("goblin_barrel",       0.7),  # goes past him
        ("balloon",             0.8),
    ],

    # ── Electro Wizard (stun chain reset) ──
    "electro_wizard": [
        ("mini_pekka",          0.9),
        ("fireball",            0.9),
        ("lightning",           0.8),
        ("musketeer",           0.7),
        ("arrows",              0.6),
    ],

    # ── Valkyrie (360° splash, great vs swarm) ──
    "valkyrie": [
        ("miner",               0.8),
        ("balloon",             0.8),
        ("lumberjack",          0.8),
        ("fireball",            0.7),
        ("mini_pekka",          0.7),
        ("pekka",               0.7),
    ],

    # ── Knight (tanky value defender) ──
    "knight": [
        ("miner",               0.7),
        ("fireball",            0.6),
        ("mini_pekka",          0.7),
        ("lumberjack",          0.7),
        ("balloon",             0.6),
    ],

    # ── Fisherman (pulls building-targeters away) ──
    "fisherman": [
        ("goblin_barrel",       0.9),  # spawns behind him
        ("miner",               0.8),
        ("fireball",            0.7),
        ("arrows",              0.6),
    ],

    # ── Musketeer (premier anti-air defender) ──
    "musketeer": [
        ("fireball",            1.0),
        ("lightning",           0.9),
        ("poison",              0.8),
        ("rocket",              0.8),
        ("mini_pekka",          0.7),
    ],

    # ── Night Witch (bat swarm spawn) ──
    "night_witch": [
        ("fireball",            1.0),
        ("poison",              0.9),
        ("lightning",           0.8),
        ("arrows",              0.8),
        ("giant_snowball",      0.6),
    ],

    # ── Witch (combined ground splash + skeleton spawner) ──
    "witch": [
        ("fireball",            1.0),
        ("poison",              0.9),
        ("lightning",           0.8),
        ("arrows",              0.7),
        ("log",                 0.6),
    ],

    # ── Executioner (piercing axe return, anti-swarm) ──
    "executioner": [
        ("fireball",            0.9),
        ("lightning",           0.9),
        ("rocket",              0.8),
        ("mini_pekka",          0.7),
    ],

    # ── Skeleton Army (15-skeleton swarm, dies to any spell) ──
    "skeleton_army": [
        ("arrows",              1.0),
        ("fireball",            1.0),
        ("the_log",             1.0),
        ("giant_snowball",      0.9),
        ("zap",                 0.8),
        ("valkyrie",            0.8),
        ("baby_dragon",         0.8),
        ("bowler",              0.8),
        ("wizard",              0.8),
    ],

    # ── Goblin Gang (mixed ground/air swarm) ──
    "goblin_gang": [
        ("the_log",             1.0),
        ("arrows",              0.9),
        ("fireball",            0.8),
        ("giant_snowball",      0.8),
        ("valkyrie",            0.8),
        ("wizard",              0.7),
    ],

    # ── Minion Horde (6 air units, high DPS) ──
    "minion_horde": [
        ("arrows",              1.0),
        ("fireball",            1.0),
        ("poison",              0.9),
        ("giant_snowball",      0.8),
        ("zap",                 0.7),
        ("wizard",              0.7),
    ],

    # ── Elixir Collector (punishable by damage spells) ──
    "elixir_collector": [
        ("fireball",            1.0),  # one-shots under double elixir
        ("poison",              0.9),
        ("lightning",           0.9),
        ("rocket",              0.8),
        ("earthquake",          0.8),
        ("goblin_barrel",       0.7),  # forces response + pressure
        ("miner",               0.7),
    ],
}
