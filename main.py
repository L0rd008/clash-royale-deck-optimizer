"""
main.py
========
Clash Royale Deck Optimizer — entry point.

Modes
-----
  python main.py                         Run all 4 towers sequentially (default)
  python main.py --tower princess        Single tower → output/results_princess.json
  python main.py --merge                 Merge per-tower JSONs → output/top_decks.json

The --tower / --merge split powers GitHub Actions matrix jobs:
  Each tower job runs independently, uploads results_{tower}.json as an artifact.
  A final merge job downloads all 4 and runs --merge.
"""

from __future__ import annotations
import argparse
import json
import os
import sys
import time

_ROOT = os.path.dirname(os.path.abspath(__file__))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

import config
from data.all_cards import CARD_BY_ID
from optimizer.card_filter  import build_candidate_pool
from optimizer.combo_cache  import ComboCache
from optimizer.beam_search  import BeamSearchOptimizer
from optimizer.hill_climber import HillClimber
from analysis.deck_report   import generate_reports
from models.deck import Deck
from scoring.deck_scorer import DeckScorer


# ── Single-tower mode ─────────────────────────────────────────────────────────

def run_tower(tower: str) -> None:
    """Run beam search + hill climbing for one tower, write results_{tower}.json."""
    t0 = time.perf_counter()
    all_cards = list(CARD_BY_ID.values())

    print(f"[{tower}] {len(all_cards)} cards  |  beam={config.BEAM_WIDTH:,}  "
          f"optimism={config.OPTIMISM_BUFFER}  passes={config.HILL_CLIMBER_PASSES}")

    pool = build_candidate_pool(all_cards)
    print(f"[{tower}] Pool: {len(pool)} cards")

    cache = ComboCache()
    cache.load_or_build(pool)

    top_n = getattr(config, "TOP_N_PER_TOWER", config.TOP_N_DECKS)
    bso   = BeamSearchOptimizer(pool, tower_troop=tower)
    beam_results = bso.run(top_n=top_n)
    print(f"[{tower}] Beam: {len(beam_results)} candidates")

    climber = HillClimber(pool)
    refined = climber.refine_all(beam_results)
    if refined:
        print(f"[{tower}] Best: {refined[0].total_score:.2f}")

    raw = [
        {"tower": tower, "score": d.total_score, "card_ids": [c.id for c in d.cards]}
        for d in refined
    ]
    out_dir  = os.path.join(_ROOT, "output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"results_{tower}.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(raw, f, indent=2)
    print(f"[{tower}] Done in {time.perf_counter()-t0:.1f}s  →  {out_path}")


# ── Merge mode ────────────────────────────────────────────────────────────────

def merge_results() -> None:
    """Merge all results_{tower}.json files → top_decks.json."""
    out_dir  = os.path.join(_ROOT, "output")
    all_raw: list[dict] = []
    for tower in config.TOWER_TROOPS:
        path = os.path.join(out_dir, f"results_{tower}.json")
        if not os.path.exists(path):
            print(f"[Merge] WARNING: {path} missing, skipping {tower}")
            continue
        with open(path, encoding="utf-8") as f:
            all_raw.extend(json.load(f))
        print(f"[Merge] Loaded results_{tower}.json")

    if not all_raw:
        print("[Merge] ERROR: no result files found.")
        return

    # Deduplicate + top N
    seen: set[frozenset[str]] = set()
    unique: list[dict] = []
    for entry in sorted(all_raw, key=lambda x: x["score"], reverse=True):
        sig = frozenset(entry["card_ids"])
        if sig not in seen:
            seen.add(sig)
            unique.append(entry)
        if len(unique) >= config.TOP_N_DECKS:
            break

    # Reconstruct + score
    scorer    = DeckScorer()
    top_decks = []
    for entry in unique:
        deck = Deck(
            cards=[CARD_BY_ID[cid] for cid in entry["card_ids"]],
            tower_troop=entry["tower"],
        )
        scorer.score(deck)
        top_decks.append(deck)

    reports  = generate_reports(top_decks)
    out_path = os.path.join(out_dir, "top_decks.json")
    os.makedirs(out_dir, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(reports, f, indent=2, ensure_ascii=False)

    print(f"\n{'='*60}")
    print(f"  TOP {len(reports)} DECKS  (Q1 2026 · {config.PATCH_VERSION})")
    print(f"{'='*60}")
    for r in reports:
        cards_str = ", ".join(c["name"] for c in r["cards"])
        cs = r["component_scores"]
        print(f"  #{r['rank']} [{r['tower_troop']}] Score={r['total_score']:.1f}  "
              f"Atk={cs['attack']:.0f}  Def={cs['defense']:.0f}  Syn={cs['synergy']:.0f}")
        print(f"       {cards_str}")
        cycle = r["cycle_analysis"]
        ctr   = r["counter_analysis"]
        print(f"       avg={cycle['avg_elixir']}e  "
              f"counter={ctr['counter_total']:.0f}/100  "
              f"bait={r['bait_analysis']['bait_score']:.0f}")
        print()
    print(f"  Written to: {out_path}")


# ── All-towers sequential (local default) ─────────────────────────────────────

def run_all_sequential() -> None:
    t0 = time.perf_counter()
    all_cards = list(CARD_BY_ID.values())

    print(f"[Main] {len(all_cards)} cards  patch={config.PATCH_VERSION}")
    print(f"[Main] beam={config.BEAM_WIDTH:,}  optimism={config.OPTIMISM_BUFFER}  "
          f"passes={config.HILL_CLIMBER_PASSES}\n")

    pool = build_candidate_pool(all_cards)
    print(f"[Main] Pool: {len(pool)} cards\n")
    cache = ComboCache()
    cache.load_or_build(pool)
    print()

    top_n   = getattr(config, "TOP_N_PER_TOWER", config.TOP_N_DECKS)
    out_dir = os.path.join(_ROOT, "output")
    os.makedirs(out_dir, exist_ok=True)

    for tower in config.TOWER_TROOPS:
        t_t = time.perf_counter()
        print(f"── Tower: {tower} " + "─" * 44)
        bso     = BeamSearchOptimizer(pool, tower_troop=tower)
        results = bso.run(top_n=top_n)
        print(f"  Beam: {len(results)} candidates")
        refined = HillClimber(pool).refine_all(results)
        best    = refined[0].total_score if refined else 0.0
        print(f"  HC done — best={best:.2f}  ({time.perf_counter()-t_t:.1f}s)\n")

        raw = [{"tower": tower, "score": d.total_score,
                "card_ids": [c.id for c in d.cards]} for d in refined]
        with open(os.path.join(out_dir, f"results_{tower}.json"), "w") as f:
            json.dump(raw, f, indent=2)

    merge_results()
    print(f"\n  Total: {time.perf_counter()-t0:.2f}s")


# ── Entry point ───────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="Clash Royale Deck Optimizer")
    group  = parser.add_mutually_exclusive_group()
    group.add_argument("--tower", choices=config.TOWER_TROOPS,
                       help="Single tower → output/results_{tower}.json")
    group.add_argument("--merge", action="store_true",
                       help="Merge all per-tower JSONs → output/top_decks.json")
    args = parser.parse_args()

    if args.tower:
        run_tower(args.tower)
    elif args.merge:
        merge_results()
    else:
        run_all_sequential()


if __name__ == "__main__":
    main()
