"""Figures for *Privatized Sovereignty*. Each reads the results dict and
writes one PNG.

Palette (CVD-checked in a prior validation; line styles and direct labels as
secondary encoding): amber, green, blue, warm gray; red reserved for harm.
"""
from __future__ import annotations

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

INK = "#1a1a1a"
GRID = "#d9d9d9"
AMBER = "#b45309"
GREEN = "#15803d"
BLUE = "#2563eb"
GRAY = "#57534e"
RED = "#b3202c"

ARCH_COLOR = {"sealed": RED, "reciprocal": BLUE, "custodial": GREEN,
              "vertical": AMBER, "network": GRAY}
ARCH_LABEL = {"sealed": "sealed wedge", "reciprocal": "reciprocal majority",
              "custodial": "state custodial", "vertical": "party vertical",
              "network": "network relational"}


def _style(ax) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(INK)
    ax.tick_params(colors=INK, labelsize=9)
    ax.grid(True, color=GRID, linewidth=0.6, alpha=0.7)
    ax.set_axisbelow(True)


def plot_lifecycle(res: dict, path: str) -> None:
    li = res["lifecycle"]
    ages = np.array(li["ages"], dtype=float)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.6, 3.8),
                                   gridspec_kw={"width_ratios": [1.25, 1]})
    # left: the insulation premium decays through the documented window
    k0 = li["constants"]["K0"]
    drag = li["constants"]["DRAG"]
    styles = {"fast": (GRAY, ":"), "median": (GRAY, "--"), "slow": (GRAY, "-.")}
    for name, (c, lsty) in styles.items():
        ts = li["types"][name]["t_star"]
        dec = li["types"][name]["decay"]
        d = k0 * np.exp(-dec * ages) - drag
        ax1.plot(ages, d, lsty, color=c, lw=1.1)
        ax1.annotate(name, (ages[-1], d[-1]), fontsize=7.5, color=GRAY,
                     xytext=(3, 0), textcoords="offset points", va="center")
    ax1.plot(ages, li["population_delta"], "-", color=BLUE, lw=2.0,
             label="population insulation premium")
    ax1.axhline(0, color=INK, lw=0.8)
    ax1.axvspan(6, 9, color=AMBER, alpha=0.12, lw=0)
    ax1.annotate("documented fade window", (7.5, 0.155), fontsize=7.5,
                 color=AMBER, ha="center")
    cx = li["population_crossover_years"]
    ax1.axvline(cx, color=BLUE, lw=0.8, ls=":")
    ax1.annotate(f"crossover {cx:.1f}y", (cx + 0.6, -0.113), fontsize=8,
                 color=BLUE)
    ax1.set_xlabel("firm age since IPO (years)", fontsize=9)
    ax1.set_ylabel("insulation premium (value-flow units)", fontsize=9)
    ax1.set_title("insulation premium by firm age",
                  fontsize=10, color=INK)
    ax1.legend(frameon=False, fontsize=8, loc="upper right")
    _style(ax1)
    # right: cumulative excess value by charter regime
    ex = li["population_excess_vs_single"]
    order = ["perpetual", "event", "hard", "renewable"]
    labels = ["perpetual\nwedge", "event\nsunset", "hard sunset\nat 7y",
              "renewable\nsunset"]
    colors = [RED, GRAY, BLUE, GREEN]
    vals = [ex[r] for r in order]
    bars = ax2.bar(range(len(order)), vals, color=colors, width=0.62)
    for i, v in enumerate(vals):
        ax2.annotate(f"{v:+.2f}", (i, v), fontsize=8.5, ha="center",
                     va="bottom" if v >= 0 else "top", color=INK,
                     xytext=(0, 3 if v >= 0 else -3),
                     textcoords="offset points")
    ax2.axhline(0, color=INK, lw=0.8)
    ax2.set_xticks(range(len(order)))
    ax2.set_xticklabels(labels, fontsize=8)
    ax2.set_ylabel("25-year value vs single class", fontsize=9)
    ax2.set_title("25-year value relative to single class", fontsize=10, color=INK)
    _style(ax2)
    fig.tight_layout()
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)


def plot_race(res: dict, path: str) -> None:
    ra = res["race"]
    y0 = ra["constants"]["YEAR0"]
    years = np.arange(len(ra["demand"])) + y0
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8.6, 5.6), sharex=True)
    # top: the documented shape
    ax1.plot(years, ra["demand"], "--", color=GRAY, lw=1.2,
             label="founder demand for the wedge")
    ax1.plot(years, ra["main"]["wedge_share"], "-", color=RED, lw=2.0,
             label="wedge share of new listings")
    ax1.axvspan(y0 + 62, y0 + 64, color=BLUE, alpha=0.15, lw=0)
    ax1.annotate("federal floor\n1988-90", (y0 + 63, 0.305), fontsize=7.5,
                 color=BLUE, ha="center")
    dc = ra["main"]["incumbent_defect_calendar"]
    ax1.axvline(dc, color=RED, lw=0.8, ls=":")
    ax1.annotate(f"incumbent defects {dc}", (dc - 1, 0.235), fontsize=8,
                 color=RED, ha="right")
    hk_yr = ra["main"]["hk_defect_calendar"]
    uk_yr = ra["main"]["uk_defect_calendar"]
    ax1.axvline(hk_yr, color=AMBER, lw=0.8, ls=":")
    ax1.annotate(f"HK {hk_yr}", (hk_yr - 1, 0.395), fontsize=7.5, color=AMBER,
                 ha="right")
    ax1.axvline(uk_yr, color=AMBER, lw=0.8, ls=":")
    ax1.annotate(f"UK {uk_yr}", (uk_yr + 1, 0.36), fontsize=7.5, color=AMBER,
                 ha="left")
    axd = ax1.twinx()
    axd.plot(years, ra["main"]["degree_mean"], "-", color=AMBER, lw=1.3)
    axd.set_ylabel("permissiveness degree (0-3)", fontsize=8.5, color=AMBER)
    axd.tick_params(colors=AMBER, labelsize=8)
    axd.spines["top"].set_visible(False)
    ax1.set_ylabel("share of new listings", fontsize=9)
    ax1.set_ylim(-0.01, 0.44)
    ax1.set_title("wedge share of new listings and permissiveness",
                  fontsize=10, color=INK)
    ax1.legend(frameon=False, fontsize=8, loc="upper left")
    _style(ax1)
    # bottom: counterfactuals
    ax2.plot(years, ra["main"]["wedge_share"], "-", color=RED, lw=1.2,
             alpha=0.4, label="history (above)")
    held = res["race"]
    ax2.plot(years, held["_held_share"], "-", color=GREEN, lw=1.8,
             label="floor never removed: domestic wedge stays zero")
    ax2.plot(years, held["_held_leakage"], "--", color=GREEN, lw=1.3,
             label="its price: listings leaking to outside venues")
    ax2.plot(years, held["_flat_share"], "-", color=BLUE, lw=1.4,
             label="demand never rises: holdout survives the century")
    ax2.set_ylabel("share of new listings", fontsize=9)
    ax2.set_xlabel("calendar year (model eras)", fontsize=9)
    ax2.set_ylim(-0.01, 0.42)
    ax2.set_title("counterfactuals: flat demand and a retained floor",
                  fontsize=10, color=INK)
    ax2.legend(frameon=False, fontsize=8, loc="upper left")
    _style(ax2)
    fig.tight_layout()
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)


def plot_correction(res: dict, path: str) -> None:
    co = res["correction"]
    g = co["grid"]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.6, 3.9),
                                   gridspec_kw={"width_ratios": [1.15, 1]})
    # left: normal-times growth vs failure-episode damage
    for name, v in g.items():
        ax1.scatter(v["normal_growth_15y"], v["mean_lost"],
                    s=90 + 700 * v["defeat_rate"], color=ARCH_COLOR[name],
                    alpha=0.85, edgecolors=INK, linewidths=0.6, zorder=3)
        dx, dy, ha = (7, 5, "left")
        if name == "network":
            dx, dy, ha = (9, -12, "left")
        if name == "reciprocal":
            dx, dy, ha = (9, 4, "left")
        if name == "custodial":
            dx, dy, ha = (-11, -4, "right")
        if name == "sealed":
            dx, dy, ha = (-12, -6, "right")
        ax1.annotate(f"{ARCH_LABEL[name]}\n(defeat {100 * v['defeat_rate']:.1f}%)",
                     (v["normal_growth_15y"], v["mean_lost"]), fontsize=7.5,
                     color=ARCH_COLOR[name], xytext=(dx, dy), ha=ha,
                     textcoords="offset points")
    ax1.set_xlabel("normal-times capability growth, 15 years", fontsize=9)
    ax1.set_ylabel("mean capability lost in a failure episode", fontsize=9)
    ax1.set_xlim(2.9, 4.85)
    ax1.set_ylim(0.4, 6.0)
    ax1.set_title("normal-times growth against loss per failure",
                  fontsize=10, color=INK)
    _style(ax1)
    # right: economic exposure as a correction channel
    sw = co["exposure_sweep"]
    a = [s["alpha"] for s in sw]
    lost = [s["mean_lost"] for s in sw]
    ax2.plot(a, lost, "-o", color=BLUE, lw=1.8, ms=4)
    en = res["lifecycle"]["entrenchment"]
    for label, alpha, dy in (("Ford family", en["ford_alpha"], -20),
                            ("SpaceX founder", en["spacex_alpha"], 8)):
        y_interp = float(np.interp(alpha, a, lost))
        ax2.scatter([alpha], [y_interp], color=RED, s=45, zorder=4,
                    edgecolors=INK, linewidths=0.5)
        ax2.annotate(f"{label} ({alpha:.2f})", (alpha, y_interp), fontsize=7.5,
                     color=RED, xytext=(6, dy), textcoords="offset points")
    ax2.set_xlabel("controller economic exposure (share of losses borne)",
                   fontsize=9)
    ax2.set_ylabel("mean capability lost", fontsize=9)
    ax2.set_title("loss per failure against controller exposure", fontsize=10, color=INK)
    _style(ax2)
    fig.tight_layout()
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)
