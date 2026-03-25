"""
analysis/deck_report.py
========================
Deck Report — Section 9.4 of final_hybrid_plan.md.

Aggregates all analysis modules into a structured JSON-serializable report dict.
Used by main.py to emit output/top_decks.json.
"""

from __future__ import annotations
from typing import TYPE_CHECKING

from analysis.counter_analyzer import CounterAnalyzer
from analysis.cycle_analyzer   import CycleAnalyzer
from analysis.bait_analyzer    import BaitAnalyzer

if TYPE_CHECKING:
    from models.deck import Deck

_counter = CounterAnalyzer()
_cycle   = CycleAnalyzer()
_bait    = BaitAnalyzer()


def generate_report(deck: "Deck", rank: int = 1) -> dict:
    """
    Build a full structured report for a scored Deck.

    Returns a JSON-serializable dict with:
      rank, tower_troop, total_score, component_scores,
      counter_analysis, cycle_analysis, bait_analysis,
      card_list (id, name, elixir, role_flags per card)
    """
    # Collect role flags per card for readability
    _flag_names = [
        "is_win_condition", "is_damage_spell", "is_anti_air",
        "is_defensive_building", "is_investment", "is_tank",
        "is_support", "is_punishment", "is_bridge_spam",
        "is_splash", "is_bait_card", "is_level_independent",
    ]

    card_list = []
    for c in deck.cards:
        flags = [f.replace("is_", "") for f in _flag_names if getattr(c, f, False)]
        card_list.append({
            "id":      c.id,
            "name":    c.name,
            "elixir":  c.cycle_elixir,
            "roles":   flags,
        })

    report = {
        "rank":   rank,
        "tower_troop": deck.tower_troop,
        "total_score": round(deck.total_score, 2),
        "component_scores": {
            "attack":        round(getattr(deck, "attack_score", 0.0), 2),
            "defense":       round(getattr(deck, "defense_score", 0.0), 2),
            "synergy":       round(getattr(deck, "synergy_score", 0.0), 2),
            "versatility":   round(getattr(deck, "versatility_score", 0.0), 2),
            "tower_synergy": round(getattr(deck, "tower_synergy_score", 0.0), 2),
        },
        "counter_analysis": _counter.analyze(deck),
        "cycle_analysis":   _cycle.analyze(deck),
        "bait_analysis":    _bait.analyze(deck),
        "cards": card_list,
    }
    return report


def generate_reports(decks: list["Deck"]) -> list[dict]:
    """Generate sorted reports for a list of ranked decks."""
    return [generate_report(d, rank=i + 1) for i, d in enumerate(decks)]
