"""
data/swc_counters.py
====================
Secondary Win Condition Counters — Layer 3 of 3-layer counter model (Section 5.3, plan).

Secondary WCs are cards that are NOT primary win conditions themselves but threaten
towers in a supporting role, or are near-comboable WCs that need specific answers.

Format: { secondary_wc_id: [(counter_id, effectiveness), ...] }

Used by: CounterAnalyzer for the third layer of meta coverage report.
Source: reference.md mechanics + Q1 2026 meta knowledge.
"""

SWC_COUNTERS: dict[str, list[tuple[str, float]]] = {

    # ── Graveyard (spawns skeletons over 10s, combos with freeze/poison) ──
    "graveyard": [
        ("poison",          1.0),  # shuts down entire GY window
        ("arrows",          0.9),  # clears skeletons continuously
        ("the_log",         0.8),
        ("tornado",         0.7),  # drags skeletons into king range
        ("giant_snowball",  0.7),
        ("valkyrie",        0.7),
        ("baby_dragon",     0.7),
        ("wizard",          0.6),
    ],

    # ── Sparky (near-unstoppable if uncontested, reset = full stop) ──
    "sparky": [
        ("zap",             1.0),
        ("electro_wizard",  0.9),
        ("electro_spirit",  0.9),
        ("lightning",       0.8),
        ("freeze",          0.7),
        ("zappies",         0.7),
        ("ice_spirit",      0.5),
    ],

    # ── Goblin Barrel (1-shots towers without counter)  ──
    "goblin_barrel": [
        ("arrows",          1.0),
        ("the_log",         1.0),
        ("zap",             0.9),
        ("giant_snowball",  0.8),
        ("valkyrie",        0.7),
        ("goblin_curse",    0.6),
        ("tornado",         0.6),
    ],

    # ── Three Musketeers (massive value if Elixir Collector active) ──
    "three_musketeers": [
        ("lightning",       1.0),
        ("rocket",          1.0),
        ("fireball",        0.9),
        ("poison",          0.8),
        ("tornado",         0.7),  # groups them for spells
    ],

    # ── Prince (charge momentum carries over damage) ──
    "prince": [
        ("guards",          1.0),  # shields block charge
        ("skarmy",          0.9),  # trades cost-effectively
        ("inferno_tower",   0.9),
        ("cannon",          0.8),
        ("knight",          0.7),
        ("mini_pekka",      0.7),
        ("tornado",         0.6),
    ],

    # ── Wall Breakers (near-instant bridge pressure) ──
    "wall_breakers": [
        ("the_log",         1.0),  # pre-emptive log
        ("arrows",          0.9),
        ("goblins",         0.8),
        ("bats",            0.7),
        ("cannon",          0.7),
        ("tesla",           0.6),
    ],

    # ── Bandit (dash phase immune to projectiles) ──
    "bandit": [
        ("cannon",          0.9),
        ("mini_pekka",      0.8),
        ("tesla",           0.8),
        ("knight",          0.7),
        ("goblin_cage",     0.7),
        ("fireball",        0.6),
    ],

    # ── Phoenix (revives once — requires two answers) ──
    "phoenix": [
        ("arrows",          0.9),  # kills hatchling
        ("poison",          0.9),
        ("fireball",        0.8),
        ("inferno_dragon",  0.8),
        ("musketeer",       0.7),
        ("mega_minion",     0.7),
    ],

    # ── Royal Hogs (4 low-HP buildings-targeters, burst) ──
    "royal_hogs": [
        ("fireball",        0.9),  # kills all 4 on field
        ("arrows",          0.8),
        ("valkyrie",        0.8),
        ("tornado",         0.7),
        ("cannon",          0.6),
        ("giant_snowball",  0.6),
    ],

    # ── Skeleton Barrel (drop-burst → skeleton swarm on death) ──
    "skeleton_barrel": [
        ("arrows",          0.9),
        ("the_log",         0.8),
        ("giant_snowball",  0.7),
        ("zap",             0.7),
        ("mega_minion",     0.7),
        ("minions",         0.6),
    ],

    # ── Goblinstein Lightning Link (king-tower activation path) ──
    "goblinstein": [
        ("zap",             0.9),   # resets lightning link chain
        ("lightning",       0.8),
        ("electro_wizard",  0.8),
        ("poison",          0.7),
        ("inferno_tower",   0.7),
    ],

    # ── Skeleton Army (massive swarm if spell not available) ──
    "skeleton_army": [
        ("arrows",          1.0),
        ("fireball",        1.0),
        ("the_log",         1.0),
        ("giant_snowball",  0.9),
        ("zap",             0.8),
        ("valkyrie",        0.8),
        ("baby_dragon",     0.8),
        ("wizard",          0.8),
    ],

    # ── Spirit Empress air-mode (6e Air Deploy) ──
    "spirit_empress": [
        ("arrows",          0.8),
        ("musketeer",       0.8),
        ("vines",           0.8),
        ("inferno_dragon",  0.7),
        ("mega_minion",     0.7),
        ("electro_dragon",  0.7),
    ],
}
