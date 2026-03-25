"""
data/synergy_matrix.py
=======================
Pairwise Synergy Matrix — 200+ entries covering all major Q1 2026 archetypes.
Section 4.3 of final_hybrid_plan.md.

Format:
    SYNERGY_MATRIX: dict[tuple[str, str], float]

Keys: SORTED tuple of two card IDs — always (lesser_id, greater_id) alphabetically.
Values: float in [-1.0, +1.0]
  +1.0  = near-perfect synergy (archetypally inseparable)
  +0.7  = strong synergy (commonly paired)
  +0.4  = mild synergy (beneficial but not mandatory)
   0.0  = neutral (not indexed — absent from matrix)
  -0.3  = mild anti-synergy (awkward together)
  -0.7  = strong anti-synergy (one undermines the other)
  -1.0  = full anti-synergy (functionally incompatible)

Used by: SynergyScorer — each pair contributes synergy_matrix[pair] * 10 to raw score.
Archetype coverage (per plan §4.3):
  ✓ Lavaloon (Balloon, Lava Hound archetypes)
  ✓ Hog-cycle (Hog Rider + cheap support)
  ✓ Graveyard control (Graveyard + Poison/Freeze)
  ✓ Beatdown (Golem/Giant + support)
  ✓ X-Bow / Mortar siege
  ✓ Bridge spam (Battle Ram, Hog, Bandit, Wall Breakers)
  ✓ Bait (Goblin Barrel, Princess, Bats)
  ✓ Miner pressure
  ✓ Spirit Empress combos
  ✓ Rune Giant enchantment combos
  ✓ Hero synergies (Boss Bandit, Hero Giant, Archer Queen)
  ✓ Tower-troop synergies (Cannoneer clusters, Chef beatdown)
  ✓ Anti-synergy penalties (spell stacking, WC flooding)
"""

from typing import NamedTuple


def _p(a: str, b: str) -> tuple[str, str]:
    """Return a canonical sorted pair key."""
    return (a, b) if a < b else (b, a)


SYNERGY_MATRIX: dict[tuple[str, str], float] = {

    # ===========================================================================
    # LAVALOON ARCHETYPE
    # Lava Hound tanks air → Balloon reaches tower for massive death damage
    # ===========================================================================
    _p("lava_hound",     "balloon"):            +1.0,
    _p("lava_hound",     "mega_minion"):         +0.8,  # air cover for pups
    _p("lava_hound",     "musketeer"):           +0.7,
    _p("lava_hound",     "flying_machine"):      +0.7,
    _p("lava_hound",     "night_witch"):         +0.8,  # bats = swarm support
    _p("lava_hound",     "tombstone"):           +0.6,  # distraction while hound tanks
    _p("lava_hound",     "arrows"):              +0.7,  # clears pup responses
    _p("lava_hound",     "freeze"):              +0.8,  # freeze while balloon hits
    _p("lava_hound",     "poison"):              +0.6,
    _p("balloon",        "freeze"):              +0.9,  # freeze = balloon hits tower
    _p("balloon",        "rage"):                +0.7,
    _p("balloon",        "vines"):               +0.8,  # vines grounds air counters
    _p("balloon",        "arrows"):              +0.7,
    _p("balloon",        "lightning"):           +0.7,  # kills Inferno Tower / Wizard

    # ===========================================================================
    # HOG CYCLE ARCHETYPE
    # Hog Rider + cheap support cards for rapid cycling
    # ===========================================================================
    _p("hog_rider",      "ice_golem"):           +0.9,  # tank in front, kite
    _p("hog_rider",      "fireball"):            +1.0,  # kills Witch/Musketeer/BB
    _p("hog_rider",      "the_log"):             +0.9,
    _p("hog_rider",      "skeletons"):           +0.7,  # cheap cycle filler
    _p("hog_rider",      "ice_spirit"):          +0.7,
    _p("hog_rider",      "cannon"):              +0.8,  # mirror defense
    _p("hog_rider",      "tesla"):               +0.8,  # mirror defense + anti-air
    _p("hog_rider",      "musketeer"):           +0.7,  # answer to Balloon / Minion Horde
    _p("hog_rider",      "zap"):                 +0.8,  # reset inferno + cheap cycle
    _p("hog_rider",      "giant_snowball"):      +0.6,
    _p("hog_rider",      "electro_spirit"):      +0.7,
    _p("hog_rider",      "goblin_barrel"):       +0.8,  # dual-lane pressure
    _p("hog_rider",      "miner"):               +0.7,  # dual-lane WC pressure
    _p("hog_rider",      "mini_pekka"):          +0.6,  # defense + counter-push
    _p("hog_rider",      "valkyrie"):            +0.5,  # support on counter-push

    # ===========================================================================
    # GRAVEYARD CONTROL ARCHETYPE
    # Graveyard + coverage spells; skeletons win if tower is frozen/poisoned
    # ===========================================================================
    _p("graveyard",      "poison"):              +1.0,  # THE core GY synergy
    _p("graveyard",      "freeze"):              +0.9,  # GY-freeze archetype
    _p("graveyard",      "knight"):              +0.8,  # cheap tank in front
    _p("graveyard",      "ice_golem"):           +0.7,  # tank + kite
    _p("graveyard",      "valkyrie"):            +0.6,
    _p("graveyard",      "tombstone"):           +0.6,  # skeleton army synergy
    _p("graveyard",      "tornado"):             +0.7,  # groups units for GY
    _p("graveyard",      "skeleton_army"):       +0.5,
    _p("graveyard",      "baby_dragon"):         +0.6,
    _p("poison",         "graveyard"):           +1.0,  # already listed above
    _p("poison",         "goblin_barrel"):       +0.7,  # spell-bait + WC combo
    _p("poison",         "miner"):               +0.7,  # miner + poison pressure
    _p("poison",         "princess"):            +0.6,  # she baits counters to poison

    # ===========================================================================
    # GOLEM BEATDOWN ARCHETYPE
    # Golem tanks → support behind = massive DPS push
    # ===========================================================================
    _p("golem",          "night_witch"):         +1.0,  # classic combo
    _p("golem",          "baby_dragon"):         +0.8,
    _p("golem",          "lightning"):           +0.9,  # kills Inferno Tower
    _p("golem",          "mega_minion"):         +0.7,
    _p("golem",          "electro_wizard"):      +0.8,  # resets Inferno Tower
    _p("golem",          "lumberjack"):          +0.9,  # death rage fuels push
    _p("golem",          "poison"):              +0.6,
    _p("golem",          "fireball"):            +0.7,
    _p("golem",          "the_log"):             +0.6,
    _p("golem",          "tornado"):             +0.7,  # chain king activation
    _p("golem",          "battle_healer"):       +0.7,
    _p("golem",          "rune_giant"):          +0.6,  # enchantment aura bonus

    # ===========================================================================
    # GIANT BEATDOWN
    # ===========================================================================
    _p("giant",          "musketeer"):           +0.8,
    _p("giant",          "witch"):               +0.8,
    _p("giant",          "wizard"):              +0.7,
    _p("giant",          "mega_minion"):         +0.7,
    _p("giant",          "electro_wizard"):      +0.7,
    _p("giant",          "lightning"):           +0.7,
    _p("giant",          "poison"):              +0.6,

    # ===========================================================================
    # X-BOW / MORTAR SIEGE ARCHETYPE
    # Siege WC + defensive cover cards
    # ===========================================================================
    _p("x_bow",          "tesla"):               +0.9,  # defends Hog/Ram beside x-bow
    _p("x_bow",          "ice_spirit"):          +0.8,  # cheap cycle
    _p("x_bow",          "the_log"):             +0.8,
    _p("x_bow",          "knight"):              +0.7,
    _p("x_bow",          "skeletons"):           +0.7,
    _p("x_bow",          "ice_golem"):           +0.7,
    _p("x_bow",          "archers"):             +0.6,
    _p("x_bow",          "mega_minion"):         +0.7,
    _p("mortar",         "ice_spirit"):          +0.8,
    _p("mortar",         "the_log"):             +0.7,
    _p("mortar",         "knight"):              +0.7,
    _p("mortar",         "firecracker"):         +0.6,
    _p("mortar",         "goblin_barrel"):       +0.8,  # dual-lane pressure
    _p("mortar",         "skeletons"):           +0.7,

    # ===========================================================================
    # BRIDGE SPAM ARCHETYPE
    # Fast units dropped at bridge + support spells
    # ===========================================================================
    _p("battle_ram",     "bandit"):              +0.8,
    _p("battle_ram",     "fireball"):            +0.7,
    _p("battle_ram",     "the_log"):             +0.7,
    _p("battle_ram",     "dark_prince"):         +0.7,
    _p("battle_ram",     "zap"):                 +0.6,
    _p("battle_ram",     "lumberjack"):          +0.8,  # lumberjack rage on death
    _p("bandit",         "goblin_barrel"):       +0.7,  # dual-lane bait
    _p("bandit",         "hog_rider"):           +0.8,
    _p("bandit",         "wall_breakers"):       +0.7,
    _p("wall_breakers",  "goblin_barrel"):       +0.8,  # double bait
    _p("wall_breakers",  "hog_rider"):           +0.7,
    _p("wall_breakers",  "miner"):               +0.7,

    # ===========================================================================
    # GOBLIN BARREL BAIT ARCHETYPE
    # Barrel baits spells → other bait cards win the trade
    # ===========================================================================
    _p("goblin_barrel",  "princess"):            +0.8,  # princess baits log → no log for barrel
    _p("goblin_barrel",  "bats"):                +0.8,  # bats bait arrows → barrel safe
    _p("goblin_barrel",  "minions"):             +0.7,
    _p("goblin_barrel",  "skeleton_army"):       +0.7,  # skarmy bait + barrel
    _p("goblin_barrel",  "minion_horde"):        +0.7,
    _p("goblin_barrel",  "dark_prince"):         +0.6,  # dark prince baits log
    _p("goblin_barrel",  "goblin_gang"):         +0.6,

    # ===========================================================================
    # MINER PRESSURE DECKS
    # Miner chips + spell support or swarm WC combos
    # ===========================================================================
    _p("miner",          "goblin_barrel"):       +0.9,  # dual-pressure classic
    _p("miner",          "goblin_gang"):         +0.7,
    _p("miner",          "goblins"):             +0.6,
    _p("miner",          "wall_breakers"):       +0.7,
    _p("miner",          "poison"):              +0.8,  # miner + poison push
    _p("miner",          "tornado"):             +0.8,  # king activation combo

    # ===========================================================================
    # CONTROL / TANK KILLER ARCHETYPES
    # ===========================================================================
    _p("inferno_dragon", "tombstone"):           +0.8,  # tombstone kites; ID melts tank
    _p("inferno_dragon", "knight"):              +0.7,
    _p("inferno_tower",  "tombstone"):           +0.7,
    _p("inferno_tower",  "knight"):              +0.7,
    _p("mega_minion",    "musketeer"):           +0.6,
    _p("musketeer",      "valkyrie"):            +0.7,  # ground + air coverage split
    _p("valkyrie",       "musketeer"):           +0.7,  # already symmetric via sorted pair

    # ===========================================================================
    # ELECTRO / RESET CHAIN SYNERGIES
    # Reset cards protect key units from Inferno ramp
    # ===========================================================================
    _p("electro_wizard", "golem"):              +0.8,
    _p("electro_wizard", "giant"):              +0.7,
    _p("electro_wizard", "lava_hound"):         +0.7,
    _p("electro_spirit", "golem"):              +0.7,
    _p("electro_spirit", "giant"):              +0.6,
    _p("electro_spirit", "lava_hound"):         +0.6,
    _p("electro_spirit", "sparky"):             -0.8,  # using spirit to protect sparky
                                                        # is anti-synergy (wastes spirit)
    _p("zap",            "sparky"):             -0.9,  # zap resets YOUR OWN Sparky
    _p("zap",            "inferno_tower"):      +0.8,  # resets their inferno
    _p("zap",            "inferno_dragon"):     +0.8,

    # ===========================================================================
    # TORNADO SYNERGIES (King Tower Activation)
    # ===========================================================================
    _p("tornado",        "electro_wizard"):     +0.8,  # group → reset chain
    _p("tornado",        "wizard"):             +0.7,
    _p("tornado",        "executioner"):        +0.8,  # group → axe hits multiple
    _p("tornado",        "bowler"):             +0.8,  # group → bowler pierces all
    _p("tornado",        "graveyard"):          +0.7,
    _p("tornado",        "giant"):              +0.5,  # pull tanks into king range
    _p("tornado",        "miner"):              +0.7,  # king activation duo

    # ===========================================================================
    # KNIGHT / ICE GOLEM KITE COMBOS
    # ===========================================================================
    _p("knight",         "musketeer"):          +0.7,  # tank + support classic
    _p("ice_golem",      "hog_rider"):          +0.9,  # already listed
    _p("ice_golem",      "musketeer"):          +0.7,
    _p("ice_golem",      "mega_minion"):        +0.7,
    _p("ice_golem",      "tornado"):            +0.6,

    # ===========================================================================
    # PRINCESS BAIT CHAIN
    # ===========================================================================
    _p("princess",       "bats"):              +0.8,  # both baited by different spells
    _p("princess",       "minions"):           +0.6,
    _p("princess",       "goblin_gang"):       +0.6,

    # ===========================================================================
    # LUMBERJACK COMBOS
    # On-death rage fuels offensive pushes
    # ===========================================================================
    _p("lumberjack",     "giant"):             +0.8,
    _p("lumberjack",     "pekka"):             +0.8,
    _p("lumberjack",     "balloon"):           +0.8,
    _p("lumberjack",     "battle_ram"):        +0.8,
    _p("lumberjack",     "golem"):             +0.9,

    # ===========================================================================
    # RUNE GIANT ENCHANTMENT AURA (high-hit-speed units)
    # Every 3rd attack of enchanted allies = bonus damage (stated)
    # ===========================================================================
    _p("rune_giant",     "berserker"):         +1.0,  # 0.6s hit speed → huge bonus
    _p("rune_giant",     "dart_goblin"):       +0.9,  # 0.7s hit speed
    _p("rune_giant",     "musketeer"):         +0.7,  # 1.0s hit speed
    _p("rune_giant",     "inferno_dragon"):    +0.7,  # 0.4s = very fast
    _p("rune_giant",     "mega_minion"):       +0.6,
    _p("rune_giant",     "wizard"):            +0.6,
    _p("rune_giant",     "electro_wizard"):    +0.7,

    # ===========================================================================
    # SPIRIT EMPRESS STATE SYNERGIES
    # Ground mode (3e) = cheap BS; Air mode (6e) = anti-air win condition
    # ===========================================================================
    _p("spirit_empress", "vines"):             +0.8,  # vines grounds air threats
                                                       # she avoids countering
    _p("spirit_empress", "musketeer"):         +0.6,
    _p("spirit_empress", "the_log"):           +0.6,

    # ===========================================================================
    # GOBLINSTEIN SYNERGIES (Lightning Link king activation)
    # ===========================================================================
    _p("goblinstein",    "tornado"):           +0.9,  # tornado + lightning link
    _p("goblinstein",    "lightning"):         +0.7,  # double lightning synergy
    _p("goblinstein",    "fireball"):          +0.6,

    # ===========================================================================
    # BOSS BANDIT COMBOS
    # ===========================================================================
    _p("boss_bandit",    "hog_rider"):         +0.8,
    _p("boss_bandit",    "goblin_barrel"):     +0.7,
    _p("boss_bandit",    "wall_breakers"):     +0.7,
    _p("boss_bandit",    "fireball"):          +0.8,

    # ===========================================================================
    # HERO GIANT BEATDOWN
    # ===========================================================================
    _p("hero_giant",     "lightning"):         +0.9,  # kills Inferno Tower
    _p("hero_giant",     "night_witch"):       +0.8,
    _p("hero_giant",     "mega_minion"):       +0.7,
    _p("hero_giant",     "electro_wizard"):    +0.7,
    _p("hero_giant",     "lumberjack"):        +0.8,
    _p("hero_giant",     "fireball"):          +0.7,

    # ===========================================================================
    # ARCHER QUEEN COMBOS
    # ===========================================================================
    _p("archer_queen",   "balloon"):           +0.7,
    _p("archer_queen",   "lava_hound"):        +0.7,
    _p("archer_queen",   "hog_rider"):         +0.7,
    _p("archer_queen",   "musketeer"):         +0.5,

    # ===========================================================================
    # ELIXIR COLLECTOR INVESTMENT + SUPPORT
    # ===========================================================================
    _p("elixir_collector", "three_musketeers"): +0.9,  # pump to afford 3M split
    _p("elixir_collector", "golem"):            +0.8,
    _p("elixir_collector", "lava_hound"):       +0.7,

    # ===========================================================================
    # TOMBSTONE UTILITY COMBOS
    # ===========================================================================
    _p("tombstone",      "hog_rider"):         +0.7,  # defend mirror + skeletons
    _p("tombstone",      "valkyrie"):          +0.6,
    _p("tombstone",      "mega_minion"):       +0.6,

    # ===========================================================================
    # FREEZE COMBOS
    # ===========================================================================
    _p("freeze",         "balloon"):           +0.9,
    _p("freeze",         "lava_hound"):        +0.7,
    _p("freeze",         "graveyard"):         +0.9,
    _p("freeze",         "pekka"):             +0.7,

    # ===========================================================================
    # LIGHTNING COMBOS
    # ===========================================================================
    _p("lightning",      "golem"):             +0.9,
    _p("lightning",      "lava_hound"):        +0.7,
    _p("lightning",      "hero_giant"):        +0.9,
    _p("lightning",      "three_musketeers"):  +0.8,
    _p("lightning",      "balloon"):           +0.7,

    # ===========================================================================
    # EARTHQUAKE COMBOS (Hog + EQ for building-heavy decks)
    # ===========================================================================
    _p("earthquake",     "hog_rider"):         +0.8,
    _p("earthquake",     "mortar"):            -0.8,  # EQ hurts own Mortar
    _p("earthquake",     "x_bow"):             -0.8,  # EQ hurts own X-Bow

    # ===========================================================================
    # GOBLIN DRILL COMBOS
    # ===========================================================================
    _p("goblin_drill",   "tornado"):           +0.8,  # king activation + drill
    _p("goblin_drill",   "goblin_barrel"):     +0.7,
    _p("goblin_drill",   "miner"):             +0.7,

    # ===========================================================================
    # NIGHT WITCH COMBOS
    # Spawns bats that provide air cover
    # ===========================================================================
    _p("night_witch",    "golem"):             +1.0,  # already listed
    _p("night_witch",    "giant"):             +0.8,
    _p("night_witch",    "mega_knight"):       +0.7,
    _p("night_witch",    "arrows"):            +0.6,  # clears counter-bats

    # ===========================================================================
    # VINES SPECIAL SYNERGY (grounds air, 0.9s delay — plan §6)
    # ===========================================================================
    _p("vines",          "balloon"):           +0.8,  # grounds Inferno Dragon / PEKKA counters
    _p("vines",          "lava_hound"):        +0.7,

    # ===========================================================================
    # ANTI-SYNERGIES (negative values)
    # ===========================================================================

    # Too many win conditions → no support / spells left
    _p("balloon",        "golem"):             -0.5,  # both are 5e+ investments
    _p("golem",          "lava_hound"):        -0.4,  # both massive investment
    _p("three_musketeers", "golem"):           -0.6,  # 14e combined; deck choked
    _p("three_musketeers", "lava_hound"):      -0.5,

    # Earthquake + own buildings = self-damage
    _p("earthquake",     "cannon"):            -0.9,
    _p("earthquake",     "tesla"):             -0.9,
    _p("earthquake",     "inferno_tower"):     -0.7,
    _p("earthquake",     "goblin_cage"):       -0.7,
    _p("earthquake",     "tombstone"):         -0.6,

    # Zap + Sparky = resetting own Sparky
    _p("zap",            "sparky"):            -0.9,  # already listed

    # Two expensive Legendaries without support
    _p("sparky",         "inferno_dragon"):    -0.5,  # both need protection

    # Triple damage spells = elixir inefficiency
    _p("fireball",       "rocket"):            -0.5,
    _p("lightning",      "rocket"):            -0.5,
    _p("fireball",       "lightning"):         -0.3,  # borderline; situational

    # Two tanks with no win condition support
    _p("giant",          "golem"):             -0.7,  # 13e combined investment
    _p("electro_giant",  "golem"):             -0.6,

    # Miner + Goblin Drill both deal direct building damage → redundant role
    _p("miner",          "goblin_drill"):      -0.3,
}
