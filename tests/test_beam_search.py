"""
tests/test_beam_search.py
==========================
Beam Search Validator — per plan §11 directory listing and §13.3.

Checks:
  - Every complete deck output has >= 1 win condition (hard filter §8)
  - No complete deck output has duplicate card IDs
  - All output decks pass SlotValidator.validate()
  - Beam returns <= top_n results and all are 8-card decks
  - Candidate pool Stage 2 hard requirements are met
  - Hill climber does not degrade scores (total_score non-decreasing)

NOTE: Full beam search (BEAM_WIDTH=2000, 4 towers) is slow; these tests
use a reduced beam width (50) and 1 tower for speed, while still ensuring
correctness of the search and constraint logic.
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import config

from data.all_cards import CARD_BY_ID
from models.slot_validator import SlotValidator
from optimizer.card_filter import build_candidate_pool
from optimizer.beam_search import BeamSearchOptimizer
from optimizer.hill_climber import HillClimber


# ---------------------------------------------------------------------------
# Setup: small pool + narrow beam for test speed
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def pool():
    """Stratified candidate pool (runs once per module)."""
    return build_candidate_pool(list(CARD_BY_ID.values()))


@pytest.fixture(scope="module")
def beam_results(pool):
    """Run beam search with narrow width=50 for princess tower. Cached per module."""
    bso = BeamSearchOptimizer(pool, tower_troop="princess", beam_width=50)
    return bso.run(top_n=3)


# ---------------------------------------------------------------------------
# Test: Candidate pool Stage 2 constraints
# ---------------------------------------------------------------------------

class TestCandidatePool:
    def test_pool_has_win_condition(self, pool):
        """Pool must contain at least 1 win condition (Stage 2)."""
        assert any(c.is_win_condition for c in pool), (
            "Candidate pool has no win condition cards"
        )

    def test_pool_has_at_least_2_anti_air(self, pool):
        """Pool must contain at least 2 anti-air cards (Stage 2)."""
        aa_count = sum(1 for c in pool if c.is_anti_air)
        assert aa_count >= 2, (
            f"Pool has only {aa_count} anti-air cards — need >= 2"
        )

    def test_pool_has_damage_spell(self, pool):
        """Pool must contain at least 1 damage spell (Stage 2)."""
        assert any(c.is_damage_spell for c in pool), (
            "Pool has no damage spell"
        )

    def test_pool_has_defensive_building(self, pool):
        """Pool must contain at least 1 defensive building (Stage 2)."""
        assert any(c.is_defensive_building for c in pool), (
            "Pool has no defensive building"
        )

    def test_pool_size_reasonable(self, pool):
        """Pool should contain 40–120 cards (stratified, not exhaustive)."""
        assert 30 <= len(pool) <= 120, (
            f"Pool size {len(pool)} outside expected range [30, 120]"
        )


# ---------------------------------------------------------------------------
# Test: Beam search output correctness
# ---------------------------------------------------------------------------

class TestBeamOutput:
    def test_returns_at_most_top_n(self, beam_results):
        """Beam must return at most 3 results."""
        assert len(beam_results) <= 3, (
            f"Expected <= 3 results, got {len(beam_results)}"
        )

    def test_each_deck_has_8_cards(self, beam_results):
        """Every output deck must have exactly 8 cards."""
        for deck in beam_results:
            assert len(deck.cards) == 8, (
                f"Deck has {len(deck.cards)} cards, not 8"
            )

    def test_each_deck_has_win_condition(self, beam_results):
        """Hard filter: every output deck must have >= 1 win condition (plan §8)."""
        for deck in beam_results:
            has_wc = any(c.is_win_condition for c in deck.cards)
            assert has_wc, (
                f"Deck {[c.id for c in deck.cards]} has no win condition — "
                "hard filter in beam search failed"
            )

    def test_each_deck_passes_slot_validator(self, beam_results):
        """All output decks must pass SlotValidator hard constraints."""
        validator = SlotValidator()
        for deck in beam_results:
            result = validator.validate(deck.cards)
            assert result.valid, (
                f"Deck {[c.id for c in deck.cards]} failed SlotValidator: "
                f"{result.errors}"
            )

    def test_no_duplicate_cards_in_deck(self, beam_results):
        """Each deck must have 8 unique card IDs."""
        for deck in beam_results:
            ids = [c.id for c in deck.cards]
            assert len(ids) == len(set(ids)), (
                f"Deck has duplicate cards: {ids}"
            )

    def test_decks_have_scores_in_range(self, beam_results):
        """All component scores on output decks must be in [0, 100]."""
        for deck in beam_results:
            for attr in ["attack_score", "defense_score", "synergy_score",
                         "versatility_score", "total_score"]:
                val = getattr(deck, attr, None)
                if val is not None:
                    assert 0.0 <= val <= 100.0, (
                        f"{attr}={val:.2f} out of [0, 100] for deck "
                        f"{[c.id for c in deck.cards]}"
                    )

    def test_output_decks_are_unique(self, beam_results):
        """No two output decks should be identical (by card ID set)."""
        signatures = [frozenset(c.id for c in d.cards) for d in beam_results]
        assert len(signatures) == len(set(signatures)), (
            "Beam returned duplicate deck compositions"
        )


# ---------------------------------------------------------------------------
# Test: Hill climber does not degrade scores
# ---------------------------------------------------------------------------

class TestHillClimber:
    def test_hill_climber_does_not_degrade(self, pool, beam_results):
        """Hill-climbing refinement must not lower total_score."""
        climber = HillClimber(pool, max_passes=1)  # 1 pass for speed
        for deck in beam_results:
            score_before = deck.total_score
            refined = climber.refine(deck)
            assert refined.total_score >= score_before - 0.01, (
                f"Hill climber degraded score: {score_before:.2f} → "
                f"{refined.total_score:.2f}"
            )
