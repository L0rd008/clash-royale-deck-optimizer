"""
optimizer/combo_cache.py
=========================
Combo Cache — Section 7 of final_hybrid_plan.md.

Pre-computes ComboScore for card subsets to speed up beam search evaluation.
Scope per plan §7.1:
  2-card combos: C(N,2) — always pre-computed
  3-card combos: C(N,3) — always pre-computed
  4-card combos: ONLY role-valid subsets (not all C(N,4))

Cache keyed by config.PATCH_VERSION — auto-invalidates when patch changes.
Stored at config.COMBO_CACHE_PATH (pickle).

ComboScore dataclass used for fast lookup during beam search.
"""

from __future__ import annotations
import pickle
import os
from itertools import combinations
from typing import Optional

import config
from models.card import Card
from models.combo_score import ComboScore
from data.synergy_matrix import SYNERGY_MATRIX


def _weights_hash() -> str:
    """Stable hash of config.WEIGHTS for cache invalidation."""
    import hashlib, json
    payload = json.dumps(config.WEIGHTS, sort_keys=True).encode()
    return hashlib.md5(payload).hexdigest()[:8]


# ---------------------------------------------------------------------------
# Role-valid subset filter for 4-card combos (plan §7.1)
# ---------------------------------------------------------------------------

def _is_role_valid_4(cards: tuple[Card, ...]) -> bool:
    """
    A 4-card subset is role-valid if:
    - At most 2 win conditions
    - At least 1 anti-air card in the partial
    """
    wc = sum(1 for c in cards if c.is_win_condition)
    aa = sum(1 for c in cards if c.is_anti_air)
    return wc <= 2 and aa >= 1


# ---------------------------------------------------------------------------
# ComboScore builder
# ---------------------------------------------------------------------------

def _build_combo_score(cards: tuple[Card, ...]) -> ComboScore:
    """Build a ComboScore from a tuple of cards (2, 3, or 4 cards)."""
    elixir_total = sum(c.cycle_elixir for c in cards)
    avg_elixir   = elixir_total / len(cards)

    roles: set[str] = set()
    for c in cards:
        for flag in [
            "is_win_condition", "is_damage_spell", "is_anti_air",
            "is_defensive_building", "is_investment", "is_tank",
            "is_support", "is_punishment", "is_bridge_spam",
            "is_splash", "is_king_activator", "is_bait_card",
        ]:
            if getattr(c, flag, False):
                roles.add(flag)

    synergy_sum = 0.0
    for c1, c2 in combinations(cards, 2):
        key = (c1.id, c2.id) if c1.id < c2.id else (c2.id, c1.id)
        synergy_sum += SYNERGY_MATRIX.get(key, 0.0)

    bait_chains: dict[str, int] = {}
    spell_ids = {c.id for c in cards if c.is_damage_spell}
    for spell_id in spell_ids:
        count = sum(1 for c in cards if spell_id in c.bait_spells)
        if count > 0:
            bait_chains[spell_id] = count

    king_act = any(c.is_king_activator for c in cards)
    has_wc   = any(c.is_win_condition  for c in cards)

    spell_ct = sum(c.ct_damage for c in cards if c.is_damage_spell)

    counter_wc:  set[str] = set()
    counter_def: set[str] = set()
    for c in cards:
        counter_wc.update(c.counters_win_conditions)
        counter_def.update(c.counters_defenders)

    # Attack contribution — scaled by config.WEIGHTS["attack"] to stay DRY
    #   35 pts if ≥1 WC,  up to 10 extra from WC strength,  up to 20 from CT damage
    #   All multiplied by the attack weight so cache heuristics track config changes.
    atk_w = config.WEIGHTS.get("attack", 0.30)
    atk = 0.0
    wc_count = sum(1 for c in cards if c.is_win_condition)
    atk += 35 * atk_w if wc_count >= 1 else 0
    atk += min(sum(c.win_condition_strength for c in cards) * 5, 10) * atk_w
    atk += min((spell_ct / 500.0) * 20.0, 20.0) * atk_w

    # Defense contribution — scaled by config.WEIGHTS["defense"]
    def_w = config.WEIGHTS.get("defense", 0.30)
    dfn  = 0.0
    aa   = sum(1 for c in cards if c.is_anti_air)
    dfn += (25 if aa >= 2 else (12 if aa == 1 else 0)) * def_w
    dfn += 20 * def_w if any(c.is_defensive_building for c in cards) else 0

    return ComboScore(
        card_ids=frozenset(c.id for c in cards),
        elixir_total=elixir_total,
        roles_covered=roles,
        synergy_sum=synergy_sum,
        bait_chains=bait_chains,
        king_activation_potential=king_act,
        has_win_condition=has_wc,
        avg_elixir=avg_elixir,
        spell_ct_damage_total=spell_ct,
        attack_contribution=atk,
        defense_contribution=dfn,
        counter_wc_coverage=counter_wc,
        counter_def_coverage=counter_def,
    )


# ---------------------------------------------------------------------------
# Cache management
# ---------------------------------------------------------------------------

class ComboCache:
    """
    Pre-computes and caches ComboScore for 2/3-card combos (all) and
    4-card combos (role-valid only) from a candidate pool.

    Usage:
        cache = ComboCache()
        cache.build(pool)
        cs = cache.get(card_a, card_b)   # returns ComboScore or None
    """

    def __init__(self) -> None:
        self._cache: dict[frozenset[str], ComboScore] = {}
        self._patch: str = ""

    def _cache_path(self) -> str:
        return os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            config.COMBO_CACHE_PATH,
        )

    def load_or_build(self, pool: list[Card]) -> None:
        """Load from disk if patch AND weights hash match; otherwise rebuild and save."""
        path = self._cache_path()
        if os.path.exists(path):
            try:
                with open(path, "rb") as f:
                    saved = pickle.load(f)
                if (saved.get("patch") == config.PATCH_VERSION
                        and saved.get("weights_hash") == _weights_hash()):
                    self._cache = saved["cache"]
                    self._patch = config.PATCH_VERSION
                    print(f"[ComboCache] Loaded {len(self._cache)} entries "
                          f"(patch={config.PATCH_VERSION}).")
                    return
            except Exception:
                pass
        self.build(pool)
        self._save()

    def build(self, pool: list[Card]) -> None:
        """Pre-compute combos from pool. Clears existing cache."""
        self._cache = {}
        self._patch = config.PATCH_VERSION
        n2, n3, n4 = 0, 0, 0

        # 2-card combos — all
        for pair in combinations(pool, 2):
            key = frozenset(c.id for c in pair)
            self._cache[key] = _build_combo_score(pair)
            n2 += 1

        # 3-card combos — all
        for trio in combinations(pool, 3):
            key = frozenset(c.id for c in trio)
            self._cache[key] = _build_combo_score(trio)
            n3 += 1

        # 4-card combos — role-valid only
        for quad in combinations(pool, 4):
            if _is_role_valid_4(quad):
                key = frozenset(c.id for c in quad)
                self._cache[key] = _build_combo_score(quad)
                n4 += 1

        print(f"[ComboCache] Built {n2} pairs + {n3} trios + {n4} quads "
              f"= {len(self._cache)} total (patch={self._patch}).")

    def get(self, *cards: Card) -> Optional[ComboScore]:
        """Look up pre-computed ComboScore for a set of 2–4 cards."""
        key = frozenset(c.id for c in cards)
        return self._cache.get(key)

    def _save(self) -> None:
        path = self._cache_path()
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as f:
            pickle.dump({
                "patch": self._patch,
                "weights_hash": _weights_hash(),
                "cache": self._cache,
            }, f)
        print(f"[ComboCache] Saved {len(self._cache)} entries → {path}")

