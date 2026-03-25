"""
data/all_cards.py
==================
Aggregates ALL Card instances into a single ALL_CARDS list and ID lookup dict.

This is the single source of truth consumed by CardFilter, ComboCache, and
BeamSearchOptimizer. Tower troops are excluded from ALL_CARDS (they are
accessed separately as deck.tower_troop for TowerSynergyScorer).

Applies meta_weight overrides from meta_weights.py on top of each card's
default meta_weight=1.0.
"""

from data.cards_troops     import ALL_TROOPS
from data.cards_spells     import ALL_SPELLS
from data.cards_buildings  import ALL_BUILDINGS
from data.cards_heroes     import ALL_HEROES
from data.cards_evolutions import ALL_EVOLUTIONS
from data.cards_tower_troops import ALL_TOWER_TROOPS
from data.meta_weights     import META_WEIGHTS
from models.card           import Card


# ---------------------------------------------------------------------------
# Merge and apply meta weights
# ---------------------------------------------------------------------------

def _apply_meta_weights(cards: list[Card]) -> list[Card]:
    for c in cards:
        if c.id in META_WEIGHTS:
            c.meta_weight = META_WEIGHTS[c.id]
            c.meta_weight_source = "manual"
    return cards


# All deck-eligible cards (excludes Tower Troops)
ALL_CARDS: list[Card] = _apply_meta_weights(
    ALL_TROOPS + ALL_SPELLS + ALL_BUILDINGS + ALL_HEROES + ALL_EVOLUTIONS
)

# Tower troops — separate, not in deck slot pool
ALL_TOWER_TROOP_CARDS: list[Card] = ALL_TOWER_TROOPS

# O(1) lookup by card ID
CARD_BY_ID: dict[str, Card] = {c.id: c for c in ALL_CARDS}
TOWER_BY_ID: dict[str, Card] = {c.id: c for c in ALL_TOWER_TROOP_CARDS}


# ---------------------------------------------------------------------------
# Integrity helpers
# ---------------------------------------------------------------------------

def get_card(card_id: str) -> Card:
    """Retrieve a card by slug. Raises KeyError if not found."""
    return CARD_BY_ID[card_id]


def verify_all_cards() -> dict:
    """
    Run basic integrity checks on ALL_CARDS.
    Returns a dict with counts and any warnings.
    """
    warnings = []
    no_flags = [c.id for c in ALL_CARDS if c.role_count() == 0
                and c.card_type.value != "spell"]
    if no_flags:
        warnings.append(f"Cards with zero role flags: {no_flags}")

    missing_meta = [c.id for c in ALL_CARDS if c.id not in META_WEIGHTS]
    if missing_meta:
        warnings.append(f"Cards missing meta_weight override: {missing_meta}")

    evo_missing_base = [
        c.id for c in ALL_CARDS
        if c.slot_type.value == "evolution" and not c.base_card_id
    ]
    if evo_missing_base:
        warnings.append(f"Evolutions missing base_card_id: {evo_missing_base}")

    dupes = [c.id for c in ALL_CARDS
             if sum(1 for x in ALL_CARDS if x.id == c.id) > 1]
    if dupes:
        warnings.append(f"Duplicate card IDs: {list(set(dupes))}")

    return {
        "total_cards":       len(ALL_CARDS),
        "troops":            len(ALL_TROOPS),
        "spells":            len(ALL_SPELLS),
        "buildings":         len(ALL_BUILDINGS),
        "heroes":            len(ALL_HEROES),
        "evolutions":        len(ALL_EVOLUTIONS),
        "tower_troops":      len(ALL_TOWER_TROOPS),
        "warnings":          warnings,
    }


if __name__ == "__main__":
    report = verify_all_cards()
    for k, v in report.items():
        print(f"{k:20s}: {v}")
