"""Three mechanisms of privatized sovereignty.

1. The lifecycle of the wedge: founder-specific knowledge decays while the
   private benefits of control persist, so insulation from the market is
   worth most exactly when the firm is young. Charter regimes (perpetual,
   hard sunset, event sunset, renewable sunset, single class) are priced on
   the same firm population, and the self-financing entrenchment threshold
   is computed: the economic stake below which a rational controller keeps
   value-destroying control.

2. The race in listing standards: exchanges compete for scarce founders;
   listing revenue is private to the venue and the governance cost is
   diffuse. The model must reproduce the documented shape: decades of
   stable restriction while founder demand for insulation is low, a fast
   cascade once demand rises and one venue defects, a coordinated floor
   that holds until removed, and a one-way ratchet in permissiveness after
   the cascade completes.

3. Correction capacity under five control architectures: one organization,
   one controller whose quality can fail, one stock of inherited capability
   that conceals the failure while it lasts. Architectures differ in
   reporting fidelity, removability, and the controller's economic
   exposure: sealed wedge, reciprocal majority owner, state custodial,
   party vertical, network relational.

Calibration is structural except where anchored to cited records (the 2026
filings, the six-to-nine-year premium window); anchors live in
results.json as cited_record entries. Mechanisms 1 and 2 are expected-value
arithmetic; mechanism 3 runs on a recorded seed. Invariants fail the run.
"""
from __future__ import annotations

import math

import numpy as np

# ----------------------------------------------------------------------
# shared
# ----------------------------------------------------------------------

SEED = 20260813


def _py(x):
    """Recursively convert numpy scalars/arrays for json.dumps."""
    if isinstance(x, dict):
        return {k: _py(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_py(v) for v in x]
    if isinstance(x, (np.floating,)):
        return round(float(x), 6)
    if isinstance(x, (np.integer,)):
        return int(x)
    if isinstance(x, np.ndarray):
        return [_py(v) for v in x.tolist()]
    if isinstance(x, float):
        return round(x, 6)
    return x


# ----------------------------------------------------------------------
# mechanism 1: the lifecycle of the wedge
# ----------------------------------------------------------------------

BASE = 1.0          # baseline annual value flow of the firm
K0 = 0.30           # founder advantage at IPO (value-flow units)
B_DIST = 0.05       # distortion cost of private-benefit extraction while insulated
M_NET = 0.07        # net value of market governance (discipline minus myopia)
DRAG = B_DIST + M_NET   # what the founder's advantage must beat: 0.12
B_PRIV = 0.05       # private-benefit flow to the controller while in control
HORIZON = 25
SUNSET_YEAR = 7     # the hard sunset (the exchange-petition number)
RENEWAL_YEARS = (7, 12, 17, 22)
RENEW_BAR = 0.01    # a renewal vote demands a demonstrated advantage
EVENT_HAZARD = 0.05  # annual founder-departure hazard (mean tenure 20 years)

# firm types: crossover targets in years; decay solved per type so that
# k(t*) = DRAG.  weights sum to 1.
FIRM_TYPES = {
    "fast":   {"t_star": 4.0,  "weight": 0.30},
    "median": {"t_star": 7.5,  "weight": 0.40},
    "slow":   {"t_star": 12.0, "weight": 0.30},
}


def _decay(t_star: float) -> float:
    return math.log(K0 / DRAG) / t_star


def _k(t: float, t_star: float) -> float:
    return K0 * math.exp(-_decay(t_star) * t)


def _delta(t: float, t_star: float) -> float:
    """Insulation premium at age t: insulated flow minus market flow."""
    return _k(t, t_star) - DRAG


def _insulated_years_renewable(t_star: float) -> float:
    """Renewable sunset: insulated until the first renewal date at which the
    unaffiliated no longer see a demonstrated advantage."""
    end = HORIZON
    for y in RENEWAL_YEARS:
        if not _delta(y, t_star) > RENEW_BAR:
            end = y
            break
    return end


def _cum_value(t_star: float, insulated_until) -> float:
    """Cumulative 25-year value; insulated_until is a year or a callable
    giving the probability of still being insulated at year t."""
    total = 0.0
    for t in range(HORIZON):
        if callable(insulated_until):
            p = insulated_until(t)
        else:
            p = 1.0 if t < insulated_until else 0.0
        ins = BASE + _k(t, t_star) - B_DIST
        mkt = BASE + M_NET
        total += p * ins + (1 - p) * mkt
    return total


def run_lifecycle() -> dict:
    types = {}
    for name, spec in FIRM_TYPES.items():
        ts = spec["t_star"]
        renew_end = _insulated_years_renewable(ts)
        types[name] = {
            "t_star": ts,
            "weight": spec["weight"],
            "decay": _decay(ts),
            "delta_ipo": _delta(0.0, ts),
            "renewable_insulated_until": renew_end,
            "cum": {
                "single":    _cum_value(ts, 0),
                "perpetual": _cum_value(ts, HORIZON),
                "hard":      _cum_value(ts, SUNSET_YEAR),
                "renewable": _cum_value(ts, renew_end),
                "event":     _cum_value(ts, lambda t: (1 - EVENT_HAZARD) ** t),
            },
        }

    # population curves and cumulative values
    ages = list(range(HORIZON + 1))
    pop_delta = [sum(s["weight"] * _delta(t, s["t_star"])
                     for s in FIRM_TYPES.values()) for t in ages]
    # population crossover by bisection on the smooth curve
    lo, hi = 0.0, float(HORIZON)
    for _ in range(80):
        mid = (lo + hi) / 2
        d = sum(s["weight"] * _delta(mid, s["t_star"]) for s in FIRM_TYPES.values())
        if d > 0:
            lo = mid
        else:
            hi = mid
    crossover = (lo + hi) / 2

    regimes = ["single", "perpetual", "hard", "renewable", "event"]
    pop_cum = {r: sum(types[n]["cum"][r] * FIRM_TYPES[n]["weight"]
                      for n in FIRM_TYPES) for r in regimes}
    single = pop_cum["single"]
    pop_excess = {r: pop_cum[r] - single for r in regimes}

    # self-financing entrenchment: a controller with economic stake alpha
    # keeps control at age t iff B_PRIV > alpha * (-delta(t)); in the mature
    # limit -delta -> DRAG, so the threshold stake is B_PRIV / DRAG.
    alpha_star = B_PRIV / DRAG
    ford_alpha = 70852076 / (3940230185 + 70852076)
    spacex_alpha = (849494440 + 5219053075) / (7696293669 + 5485486276)
    entrench = {
        "alpha_star": alpha_star,
        "ford_alpha": ford_alpha,
        "ford_keeps": ford_alpha < alpha_star,
        "ford_benefit_to_exposure": B_PRIV / (ford_alpha * DRAG),
        "spacex_alpha": spacex_alpha,
        "spacex_keeps": spacex_alpha < alpha_star,
        "spacex_margin": spacex_alpha - alpha_star,
    }

    return {
        "constants": {
            "BASE": BASE, "K0": K0, "B_DIST": B_DIST, "M_NET": M_NET,
            "DRAG": DRAG, "B_PRIV": B_PRIV, "HORIZON": HORIZON,
            "SUNSET_YEAR": SUNSET_YEAR, "RENEWAL_YEARS": list(RENEWAL_YEARS),
            "RENEW_BAR": RENEW_BAR,
            "EVENT_HAZARD": EVENT_HAZARD,
        },
        "types": types,
        "ages": ages,
        "population_delta": pop_delta,
        "population_crossover_years": crossover,
        "population_cum": pop_cum,
        "population_excess_vs_single": pop_excess,
        "perpetual_value_destroyed": -pop_excess["perpetual"],
        "entrenchment": entrench,
    }


# ----------------------------------------------------------------------
# mechanism 2: the race in listing standards
# ----------------------------------------------------------------------

YEARS = 105                 # model years 0..104, calendar 1926 + y
YEAR0 = 1926
N_LIST = 100.0              # new listings per year (all venues combined)
W_MAX = 0.6                 # founder insulation value W ~ Uniform(0, W_MAX)
GAP_DOM = 0.25              # incumbent prestige premium over the domestic rival
GAP_INT = 0.35              # home prestige premium over a foreign venue
DEFECT_WINDOW = 10          # rolling years over which a venue counts its losses
DEFECT_THRESHOLD = 41.0     # listings lost per window that trigger defection
DEFECT_THRESHOLD_INTL = 25.0  # thinner-margin venues defect at smaller losses
FLOOR_START, FLOOR_END = 62, 64     # 1988-1990: the federal floor
INTL_START = 84             # 2010: founders become internationally mobile
MOBILE_FRAC = 0.25          # wedge-demanders willing to list abroad
DEGREE_MAX = 3              # permissiveness notches: 0 none, 1 10:1+sunset,
                            # 2 10:1 no sunset, 3 20:1 no sunset
D_LOW = 0.04                # wedge demand among founders, base era
D_MID = 0.15                # after the venture era's first rise
D_HIGH = 0.35               # after the intangible era's second rise
DEMAND_RISE = 54            # 1980: the venture era begins
DEMAND_MID_AT = 64          # 1990: first rise complete
DEMAND_RISE2 = 84           # 2010: the intangible era begins
DEMAND_HIGH_AT = 95         # 2021: second rise complete


def _demand(y: int) -> float:
    """Fraction of new listings whose founders demand a wedge.
    Piecewise linear across three documented eras."""
    if y < DEMAND_RISE:
        return D_LOW
    if y < DEMAND_MID_AT:
        f = (y - DEMAND_RISE) / (DEMAND_MID_AT - DEMAND_RISE)
        return D_LOW + f * (D_MID - D_LOW)
    if y < DEMAND_RISE2:
        return D_MID
    if y < DEMAND_HIGH_AT:
        f = (y - DEMAND_RISE2) / (DEMAND_HIGH_AT - DEMAND_RISE2)
        return D_MID + f * (D_HIGH - D_MID)
    return D_HIGH


def _frac_above(threshold: float) -> float:
    """P(W > threshold) for W ~ Uniform(0, W_MAX)."""
    return max(0.0, 1.0 - threshold / W_MAX)


def _race(demand_fn, floor_years=None, floor_removed=True) -> dict:
    """One run of the standards race. Returns per-year series and events."""
    floor_years = floor_years if floor_years is not None else set(
        range(FLOOR_START, FLOOR_END))
    inc_permissive = False
    inc_defect_year = None
    losses = []                      # incumbent's rolling annual losses
    uk_permissive, hk_permissive = False, False
    uk_year, hk_year = None, None
    uk_losses, hk_losses = [], []
    degree = {"inc": 0, "uk": 0, "hk": 0}
    degree_series = []
    wedge_share = []
    leakage = []                     # listings leaving the coordinated zone
    for y in range(YEARS):
        d = demand_fn(y)
        floor_active = (y in floor_years) or (
            not floor_removed and y >= FLOOR_START)
        # -- domestic era: wedge-demanders defect to the permissive rival
        #    when their insulation value exceeds the prestige gap.
        if floor_active:
            share = 0.0
            lost = 0.0
            leak = N_LIST * d * _frac_above(GAP_INT) * (
                MOBILE_FRAC if y >= INTL_START else 0.0)
        elif not inc_permissive:
            lost = N_LIST * d * _frac_above(GAP_DOM)
            share = lost / N_LIST
            leak = 0.0
        else:
            share = d
            lost = 0.0
            leak = 0.0
        losses.append(lost)
        if (not inc_permissive and not floor_active
                and sum(losses[-DEFECT_WINDOW:]) >= DEFECT_THRESHOLD):
            inc_permissive = True
            inc_defect_year = y
            share = d
        # -- international era: restrictive jurisdictions lose mobile
        #    wedge-demanders to permissive ones.
        if y >= INTL_START and inc_permissive and not floor_active:
            intl_loss = N_LIST * d * MOBILE_FRAC * _frac_above(GAP_INT)
            for name, permissive, ls in (("hk", hk_permissive, hk_losses),
                                         ("uk", uk_permissive, uk_losses)):
                if not permissive:
                    ls.append(intl_loss * (1.0 if name == "hk" else 0.8))
            if not hk_permissive and sum(hk_losses[-DEFECT_WINDOW:]) >= DEFECT_THRESHOLD_INTL:
                hk_permissive, hk_year = True, y
            if not uk_permissive and sum(uk_losses[-DEFECT_WINDOW:]) >= DEFECT_THRESHOLD_INTL:
                uk_permissive, uk_year = True, y
        # -- degree ratchet: once every venue is permissive, each venue
        #    escalates one notch per year while below the frontier; nothing
        #    ever de-escalates.
        if inc_permissive and hk_permissive and uk_permissive and not floor_active:
            for v in degree:
                if degree[v] < DEGREE_MAX:
                    degree[v] += 1
        degree_series.append(sum(degree.values()) / 3.0)
        wedge_share.append(share)
        leakage.append(leak / N_LIST)
    return {
        "incumbent_defect_year": inc_defect_year,
        "incumbent_defect_calendar": None if inc_defect_year is None
            else YEAR0 + inc_defect_year,
        "hk_defect_calendar": None if hk_year is None else YEAR0 + hk_year,
        "uk_defect_calendar": None if uk_year is None else YEAR0 + uk_year,
        "wedge_share": wedge_share,
        "degree_mean": degree_series,
        "leakage": leakage,
    }


def run_race() -> dict:
    main = _race(_demand)
    flat = _race(lambda y: D_LOW)                       # demand never rises
    held = _race(_demand, floor_removed=False)          # floor never removed

    demand_path = [_demand(y) for y in range(YEARS)]
    defect = main["incumbent_defect_year"]
    share = main["wedge_share"]
    cascade_lag = next((i for i in range(0, YEARS - defect)
                        if share[defect + i] >= 0.9 * demand_path[defect + i]), None)
    floor_share = [share[y] for y in range(FLOOR_START, FLOOR_END)]
    post_floor = share[FLOOR_END + 1]

    held_leak_final = held["leakage"][-1]
    held_leak_vs_demand = held_leak_final / demand_path[-1]

    return {
        "constants": {
            "YEARS": YEARS, "YEAR0": YEAR0, "W_MAX": W_MAX,
            "GAP_DOM": GAP_DOM, "GAP_INT": GAP_INT,
            "DEFECT_WINDOW": DEFECT_WINDOW,
            "DEFECT_THRESHOLD": DEFECT_THRESHOLD,
            "DEFECT_THRESHOLD_INTL": DEFECT_THRESHOLD_INTL,
            "MOBILE_FRAC": MOBILE_FRAC, "D_LOW": D_LOW, "D_MID": D_MID,
            "D_HIGH": D_HIGH,
        },
        "demand": demand_path,
        "main": main,
        "holdout_years": defect,
        "demand_rise_year": DEMAND_RISE,
        "defection_lag_after_demand_rise": defect - DEMAND_RISE,
        "cascade_lag_years": cascade_lag,
        "floor_share": floor_share,
        "post_floor_share": post_floor,
        "final_wedge_share": share[-1],
        "final_degree_mean": main["degree_mean"][-1],
        "degree_monotone": all(b >= a for a, b in
                               zip(main["degree_mean"], main["degree_mean"][1:])),
        "flat_demand_defected": flat["incumbent_defect_year"] is not None,
        "floor_held": {
            "domestic_share_final": held["wedge_share"][-1],
            "leakage_final": held_leak_final,
            "leakage_over_demand": held_leak_vs_demand,
        },
        "_held_share": held["wedge_share"],
        "_held_leakage": held["leakage"],
        "_flat_share": flat["wedge_share"],
    }


# ----------------------------------------------------------------------
# mechanism 3: correction capacity under five architectures
# ----------------------------------------------------------------------

S0 = 10.0
S_CAP = 12.0
S_VIS = 6.0        # output visibly degrades below this: external detection
S_DEAD = 2.0       # irrecoverable: defeat without an external enemy
GROW = 0.25        # capability growth under a good controller
GROW_SEALED = 0.30  # the insulation premium while the controller is good
DAMAGE = 0.8       # capability loss per year under a failed controller
SELF_MAX = 0.5     # self-correction rate at full economic exposure
EPISODES = 4000
MAX_YEARS = 40
CHURN_COST = 0.5   # capability lost per false-positive removal (vertical)

ARCHITECTURES = {
    # phi: reporting fidelity that reaches the removal institution
    # rho: removal probability per year once detected
    # alpha: controller economic exposure (drives self-correction)
    # drift: damage multiplier (network consensus dampens extremes)
    "sealed":     {"phi": 0.50, "suppress": 0.80, "rho": 0.06, "alpha": 0.10,
                   "drift": 1.0},
    "reciprocal": {"phi": 0.35, "suppress": 0.00, "rho": 0.18, "alpha": 0.60,
                   "drift": 1.0},
    "custodial":  {"phi": 0.65, "suppress": 0.00, "rho": 0.65, "alpha": 0.30,
                   "drift": 1.0, "elite_closure": 0.15,
                   "closed_phi": 0.10, "closed_rho": 0.30},
    "vertical":   {"phi": 0.12, "suppress": 0.00, "rho": 0.92, "alpha": 0.05,
                   "drift": 1.0, "false_positive": 0.06},
    "network":    {"phi": 0.50, "suppress": 0.00, "rho": 0.02, "alpha": 0.03,
                   "drift": 0.5, "reform_from": 15, "reform_rate": 0.10},
}


def _episode(rng, spec, override=None) -> dict:
    p = dict(spec)
    if override:
        p.update(override)
    phi = p["phi"] * (1 - p["suppress"])
    rho, alpha, drift = p["rho"], p["alpha"], p["drift"]
    if "elite_closure" in p and rng.random() < p["elite_closure"]:
        phi, rho = p["closed_phi"], p["closed_rho"]
        closed = True
    else:
        closed = False
    fail_year = int(rng.integers(2, 7))
    S = S0
    detected = False
    detect_year = None
    detect_channel = None
    for t in range(MAX_YEARS):
        if t < fail_year:
            S = min(S_CAP, S + GROW)
            continue
        # failed controller in place
        S -= DAMAGE * drift
        if S <= S_DEAD:
            return {"years": t - fail_year + 1, "lost": S0 - S_DEAD,
                    "defeat": True, "channel": detect_channel or "none",
                    "detect_lag": None if detect_year is None
                    else detect_year - fail_year, "closed": closed,
                    "corrected_by": "none"}
        if not detected:
            if S < S_VIS:
                detected, detect_year, detect_channel = True, t, "external"
            elif rng.random() < phi:
                detected, detect_year, detect_channel = True, t, "internal"
        if rng.random() < SELF_MAX * alpha:
            return {"years": t - fail_year + 1, "lost": max(0.0, S0 - S),
                    "defeat": False, "channel": detect_channel or "self",
                    "detect_lag": None if detect_year is None
                    else detect_year - fail_year, "closed": closed,
                    "corrected_by": "self"}
        if detected and rng.random() < rho:
            return {"years": t - fail_year + 1, "lost": max(0.0, S0 - S),
                    "defeat": False, "channel": detect_channel,
                    "detect_lag": detect_year - fail_year, "closed": closed,
                    "corrected_by": "removal"}
        if ("reform_from" in p and t >= p["reform_from"]
                and rng.random() < p["reform_rate"]):
            return {"years": t - fail_year + 1, "lost": max(0.0, S0 - S),
                    "defeat": False, "channel": detect_channel or "reform",
                    "detect_lag": None if detect_year is None
                    else detect_year - fail_year, "closed": closed,
                    "corrected_by": "reform"}
    return {"years": MAX_YEARS - fail_year, "lost": max(0.0, S0 - S),
            "defeat": S <= S_DEAD, "channel": detect_channel or "none",
            "detect_lag": None if detect_year is None
            else detect_year - fail_year, "closed": closed,
            "corrected_by": "none"}


def _summarize(episodes) -> dict:
    years = np.array([e["years"] for e in episodes], dtype=float)
    lost = np.array([e["lost"] for e in episodes], dtype=float)
    defeat = np.array([e["defeat"] for e in episodes], dtype=float)
    lags = [e["detect_lag"] for e in episodes if e["detect_lag"] is not None]
    channels = {}
    for e in episodes:
        channels[e["corrected_by"]] = channels.get(e["corrected_by"], 0) + 1
    n = len(episodes)
    return {
        "mean_years": float(years.mean()),
        "mean_lost": float(lost.mean()),
        "defeat_rate": float(defeat.mean()),
        "mean_detect_lag": float(np.mean(lags)) if lags else None,
        "corrected_by": {k: v / n for k, v in sorted(channels.items())},
    }


def _normal_growth(name: str, spec: dict, rng) -> float:
    """15-year capability growth with a good controller throughout."""
    years = 15
    grow = GROW_SEALED if name == "sealed" else GROW
    if name == "custodial":
        grow -= 0.02          # process cost of the custodial apparatus
    if name == "network":
        grow -= 0.03          # consensus cost
    total = grow * years
    if "false_positive" in spec:
        # campaign risk removes good controllers too
        churns = rng.binomial(years, spec["false_positive"], size=EPISODES)
        total -= float(churns.mean()) * CHURN_COST
    return total


def run_correction() -> dict:
    rng = np.random.default_rng(SEED)
    grid = {}
    raw = {}
    for name, spec in ARCHITECTURES.items():
        eps = [_episode(rng, spec) for _ in range(EPISODES)]
        raw[name] = eps
        grid[name] = _summarize(eps)
        grid[name]["normal_growth_15y"] = _normal_growth(name, spec, rng)

    # custodial conditional on elite closure
    cust = raw["custodial"]
    closed = [e for e in cust if e["closed"]]
    open_ = [e for e in cust if not e["closed"]]
    custodial_split = {"closed": _summarize(closed), "open": _summarize(open_)}

    # sealed counterfactuals: free reporting alone, removability alone, both
    sealed = ARCHITECTURES["sealed"]
    cf = {}
    for label, override in (
            ("free_reporting", {"suppress": 0.0}),
            ("removability", {"rho": 0.65}),
            ("both", {"suppress": 0.0, "rho": 0.65})):
        eps = [_episode(rng, sealed, override) for _ in range(EPISODES)]
        cf[label] = _summarize(eps)
    base_lost = grid["sealed"]["mean_lost"]
    cf_reduction = {k: 1 - v["mean_lost"] / base_lost for k, v in cf.items()}

    # exposure sweep on the reciprocal architecture: economic exposure as a
    # correction channel
    alphas = [0.02, 0.1, 0.2, 0.3, 0.46, 0.6, 0.75, 0.9]
    sweep = []
    for a in alphas:
        eps = [_episode(rng, ARCHITECTURES["reciprocal"], {"alpha": a})
               for _ in range(EPISODES // 2)]
        s = _summarize(eps)
        sweep.append({"alpha": a, "mean_lost": s["mean_lost"],
                      "mean_years": s["mean_years"]})

    return {
        "constants": {
            "S0": S0, "S_VIS": S_VIS, "S_DEAD": S_DEAD, "GROW": GROW,
            "GROW_SEALED": GROW_SEALED, "DAMAGE": DAMAGE,
            "SELF_MAX": SELF_MAX, "EPISODES": EPISODES, "SEED": SEED,
        },
        "architectures": {k: dict(v) for k, v in ARCHITECTURES.items()},
        "grid": grid,
        "custodial_split": custodial_split,
        "sealed_counterfactuals": cf,
        "sealed_counterfactual_reduction": cf_reduction,
        "exposure_sweep": sweep,
    }


# ----------------------------------------------------------------------
# cited records (verified external figures used in prose)
# ----------------------------------------------------------------------

CITED_RECORDS = {
    "spacex_musk_voting_pct": {
        "value": 82.4,
        "source": "SpaceX Form 424B4, June 12, 2026 (SEC EDGAR 1181412)"},
    "spacex_musk_classb_pct": {
        "value": 91.6,
        "source": "SpaceX Form 424B4, June 12, 2026"},
    "spacex_musk_economic_pct": {
        "value": 46.0,
        "source": "computed from Form 10-Q cover, July 28, 2026: "
                  "(849,494,440 + 5,219,053,075) / (7,696,293,669 + 5,485,486,276)"},
    "meta_zuckerberg_voting_pct": {
        "value": 60.8,
        "source": "Meta DEF 14A, April 2026 (SEC EDGAR 1326801)"},
    "meta_zuckerberg_classb_pct": {
        "value": 99.8,
        "source": "Meta DEF 14A, April 2026"},
    "alphabet_page_voting_pct": {
        "value": 27.4, "source": "Alphabet DEF 14A, April 2026"},
    "alphabet_brin_voting_pct": {
        "value": 25.3, "source": "Alphabet DEF 14A, April 2026"},
    "alphabet_joint_voting_pct": {
        "value": 52.7, "source": "Alphabet DEF 14A, April 2026 (27.4 + 25.3)"},
    "palantir_class_f_pct": {
        "value": 49.999999,
        "source": "Palantir DEF 14A, April 2026, Class F formula"},
    "ford_class_b_voting_pct": {
        "value": 40.0, "source": "Ford DEF 14A, March 2026"},
    "ford_class_b_share_of_shares_pct": {
        "value": 1.8,
        "source": "computed from Ford DEF 14A record-date counts: "
                  "70,852,076 / (3,940,230,185 + 70,852,076)"},
    "big_three_median_stake_pct": {
        "value": 21.9,
        "source": "Bebchuk and Hirst 2022, BU L. Rev. 102: 1547"},
    "big_three_votes_cast_pct": {
        "value": 24.9,
        "source": "Bebchuk and Hirst 2022, BU L. Rev. 102: 1547"},
    "retail_voted_pct": {
        "value": 28.0, "source": "Broadridge ProxyPulse 2025"},
    "pew_trust_2025_pct": {
        "value": 17.0, "source": "Pew Research Center, December 4, 2025"},
    "pew_trust_1958_pct": {
        "value": 73.0, "source": "Pew Research Center, December 4, 2025"},
    "nse_promoter_share_pct": {
        "value": 50.1,
        "source": "NSE India Ownership Tracker, September 2025"},
    "premium_fade_window_years": {
        "value": [6, 9],
        "source": "Cremers, Lauterbach and Pajuste 2024, RCFS 13: 459-493; "
                  "CII 2018 petitions"},
}


# ----------------------------------------------------------------------
# invariants
# ----------------------------------------------------------------------

def _checks(life: dict, race: dict, corr: dict) -> dict:
    c = {}
    # mechanism 1
    c["ipo_premium_positive"] = life["population_delta"][0] > 0
    c["crossover_in_documented_window"] = 6.0 <= life["population_crossover_years"] <= 9.0
    ex = life["population_excess_vs_single"]
    c["renewable_beats_hard"] = ex["renewable"] >= ex["hard"]
    c["hard_beats_single"] = ex["hard"] > 0
    c["perpetual_destroys_value"] = ex["perpetual"] < 0
    c["perpetual_worst_wedge_regime"] = ex["perpetual"] <= min(
        ex["event"], ex["hard"], ex["renewable"])
    c["renewable_tracks_each_crossover"] = all(
        abs(life["types"][n]["renewable_insulated_until"] - FIRM_TYPES[n]["t_star"]) <= 5
        for n in FIRM_TYPES)
    en = life["entrenchment"]
    c["entrenchment_threshold_below_half"] = 0 < en["alpha_star"] < 0.5
    c["ford_stake_below_threshold"] = en["ford_keeps"]
    c["spacex_stake_above_threshold"] = not en["spacex_keeps"]
    # mechanism 2
    c["holdout_survives_low_demand_for_decades"] = race["holdout_years"] >= 40
    c["flat_demand_never_defects"] = not race["flat_demand_defected"]
    c["defection_within_decade_of_demand_rise"] = 0 <= race["defection_lag_after_demand_rise"] <= 10
    c["cascade_fast_after_defection"] = (race["cascade_lag_years"] is not None
                                         and race["cascade_lag_years"] <= 3)
    c["floor_binds_while_active"] = all(s == 0.0 for s in race["floor_share"])
    c["floor_removal_completes_cascade"] = (
        race["post_floor_share"] >= 0.9 * race["demand"][FLOOR_END + 1])
    c["race_ends_at_full_demand"] = abs(race["final_wedge_share"] - D_HIGH) < 0.01
    c["degree_ratchet_monotone"] = race["degree_monotone"]
    c["degree_reaches_max"] = race["final_degree_mean"] == DEGREE_MAX
    fh = race["floor_held"]
    c["held_floor_keeps_domestic_zero"] = fh["domestic_share_final"] == 0.0
    c["held_floor_leaks_abroad"] = 0 < fh["leakage_over_demand"] < 1
    # mechanism 3
    g = corr["grid"]
    c["sealed_max_damage"] = all(g["sealed"]["mean_lost"] >= g[a]["mean_lost"]
                                 for a in g)
    c["sealed_max_defeat"] = all(g["sealed"]["defeat_rate"] >= g[a]["defeat_rate"]
                                 for a in g)
    c["sealed_best_normal_times"] = all(
        g["sealed"]["normal_growth_15y"] >= g[a]["normal_growth_15y"] for a in g)
    cr = corr["sealed_counterfactual_reduction"]
    c["reporting_alone_buys_little"] = cr["free_reporting"] < 0.15
    c["removability_does_the_work"] = cr["removability"] > 2 * cr["free_reporting"]
    c["both_approach_custodial"] = (corr["sealed_counterfactuals"]["both"]["mean_lost"]
                                    < 2.0 * g["custodial"]["mean_lost"])
    c["vertical_detects_later_than_custodial"] = (
        g["vertical"]["mean_detect_lag"] > g["custodial"]["mean_detect_lag"])
    c["vertical_beats_sealed_on_damage"] = (
        g["vertical"]["mean_lost"] < g["sealed"]["mean_lost"])
    c["network_slowest_but_dampened"] = (
        g["network"]["mean_years"] >= max(g[a]["mean_years"] for a in g) - 1e-9
        and g["network"]["mean_lost"] < g["sealed"]["mean_lost"])
    nb = g["network"]["corrected_by"]
    c["network_reform_is_largest_channel"] = (
        nb.get("reform", 0) >= max(nb.get("removal", 0), nb.get("self", 0),
                                   nb.get("none", 0)))
    c["custodial_best_mean_damage"] = all(
        g["custodial"]["mean_lost"] <= g[a]["mean_lost"] for a in g)
    cs = corr["custodial_split"]
    c["elite_closure_degrades_custodial"] = (
        cs["closed"]["mean_lost"] > 2 * cs["open"]["mean_lost"])
    sw = corr["exposure_sweep"]
    c["exposure_sweep_monotone_damage"] = all(
        b["mean_lost"] <= a["mean_lost"] + 0.05
        for a, b in zip(sw, sw[1:]))
    return c


def run() -> dict:
    life = run_lifecycle()
    race = run_race()
    corr = run_correction()
    checks = _checks(life, race, corr)
    failed = [k for k, v in checks.items() if not v]
    if failed:
        raise SystemExit(f"INVARIANT FAILURES: {failed}")
    return _py({
        "lifecycle": life,
        "race": race,
        "correction": corr,
        "cited_records": CITED_RECORDS,
        "checks": checks,
    })
