"""
models/combo_score.py
=====================
ComboScore dataclass used by the combo cache.

Stores pre-computed analysis for 2, 3, and 4-card subsets so the beam
search can evaluate partial decks without recomputing pair synergies.

Architecture: Final Hybrid Plan v2.0 — Q1 2026 Meta.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ComboScore:
    """
    Pre-computed metrics for a N-card subset (N = 2, 3, or 4).
    Keyed in ComboCache by frozenset of card IDs.
    """

    card_ids: frozenset[str]        # The cards in this combo

    # --- Elixir ---
    elixir_total: int = 0
    avg_elixir: float = 0.0

    # --- Role Coverage ---
    roles_covered: set[str] = field(default_factory=set)
    # ^ Union of all active role flags across cards in this combo

    # --- Synergy ---
    synergy_sum: float = 0.0
    # ^ Sum of SYNERGY_MATRIX pair values for all pairs within this combo.
    # Positive = synergistic, negative = anti-synergy.

    # --- Bait Chains ---
    bait_chains: dict[str, int] = field(default_factory=dict)
    # ^ spell_id → count of cards in this combo that bait that spell.
    # e.g. {"log": 2, "arrows": 1} means the combo double-baits Log.

    # --- Key Flags ---
    has_win_condition: bool = False
    has_damage_spell: bool = False
    has_anti_air: bool = False
    has_defensive_building: bool = False
    king_activation_potential: bool = False

    # --- Spell Pressure ---
    spell_ct_damage_total: int = 0
    # ^ Sum of ct_damage for all damage spells in this combo.
    # Used for attack scoring of partial decks.

    # --- Counter Coverage ---
    counter_wc_coverage: set[str] = field(default_factory=set)
    # ^ Set of meta win condition IDs this combo can counter (via counters_win_conditions).

    counter_def_coverage: set[str] = field(default_factory=set)
    # ^ Set of defending unit/building IDs this combo can remove offensively.

    # --- Partial Score Contributions ---
    attack_contribution: float = 0.0
    # ^ Partial attack score for this subset (before the rest of the deck is filled).

    defense_contribution: float = 0.0
    # ^ Partial defense score for this subset.

    def __repr__(self) -> str:
        ids = ", ".join(sorted(self.card_ids))
        return (
            f"ComboScore([{ids}], syn={self.synergy_sum:.2f}, "
            f"wc={self.has_win_condition}, ct={self.spell_ct_damage_total})"
        )
