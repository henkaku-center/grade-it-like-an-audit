#!/usr/bin/env python3
"""Systematic comparison: what a fresh harness run finds vs. the grades actually issued.

Design constraint learned the hard way: lexical similarity CANNOT decide whether two
differently-worded findings are the same defect. On a real corpus it paired "Unfilled named
template fields" with "Quota prediction recorded after the run" and, being greedy, consumed
the slot the true match needed. So this tool **proposes** pairings and **tabulates**
verdicts; it never decides. Adjudication is a separate, recorded step.

Two phases:
  worksheet  — align units, pair candidates by component, emit a markdown worksheet plus a
               machine-readable pairs.json for a judge (human or agent) to adjudicate
  report     — ingest verdicts.json and produce the comparison table with real counts

Unit identities never appear in output: units are the coded labels, and any name occurring
in an evaluations heading is redacted from every printed line.

Usage:
  compare-runs.py worksheet --new DIR --evaluations FILE --map FILE --out DIR [--basis 90]
  compare-runs.py report    --worksheet DIR --verdicts FILE
  compare-runs.py --self-test
"""

import argparse
import glob
import importlib.util
import json
import re
import sys
from collections import Counter
from pathlib import Path

_spec = importlib.util.spec_from_file_location(
    "recon", str(Path(__file__).with_name("reconcile-deductions.py")))
recon = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(recon)


def issue_name(label):
    """`** — Hack shipped without its engine (−1, matrix row 11): evidence…` -> the issue."""
    s = re.sub(r"^[\s*—–-]+", "", label)
    s = re.split(r"\s*\((?:−|–|-)\s*\d", s)[0]
    s = re.split(r"\s*[::]\s", s)[0]
    # An original whose label will not parse must be VISIBLY unlabelled: silently emitting
    # an empty string once made an entire unit uncomparable without anyone noticing.
    return s.strip(" *—–-") or label.strip(" *—–-") or "(unlabelled in source)"


def is_unlabelled(name):
    """A deduction that names no issue cannot be paired with a finding, whichever way the
    source left it: absent entirely, or recorded as `(unnamed issue in <Component>)` by
    reconcile-deductions. Both mean the same thing — nothing to match on."""
    return name.startswith("(unlabelled") or name.startswith("(unnamed issue in ")


def load_new_run(d):
    """Accepts both schemas: components[].deductions[] and components[].findings[] with a
    `disposition` of deduct / waived-note."""
    out = {}
    for f in sorted(glob.glob(str(Path(d) / "*.json"))):
        r = json.load(open(f, encoding="utf-8"))
        items = []
        for c in r.get("components", []):
            for x in c.get("findings", c.get("deductions", [])):
                disp = x.get("disposition", "deduct")
                items.append({"component": c["name"], "amount": float(x.get("amount", 0) or 0),
                              "issue": x.get("issue", ""), "disposition": disp,
                              "waived_family": x.get("waived_family")})
        out[r["unit"]] = {"items": items, "awarded": r.get("total_awarded"),
                          "possible": r.get("total_possible"), "coverage": r.get("coverage", "")}
    return out


def align_units(mapfile, names):
    """coded unit -> the evaluations heading for the same person, by token overlap."""
    kmap = json.load(open(mapfile, encoding="utf-8"))
    out = {}
    for u in kmap["units"]:
        toks = {t.lower() for t in re.split(r"[^A-Za-z]+", u["path"]) if len(t) > 2}
        best, sc = None, 0
        for h in names:
            ht = {t.lower() for t in re.split(r"[^A-Za-z]+", h) if len(t) > 2}
            if len(toks & ht) > sc:
                best, sc = h, len(toks & ht)
        out[u["code"]] = best
    return out


def worksheet(args):
    units, ded, names = recon.parse(args.evaluations)
    head_label = {names[i]: units[i]["label"] for i in range(len(units))}
    code_head = align_units(args.map, names)
    new = load_new_run(args.new)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    exclude = [e.strip().lower() for e in (args.exclude_component or "").split(",") if e.strip()]
    pairs, lines = [], []
    lines.append("# Adjudication worksheet — fresh run vs. issued grades\n")
    lines.append(f"Basis: /{args.basis}. Components excluded from the original as "
                 f"out-of-scope: {', '.join(exclude) or '(none)'}\n")
    lines.append("For each ORIGINAL finding, mark the candidate that is the SAME DEFECT, or "
                 "`miss` if none is.\nCandidates are proposals by component, not decisions. "
                 "Record verdicts in verdicts.json as\n`{\"unit\": {\"O1\": \"N3\", \"O2\": "
                 "\"miss\"}}`.\n")

    for code in sorted(new):
        head = code_head.get(code)
        lbl = head_label.get(head)
        o = [d for d in ded if d["unit"] == lbl
             and not any(x in d["component"].lower() for x in exclude)]
        seen, o2 = set(), []
        for d in o:
            k = (d["component"], d["amount"], issue_name(d["label"])[:60])
            if k in seen:
                continue
            seen.add(k)
            o2.append(d)
        ou = next((u for u in units if u["label"] == lbl), None)
        orig_basis = args.basis - sum(d["amount"] for d in o2) if ou else None
        n = new[code]["items"]
        deducts = [x for x in n if x["disposition"] == "deduct"]
        waived = [x for x in n if x["disposition"] != "deduct"]

        lines.append(f"\n## {code}\n")
        lines.append(f"- issued (rescored to /{args.basis}): **{orig_basis}**  ·  "
                     f"fresh: **{new[code]['awarded']}/{new[code]['possible']}**")
        lines.append(f"- original findings in scope: {len(o2)}  ·  fresh deductions: "
                     f"{len(deducts)}  ·  fresh waived-notes: {len(waived)}\n")
        for i, d in enumerate(o2, 1):
            nm = recon.redact(issue_name(d["label"]), names)
            unlabelled = is_unlabelled(nm)
            mark = "  ← **UNCOMPARABLE: no parseable label; verdict must be `uncomparable`**" \
                if unlabelled else ""
            lines.append(f"**O{i}** −{d['amount']:g} [{d['component']}] {nm}{mark}")
            cands = [(j, x) for j, x in enumerate(deducts, 1)
                     if x["component"].lower()[:4] == d["component"].lower()[:4]]
            if not cands:
                lines.append("  - _no fresh deduction in this component_")
            for j, x in cands:
                lines.append(f"  - N{j} −{x['amount']:g}: {x['issue']}")
                pairs.append({"unit": code, "orig": f"O{i}", "new": f"N{j}",
                              "orig_issue": nm, "new_issue": x["issue"],
                              "orig_amount": d["amount"], "new_amount": x["amount"],
                              "component": d["component"]})
            lines.append("")
        unpaired = [(j, x) for j, x in enumerate(deducts, 1)
                    if not any(x["component"].lower()[:4] == d["component"].lower()[:4] for d in o2)]
        if unpaired:
            lines.append("_Fresh deductions in components the original never charged:_")
            for j, x in unpaired:
                lines.append(f"  - N{j} −{x['amount']:g} [{x['component']}]: {x['issue']}")
            lines.append("")
        if waived:
            lines.append("_Fresh waived-notes (zero points, correctly routed if the waiver "
                         "applies):_")
            for x in waived:
                lines.append(f"  - family {x['waived_family']} [{x['component']}]: {x['issue']}")
            lines.append("")

    (out / "worksheet.md").write_text("\n".join(lines), encoding="utf-8")
    (out / "pairs.json").write_text(json.dumps(pairs, indent=2), encoding="utf-8")
    print(f"worksheet: {out/'worksheet.md'}")
    print(f"pairs    : {out/'pairs.json'}  ({len(pairs)} candidate pairs)")
    print("Adjudicate, then run: compare-runs.py report --worksheet DIR --verdicts FILE")
    return 0


def report(args):
    ws = Path(args.worksheet)
    pairs = json.load(open(ws / "pairs.json", encoding="utf-8"))
    verdicts = json.load(open(args.verdicts, encoding="utf-8"))
    by_unit = {}
    for p in pairs:
        by_unit.setdefault(p["unit"], {"orig": set(), "new": set()})
        by_unit[p["unit"]]["orig"].add(p["orig"])
        by_unit[p["unit"]]["new"].add(p["new"])

    tot = Counter()
    print(f"{'unit':8s} {'orig':>5s} {'matched':>8s} {'missed':>7s} {'uncomparable':>13s}")
    for unit in sorted(verdicts):
        v = verdicts[unit]
        matched = sum(1 for k, x in v.items() if x not in ("miss", "uncomparable"))
        missed = sum(1 for x in v.values() if x == "miss")
        unc = sum(1 for x in v.values() if x == "uncomparable")
        print(f"{unit:8s} {len(v):>5d} {matched:>8d} {missed:>7d} {unc:>13d}")
        tot["o"] += len(v); tot["m"] += matched; tot["x"] += missed; tot["u"] += unc
    den = tot["m"] + tot["x"]
    print(f"\ncomparable original findings: {den}  (excluded as uncomparable: {tot['u']})")
    if den:
        print(f"matched {tot['m']}/{den} = {tot['m']/den:.0%} recall of the issued findings")
    print(f"missed  {tot['x']}")
    return 0


def self_test():
    import tempfile
    checks, failures = 0, []

    def check(name, cond):
        nonlocal checks
        checks += 1
        if not cond:
            failures.append(name)

    check("issue_name strips the amount and evidence",
          issue_name("** — Hack shipped without its engine (−1, matrix row 11): because…")
          == "Hack shipped without its engine")
    check("issue_name survives a plain label", issue_name("Author placeholder") == "Author placeholder")
    check("both forms of 'names no issue' are recognised as uncomparable",
          is_unlabelled("(unlabelled in source)")
          and is_unlabelled("(unnamed issue in Write-up clarity)")
          and not is_unlabelled("Missing degrees of freedom"))
    check("an unparseable label is surfaced, never silently empty",
          issue_name("**") == "(unlabelled in source)")

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        (tmp / "new").mkdir()
        json.dump({"unit": "unit-a", "total_awarded": 86, "total_possible": 90,
                   "components": [{"name": "Investigation", "possible": 30, "awarded": 28,
                                   "findings": [
                                       {"disposition": "deduct", "amount": 2,
                                        "issue": "Fabricated calibration number"},
                                       {"disposition": "waived-note", "amount": 0,
                                        "waived_family": 1, "issue": "Blank header"}]}]},
                  open(tmp / "new" / "unit-a.json", "w"))
        loaded = load_new_run(tmp / "new")
        check("both schemas load", "unit-a" in loaded and len(loaded["unit-a"]["items"]) == 2)
        check("waived notes are separated from deductions",
              len([x for x in loaded["unit-a"]["items"] if x["disposition"] == "deduct"]) == 1)
        check("waived note carries zero points",
              all(x["amount"] == 0 for x in loaded["unit-a"]["items"]
                  if x["disposition"] != "deduct"))

        ev = tmp / "MPX" / "evaluations.md"
        ev.parent.mkdir()
        ev.write_text("# E\n\n## Ada Lovelace — 88/90\n"
                      "- Investigation: 28/30 — **Fabricated calibration number (-2).**\n",
                      encoding="utf-8")
        json.dump({"units": [{"code": "unit-a", "path": "mpx-ada-lovelace"}]},
                  open(tmp / "map.json", "w"))
        units, ded, names = recon.parse(ev)
        al = align_units(tmp / "map.json", names)
        check("coded unit aligns to its evaluations heading", al["unit-a"] == "Ada Lovelace")

        class A:
            new, evaluations, map = str(tmp / "new"), str(ev), str(tmp / "map.json")
            out, basis, exclude_component = str(tmp / "ws"), 90, "presentation"
        worksheet(A())
        text = (tmp / "ws" / "worksheet.md").read_text()
        check("worksheet proposes a candidate pair", "N1" in text and "O1" in text)
        check("worksheet lists waived notes separately", "waived-note" in text or "family 1" in text)
        check("worksheet redacts the person's name",
              "Ada" not in text and "Lovelace" not in text)
        pj = json.load(open(tmp / "ws" / "pairs.json"))
        check("pairs.json is machine-readable and non-empty", len(pj) == 1)
        check("pairs carry both amounts", pj[0]["orig_amount"] == 2 and pj[0]["new_amount"] == 2)

        ev2 = tmp / "MPY" / "evaluations.md"
        ev2.parent.mkdir()
        ev2.write_text("# E\n\n## Ada Lovelace — 85/90\n"
                       "- AI collaboration: 15/20 — ****\n", encoding="utf-8")
        class B(A):
            evaluations, out = str(ev2), str(tmp / "ws2")
        worksheet(B())
        t2 = (tmp / "ws2" / "worksheet.md").read_text()
        check("an unlabelled original is flagged UNCOMPARABLE in the worksheet",
              "UNCOMPARABLE" in t2)

    print(f"self-test: {checks - len(failures)}/{checks} checks passed")
    for f in failures:
        print(f"  FAIL: {f}")
    return 1 if failures else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd")
    w = sub.add_parser("worksheet")
    w.add_argument("--new", required=True)
    w.add_argument("--evaluations", required=True)
    w.add_argument("--map", required=True)
    w.add_argument("--out", required=True)
    w.add_argument("--basis", type=int, default=90)
    w.add_argument("--exclude-component", default="")
    r = sub.add_parser("report")
    r.add_argument("--worksheet", required=True)
    r.add_argument("--verdicts", required=True)
    ap.add_argument("--self-test", action="store_true")
    if "--self-test" in sys.argv[1:]:
        return self_test()
    a = ap.parse_args()
    if a.cmd == "worksheet":
        return worksheet(a)
    if a.cmd == "report":
        return report(a)
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
