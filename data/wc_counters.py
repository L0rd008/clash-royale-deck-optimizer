"""
data/wc_counters.py
===================
Win Condition Counters — Layer 1 of 3-layer counter model (Section 5.1, plan).

Format: { wc_card_id: [(counter_card_id, effectiveness_0_to_1), ...] }
  - 1.0 = hard counter (nearly always negates WC)
  - 0.8 = strong counter
  - 0.6 = situational counter
  - 0.4 = soft counter (slows but doesn't fully stop)

Source: reference.md mechanics + Q1 2026 meta knowledge.
Used by: CounterAnalyzer, DeckScorer (counter coverage component).
"""

WC_COUNTERS: dict[str, list[tuple[str, float]]] = {

    # ── Hog Rider ──
    "hog_rider": [
        ("cannon",          1.0),
        ("tesla",           1.0),
        ("goblin_cage",     1.0),
        ("mini_pekka",      0.9),
        ("knight",          0.8),
        ("inferno_tower",   0.8),
        ("tombstone",       0.8),
        ("ice_golem",       0.7),
        ("guards",          0.7),
        ("the_log",         0.6),
        ("fisherman",       0.6),
        ("bomb_tower",      0.5),
    ],

    # ── Balloon ──
    "balloon": [
        ("arrows",          1.0),
        ("musketeer",       0.9),
        ("vines",           0.9),
        ("mega_minion",     0.9),
        ("inferno_dragon",  0.9),
        ("inferno_tower",   0.9),
        ("minions",         0.8),
        ("minion_horde",    0.8),
        ("flying_machine",  0.8),
        ("hunter",          0.8),
        ("electro_dragon",  0.7),
        ("bats",            0.7),
        ("tesla",           0.7),
        ("poison",          0.6),
        ("baby_dragon",     0.6),
    ],

    # ── Giant ──
    "giant": [
        ("inferno_tower",   1.0),
        ("inferno_dragon",  1.0),
        ("mini_pekka",      0.8),
        ("pekka",           0.8),
        ("poison",          0.7),
        ("lightning",       0.7),
        ("mega_knight",     0.6),
        ("executioner",     0.6),
    ],

    # ── Golem ──
    "golem": [
        ("inferno_tower",   1.0),
        ("inferno_dragon",  1.0),
        ("lightning",       0.9),
        ("pekka",           0.8),
        ("mini_pekka",      0.7),
        ("earthquake",      0.6),
        ("poison",          0.6),
    ],

    # ── Goblin Barrel ──
    "goblin_barrel": [
        ("arrows",          1.0),
        ("the_log",         1.0),
        ("zap",             0.9),
        ("giant_snowball",  0.9),
        ("valkyrie",        0.8),
        ("baby_dragon",     0.7),
        ("goblin_curse",    0.7),
        ("tornado",         0.7),
        ("princess",        0.6),
    ],

    # ── Miner ──
    "miner": [
        ("tornado",         0.9),
        ("mini_pekka",      0.8),
        ("knight",          0.8),
        ("fisherman",       0.8),
        ("goblin_gang",     0.7),
        ("goblins",         0.6),
        ("valkyrie",        0.6),
    ],

    # ── Graveyard ──
    "graveyard": [
        ("poison",          1.0),
        ("giant_snowball",  0.9),
        ("arrows",          0.9),
        ("valkyrie",        0.8),
        ("baby_dragon",     0.8),
        ("wizard",          0.8),
        ("executioner",     0.8),
        ("bowler",          0.7),
        ("tornado",         0.7),
        ("the_log",         0.6),
    ],

    # ── Battle Ram ──
    "battle_ram": [
        ("cannon",          1.0),
        ("tesla",           1.0),
        ("goblin_cage",     1.0),
        ("mini_pekka",      0.9),
        ("inferno_tower",   0.8),
        ("knight",          0.7),
        ("fireball",        0.6),
        ("fisherman",       0.6),
    ],

    # ── Royal Giant ──
    "royal_giant": [
        ("inferno_tower",   1.0),
        ("inferno_dragon",  0.9),
        ("pekka",           0.8),
        ("lightning",       0.7),
        ("mini_pekka",      0.7),
        ("cannon",          0.5),
    ],

    # ── X-Bow ──
    "x_bow": [
        ("earthquake",      1.0),
        ("goblin_barrel",   0.9),
        ("miner",           0.9),
        ("goblin_drill",    0.9),
        ("lightning",       0.8),
        ("rocket",          0.7),
        ("pekka",           0.7),
        ("mini_pekka",      0.6),
    ],

    # ── Mortar ──
    "mortar": [
        ("earthquake",      1.0),
        ("goblin_barrel",   0.9),
        ("miner",           0.9),
        ("goblin_drill",    0.8),
        ("lightning",       0.7),
        ("rocket",          0.7),
    ],

    # ── Lava Hound ──
    "lava_hound": [
        ("inferno_dragon",  1.0),
        ("inferno_tower",   1.0),
        ("arrows",          0.9),  # to kill pups quickly
        ("musketeer",       0.8),
        ("mega_minion",     0.8),
        ("flying_machine",  0.7),
        ("electro_dragon",  0.7),
        ("vines",           0.7),
        ("electro_wizard",  0.6),
    ],

    # ── Ram Rider ──
    "ram_rider": [
        ("tesla",           1.0),
        ("cannon",          1.0),
        ("goblin_cage",     1.0),
        ("mini_pekka",      0.9),
        ("inferno_tower",   0.8),
        ("fireball",        0.7),
        ("knight",          0.6),
    ],

    # ── Electro Giant ──
    "electro_giant": [
        ("inferno_tower",   0.9),
        ("inferno_dragon",  0.9),
        ("lightning",       0.8),
        ("pekka",           0.8),
        ("poison",          0.7),
        ("rocket",          0.6),
    ],

    # ── Giant Skeleton ──
    "giant_skeleton": [
        ("tornado",         1.0),  # drag WC away from tower to waste death bomb
        ("inferno_tower",   0.9),
        ("inferno_dragon",  0.9),
        ("pekka",           0.8),
        ("mini_pekka",      0.7),
        ("fireball",        0.6),
    ],

    # ── Goblin Giant ──
    "goblin_giant": [
        ("inferno_tower",   1.0),
        ("inferno_dragon",  1.0),
        ("pekka",           0.8),
        ("arrows",          0.7),  # kills backpack goblins
        ("fireball",        0.7),
        ("lightning",       0.7),
    ],

    # ── Goblin Drill ──
    "goblin_drill": [
        ("tesla",           1.0),
        ("cannon",          1.0),
        ("goblin_cage",     0.9),
        ("tornado",         0.9),
        ("earthquake",      0.8),
        ("miner",           0.7),  # king activator assist
        ("fireball",        0.6),
    ],

    # ── Boss Bandit ──
    "boss_bandit": [
        ("cannon",          0.9),
        ("tesla",           0.9),
        ("mini_pekka",      0.8),
        ("knight",          0.8),
        ("goblin_cage",     0.8),
        ("inferno_tower",   0.7),
        ("fireball",        0.7),
    ],

    # ── Hero Giant ──
    "hero_giant": [
        ("inferno_tower",   1.0),
        ("inferno_dragon",  1.0),
        ("lightning",       0.9),
        ("pekka",           0.8),
        ("poison",          0.7),
        ("tornado",         0.6),
    ],

    # ── Mighty Miner ──
    "mighty_miner": [
        ("tornado",         0.9),
        ("mini_pekka",      0.8),
        ("cannon",          0.8),
        ("knight",          0.7),
        ("goblin_gang",     0.7),
        ("fisherman",       0.6),
    ],
}
