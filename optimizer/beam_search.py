"""
optimizer/beam_search.py
=========================
Beam Search Optimizer — Section 8, Stages 3 of final_hybrid_plan.md.

Algorithm (verbatim from plan):
  BEAM_WIDTH = 2000
  MAX_DEPTH  = 8

  For each depth d from 1 to 8:
      candidates = []
      For each state in current_beam:
          For each card in CANDIDATE_POOL not in state:
              if SlotValidator.can_add(card, state):
                  new_state = state + [card]
                  if d < 8:
                      partial_score = partial_deck_score(new_state, d, optimism_buffer=0.8)
                  else:
                      if not has_win_condition(new_state):  # HARD FINAL FILTER
                          skip
                      partial_score = full_deck_score(new_state)
                  candidates.append((partial_score, new_state))
      Sort candidates by score descending
      current_beam = top BEAM_WIDTH candidates

  Return top 3 unique valid complete decks from final beam.

Key fixes from plan:
  - WC check enforced as hard filter at depth=8 (not just pool guarantee)
  - optimism_buffer=0.8 applied by PartialScorer
"""

from __future__ import annotations

import config
from models.card import Card
from models.deck import Deck
from optimizer.constraint_checker import ConstraintChecker
from optimizer.partial_scorer import PartialScorer
from scoring.deck_scorer import DeckScorer


class BeamSearchOptimizer:
    """
    Beam search over the candidate pool to find the top N decks.

    Usage:
        bso = BeamSearchOptimizer(pool, tower_troop="princess")
        top_decks = bso.run(top_n=3)
    """

    def __init__(
        self,
        candidate_pool: list[Card],
        tower_troop: str = "princess",
        beam_width: int | None = None,
    ) -> None:
        self.pool         = candidate_pool
        self.tower_troop  = tower_troop
        self.beam_width   = beam_width or config.BEAM_WIDTH
        self._checker     = ConstraintChecker()
        self._partial     = PartialScorer()
        self._scorer      = DeckScorer()

    def run(self, top_n: int = 3) -> list[Deck]:
        """
        Execute beam search. Returns up to top_n complete, valid Deck objects,
        already fully scored (all component scores cached on each Deck).
        """
        # Beam state: list of (score, partial_card_list)
        beam: list[tuple[float, list[Card]]] = [(0.0, [])]

        for depth in range(1, 9):
            candidates: list[tuple[float, list[Card]]] = []

            for _, state in beam:
                state_ids = {c.id for c in state}

                for card in self.pool:
                    if card.id in state_ids:
                        continue
                    if not self._checker.can_add(card, state):
                        continue

                    new_state = state + [card]

                    if depth < 8:
                        score = self._partial.score(new_state, depth)
                    else:
                        # Hard WC filter at final depth (plan fix §8 Stage 3)
                        if not self._checker.has_win_condition(new_state):
                            continue
                        if not self._checker.is_complete_valid(new_state):
                            continue
                        # Full score
                        deck = Deck(cards=new_state, tower_troop=self.tower_troop)
                        score = self._scorer.score(deck)

                    candidates.append((score, new_state))

            if not candidates:
                break

            # Sort descending, keep top BEAM_WIDTH states
            candidates.sort(key=lambda x: x[0], reverse=True)
            beam = candidates[:self.beam_width]
            print(f"    Depth {depth}/8 — {len(beam)} states", flush=True)

        # ── Extract top N unique complete decks from final beam ───────────────
        results: list[Deck] = []
        seen_signatures: set[frozenset[str]] = set()

        for _, state in beam:
            if len(state) != 8:
                continue
            sig = frozenset(c.id for c in state)
            if sig in seen_signatures:
                continue
            seen_signatures.add(sig)

            deck = Deck(cards=state, tower_troop=self.tower_troop)
            self._scorer.score(deck)   # ensures all component scores cached
            results.append(deck)

            if len(results) >= top_n:
                break

        return results
