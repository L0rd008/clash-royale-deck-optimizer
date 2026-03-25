"""
data/tower_synergy_rules.py
============================
Tower Synergy Rules — per-tower-troop deck compatibility bonuses/penalties.
Section 4.5 of final_hybrid_plan.md.

Structure:
  TOWER_SYNERGY_RULES: dict[tower_troop_id → rule_dict]

Each rule_dict can contain:
  "preferred_cards"    : list[str]  — card IDs that combo well with this tower
  "anti_cards"         : list[str]  — card IDs that have negative synergy
  "preferred_role_flag": str        — boolean Card flag that synergizes (e.g. "is_splash")
  "anti_role_flag"     : str        — boolean Card flag that is penalized
  "preferred_archetype": str        — one of: "beatdown","cycle","bridge_spam","control","siege"
  "bonus_per_preferred": float      — score bonus per preferred card found in deck
  "penalty_per_anti"  : float       — score penalty per anti card found
  "notes"             : str         — human-readable explanation

Scoring (used by TowerSynergyScorer):
  raw = Σ bonus_per_preferred * (preferred cards in deck)
      - Σ penalty_per_anti    * (anti cards in deck)
      + role_flag_bonus (if deck has preferred role flags)
  tower_synergy_score = clamp(raw, 0, 100)
  → Folded into versatility_score as up to 10 bonus pts (plan §4.4).
"""

TOWER_SYNERGY_RULES: dict[str, dict] = {

    # ─────────────────────────────────────────────────────────────────────────
    # PRINCESS TOWER (baseline — balanced generalist)
    # No specific bonus/penalty. Acts as the neutral reference point.
    # ─────────────────────────────────────────────────────────────────────────
    "princess": {
        "preferred_cards":     [],
        "anti_cards":          [],
        "preferred_role_flags": [],
        "anti_role_flags":     [],
        "preferred_archetype": None,
        "bonus_per_preferred": 5.0,
        "penalty_per_anti":    4.0,
        "notes": (
            "Princess Tower is the default baseline tower troop. "
            "No special synergies or penalties — scores a flat 50 baseline."
        ),
        "base_score": 50.0,
    },

    # ─────────────────────────────────────────────────────────────────────────
    # CANNONEER — fires a cannonball that bounces between troop clusters.
    # Reward: splash coverage partners (crowd-control cards let Cannoneer hit
    #   dense clusters for chain damage).
    # Penalty: if NO splash in deck, Cannoneer ball hits isolated single targets
    #   for sub-optimal value.
    # Reference: reference.md "Cannoneer fires bouncing cannonball; best vs clusters"
    # ─────────────────────────────────────────────────────────────────────────
    "cannoneer": {
        "preferred_cards": [
            "electro_spirit",   # folds swarms into tight clusters → multi-bounce
            "valkyrie",         # pulls melee into range
            "bowler",           # linear push creates cluster lines
            "tornado",          # active grouping
            "baby_dragon",      # complementary AoE to cannoneer
            "wizard",           # stacks with Cannoneer on ground waves
            "goblinstein",      # lightning link + cannoneer ball = double splash
            "bomb_tower",       # building splash + bouncing ball
        ],
        "anti_cards": [
            "miner",            # solo no-swarm unit; Cannoneer ball can't bounce
            "lava_hound",       # pup dispersal hurts bounce
        ],
        "preferred_role_flags": ["is_splash", "is_anti_ground_swarm"],
        "anti_role_flags":      [],
        "preferred_archetype": "control",
        "bonus_per_preferred": 6.0,
        "penalty_per_anti":    5.0,
        "notes": (
            "Cannoneer's bouncing cannonball deals maximum value vs. clustered troops. "
            "Decks with splash/crowd-control cards funnel troops into tight groups for "
            "chain damage. Penalty if deck has no splash coverage — ball hits one target."
        ),
        "base_score": 40.0,
    },

    # ─────────────────────────────────────────────────────────────────────────
    # DAGGER DUCHESS — alternates between 8-dagger burst (306 burst DPS) and
    # sustained fire (76 DPS). Best abused with HP sponges that let her reload.
    # Reward: high-HP tank cards (absorb incoming while she fires burst)
    # Reward: cheap spells (defend Dagger Duchess from counters quickly)
    # Reference: reference.md "Dagger Duchess two-phase: 306 burst → 76 sustained"
    # ─────────────────────────────────────────────────────────────────────────
    "dagger_duchess": {
        "preferred_cards": [
            "giant",          # absorbs incoming; lets burst fire uninterrupted
            "golem",          # max HP sponge for sustained burst abuse
            "lava_hound",     # air tank; Dagger Duchess handles ground threats
            "electro_giant",  # high-HP tank
            "battle_healer",  # sustains HP to keep absorbing incoming
            "ice_golem",      # cheap HP sponge + death slow for burst window
            "the_log",        # cheap spell to clear bats / skeletons distracting her
            "zap",            # reset any inferno ramping on her
            "ice_spirit",     # cheap cycle defense
        ],
        "anti_cards": [
            "goblin_drill",   # targeted on HER tower directly, she can't prevent
        ],
        "preferred_role_flags": ["is_tank", "is_level_independent"],
        "anti_role_flags":      [],
        "preferred_archetype": "beatdown",
        "bonus_per_preferred": 7.0,
        "penalty_per_anti":    6.0,
        "notes": (
            "Dagger Duchess excels when supported by HP sponges that let her reload "
            "her dagger burst without interruption. Cheap spells protect her from "
            "the swarms and inferno stacks she can't handle on her own. "
            "Beatdown archetypes (Golem, Giant, Lava Hound) exploit her burst optimally."
        ),
        "base_score": 42.0,
    },

    # ─────────────────────────────────────────────────────────────────────────
    # ROYAL CHEF — applies a HP buff aura to nearby allied troops (+10% HP).
    # Reward: beatdown tanks that benefit most in absolute HP from the buff
    # Reward: high-HP troops near the tower (Golem, Giant, Hero Giant, Lava Hound)
    # Note: buff has a delay under pressure — tower must survive to apply it.
    # Reference: reference.md "Royal Chef gives +10% HP aura to nearby allied troops"
    # ─────────────────────────────────────────────────────────────────────────
    "royal_chef": {
        "preferred_cards": [
            "golem",          # +512 HP from buff (10% × 5120)
            "giant",          # +396 HP
            "hero_giant",     # large HP pool → large absolute buff
            "lava_hound",     # +380 HP
            "electro_giant",  # +384 HP
            "p_e_k_k_a",      # +376 HP
            "mega_knight",    # +399 HP
            "battle_healer",  # stacks with her healing
            "golem",          # already listed → biggest beneficiary
        ],
        "anti_cards": [
            "miner",          # single low-HP unit; buff has minimal impact
            "wall_breakers",  # very low HP; buff = 32 HP only
        ],
        "preferred_role_flags": ["is_tank", "is_investment"],
        "anti_role_flags":      ["is_bait_card"],  # bait = low HP = small buff benefit
        "preferred_archetype": "beatdown",
        "bonus_per_preferred": 8.0,
        "penalty_per_anti":    4.0,
        "notes": (
            "Royal Chef's +10% HP aura gives biggest absolute value to already-large "
            "HP pools. Beatdown tanks (Golem, Giant, Lava Hound) benefit over 300+ HP "
            "each. Bait / low-HP decks barely notice the buff. Note: buff has application "
            "delay under pressure — works best in slower-paced beatdown decks."
        ),
        "base_score": 38.0,
    },
}
