"""
analysis/counter_analyzer.py
==============================
Counter Analyzer — Section 9.1 of final_hybrid_plan.md.

Aggregates all 3 counter layers (WC, DEF, SWC) to compute:
  wc_coverage_score(deck):  how well deck handles opponent WCs
  def_coverage_score(deck): how well deck handles defensive units
  swc_coverage_score(deck): how well deck handles secondary threats
  total_counter_score(deck): weighted sum (0–100)

Weights per plan §9.1:
  wc_weight  = 0.50
  def_weight = 0.30
  swc_weight = 0.20
"""

from __future__ import annotations
from typing import TYPE_CHECKING

from data.wc_counters  import WC_COUNTERS
from data.def_counters import DEF_COUNTERS
from data.swc_counters import SWC_COUNTERS

if TYPE_CHECKING:
    from models.deck import Deck

_WC_W  = 0.50
_DEF_W = 0.30
_SWC_W = 0.20


def _layer_score(
    threat_dict: dict,
    deck_ids: set[str],
    normalize_by: int,
) -> float:
    """
    Generic layer scorer.
    threat_dict: {threat_id: [(counter_id, effectiveness), ...]}
    Returns 0–100 representing average top-counter effectiveness across threats.
    """
    if not threat_dict:
        return 0.0

    total = 0.0
    for threat_id, counters in threat_dict.items():
        best = max(
            (eff for cid, eff in counters if cid in deck_ids),
            default=0.0,
        )
        total += best

    max_possible = len(threat_dict) * 1.0  # each threat can contribute max 1.0
    return min((total / max_possible) * 100.0, 100.0)


class CounterAnalyzer:
    """Computes per-layer and aggregate counter score for a deck."""

    def wc_coverage(self, deck: "Deck") -> float:
        """WC layer — how well deck counters opponent win conditions (0–100)."""
        ids = {c.id for c in deck.cards}
        return _layer_score(WC_COUNTERS, ids, normalize_by=len(WC_COUNTERS))

    def def_coverage(self, deck: "Deck") -> float:
        """DEF layer — how well deck handles defensive units (0–100)."""
        ids = {c.id for c in deck.cards}
        return _layer_score(DEF_COUNTERS, ids, normalize_by=len(DEF_COUNTERS))

    def swc_coverage(self, deck: "Deck") -> float:
        """SWC layer — how well deck handles secondary threats (0–100)."""
        ids = {c.id for c in deck.cards}
        return _layer_score(SWC_COUNTERS, ids, normalize_by=len(SWC_COUNTERS))

    def total_counter_score(self, deck: "Deck") -> float:
        """Weighted aggregate of all 3 layers (0–100)."""
        wc  = self.wc_coverage(deck)
        dfc = self.def_coverage(deck)
        swc = self.swc_coverage(deck)
        return wc * _WC_W + dfc * _DEF_W + swc * _SWC_W

    def analyze(self, deck: "Deck") -> dict[str, float]:
        """Return full breakdown as a named dict."""
        return {
            "wc_coverage":    self.wc_coverage(deck),
            "def_coverage":   self.def_coverage(deck),
            "swc_coverage":   self.swc_coverage(deck),
            "counter_total":  self.total_counter_score(deck),
        }
