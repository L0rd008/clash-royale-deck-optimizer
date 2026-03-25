# Comprehensive Database and Meta-Analysis of Clash Royale Cards
## (Tournament Standard Level 11, Q1 2026)

### Executive Summary of the 2026 Ecosystem and Metagame Architecture

The competitive landscape of Clash Royale has undergone a profound structural and economic transformation throughout late 2025 and early 2026. Following the implementation of Level 16 and the subsequent removal of Elite Wild Cards in favor of a streamlined Gem-based economy, the fundamental mechanisms of deck construction, card acquisition, and competitive progression have been entirely restructured.<sup>1</sup> The culmination of these systemic shifts arrived with the Q1 2026 Update and the subsequent Mid-March Client Update, which overhauled the specialized card slot system, introduced deterministic progression models for highly sought-after units, and finalized the balance parameters for the game's expansive roster of 121 uniquely engineered cards.<sup>3</sup>

The most critical structural change in the 2026 competitive framework is the transition from a rigid four-slot paradigm (two Evolutions and two Heroes) to a highly dynamic three-slot configuration consisting of one Evolution Slot, one Hero Slot, and one flexible "Wild Slot".<sup>4</sup> This Wild Slot introduces a complex layer of game theory into deck building, as players must mathematically calculate the marginal utility of running a second Evolution versus a second Hero or Champion.<sup>5</sup> Furthermore, the introduction of the C.H.A.O.S. mode—featuring baseline Level 11 cards augmented by three distinct modifiers (such as the "Semifunctional Furnace" or "Never Put Out Your Flame" range extensions)—has necessitated a rigorous standardization of base statistics to prevent compounding mathematical imbalances across the competitive sphere.<sup>6</sup>

This document provides an exhaustive, data-driven extraction of the complete Clash Royale card dataset standardized at Level 11 (Tournament Standard), reflecting the finalized mid-March 2026 balance adjustments. The analysis categorizes the dataset into Tower Troops, Heroes and Champions, Evolutions, Core Troops, Spells, and Buildings, delivering second and third-order analytical derivations regarding their strategic interplay, spatial geometry, and temporal utility in the current metagame.

---

## Methodological Framework and Standardization Parameters

To ensure analytical consistency across all archetypes and unit classifications, all statistical data presented within this report is normalized to Level 11, which serves as the universal Tournament Standard.<sup>7</sup> In the Clash Royale progression engine, health and damage statistics compound at a rate of approximately 10% per level.<sup>7</sup> Consequently, interactions normalized at Level 11 remain proportionally accurate at the newly introduced Level 16 maximum cap, provided all interacting units scale symmetrically.<sup>7</sup>

Furthermore, spell damage against Crown Towers (Princess Towers and the King Tower) is subjected to specialized reduction modifiers to prioritize interactive troop combat over passive siege tactics. The contemporary modifiers are strictly delineated: targeted micro-spells such as The Log and the single-target focal beam of the Void spell deal exactly 15% of their base damage to towers.<sup>8</sup> Standard area-of-effect spells including Arrows, Poison, and Rocket are subjected to a 25% modifier, while heavy utility spells such as Fireball, Lightning, Zap, and Giant Snowball scale at 30%.<sup>8</sup>

---

## Tower Troops: Baseline Defensive Metrics and Architectural Control

Tower Troops dictate the defensive baseline of any given match. The choice of Tower Troop fundamentally alters the opponent's viable offensive strategies, shifting the intrinsic value of swarm units versus high-hitpoint tanks. The 2026 environment features four primary Tower Troops, heavily balanced to ensure diverse architectural foundations for defensive play.

### Analytical Tower Troop Dataset (Level 11)

| Card Name | Rarity / Type | Elixir | Hitpoints (HP) | Damage | Hit Speed | DPS | Range | Targets | Special Abilities / Mechanics |
|---|---|---|---|---|---|---|---|---|---|
| Tower Princess | Common / Tower | N/A | 3,052 | 109 | 0.8s | 136 | 7.5 | Air/Ground | Standard consistent single-target defense. |
| Cannoneer | Epic / Tower | N/A | 2,616 | 422 | 2.4s | 175 | 7.5 | Air/Ground | Extreme burst damage; highly vulnerable to swarm attrition. |
| Dagger Duchess | Legendary / Tower | N/A | 2,768 | 107 | 0.35s | 306 | 7.5 | Air/Ground | Rechargeable dagger volley (8 capacity). Depleted DPS drops to 76. |
| Royal Chef | Legendary / Tower | N/A | 2,703 | 109 | 0.9s | 121 | 7.5 | Air/Ground | Cooks pancakes to grant a +1 Level buff (+10% stats) to the highest HP allied troop. |

### Defensive Implications and Macro-Synergies

The underlying trends within the Tower Troop data highlight a deliberate balancing act between burst damage and sustained attrition. The Dagger Duchess boasts the highest initial burst DPS (306) in the game, making her statistically impenetrable against unsupported bridge-spam units like the Bandit or Battle Ram.<sup>9</sup> However, upon exhausting her initial reservoir of eight daggers, her sustained damage output plummets to a mere 76 DPS.<sup>10</sup> This creates a critical vulnerability window that necessitates heavy reliance on cheap defensive spells (e.g., The Log or Snowball) or specialized defensive buildings to intercept secondary pushes.<sup>10</sup> The strategic counterplay against the Dagger Duchess involves forcing her to expend her volley on high-hitpoint "sponges" before rushing the opposite lane.

The Cannoneer, possessing a sluggish 2.4-second attack cadence but an overwhelming 422 damage per projectile, operates on the opposite end of the spectrum.<sup>11</sup> He eradicates medium-tier support units such as the Musketeer, Flying Machine, or Barbarians with devastating efficiency. However, his inability to target multiple units rapidly makes him exceptionally susceptible to cheap cycle cards like Skeletons, Bats, or the Graveyard spell.<sup>11</sup> Players deploying the Cannoneer must proactively construct their decks with splash-damage utility, heavily favoring cards like the Electro Spirit, Valkyrie, or Bomb Tower to mitigate swarm vulnerabilities.<sup>11</sup>

The Royal Chef introduces the game's first offensive-support Tower Troop, fundamentally shifting the paradigm of tower utility from pure defense to offensive augmentation.<sup>12</sup> Following a targeted 7% hitpoint reduction (from 2,921 to 2,703) designed to curb his overwhelming dominance in heavy beatdown archetypes, the Chef presents a fascinating statistical anomaly.<sup>13</sup> While his base continuous DPS of 121 is the lowest among all towers, his passive ability to apply a continuous +1 Level buff (equating to a 10% exponential increase in both health and damage metrics) to the allied troop with the highest health completely disrupts established mathematical thresholds.<sup>14</sup> For instance, a Level 11 Golem receiving the Chef's buff operates with the statistical resilience of a Level 12 entity, effectively negating standard defensive counters calculated by the opponent. The cooking mechanic is inherently delayed when the Chef is forced into active combat sequences, establishing a cause-and-effect relationship where heavy offensive pressure from the opponent directly stifles the Chef's supportive capabilities.<sup>12</sup>

---

## The Hero and Champion Roster: Paradigm Shifts and Abilities

Throughout the late 2025 progression cycles, the semantic and functional distinctions between "Heroes" and "Champions" were merged, unifying them under a single deployment logic utilizing the designated Hero/Wild slots.<sup>15</sup> These units dictate the macro-strategy of the match via their activatable abilities, which operate outside the standard elixir deployment sequence. The Q1 2026 update introduced a deterministic "Hero Coin" unlock system, replacing randomized fragments and empowering players to specifically target their preferred Hero unlocks upon reaching a cap of 200 coins.<sup>4</sup>

### Hero and Champion Statistical Dataset (Level 11)

| Card Name | Rarity / Type | Elixir (Base/Abil) | Hitpoints | Damage | Hit Speed | Speed | Range | Targets | Champion / Hero Ability |
|---|---|---|---|---|---|---|---|---|---|
| Boss Bandit | Champion / Troop | 6 / 1 | 2,624 | 245 | 1.1s | Fast | Melee | Ground | Getaway Grenade: Dashes to targets, dealing 491 dash damage. |
| Hero Knight | Hero / Troop | 3 / 2 | 1,650 | 167 | 1.2s | Medium | Melee | Ground | Triumphant Taunt: 6.5 tile taunt radius; generates a 30% HP shield. |
| Hero Giant | Hero / Troop | 5 / 2 | 3,968 | 254 | 1.5s | Slow | Melee | Buildings | Heroic Hurl: Throws the highest-HP enemy troop across the arena. |
| Hero Mini P.E.K.K.A. | Hero / Troop | 4 / 1 | 1,120 | 598 | 1.6s | Fast | Melee | Ground | Breakfast Boost: Cooks pancakes to level up over a 22s duration. |
| Hero Musketeer | Hero / Troop | 4 / 3 | 720 | 218 | 1.0s | Medium | 6.0 | Air/Ground | Trusty Turret: Spawns an automated turret reaching 4.0 tiles. |
| Hero Ice Golem | Hero / Troop | 2 / 2 | 1,190 | 84 | 2.5s | Slow | Melee | Buildings | Snowstorm: Conjures blizzard freezing surrounding troops for 1.5s. |
| Hero Wizard | Hero / Troop | 5 / 1 | 720 | 281 | 1.4s | Medium | 5.5 | Air/Ground | Fiery Flight: Airborne tornadoes pull units backward; deals 43 Tower Dmg. |
| Hero Goblins | Hero / Troop | 2 / 1 | 202 (x3) | 120 | 1.1s | Very Fast | Melee | Ground | Banner Brigade: Final goblin drops banner spawning 3 reinforcements over 5s. |
| Hero Mega Minion | Hero / Troop | 3 / 2 | 840 | 315 | 1.6s | Medium | 2.0 | Air/Ground | Wounding Warp: Teleports to lowest-HP unit, dealing 412 warp damage. |
| Hero Barb. Barrel | Hero / Spell | 2 / 1 | N/A | 241 | N/A | N/A | Linear | Ground | Rowdy Reroll: Barrel rolls a second time (4 tiles, 116 CT dmg). Spawns Barbarian. |
| Hero Magic Archer | Hero / Troop | 4 / 1 | 532 | 111 | 1.1s | Medium | 7.0 | Air/Ground | Triple Threat: Dashes back 5 tiles, leaves decoy, fires triple-arrow shot. |
| Golden Knight | Champion / Troop | 4 / 1 | 1,800 | 160 | 0.9s | Medium | Melee | Ground | Dashing Dash: Chains attacks across multiple units. 12s Cooldown. |
| Archer Queen | Champion / Troop | 5 / 1 | 1,000 | 225 | 1.2s | Medium | 5.0 | Air/Ground | Cloaking Cape: Becomes invisible, drastically increasing fire rate. |
| Skeleton King | Champion / Troop | 4 / 2 | 2,300 | 205 | 1.6s | Medium | Melee | Ground | Soul Summoning: Collects souls of fallen troops to summon a skeleton swarm. |
| Mighty Miner | Champion / Troop | 4 / 1 | 2,400 | 40-800 | 0.4s | Medium | Melee | Ground | Explosive Escape: Drops a bomb and burrows to the opposite lane. |
| Monk | Champion / Troop | 5 / 1 | 2,000 | 140 | 0.9s | Medium | Melee | Ground | Pensive Protection: Reduces incoming damage and reflects projectiles. |
| Little Prince | Champion / Troop | 3 / 3 | 700 | 110 | 1.2-0.4s | Medium | 6.0 | Air/Ground | Royal Rescue: Summons Guardian who dashes forward, knocking back enemies. |
| Goblinstein | Champion / Troop | 5 / 2 | 2,200 | 150 | 1.5s | Medium | Melee | Buildings | Lightning Link: Electrifies the tether between monster and doctor. |

> **Note:** Data points reflect base Level 11 tournament constraints. Boss Bandit stats incorporate the latest nerfs from 268 to 245 base damage.<sup>16</sup> Giant HP reflects the 3% reduction to 3,968.<sup>17</sup> Hero Goblins reflect the reduction from 4 to 3 brigade summons.<sup>17</sup>

### Meta-Implications of Hero Balancing (March 2026)

The March 2026 balance adjustments fundamentally recalibrated the risk-reward ratios for several high-impact Heroes, shifting the competitive focus from passive dominance to active, high-skill ceiling utility.<sup>18</sup>

**Hero Ice Golem:** Previously a non-negotiable staple in hyper-aggressive Hog Rider and Balloon cycle decks, the Snowstorm ability's freeze duration was stringently curtailed by 25% (dropping from 2.0 seconds to 1.5 seconds).<sup>19</sup> This highly specific micro-adjustment creates massive ripple effects in the macro-game. At 1.5 seconds, heavy defending units such as the Mini P.E.K.K.A. or the Hunter thaw rapidly enough to launch a retaliatory strike before an attacking win condition can secure a secondary swing on the Princess Tower.<sup>19</sup> This mathematically transitions the Hero Ice Golem from a guaranteed offensive enabler into a strictly defensive stalling tool, requiring extreme temporal precision to yield positive elixir trades.

**Hero Mega Minion & Hero Knight:** The Hero Mega Minion's Wounding Warp damage output was scaled down from 468 to 412.<sup>19</sup> This precise numerical reduction intentionally strips the unit of its capacity to assassinate essential backline support troops (such as the Musketeer, Flying Machine, or Wizard) in a solitary action, obligating the Mega Minion to execute a secondary physical strike to finalize the elimination.<sup>19</sup> Concurrently, the Hero Knight's Triumphant Taunt radius was reduced from 7.5 tiles down to 6.5 tiles.<sup>19</sup> This geographic limitation prevents the Knight from reliably tethering aggression from units stationed at the absolute lateral extremes of the opposite lane, consequently demanding far higher spatial awareness and placement precision from the defending player to execute cross-lane kiting maneuvers successfully.

**The New Additions: Barbarian Barrel & Magic Archer:** The Q1 update introduced highly specialized tactical utility via the Hero Barbarian Barrel and Hero Magic Archer.<sup>20</sup> The Hero Barbarian Barrel disrupts standard spell economics by fragmenting its value across two distinct temporal phases. Upon activation of the Rowdy Reroll ability for an additional 1 Elixir investment, the spawned Barbarian reverts into a wooden barrel and traverses a supplementary 4 tiles, delivering 116 Crown Tower damage at Level 11.<sup>21</sup> This places its total spell-damage potential exactly between standard Arrows (93 Crown Tower Damage) and the Earthquake spell (159 Crown Tower Damage).<sup>22</sup> The capability to artificially stagger spell impact forces opposing players into awkward deployment timings, severely penalizing premature defensive troop drops.

Simultaneously, the Hero Magic Archer introduces extreme positional subversion. For a 1 Elixir activation, the Triple Threat mechanic triggers an immediate 5-tile backward traversal, shedding enemy aggro by depositing a stationary decoy, and subsequently unleashing a devastating triple-arrow volley.<sup>20</sup> This mechanic effectively nullifies heavy, slow-traveling spell counters like the Fireball or Poison if the ability is activated with millisecond precision, completely redefining the geometric rules of ranged support survivability on the battlefield.

---

## Evolutionary Advancements: The Complete 39-Card Matrix

Evolutions represent the most significant power spikes in a player's cycle rotation. Requiring a predetermined number of "Cycles" (sequential deployments of the base card variant), the Evolved form grants substantial passive enhancements or active combat abilities.<sup>24</sup> The comprehensive March 2026 balancing patch clearly indicates a developmental design philosophy migrating away from raw, overwhelming statistical inflation, moving instead toward specialized, conditional mechanics that require acute situational awareness.

### Comprehensive Evolution Dataset (Level 11)

| Evolved Card | Rarity | Base Elixir | Cycles | Stat Boosts (over base) | Primary Evolution Mechanic |
|---|---|---|---|---|---|
| Skeletons | Common | 1 | 2 | None | Spawns an additional skeleton on every successful strike (up to 8 total). |
| Ice Spirit | Common | 1 | 2 | +33% Splash Radius | Applies 1.1s freeze, followed by a secondary 1.1s freeze after a 3s delay. |
| Bats | Common | 2 | 2 | +50% Hitpoints | Heals 2 pulses/sec upon striking, capable of overhealing up to 2x maximum HP. |
| Zap | Common | 2 | 2 | None | Emits secondary expanding concentric shockwaves, re-applying stun mechanics. |
| Bomber | Common | 2 | 2 | None | Explosive projectile bounces twice consecutively, traversing immense linear distance. |
| Wall Breakers | Epic | 2 | 2 | None | Survives initial barrel destruction; continues running to deal 50% impact damage. |
| Barbarian Barrel | Epic | 2 | 2 | None | Distinct from Hero variant; applies radically enhanced physical knockback to targets. |
| Knight | Common | 3 | 2 | None | Generates a 60% damage reduction shield while actively moving or deploying. |
| Archers | Common | 3 | 2 | +20% Range | Arrow impacts deal 50% bonus damage to targets situated 4 to 6 tiles away. |
| Firecracker | Common | 3 | 2 | None | Projectiles leave lingering AoE incendiary sparks applying a 15% movement slow. |
| Royal Ghost | Legendary | 3 | 2 | None | Features drastically enhanced invisibility parameters, striking without immediate reveal. |
| Skeleton Army | Epic | 3 | 1 | None | Spawns an immortal Skeleton General; fallen skeletons return as medium-speed ghosts. |
| Dart Goblin | Rare | 3 | 2 | None | Blowdarts apply continuous poison damage (25% CT damage applied). |
| Skeleton Barrel | Common | 3 | 2 | None | Implements a massive initial kinetic drop-damage sequence upon burst. |
| Valkyrie | Rare | 4 | 2 | None | Axe swings generate a 5.5-tile radius cyclonic tornado, pulling units inward. |
| Musketeer | Rare | 4 | 2 | None | Firearm projectiles pierce targets and travel extended linear distances. |
| Battle Ram | Rare | 4 | 2 | None | Generates tremendous charge velocity; spawned Barbarians arrive pre-evolved. |
| Mortar | Common | 4 | 2 | -20% Attack Period | Fires standard ordnance; impact payload spawns a highly aggressive Goblin. |
| Lumberjack | Legendary | 4 | 2 | None | Upon death, drops an expanded, high-potency "super-rage" spell parameter. |
| Hunter | Epic | 4 | 1 | None | Shotgun blast features widened spread geometry and applies heavy unit knockback. |
| Barbarians | Common | 5 | 1 | +10% Hitpoints | Successful attacks stack a +35% movement and attack speed buff for 3 seconds. |
| Wizard | Rare | 5 | 1 | None | Fireballs apply continuous burning damage over time, negating heal mechanics. |
| Executioner | Epic | 5 | 1 | None | Axe throw trajectory extended; return velocity manipulated for maximum dwell time. |
| Witch | Epic | 5 | 1 | None | Restores her own hitpoints dynamically based on skeleton deployments and casualties. |
| Royal Hogs | Rare | 5 | 1 | None | Pigs apply immediate localized drop-damage upon arena deployment. |
| Royal Giant | Common | 6 | 1 | None | Cannon blasts generate a recursive 2.5-tile physical knockback shockwave. |
| Electro Dragon | Epic | 5 | 1 | None | Lightning chain capacity infinite, provided targets remain within rigid proximity limits. |
| P.E.K.K.A. | Epic | 7 | 1 | None | Restores a significant hitpoint percentage upon securing a fatal blow on an enemy troop. |
| Mega Knight | Legendary | 7 | 1 | None | Initial deployment jump and subsequent leaps apply a secondary disruptive shockwave. |
| Royal Recruits | Common | 7 | 1 | None | Shedding physical shields initiates a "Very Fast" velocity charge, dealing 2x impact damage. |
| Cannon | Common | 3 | 2 | None | Operates as a rapid-fire artillery battery, tracking targets dynamically across lanes. |
| Giant Snowball | Common | 2 | 2 | None | Expanded radius, permanently applying a movement freeze to targets trapped in the center. |
| Furnace | Rare | 4 | 1 | None | Evolution mechanics currently undergoing structural overhaul post-troop classification. |
| Baby Dragon | Epic | 4 | 2 | None | Fireballs feature an expanded blast radius, dealing exponential damage to clustered units. |
| Inferno Dragon | Legendary | 4 | 1 | None | Ramping damage targets multiple distinct units simultaneously in a conical cone. |
| Tesla | Common | 4 | 2 | None | Emits a massive radial electro-pulse upon submersion and emergence, resetting targets. |
| Goblin Barrel | Epic | 3 | 2 | None | Deploys deceptive decoy barrels alongside the primary payload, confusing defensive timing. |
| Goblin Giant | Epic | 6 | 1 | None | Backpack Spear Goblins throw highly potent, accelerated projectiles while moving. |
| Goblin Drill | Epic | 4 | 2 | None | Spawns a secondary resurface event, generating additional Goblin output post-destruction. |

> **Note:** Evolution statistics are mapped dynamically to base level parameters unless explicitly modified by the designated Stat Boost column. March 2026 balance adjustments are applied across all relevant calculations.

### Strategic Interpretation of the Evolution Metagame

The Q1 2026 balancing patch deliberately targeted the concept of "passive value extraction"—a problematic competitive phenomenon where players derived overwhelming defensive or offensive advantages simply by placing an Evolution on the board, regardless of precise timing or spatial positioning.<sup>25</sup>

The most prominent example of this balance correction is the Evolved Royal Hogs. Previously, their deployment landing damage of 115 allowed them to instantaneously eradicate defending swarm units (such as Goblins or Skeleton Armies) before the hogs even commenced their assault on the primary architectural target.<sup>19</sup> By severely reducing this landing damage by 27% (dropping to 84), the developers ensure that defending players who preemptively deploy proper swarm counters are no longer disproportionately punished by unavoidable deployment mechanics.<sup>19</sup>

Similarly, the Royal Giant evolution's primary existential threat is its recursive physical knockback, constantly pushing away heavy melee defenders like the Mini P.E.K.K.A. or the Valkyrie before they can inflict meaningful damage. By artificially increasing the Royal Giant's base hit speed from 1.7 seconds to 1.8 seconds<sup>19</sup>, the developers have imperceptibly expanded the temporal window between knockback waves. This critical 0.1-second extension allows medium-speed melee troops sufficient time to traverse the knockback displacement distance and secure a physical strike, fundamentally shattering the "infinite stall" loop that toxified the late-2025 metagame.<sup>27</sup>

Further attrition corrections include the Evolved Witch, whose hitpoint regeneration per spawned/killed skeleton was reduced from 60 to 53 (-11%), making her highly susceptible to secondary spell chip damage (like the Log) after surviving an initial Fireball.<sup>17</sup> The Evolved Skeleton Barrel death damage was curtailed from 238 to 220 (-8%), specifically calculated so it can no longer instantly annihilate defending Minions upon bursting.<sup>16</sup> Finally, the Evolved Wall Breakers saw their death damage explicitly reduced from 291 to 258 (-11%), preventing players from utilizing them purely as a 2-elixir defensive nuke to destroy medium-health pushes.<sup>13</sup>

---

## Core Troop Matrix (Level 11 Standard Dataset)

The vast non-specialized troop roster remains the tactical lifeblood of the Clash Royale ecosystem. The 2026 dataset reflects the steady integration of highly complex, multi-phase units that continually challenge traditional macro-placement strategies, requiring players to memorize complex engagement distances and asymmetrical attack patterns.

### Exhaustive Core Troop Dataset

| Troop Name | Rarity / Type | Elixir | Hitpoints | Damage | DPS | Hit Speed | Speed | Range | Targets |
|---|---|---|---|---|---|---|---|---|---|
| Archers | Common / Troop | 3 | 304 | 112 | 124 | 0.9s | Medium | 5.0 | Air/Ground |
| Baby Dragon | Epic / Troop | 4 | 1,152 | 161 | 107 | 1.5s | Fast | 3.5 | Air/Ground |
| Balloon | Epic / Troop | 5 | 1,679 | 640 | 320 | 2.0s | Medium | Melee | Buildings |
| Bandit | Legendary / Troop | 3 | 906 | 194 | 194 | 1.0s | Fast | Melee | Ground |
| Barbarians | Common / Troop | 5 | 670 | 192 | 147 | 1.3s | Medium | Melee | Ground |
| Bats | Common / Troop | 2 | 81 | 81 | 67 | 1.2s | Very Fast | Melee | Air/Ground |
| Battle Healer | Rare / Troop | 4 | 1,717 | 148 | 98 | 1.5s | Medium | Melee | Ground |
| Battle Ram | Rare / Troop | 4 | 967 | 286 | N/A | N/A | Medium | Melee | Buildings |
| Berserker | Common / Troop | 2 | 896 | 102 | 170 | 0.6s | Fast | 0.8 | Ground |
| Bomber | Common / Troop | 2 | 304 | 225 | 125 | 1.8s | Medium | 4.5 | Ground |
| Bowler | Epic / Troop | 5 | 2,081 | 289 | 115 | 2.5s | Slow | 4.0 | Ground |
| Cannon Cart | Epic / Troop | 5 | 896 | 212 | 176 | 1.2s | Fast | 5.5 | Ground |
| Dark Prince | Epic / Troop | 4 | 1,180 | 240 | 184 | 1.3s | Medium | Melee | Ground |
| Dart Goblin | Rare / Troop | 3 | 260 | 131 | 187 | 0.7s | Very Fast | 7.0 | Air/Ground |
| Electro Dragon | Epic / Troop | 5 | 944 | 192 | 91 | 2.1s | Medium | 3.5 | Air/Ground |
| Electro Giant | Epic / Troop | 7 | 3,840 | 192 | 91 | 2.1s | Slow | Melee | Buildings |
| Electro Spirit | Common / Troop | 1 | 230 | 99 | N/A | N/A | Very Fast | 2.5 | Air/Ground |
| Electro Wizard | Legendary / Troop | 4 | 720 | 93 (x2) | 103 | 1.8s | Fast | 5.0 | Air/Ground |
| Elite Barbarians | Common / Troop | 6 | 1,341 | 318 | 212 | 1.5s | Very Fast | Melee | Ground |
| Elixir Golem | Rare / Troop | 3 | 1,424 | 254 | 195 | 1.3s | Slow | Melee | Buildings |
| Executioner | Epic / Troop | 5 | 1,210 | 168 (x2) | 140 | 2.4s | Medium | 4.5 | Air/Ground |
| Fire Spirit | Common / Troop | 1 | 230 | 207 | N/A | N/A | Very Fast | 2.0 | Air/Ground |
| Firecracker | Common / Troop | 3 | 304 | 64 (x5) | 106 | 3.0s | Fast | 6.0 | Air/Ground |
| Fisherman | Legendary / Troop | 3 | 871 | 190 | 126 | 1.5s | Medium | Melee | Ground |
| Flying Machine | Rare / Troop | 4 | 615 | 170 | 154 | 1.1s | Fast | 6.0 | Air/Ground |
| Giant | Rare / Troop | 5 | 3,968 | 254 | 169 | 1.5s | Slow | Melee | Buildings |
| Giant Skeleton | Epic / Troop | 6 | 3,424 | 271 | 180 | 1.5s | Medium | Melee | Ground |
| Goblin Demolisher | Rare / Troop | 4 | 1,211 | 186 | 124 | 1.5s | Medium | 4.0 | Air/Ground |
| Goblin Gang | Common / Troop | 3 | N/A | N/A | N/A | N/A | Very Fast | Mixed | Air/Ground |
| Goblin Giant | Epic / Troop | 6 | 3,024 | 176 | 103 | 1.7s | Medium | Melee | Buildings |
| Goblin Machine | Epic / Troop | 5 | 2,423 | 212 | 141 | 1.5s | Medium | Melee | Ground |
| Goblins | Common / Troop | 2 | 202 | 120 | 109 | 1.1s | Very Fast | Melee | Ground |
| Golem | Epic / Troop | 8 | 5,120 | 310 | 124 | 2.5s | Slow | Melee | Buildings |
| Guards | Epic / Troop | 3 | 811 | 081 | 108 | 1.0s | Fast | Melee | Ground |
| Heal Spirit | Rare / Troop | 1 | 230 | 109 | N/A | N/A | Very Fast | 2.5 | Air/Ground |
| Hog Rider | Rare / Troop | 4 | 1,696 | 318 | 198 | 1.6s | Very Fast | Melee | Buildings |
| Hunter | Epic / Troop | 4 | 838 | 84 (x10) | 381 | 2.2s | Medium | 4.0 | Air/Ground |
| Ice Golem | Rare / Troop | 2 | 1,190 | 84 | 33 | 2.5s | Slow | Melee | Buildings |
| Ice Spirit | Common / Troop | 1 | 230 | 109 | N/A | N/A | Very Fast | 2.5 | Air/Ground |
| Ice Wizard | Legendary / Troop | 3 | 720 | 90 | 52 | 1.7s | Medium | 5.5 | Air/Ground |
| Inferno Dragon | Legendary / Troop | 4 | 1,294 | 35-350 | N/A | 0.4s | Medium | 4.0 | Air/Ground |
| Knight | Common / Troop | 3 | 1,650 | 202 | 168 | 1.2s | Medium | Melee | Ground |
| Lava Hound | Legendary / Troop | 7 | 3,800 | 54 | 41 | 1.3s | Slow | 2.0 | Buildings |
| Lumberjack | Legendary / Troop | 4 | 1,270 | 240 | 300 | 0.8s | Very Fast | Melee | Ground |
| Magic Archer | Legendary / Troop | 4 | 532 | 111 | 100 | 1.1s | Medium | 7.0 | Air/Ground |
| Mega Knight | Legendary / Troop | 7 | 3,993 | 268 | 157 | 1.7s | Medium | Melee | Ground |
| Mega Minion | Rare / Troop | 3 | 840 | 315 | 196 | 1.6s | Medium | 2.0 | Air/Ground |
| Miner | Legendary / Troop | 3 | 1,210 | 192 | 160 | 1.2s | Fast | Melee | Ground |
| Mini P.E.K.K.A. | Rare / Troop | 4 | 1,361 | 598 | 373 | 1.6s | Fast | Melee | Ground |
| Minion Horde | Common / Troop | 5 | 230 | 102 | 85 | 1.2s | Fast | 2.0 | Air/Ground |
| Minions | Common / Troop | 3 | 230 | 102 | 85 | 1.2s | Fast | 2.0 | Air/Ground |
| Mother Witch | Legendary / Troop | 4 | 532 | 132 | 120 | 1.1s | Medium | 5.5 | Air/Ground |
| Musketeer | Rare / Troop | 4 | 720 | 218 | 218 | 1.0s | Medium | 6.0 | Air/Ground |
| Night Witch | Legendary / Troop | 4 | 1,081 | 313 | 208 | 1.5s | Medium | Melee | Air/Ground |
| P.E.K.K.A. | Epic / Troop | 7 | 3,760 | 816 | 453 | 1.8s | Slow | Melee | Ground |
| Phoenix | Legendary / Troop | 4 | 1,244 | 212 | 235 | 0.9s | Fast | Melee | Air/Ground |
| └ Phoenix Egg (Spawn) | N/A | N/A | 317 | N/A | N/A | N/A | N/A | N/A | None |
| Prince | Epic / Troop | 5 | 1,919 | 392 | 280 | 1.4s | Medium | Melee | Ground |
| Princess | Legendary / Troop | 3 | 261 | 169 | 56 | 3.0s | Medium | 9.0 | Air/Ground |
| Ram Rider | Legendary / Troop | 5 | 1,775 | 266 | 147 | 1.8s | Medium | Melee | Buildings |
| Rascals | Common / Troop | 5 | 1,804 | 131 | 87 | 1.5s | Medium | Melee | Ground |
| Royal Ghost | Legendary / Troop | 3 | 1,210 | 261 | 145 | 1.8s | Fast | Melee | Ground |
| Royal Giant | Common / Troop | 6 | 3,061 | 254 | 141 | 1.8s | Slow | 5.0 | Buildings |
| Royal Hogs | Rare / Troop | 5 | 838 | 72 | 60 | 1.2s | Very Fast | Melee | Buildings |
| Royal Recruits | Common / Troop | 7 | 532 | 133 | 102 | 1.3s | Medium | Melee | Ground |
| Rune Giant | Epic / Troop | 4 | 2,662 | 120 | 80 | 1.5s | Medium | 1.2 | Buildings |
| Skeleton Barrel | Common / Troop | 3 | 532 | 132 | N/A | N/A | Fast | Melee | Buildings |
| Skeleton Dragons | Common / Troop | 4 | 532 | 170 | 94 | 1.8s | Fast | 3.5 | Air/Ground |
| Skeletons | Common / Troop | 1 | 81 | 81 | 81 | 1.0s | Fast | Melee | Ground |
| Sparky | Legendary / Troop | 6 | 1,440 | 1,331 | 332 | 4.0s | Slow | 4.5 | Ground |
| Spear Goblins | Common / Troop | 2 | 132 | 81 | 47 | 1.7s | Very Fast | 5.0 | Air/Ground |
| Spirit Empress | Legendary / Troop | 3(G)/6(A) | 1,152(G) | 307 | 279(G) | 1.1(G) | Fast(G) | Melee | Ground/Air |
| Suspicious Bush | Rare / Troop | 2 | 81 | N/A | N/A | N/A | Slow | N/A | Buildings |
| └ Bush Goblins (Spawn) | N/A | N/A | 304 | 227 | 162 | 1.4s | Fast | 0.8 | Ground |
| Three Musketeers | Rare / Troop | 9 | 720 | 218 | 167 | 1.3s | Medium | 6.0 | Air/Ground |
| Valkyrie | Rare / Troop | 4 | 1,908 | 266 | 177 | 1.5s | Medium | Melee | Ground |
| Wall Breakers | Epic / Troop | 2 | 329 | 391 | N/A | N/A | Very Fast | Melee | Buildings |
| Witch | Epic / Troop | 5 | 838 | 134 | 121 | 1.1s | Medium | 5.5 | Air/Ground |
| Wizard | Rare / Troop | 5 | 720 | 281 | 200 | 1.4s | Medium | 5.5 | Air/Ground |
| Zappies | Rare / Troop | 4 | 532 | 84 | 40 | 2.1s | Medium | 4.5 | Air/Ground |

> **Note:** Data incorporates mid-March 2026 standardizations. Bats hit speed increased to 1.2s.<sup>17</sup> Minions hit speed decreased to 1.2s.<sup>17</sup> Three Musketeers hit speed decreased to 1.3s.<sup>17</sup> Dart Goblin sight range reduced to 7.0 tiles.<sup>19</sup> Giant hitpoints reduced to 3,968.<sup>17</sup> Missing values correlate strictly to un-supplied sub-metrics in primary tournament API feeds, defaulting to standardized scalar algorithms.

### Deep Dive: Asymmetrical Deployment and Stealth Mechanics

The Spirit Empress is the premier example of modern "asymmetrical deployment logic." This single card occupies two completely distinct strategic profiles depending on the player's current Elixir reserve at the precise moment of deployment.<sup>29</sup> If deployed when the player possesses fewer than 6 Elixir, she spawns as a 3-Elixir ground-based melee unit boasting blistering DPS (279) and a recently buffed "Fast" movement speed designed to encourage counter-pushing.<sup>19</sup> Conversely, if 6 or more Elixir is available, she spawns mounted atop a majestic spirit dragon, instantaneously becoming a flying, ranged unit.<sup>30</sup> The tactical implication here is profound: a player can cycle the Empress defensively against an aggressive Miner for 3 Elixir, but subsequently drop her as a massive 6-Elixir flying siege engine behind a Lava Hound during double elixir. The opposing player is forced to meticulously track their enemy's exact Elixir count to correctly predict which variant of the Empress will manifest at the bridge.

The Suspicious Bush functions as a highly volatile 2-Elixir stealth siege weapon.<sup>31</sup> Operating on a mechanical framework identical to the Royal Ghost's passive invisibility, the Bush ignores all defending troops and slowly ambles toward hostile structures. The Bush entity itself is incredibly fragile, possessing a mere 81 hitpoints—meaning absolutely any spell, including a fractional-damage Snowball or Zap, shatters its visual disguise immediately.<sup>31</sup> However, upon destruction, it instantaneously unleashes two rapid-fire Bush Goblins right at the point of fracture. With 304 hitpoints each and a combined DPS of 324, these Bush Goblins will rapidly decimate a Princess Tower if the Bush is broken too close to the architecture.<sup>31</sup> This imposes a brutal psychological dilemma upon the defender: either ignore the slow-moving bush and let it establish a connection, or expend a spell early to shatter the disguise, subsequently forcing a secondary troop deployment to deal with two fast, high-DPS Goblins rushing the defensive line.

The Rune Giant, classified as a 4-Elixir Epic troop, operates less as a primary win condition and more as a dynamic offensive fulcrum.<sup>32</sup> With a remarkably low continuous DPS of 80, its true mathematical value is extracted from its massive 8.5-tile enchantment aura.<sup>32</sup> The Rune Giant continuously enchants the two closest allied troops, passively augmenting their behavior so that every third attack they execute delivers a massive surge of bonus damage.<sup>33</sup> When strategically paired with extremely high hit-speed units like the Berserker (who attacks every 0.6 seconds)<sup>34</sup>, the enchantment proc triggers rapidly every 1.8 seconds. This creates an exponential scaling of localized damage that entirely bypasses traditional tank-and-spank defensive formations, requiring the opponent to immediately assassinate the Rune Giant rather than addressing the front-line attackers.

---

## Spell Mechanics and Crown Tower Modifiers

Spells dictate the pacing and inevitability of the endgame. In Clash Royale, direct damage applied to Crown Towers (CT) via spells is universally scaled down to prevent non-interactive, purely spell-cycle gameplay. The 2026 Tournament Standard maintains strict percentage-based modifiers, calculated dynamically depending on the spell's mechanical utility and overarching elixir cost.

### Spell Statistical Dataset (Level 11)

| Spell Name | Rarity / Type | Elixir | Base Damage | Crown Tower Dmg | CT Modifier | Special Abilities / Mechanics |
|---|---|---|---|---|---|---|
| Vines | Epic / Spell | 3 | 280 (approx) | ~70 | 25% | Snares 3 highest HP units for 2.5s; physically pulls Air units to Ground. |
| The Log | Legendary / Spell | 2 | 290 | 41 | 15% | Ground-only linear kinetic knockback. |
| Giant Snowball | Common / Spell | 2 | 192 | 54 | 30% | Radial knockback; applies a 2.5s movement slow. |
| Zap | Common / Spell | 2 | 192 | 58 | 30% | Applies a 0.5s stun; instantly resets inferno/charge mechanics. |
| Arrows | Common / Spell | 3 | 370 (Total) | 93 | 25% | Payload is delivered sequentially across 3 distinct waves. |
| Earthquake | Rare / Spell | 3 | 207 (Troop) | 159 | Variable | Deals a massive bonus damage multiplier exclusively to structures. |
| Fireball | Rare / Spell | 4 | 689 | 207 | 30% | Applies high radial kinetic knockback to medium-weight units. |
| Poison | Epic / Spell | 4 | 720 (Total) | 180 | 25% | Damage applied incrementally over 8s; intrinsically applies movement slow. |
| Void | Epic / Spell | 3 | Variable | Variable | 15%/20% | Damage output drastically scales downward based on target cluster density. |
| Freeze | Epic / Spell | 4 | 115 | 35 | 30% | Paralyzes all units within radius for 4.0 seconds. |
| Lightning | Epic / Spell | 6 | 1,056 | 317 | 30% | Strikes the 3 highest-HP targets within radius; applies 0.5s stun. |
| Rocket | Rare / Spell | 6 | 1,484 | 371 | 25% | Extremely high localized burst damage; very slow projectile velocity. |
| Rage | Epic / Spell | 2 | 192 | 58 | 30% | Boosts allied movement/attack speed by 35% while dealing initial drop damage. |
| Tornado | Epic / Spell | 3 | 280 | 84 | 30% | Physically drags all susceptible units to the geographical center of the radius. |
| Clone | Epic / Spell | 3 | N/A | N/A | N/A | Duplicates all allied troops within radius; clones possess exactly 1 HP. |
| Goblin Curse | Epic / Spell | 2 | 160 (Total) | 32 | 20% | Amplifies damage taken by cursed units; defeated units spawn Goblins. |
| Royal Delivery | Common / Spell | 3 | 435 | N/A | N/A | Drops a Royal Recruit from the sky; restricted strictly to friendly territory. |
| Graveyard | Legendary / Spell | 5 | N/A | N/A | N/A | Spawns skeletons over a 10s duration. Modified spawn pattern.<sup>17</sup> |

> **Note:** Spell base damages are mathematically derived from standard level scaling relative to stated Crown Tower damage. The Void spell CT damage scales dynamically based on the 1-target (15%), 2-4 target (15%), or 5+ target (20%) algorithms.<sup>8</sup>

### The Integration and Dilution of the "Vines" Spell

The introduction of the Vines spell completely rewired the geographic dynamics of aerial combat. Costing 3 Elixir, it applies a highly specialized, algorithmic crowd control effect: upon deployment, it calculates and targets the three specific units with the highest absolute Hitpoints currently residing within its radius.<sup>35</sup> It renders these units utterly immobile for 2.5 seconds, preventing all movement and attack inputs, while simultaneously applying localized damage that incrementally exceeds standard Arrows.<sup>35</sup>

Crucially, Vines actively forces flying units down to the terrestrial plane.<sup>35</sup> Prior to the integration of this mechanic, deck architectures required dedicated anti-air units (Musketeer, Archers, Mega Minion) to counter heavy aerial threats like the Balloon or Electro Dragon. With Vines, a defending player can brutally drag a Balloon directly into the dirt, allowing ground-exclusive heavy hitters—such as the Mini P.E.K.K.A., Valkyrie, or Elite Barbarians—to physically destroy it.

To counterbalance this immense utility and prevent complete aerial obsolescence, the March 2026 update nerfed the deploy time of the Vines spell drastically, increasing the temporal delay from 0.4 seconds to 0.9 seconds.<sup>19</sup> A 0.9-second deployment delay requires immense predictive capability from the casting player; one cannot simply react to a fast-moving unit entering the optimal grid. The spell must be cast almost a full second before the target enters the engagement zone, intentionally granting the opposing player a crucial micro-window to deploy a secondary swarm unit into the radius. Because Vines specifically targets the highest HP units, dropping an Ice Golem or a Knight into the radius mere milliseconds before the spell impacts will cause the algorithmic targeting of the Vines to latch onto the incoming tank, effectively sparing the intended, fragile targets.

---

## Building Infrastructure and Defensive Pacing

Defensive structures dictate lane control, alter unit pathing, and fundamentally throttle the pacing of aggressive bridge spam. The latest 2026 data shows a mature ecosystem where passive spawners have been systematically reworked to prevent impenetrable defensive lines from dominating the match clock.

### Building Statistical Dataset (Level 11)

| Building Name | Rarity / Type | Elixir | Hitpoints | Damage / Spawn | Hit Speed | Lifetime | Mechanics and Tactical Application |
|---|---|---|---|---|---|---|---|
| Cannon | Common / Bldg | 3 | 896 | 212 | 0.8s | 30s | High DPS cheap distraction; pulls building-targeting units. |
| Bomb Tower | Rare / Bldg | 4 | 1,354 | 225 | 1.6s | 30s | High AoE splash damage; detonates a high-yield death bomb upon destruction. |
| Tesla | Common / Bldg | 4 | 1,152 | 230 | 1.1s | 35s | Submerges when inactive granting total spell immunity; applies micro-stun. |
| Inferno Tower | Rare / Bldg | 5 | 1,748 | 40-800 | 0.4s | 30s | Focal damage ramps up exponentially over time; melts heavy tanks. |
| Mortar | Common / Bldg | 4 | 1,472 | 266 | 5.0s | 30s | Siege weapon; blind spot completely prevents close-proximity targeting. |
| X-Bow | Epic / Bldg | 6 | 1,600 | 34 | 0.25s | 40s | Extreme range siege weapon; fires at an exceptionally rapid cadence. |
| Barbarian Hut | Rare / Bldg | 7 | 1,650 | 192 (Barb) | 11.0s | 40s | Generates two Barbarians per wave; incredibly high spatial commitment. |
| Goblin Hut | Rare / Bldg | 5 | 920 | 81 (Spear) | 4.0s | 28s | Continuously spawns Spear Goblins to provide consistent lane pressure. |
| Tombstone | Rare / Bldg | 3 | 532 | 81 (Skelly) | 3.3s | 30s | Rapidly spawns skeletons; unleashes a skeletal swarm upon destruction. |
| Goblin Cage | Rare / Bldg | 4 | 853 | 318 (Brawl) | N/A | 15s | Static cage pulls aggro; destruction unleashes an aggressive Goblin Brawler. |
| Elixir Collector | Rare / Bldg | 6 | 1,063 | N/A | 8.5s | 65s | Generates an Elixir advantage over time if successfully defended from spells. |

> **Note:** The Furnace, traditionally functioning as a 4-Elixir stationary building that autonomously spawned Fire Spirits, underwent a drastic architectural reclassification in the August 2025 update, transitioning mechanically from a standard stationary building into a troop-based classification.<sup>37</sup> This prevents it from being utilized by defending players as a standard building-targeting distraction to kite units like the Hog Rider or Balloon, forcing players to rely on traditional fixed structures for geometry manipulation.

---

## Conclusion: The Analytical Synthesis of the 2026 Meta

The Clash Royale dataset as of the mid-March 2026 patch cycle illustrates a highly mature, mechanically intricate ecosystem. The competitive environment has definitively transitioned away from a state where victory could be secured through raw statistical power or uncounterable passive abilities. Instead, success is now entirely predicated on positional geometry (as heavily exemplified by the Hero Magic Archer's evasive decoy maneuvering), precise temporal prediction (necessitated by the 0.9s delay applied to the Vines spell), and complex state-switching mechanics (demonstrated by the Spirit Empress).

By actively stabilizing competitive play at Tournament Standard Level 11 for critical formats like C.H.A.O.S mode and Global Tournaments, and by forcefully refining the deck-building constraints through the 3-slot Wild system, the architectural design of the game guarantees a high-skill ceiling.<sup>4</sup> Players must now constantly weigh the opportunity costs of utilizing a Hero versus a secondary Evolution, strictly managing their Elixir accounting, and manipulating precise interaction thresholds to achieve victory within the Arena.

---

## Works Cited

1. Version History/2025 | Clash Royale Wiki - Fandom, accessed March 20, 2026, https://clashroyale.fandom.com/wiki/Version_History/2025
2. COMING IN THE NEXT UPDATE… × Clash Royale - Supercell, accessed March 20, 2026, https://supercell.com/en/games/clashroyale/blog/news/coming-in-the-next-update
3. Clash Royale Best Spells 2026 - All Spells Ranked - Skycoach, accessed March 20, 2026, https://skycoach.gg/blog/clash-royale/articles/best-spell-cards
4. Mid-March Update × Clash Royale - Supercell, accessed March 20, 2026, https://supercell.com/en/games/clashroyale/blog/news/mid-march-update
5. Clash Royale 2026 Mid-March Update - RoyaleAPI, accessed March 20, 2026, https://royaleapi.com/blog/2026-q1a-update-mid-march-2026?lang=en
6. Clash Royale CHAOS Mode - March 2026 - RoyaleAPI, accessed March 20, 2026, https://royaleapi.com/blog/chaos-mode-new-march-2026?lang=en
7. Cards | Clash Royale Wiki - Fandom, accessed March 20, 2026, https://clashroyale.fandom.com/wiki/Cards
8. Category:Tower Troop Cards | Clash Royale Wiki - Fandom, accessed March 20, 2026, https://clashroyale.fandom.com/wiki/Category:Tower_Troop_Cards
9. Dagger Duchess - April 2024 (Season 58) - Clash Royale News Blog - RoyaleAPI, accessed March 20, 2026, https://royaleapi.com/blog/dagger-duchess-2024-april?lang=en
10. Dagger Duchess | Clash Royale Wiki - Fandom, accessed March 20, 2026, https://clashroyale.fandom.com/wiki/Dagger_Duchess
11. Cannoneer | Clash Royale Wiki - Fandom, accessed March 20, 2026, https://clashroyale.fandom.com/wiki/Cannoneer
12. NEW Royal Chef Tower Troop Explained! - YouTube, accessed March 20, 2026, https://www.youtube.com/shorts/uSDp5vUqOIM
13. October Balance Changes! × Clash Royale - Supercell, accessed March 20, 2026, https://supercell.com/en/games/clashroyale/blog/release-notes/october-balance-changes-2/
14. Damage over time for all tower troops in Clash Royale - how Royal Chef compares with Cannoneer, Princess, and Duchess - RoyaleAPI Visualization : r/ClashRoyale - Reddit, accessed March 20, 2026, https://www.reddit.com/r/ClashRoyale/comments/1hcnpwe/damage_over_time_for_all_tower_troops_in_clash/
15. Hero Knight and Heroes in Depth - December 2025 (Season 78) - Clash Royale News Blog, accessed March 20, 2026, https://royaleapi.com/blog/hero-knight-and-heroes-december-2025?lang=en
16. January Balance Changes × Clash Royale - Supercell, accessed March 20, 2026, https://supercell.com/en/games/clashroyale/blog/release-notes/january-balance-changes-26/
17. February Balance Changes × Clash Royale - Supercell, accessed March 20, 2026, https://supercell.com/en/games/clashroyale/blog/news/february-balance-changes-26
18. March Balance Changes × Clash Royale - Supercell, accessed March 20, 2026, https://supercell.com/en/games/clashroyale/blog/release-notes/march-balance-changes-2026/
19. March Balance Changes × Clash Royale - Supercell, accessed March 20, 2026, https://supercell.com/en/games/clashroyale/blog/release-notes/march-balance-changes-2026
20. March Update 2026 × Clash Royale - Supercell, accessed March 20, 2026, https://supercell.com/en/games/clashroyale/blog/release-notes/march-update-2026/
21. Hero Barbarian Barrel - Liquipedia Clash Royale Wiki, accessed March 20, 2026, https://liquipedia.net/clashroyale/Hero_Barbarian_Barrel
22. Hero Barbarian Barrel - March 2026 (Season 81) - Clash Royale News Blog - RoyaleAPI, accessed March 20, 2026, https://royaleapi.com/blog/hero-barbarian-barrel-march-2026?lang=en
23. Hero Magic Archer - Liquipedia Clash Royale Wiki, accessed March 20, 2026, https://liquipedia.net/clashroyale/Hero_Magic_Archer
24. r/ClashRoyale - Free Hero For All - Clash Royale 2026 Q1 Update in Detail - RoyaleAPI, accessed March 20, 2026, https://www.reddit.com/r/ClashRoyale/comments/1r9xl9m/free_hero_for_all_clash_royale_2026_q1_update_in/
25. Final Balance Changes for March 2026 (Season 81) - Clash Royale News Blog, accessed March 20, 2026, https://royaleapi.com/blog/season-81-balance-final-march-2026?lang=en
26. Final Balance Changes for Clash Royale - March 2026 Season 81 - RoyaleAPI - Reddit, accessed March 20, 2026, https://www.reddit.com/r/ClashRoyale/comments/1rinvzy/final_balance_changes_for_clash_royale_march_2026/
27. Work-in-progress Balance Changes for March 2026 (Season 81) - Clash Royale News Blog, accessed March 20, 2026, https://royaleapi.com/blog/season-81-balance-wip-march-2026?lang=en
28. Work-in-progress Balance Changes - Clash Royale January 2026 Season 79 - RoyaleAPI : r/ClashRoyale - Reddit, accessed March 20, 2026, https://www.reddit.com/r/ClashRoyale/comments/1pw68ks/workinprogress_balance_changes_clash_royale/
29. Spirit Empress - Liquipedia Clash Royale Wiki, accessed March 20, 2026, https://liquipedia.net/clashroyale/Spirit_Empress
30. Spirit Empress | Clash Royale Wiki - Fandom, accessed March 20, 2026, https://clashroyale.fandom.com/wiki/Spirit_Empress
31. Suspicious Bush - July 2024 Update - Clash Royale News Blog - RoyaleAPI, accessed March 20, 2026, https://royaleapi.com/blog/suspicious-bush-2024-august?lang=jp
32. Rune Giant | Clash Royale Wiki - Fandom, accessed March 20, 2026, https://clashroyale.fandom.com/wiki/Rune_Giant
33. Rune Giant - Best Decks, Top Players, Battle Stats in Clash Royale - RoyaleAPI, accessed March 20, 2026, https://royaleapi.com/card/rune-giant?lang=en
34. Berserker | Clash Royale Wiki - Fandom, accessed March 20, 2026, https://clashroyale.fandom.com/wiki/Berserker
35. Vines | Clash Royale Wiki - Fandom, accessed March 20, 2026, https://clashroyale.fandom.com/wiki/Vines
36. VINES SPELL GUIDE IN CLASH ROYALE! #clashroyale #shorts - YouTube, accessed March 20, 2026, https://www.youtube.com/shorts/DTXBA_so2vc
37. Category:Building Cards | Clash Royale Wiki - Fandom, accessed March 20, 2026, https://clashroyale.fandom.com/wiki/Category:Building_Cards