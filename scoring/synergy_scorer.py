"""
scoring/synergy_scorer.py
==========================
Synergy Score — Section 4.3 of final_hybrid_plan.md.

Formula (verbatim from plan):
  # Pairwise from SYNERGY_MATRIX
  for pair in combinations(deck.cards, 2):
      key = tuple(sorted([pair[0].id, pair[1].id]))
      synergy_score += SYNERGY_MATRIX.get(key, 0.0) * 10

  # Structural combos
  if has_tank and has_support_behind_tank:            synergy_score += 8
  if win_condition_supported_by_spell:                synergy_score += 8
  if investment_card and cheap_cycle_card:            synergy_score += 5
  if anti_air_count >= 2:                             synergy_score += 6

  # Bait synergy — graduated (fix: single bait also scores)
  for spell_id in all_spells_in_deck:
      baiters = count(c for c in deck if spell_id in c.bait_spells)
      if baiters == 1: synergy_score += 5
      if baiters >= 2: synergy_score += 14

  # Elixir curve coherence
  elixir_variance = variance(c.cycle_elixir for c in deck)
  synergy_score -= min(elixir_variance * 2, 15)

  # Anti-synergy penalties
  if wc_count >= 3:           synergy_score -= 10
  if damage_spell_count >= 4: synergy_score -= 10
  if def_building_count >= 2: synergy_score -= 8

  # Normalize — clamped at BOTH ends
  raw = synergy_score
  synergy_score = max(0.0, min(1.0, (raw + 30) / 150)) * 100
"""

from __future__ import annotations
from itertools import combinations
from statistics import variance as stat_variance
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.deck import Deck

from data.synergy_matrix import SYNERGY_MATRIX


class SynergyScorer:
    """Computes the Synergy component score for a Deck (0–100)."""

    def score(self, deck: "Deck") -> float:
        cards = deck.cards
        raw = 0.0

        # ── Level 1: Pairwise synergy from SYNERGY_MATRIX ─────────────────────
        for c1, c2 in combinations(cards, 2):
            key = (c1.id, c2.id) if c1.id < c2.id else (c2.id, c1.id)
            raw += SYNERGY_MATRIX.get(key, 0.0) * 10.0

        # ── Level 2: Structural synergy ────────────────────────────────────────

        has_tank = any(c.is_tank for c in cards)
        has_support = any(c.is_support for c in cards)
        if has_tank and has_support:
            raw += 8.0  # tank + support behind

        has_wc = any(c.is_win_condition for c in cards)
        has_damage_spell = any(c.is_damage_spell for c in cards)
        if has_wc and has_damage_spell:
            raw += 8.0  # win condition supported by spell

        has_investment = any(c.is_investment for c in cards)
        has_cheap_cycle = any(c.cycle_elixir <= 2 for c in cards)
        if has_investment and has_cheap_cycle:
            raw += 5.0  # investment + cheap filler cycle

        anti_air_count = sum(1 for c in cards if c.is_anti_air)
        if anti_air_count >= 2:
            raw += 6.0  # layered anti-air coverage

        # ── Level 3: Graduated bait synergy ───────────────────────────────────
        # Correct logic: count how many of YOUR cards bait each OPPONENT spell.
        # Bait synergy is about overloading the opponent's spell cycle, completely
        # independent of which spells YOU run. Iterating over your own deck's spell
        # IDs (the previous bug) awarded 0 pts to classic Log-Bait if you didn't
        # run The Log yourself — defeating the entire purpose of bait synergy.
        all_baited_spells: set[str] = set()
        for c in cards:
            all_baited_spells.update(c.bait_spells)

        for spell_id in all_baited_spells:
            baiters = sum(1 for c in cards if spell_id in c.bait_spells)
            if baiters == 1:
                raw += 5.0    # single bait
            elif baiters >= 2:
                raw += 14.0   # double-bait overload

        # ── Elixir curve coherence penalty ────────────────────────────────────
        elixirs = [c.cycle_elixir for c in cards]
        if len(set(elixirs)) > 1:   # variance needs at least 2 distinct values
            try:
                elixir_var = stat_variance(elixirs)
            except Exception:
                elixir_var = 0.0
        else:
            elixir_var = 0.0
        raw -= min(elixir_var * 2.0, 15.0)

        # ── Anti-synergy penalties ─────────────────────────────────────────────
        wc_count = sum(1 for c in cards if c.is_win_condition)
        damage_spell_count = sum(1 for c in cards if c.is_damage_spell)
        def_building_count = sum(1 for c in cards if c.is_defensive_building)

        if wc_count >= 3:
            raw -= 10.0
        if damage_spell_count >= 4:
            raw -= 10.0
        if def_building_count >= 2:
            raw -= 8.0

        # ── Normalize: range = [-30, +120] → [0, 100] (plan §4.3) ────────────
        # Formula: max(0, min(1, (raw + 30) / 150)) * 100
        normalized = max(0.0, min(1.0, (raw + 30.0) / 150.0)) * 100.0
        return normalized
