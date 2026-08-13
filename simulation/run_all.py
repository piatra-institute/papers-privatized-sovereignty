"""Orchestrator: reproduces every number and all three figures in the paper.

    cd simulation
    uv run run_all.py

Writes output/results.json and output/figures/*.png. Mechanisms 1 and 2 are
expected-value arithmetic; mechanism 3 runs on a recorded seed, so a rerun
reproduces every number bit for bit. A failed invariant fails the run.
"""
from __future__ import annotations

import json
from pathlib import Path

from analyses import run

OUT = Path(__file__).parent / "output"


def main() -> None:
    (OUT / "figures").mkdir(parents=True, exist_ok=True)
    results = run()
    (OUT / "results.json").write_text(json.dumps(results, indent=2))

    from figures import plot_lifecycle, plot_race, plot_correction
    plot_lifecycle(results, str(OUT / "figures" / "lifecycle.png"))
    plot_race(results, str(OUT / "figures" / "race.png"))
    plot_correction(results, str(OUT / "figures" / "correction.png"))

    li = results["lifecycle"]
    ex = li["population_excess_vs_single"]
    print(f"lifecycle: crossover {li['population_crossover_years']:.2f}y; "
          f"excess vs single-class: perpetual {ex['perpetual']:.3f}, "
          f"event {ex['event']:.3f}, hard {ex['hard']:.3f}, "
          f"renewable {ex['renewable']:.3f}")
    en = li["entrenchment"]
    print(f"  entrenchment threshold alpha* {en['alpha_star']:.3f}; "
          f"ford alpha {en['ford_alpha']:.3f} (keeps: {en['ford_keeps']}), "
          f"spacex alpha {en['spacex_alpha']:.3f} (keeps: {en['spacex_keeps']})")
    ra = results["race"]
    print(f"race: holdout {ra['holdout_years']}y "
          f"(defects {ra['main']['incumbent_defect_calendar']}), "
          f"lag after demand rise {ra['defection_lag_after_demand_rise']}y, "
          f"cascade {ra['cascade_lag_years']}y; hk {ra['main']['hk_defect_calendar']}, "
          f"uk {ra['main']['uk_defect_calendar']}; final share "
          f"{ra['final_wedge_share']:.2f}, degree {ra['final_degree_mean']:.1f}")
    print(f"  floor held: domestic {ra['floor_held']['domestic_share_final']:.2f}, "
          f"leakage/demand {ra['floor_held']['leakage_over_demand']:.2f}")
    co = results["correction"]
    for a, v in co["grid"].items():
        print(f"  {a}: lost {v['mean_lost']:.2f}, years {v['mean_years']:.1f}, "
              f"defeat {v['defeat_rate']:.3f}, normal15y {v['normal_growth_15y']:.2f}")
    cr = co["sealed_counterfactual_reduction"]
    print(f"  sealed counterfactuals: reporting {cr['free_reporting']:.2f}, "
          f"removability {cr['removability']:.2f}, both {cr['both']:.2f}")
    print("checks:", f"{sum(results['checks'].values())}/{len(results['checks'])}")
    print("wrote", OUT / "results.json")


if __name__ == "__main__":
    main()
