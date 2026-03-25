"""
scoring/deck_scorer.py
=======================
Deck Score Aggregator — Section 4.6 of final_hybrid_plan.md.

Final formula (verbatim from plan):
  WEIGHTS = {
      "attack":      0.30,
      "defense":     0.30,
      "synergy":     0.25,
      "versatility": 0.15,
  }
  total_score = (
      attack_score      * WEIGHTS["attack"]      +
      defense_score     * WEIGHTS["defense"]     +
      synergy_score     * WEIGHTS["synergy"]     +
      versatility_score * WEIGHTS["versatility"]
  )

Also applies optional Ladder Viability Modifier (Section 10):
  if config.LADDER_MODE:
      level_penalty = sum(-5 for c in deck if c.is_weak_underleveled)
      level_bonus   = sum(+3 for c in deck if c.is_level_independent)
      total_score += (level_penalty + level_bonus)

All component scores are stored back on deck for inspection.
"""

from __future__ import annotations

import config
from models.deck import Deck
from scoring.attack_scorer import AttackScorer
from scoring.defense_scorer import DefenseScorer
from scoring.synergy_scorer import SynergyScorer
from scoring.tower_synergy_scorer import TowerSynergyScorer
from scoring.versatility_scorer import VersatilityScorer


# Module-level shared instances (stateless scorers — safe to reuse)
_attack = AttackScorer()
_defense = DefenseScorer()
_synergy = SynergyScorer()
_tower = TowerSynergyScorer()
_versatility = VersatilityScorer()

# Weights from plan §4.6 — sourced from config.py
_WEIGHTS = config.WEIGHTS


class DeckScorer:
    """
    Aggregates all component scorers into a single total_score.
    Mutates deck.attack_score, defense_score, synergy_score,
    versatility_score, tower_synergy_score, total_score in place.
    """

    def score(self, deck: Deck) -> float:
        """Compute and cache all scores on *deck*. Returns total_score."""

        # ── Component scores ──────────────────────────────────────────────────
        atk  = _attack.score(deck)
        dfn  = _defense.score(deck)
        syn  = _synergy.score(deck)
        twr  = _tower.score(deck)
        vrs  = _versatility.score(deck, tower_synergy_score=twr)

        # ── Store on deck (all cached) ────────────────────────────────────────
        deck.attack_score         = atk
        deck.defense_score        = dfn
        deck.synergy_score        = syn
        deck.tower_synergy_score  = twr
        deck.versatility_score    = vrs

        # ── Weighted total (plan §4.6) ────────────────────────────────────────
        w = _WEIGHTS
        total = (
            atk * w["attack"] +
            dfn * w["defense"] +
            syn * w["synergy"] +
            vrs * w["versatility"]
        )

        # ── Ladder Viability Modifier (plan §10) ──────────────────────────────
        if getattr(config, "LADDER_MODE", False):
            level_penalty = sum(
                -5 for c in deck.cards if c.is_weak_underleveled
            )
            level_bonus = sum(
                +3 for c in deck.cards if c.is_level_independent
            )
            total += level_penalty + level_bonus

        # ── Clamp and cache total ─────────────────────────────────────────────
        total = max(0.0, min(100.0, total))
        deck.total_score = total
        return total

    def score_dict(self, deck: Deck) -> dict[str, float]:
        """Score deck and return all components as a named dict."""
        self.score(deck)
        return {
            "attack":        deck.attack_score,
            "defense":       deck.defense_score,
            "synergy":       deck.synergy_score,
            "tower_synergy": deck.tower_synergy_score,
            "versatility":   deck.versatility_score,
            "total":         deck.total_score,
        }


# Convenience singleton
_SCORER = DeckScorer()


def score_deck(deck: Deck) -> float:
    """Module-level helper. Scores deck in place and returns total_score."""
    return _SCORER.score(deck)


def score_deck_dict(deck: Deck) -> dict[str, float]:
    """Module-level helper returning full score breakdown."""
    return _SCORER.score_dict(deck)
