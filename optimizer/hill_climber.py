"""
optimizer/hill_climber.py
==========================
Hill-Climbing Refinement — Section 8, Stage 4 of final_hybrid_plan.md.

For each of the top-3 beam outputs:
  For each position i in deck (0–7):
      For each card c in CANDIDATE_POOL not in deck:
          if c can legally replace deck[i]:
              test_deck = deck with deck[i] replaced by c
              if full_deck_score(test_deck) > full_deck_score(deck):
                  deck = test_deck   # accept improvement
  Max 3 passes. Breaks out of local optima missed by beam search.
"""

from __future__ import annotations

import config
from models.card import Card
from models.deck import Deck
from models.slot_validator import SlotValidator
from scoring.deck_scorer import DeckScorer


class HillClimber:
    """
    Applies card-swap refinement to a scored Deck.
    Each pass tries swapping every card with every candidate pool card.
    """

    def __init__(
        self,
        candidate_pool: list[Card],
        max_passes: int | None = None,
    ) -> None:
        self.pool       = candidate_pool
        self.max_passes = max_passes or config.HILL_CLIMBER_PASSES
        self._scorer    = DeckScorer()
        self._validator = SlotValidator()

    def refine(self, deck: Deck) -> Deck:
        """
        Perform up to max_passes of 1-card swap refinement.
        Returns the (possibly improved) Deck with updated scores.
        """
        for _pass in range(self.max_passes):
            improved = False

            for i, card_to_replace in enumerate(deck.cards):
                remaining = [c for j, c in enumerate(deck.cards) if j != i]

                best_score = deck.total_score
                best_card  = None

                for candidate in self.pool:
                    # Skip if already in deck
                    if any(c.id == candidate.id for c in deck.cards):
                        continue
                    # Skip if same card being replaced
                    if candidate.id == card_to_replace.id:
                        continue
                    # Slot validity: can we legally form remaining + candidate?
                    test_cards = remaining + [candidate]
                    result = self._validator.validate(test_cards)
                    if not result.valid:
                        continue

                    # Must still have win condition after swap
                    if not any(c.is_win_condition for c in test_cards):
                        continue

                    test_deck = Deck(
                        cards=test_cards,
                        tower_troop=deck.tower_troop,
                    )
                    new_score = self._scorer.score(test_deck)

                    if new_score > best_score:
                        best_score = new_score
                        best_card  = candidate
                        # Keep test_deck for acceptance
                        best_deck  = test_deck

                if best_card is not None:
                    deck = best_deck
                    improved = True

            if not improved:
                break  # Converged — no more improvements found this pass

        return deck

    def refine_all(self, decks: list[Deck]) -> list[Deck]:
        """Apply refine() to each deck in a list. Returns refined decks sorted by score."""
        refined = [self.refine(d) for d in decks]
        return sorted(refined, key=lambda d: d.total_score, reverse=True)
