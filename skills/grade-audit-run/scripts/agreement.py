#!/usr/bin/env python3
"""Agreement metrics for calibration mode: human vs. harness scores.

Usage:
    python3 agreement.py scores.csv [--scale-min N] [--scale-max N]

Input: CSV with header `unit,human,ai` — one row per calibration unit, scores numeric.
Output: per-unit table, then quadratic-weighted Cohen's kappa (on integer-rounded
scores), Spearman rho, mean absolute difference, and exact-agreement rate — with
honest caveats for the tiny samples calibration uses.

Stdlib only, deliberately: no numpy/scipy, so it runs on any Python 3.8+.
The point of a deterministic script is that the agreement numbers are computed,
not asserted by a model.
"""

import argparse
import csv
import sys


def spearman_rho(xs, ys):
    """Spearman rank correlation with average ranks for ties."""

    def avg_ranks(vals):
        order = sorted(range(len(vals)), key=lambda i: vals[i])
        ranks = [0.0] * len(vals)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and vals[order[j + 1]] == vals[order[i]]:
                j += 1
            avg = (i + j) / 2 + 1
            for k in range(i, j + 1):
                ranks[order[k]] = avg
            i = j + 1
        return ranks

    rx, ry = avg_ranks(xs), avg_ranks(ys)
    n = len(xs)
    mx, my = sum(rx) / n, sum(ry) / n
    cov = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    vx = sum((a - mx) ** 2 for a in rx)
    vy = sum((b - my) ** 2 for b in ry)
    if vx == 0 or vy == 0:
        return None  # a constant ranking has no defined correlation
    return cov / (vx * vy) ** 0.5


def quadratic_weighted_kappa(hs, ais, lo, hi):
    """QWK on integer categories lo..hi (scores rounded to nearest integer)."""
    cats = list(range(lo, hi + 1))
    k = len(cats)
    if k < 2:
        return None
    idx = {c: i for i, c in enumerate(cats)}
    h_idx = [idx[min(max(round(s), lo), hi)] for s in hs]
    a_idx = [idx[min(max(round(s), lo), hi)] for s in ais]
    n = len(h_idx)
    obs = [[0.0] * k for _ in range(k)]
    for i, j in zip(h_idx, a_idx):
        obs[i][j] += 1 / n
    h_marg = [h_idx.count(i) / n for i in range(k)]
    a_marg = [a_idx.count(j) / n for j in range(k)]
    num = den = 0.0
    for i in range(k):
        for j in range(k):
            w = ((i - j) ** 2) / ((k - 1) ** 2)
            num += w * obs[i][j]
            den += w * h_marg[i] * a_marg[j]
    if den == 0:
        return None  # both raters constant — agreement is trivial, kappa undefined
    return 1 - num / den


def kappa_band(kappa):
    for cutoff, label in [(0.8, "almost perfect"), (0.6, "substantial"),
                          (0.4, "moderate"), (0.2, "fair"), (0.0, "slight")]:
        if kappa >= cutoff:
            return label
    return "poor"


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("csv_path")
    p.add_argument("--scale-min", type=int, default=None,
                   help="lowest possible score on the scale (default: observed min)")
    p.add_argument("--scale-max", type=int, default=None,
                   help="highest possible score on the scale (default: observed max)")
    args = p.parse_args()

    units, hs, ais = [], [], []
    with open(args.csv_path, newline="") as f:
        for row in csv.DictReader(f):
            try:
                units.append(row["unit"])
                hs.append(float(row["human"]))
                ais.append(float(row["ai"]))
            except (KeyError, ValueError) as e:
                sys.exit(f"bad row {row!r}: {e} (need header unit,human,ai; numeric scores)")
    n = len(units)
    if n < 2:
        sys.exit("need at least 2 rows to compute agreement")

    lo = args.scale_min if args.scale_min is not None else round(min(hs + ais))
    hi = args.scale_max if args.scale_max is not None else round(max(hs + ais))

    width = max(len(u) for u in units + ["unit"])
    print(f"{'unit':<{width}}  human     ai   diff")
    for u, h, a in zip(units, hs, ais):
        print(f"{u:<{width}}  {h:5g}  {a:5g}  {a - h:+5g}")
    print()

    mad = sum(abs(a - h) for h, a in zip(hs, ais)) / n
    exact = sum(1 for h, a in zip(hs, ais) if h == a)
    rho = spearman_rho(hs, ais)
    qwk = quadratic_weighted_kappa(hs, ais, lo, hi)

    print(f"n = {n} units, scale {lo}..{hi}")
    print(f"mean absolute difference : {mad:.2f} points")
    print(f"exact agreement          : {exact}/{n}")
    print(f"Spearman rho             : "
          + (f"{rho:.3f}" if rho is not None else "undefined (constant scores)"))
    if qwk is not None:
        print(f"quadratic-weighted kappa : {qwk:.3f} ({kappa_band(qwk)})")
    else:
        print("quadratic-weighted kappa : undefined (no score variation)")
    print()
    if n < 10:
        print(f"CAVEAT: with n={n}, these numbers are directional, not conclusive —")
        print("kappa and rho are noisy on small samples. Read the per-unit diffs and")
        print("the harness's written rationales alongside them; disagreement on WHICH")
        print("units and WHY matters more than the coefficient.")


if __name__ == "__main__":
    main()
