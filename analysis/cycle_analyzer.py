"""
analysis/cycle_analyzer.py
===========================
Cycle Analyzer — Section 9.2 of final_hybrid_plan.md.

Metrics:
  avg_elixir:          average of all 8 cycle_elixir values
  cheapest_four:       sum of 4 cheapest cards (one full cycle = reach same card in ~10s)
  cycle_speed_score:   0–100 based on cheapest_four (plan: 35 pts max, normalized)
  elixir_variance:     statistical variance of cycle_elixir values
  balance_score:       penalty for high variance (ideal avg = 3.5–4.2)
  has_spell:           bool — deck includes a damage spell
  has_cheap_cycle:     bool — deck has at least 3 cards at ≤ 2e
"""

from __future__ import annotations
from statistics import variance as stat_var
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.deck import Deck


class CycleAnalyzer:
    """Computes cycle-speed and elixir-balance metrics for a deck."""

    def analyze(self, deck: "Deck") -> dict:
        cards  = deck.cards
        costs  = sorted(c.cycle_elixir for c in cards)

        avg    = sum(costs) / 8
        cheapest_four = sum(costs[:4])

        # Cycle speed score: plan formula min((16 - cheapest_four) * 5, 35)
        cycle_pts = max(0, 16 - cheapest_four) * 5
        cycle_speed_score = min(cycle_pts, 35.0)

        # Elixir variance
        try:
            elixir_var = stat_var(costs) if len(set(costs)) > 1 else 0.0
        except Exception:
            elixir_var = 0.0

        # Balance score: penalty for deviation from 3.85 centre
        balance_score = max(0.0, 10.0 - abs(avg - 3.85) * 6.0)

        has_spell      = any(c.is_damage_spell for c in cards)
        has_cheap_cycle = sum(1 for c in cards if c.cycle_elixir <= 2) >= 3

        return {
            "avg_elixir":          round(avg, 2),
            "cheapest_four":       cheapest_four,
            "cycle_speed_score":   round(cycle_speed_score, 1),
            "elixir_variance":     round(elixir_var, 3),
            "balance_score":       round(balance_score, 1),
            "has_spell":           has_spell,
            "has_cheap_cycle":     has_cheap_cycle,
            "by_cost":             costs,
        }
