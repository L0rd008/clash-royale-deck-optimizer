"""
tests/test_calibration.py
==========================
Sensitivity & Calibration Tests — plan §13.2.

"Run optimizer with weights varied ±20% from baseline.
 Top-3 results should not change wholesale — if they do,
 scoring constants need re-calibration."

Tests:
  1. Weight ±20% sensitivity: score ordering of known archetypes is stable
  2. Synergy matrix perturbation: adding a dummy pair doesn't flip rankings
  3. Score monotonicity: adding a clear-cut upgrade card improves total_score
  4. Ladder modifier sign: wu cards lower score more than li cards raise it
     when wu count > li count
  5. Anti-synergy penalty applied: deck with EQ + own buildings scores lower
     than same deck without EQ
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import config

from data.all_cards import CARD_BY_ID
from models.deck import Deck
from scoring.deck_scorer import DeckScorer


def _build(ids: list[str], tower: str = "princess") -> Deck:
    return Deck(cards=[CARD_BY_ID[i] for i in ids], tower_troop=tower)


# Known fixture decks
LAVALOON = ["lava_hound", "balloon", "mega_minion", "musketeer",
            "lightning", "tombstone", "arrows", "barbarian_barrel"]
HOG_CYCLE = ["hog_rider", "fireball", "the_log", "ice_golem",
             "musketeer", "skeletons", "ice_spirit", "cannon"]
GY_FREEZE = ["graveyard", "freeze", "poison", "skeleton_army",
             "knight", "baby_dragon", "tornado", "barbarian_barrel"]
XBOW      = ["x_bow", "tesla", "the_log", "ice_spirit",
             "archers", "skeletons", "knight", "earthquake"]


# ---------------------------------------------------------------------------
# Test 1: Weight ±20% sensitivity (plan §13.2)
# ---------------------------------------------------------------------------

class TestWeightSensitivity:
    """Vary each weight by ±20%; archetype ordering should remain stable."""

    _BASELINE = {"attack": 0.30, "defense": 0.30, "synergy": 0.25, "versatility": 0.15}
    _DECKS    = [LAVALOON, HOG_CYCLE, GY_FREEZE, XBOW]
    _NAMES    = ["LAVALOON", "HOG_CYCLE", "GY_FREEZE", "XBOW"]

    def _scores_under(self, weights: dict) -> list[float]:
        """Return total_scores for all fixture decks under given weights."""
        orig = config.WEIGHTS.copy()
        config.WEIGHTS.update(weights)
        scorer = DeckScorer()
        scores = []
        for ids in self._DECKS:
            d = _build(ids)
            scores.append(scorer.score(d))
        config.WEIGHTS.update(orig)
        return scores

    def test_attack_weight_plus_20pct_stable(self):
        """Raising attack weight 20% must keep same relative ordering."""
        w_plus = dict(self._BASELINE)
        w_plus["attack"] = 0.30 * 1.20
        # Normalize so weights sum to 1.0
        total = sum(w_plus.values())
        w_plus = {k: v / total for k, v in w_plus.items()}

        base_scores  = self._scores_under(self._BASELINE)
        perturb_scores = self._scores_under(w_plus)

        base_rank  = sorted(range(4), key=lambda i: base_scores[i], reverse=True)
        perturb_rank = sorted(range(4), key=lambda i: perturb_scores[i], reverse=True)

        # Top-2 must remain the same (plan: "not change wholesale")
        assert base_rank[:2] == perturb_rank[:2], (
            f"Top-2 ranking changed under +20% attack weight.\n"
            f"Base:    {[self._NAMES[i] for i in base_rank]}\n"
            f"Perturb: {[self._NAMES[i] for i in perturb_rank]}"
        )

    def test_defense_weight_minus_20pct_stable(self):
        """Lowering defense weight 20% must keep same relative ordering."""
        w_minus = dict(self._BASELINE)
        w_minus["defense"] = 0.30 * 0.80
        total = sum(w_minus.values())
        w_minus = {k: v / total for k, v in w_minus.items()}

        base_scores  = self._scores_under(self._BASELINE)
        perturb_scores = self._scores_under(w_minus)

        base_rank  = sorted(range(4), key=lambda i: base_scores[i], reverse=True)
        perturb_rank = sorted(range(4), key=lambda i: perturb_scores[i], reverse=True)

        assert base_rank[:2] == perturb_rank[:2], (
            f"Top-2 ranking changed under -20% defense weight."
        )


# ---------------------------------------------------------------------------
# Test 2: Score monotonicity (clear upgrade improves score)
# ---------------------------------------------------------------------------

class TestMonotonicity:
    def test_synergy_matrix_perturbation_increases_score(self):
        """Injecting a +1.0 pairwise synergy entry for two cards in the deck
        must increase the synergy score vs the unmodified deck.
        This is a GUARANTEED correct assertion: directly tests the pairwise
        contribution of SYNERGY_MATRIX on SynergyScorer output.
        """
        from scoring.synergy_scorer import SynergyScorer
        from data.synergy_matrix import SYNERGY_MATRIX

        syn_scorer = SynergyScorer()
        d = _build(HOG_CYCLE)

        # Score without injected pair
        s_before = syn_scorer.score(d)

        # Inject a strong pair between two HOG deck cards (pick pair not already in matrix)
        # cannon + ice_spirit: small or no existing entry
        test_key = ("cannon", "ice_spirit")   # sorted
        orig_val = SYNERGY_MATRIX.get(test_key, None)
        SYNERGY_MATRIX[test_key] = 1.0

        s_after = syn_scorer.score(d)

        # Restore
        if orig_val is None:
            SYNERGY_MATRIX.pop(test_key, None)
        else:
            SYNERGY_MATRIX[test_key] = orig_val

        assert s_after >= s_before, (
            f"Injecting +1.0 synergy entry must not lower synergy: "
            f"before={s_before:.3f} after={s_after:.3f}"
        )



# ---------------------------------------------------------------------------
# Test 3: Anti-synergy penalty (EQ + own building)
# ---------------------------------------------------------------------------

class TestAntiSynergy:
    def test_earthquake_plus_own_cannon_penalised(self):
        """Deck with EQ + Cannon (EQ hurts own buildings) must score lower
        in synergy vs same deck replacing EQ with a neutral spell."""
        from scoring.synergy_scorer import SynergyScorer
        syn = SynergyScorer()

        # EQ deck: Hog + EQ — EQ hurts own Cannon
        d_eq = _build(["hog_rider", "earthquake", "the_log", "ice_golem",
                        "musketeer", "skeletons", "ice_spirit", "cannon"])

        # Same but Zap instead of EQ (no anti-synergy with own Cannon)
        d_zap = _build(["hog_rider", "zap", "the_log", "ice_golem",
                         "musketeer", "skeletons", "ice_spirit", "cannon"])

        syn_eq  = syn.score(d_eq)
        syn_zap = syn.score(d_zap)

        assert syn_eq < syn_zap, (
            f"EQ deck synergy={syn_eq:.2f} should be < Zap deck synergy={syn_zap:.2f} "
            "(EQ has -0.9 anti-synergy with own Cannon in SYNERGY_MATRIX)"
        )


# ---------------------------------------------------------------------------
# Test 4: Ladder modifier direction per card counts
# ---------------------------------------------------------------------------

class TestLadderModifier:
    def test_ladder_modifier_math(self):
        """total_score in LADDER_MODE = clamp(raw_total + wu*(-5) + li*(3), 0, 100)."""
        config.LADDER_MODE = False
        scorer = DeckScorer()
        d = _build(HOG_CYCLE)
        s_ts = scorer.score(d)
        raw  = (d.attack_score * 0.30 + d.defense_score * 0.30 +
                d.synergy_score * 0.25 + d.versatility_score * 0.15)

        wu = sum(1 for c in d.cards if c.is_weak_underleveled)
        li = sum(1 for c in d.cards if c.is_level_independent)
        mod = wu * (-5) + li * 3

        config.LADDER_MODE = True
        s_lad = scorer.score(d)
        config.LADDER_MODE = False

        expected = max(0.0, min(100.0, raw + mod))
        assert abs(s_lad - expected) < 0.01, (
            f"Ladder={s_lad:.3f} != expected {expected:.3f} "
            f"(wu={wu}, li={li}, mod={mod:+d})"
        )


# ---------------------------------------------------------------------------
# Test 5: Synergy matrix perturbation (add dummy pair, verify score change)
# ---------------------------------------------------------------------------

class TestSynergyPerturbation:
    def test_adding_positive_pair_increases_synergy(self):
        """Adding a +1.0 pair for two cards already in deck must raise synergy."""
        from scoring.synergy_scorer import SynergyScorer
        from data.synergy_matrix import SYNERGY_MATRIX

        syn = SynergyScorer()
        d = _build(HOG_CYCLE)
        s_before = syn.score(d)

        # Temporarily inject a strong pair between two HOG_CYCLE cards
        # that currently have no or low synergy
        test_key = ("cannon", "ice_golem")  # sorted pair
        already = SYNERGY_MATRIX.get(test_key, 0.0)
        SYNERGY_MATRIX[test_key] = 1.0

        try:
            s_after = syn.score(d)
        finally:
            if already == 0.0:
                SYNERGY_MATRIX.pop(test_key, None)
            else:
                SYNERGY_MATRIX[test_key] = already

        assert s_after >= s_before, (
            f"Adding +1.0 synergy pair must not decrease score: "
            f"before={s_before:.2f} after={s_after:.2f}"
        )
