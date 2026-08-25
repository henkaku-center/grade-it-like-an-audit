#!/usr/bin/env python3
"""Cross-unit reconciliation audit for point deductions.

The blind auditors cannot see it and the lead pass is the only thing that can: the same
issue deducted in one unit and silently waived in another. This script makes that
checkable — it extracts every itemized deduction from an evaluations file, clusters the
issues by similarity, and reports:

  1. issues deducted in more than one unit for DIFFERENT amounts   (inconsistent price)
  2. issues deducted in exactly one unit                           (was it checked elsewhere?)
  3. the per-unit deduction inventory                              (what was actually charged)

(2) is the high-value output: a singleton is either a genuinely unique defect or a
consistency failure, and only a human reading the other units can tell which. The script
does not decide; it hands you the shortlist.

Unit identities never reach the output — units are U1..Un in order of appearance, and any
name that appears in a unit heading is redacted from every printed line.

Stdlib only. Usage:
    python3 reconcile-deductions.py evaluations.md [more.md ...] [--threshold 0.62]
"""

import argparse
import difflib
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

# `## Name — 97/100`  (em dash, en dash or hyphen; score optional on some headings)
UNIT_HEAD = re.compile(r"^##\s+(?P<label>.+?)\s*[—–-]\s*(?P<got>\d+)\s*/\s*(?P<max>\d+)\s*$")
ANY_HEAD = re.compile(r"^(?P<hashes>#{1,6})\s+(?P<label>.+?)\s*$")
# `- **Communication: 9/10** — …` or `- Task 5: 19/20 — …`
COMPONENT = re.compile(r"^\s*[-*]\s+\*{0,2}(?P<name>[^:*]{1,60}?):?\s*\*{0,2}\s*"
                       r"(?P<got>\d+)\s*/\s*(?P<max>\d+)")
# A deduction must be *enclosed*: `(-1)` or `(−1)`. Without the brackets this also matches
# every number range in the prose ("Tasks 19–25") and every hyphenated figure reference,
# which is how the first version reported 9 points lost from a 99/100 unit.
DEDUCT = re.compile(r"[(\[]\s*[-−–]\s*(?P<amt>\d+(?:\.\d+)?)\s*[)\]]")
BOLD = re.compile(r"\*\*(?P<text>.+?)\*\*")
STOP = {"the", "a", "an", "and", "or", "but", "for", "of", "to", "in", "on", "is", "was",
        "it", "its", "this", "that", "with", "as", "at", "by", "from", "not", "no", "one",
        "two", "task", "point", "points", "deduction", "deducted", "added", "sweep"}


def issue_name(label):
    """`Unfilled named template fields (−1, row 3): the 1A blanks…` -> the family name.

    Clustering must run on this, not on the whole label: the evidence tail is different in
    every unit by construction, so a full-label match splits one family across several rows
    and the matrix stops being able to show an inconsistency at all.
    """
    s = re.sub(r"^[\s*—–-]+", "", label)
    s = re.split(r"\s*\((?:−|–|-)\s*\d", s)[0]
    s = re.split(r"\s*[::]\s", s)[0]
    return s.strip(" *—–-") or label.strip(" *—–-") or "(unlabelled in source)"


def normalize(text):
    text = re.sub(r"`[^`]*`", " ", text)
    text = re.sub(r"[^\w\s]", " ", text.lower())
    return " ".join(w for w in text.split() if w not in STOP and len(w) > 2)


def similar(a, b):
    """Token overlap first (cheap, order-free), sequence ratio as a tiebreak."""
    ta, tb = set(a.split()), set(b.split())
    if not ta or not tb:
        return 0.0
    jaccard = len(ta & tb) / len(ta | tb)
    return max(jaccard, difflib.SequenceMatcher(None, a, b).ratio() * 0.9)


def parse(path):
    """-> (units, deductions). A deduction is (unit_index, component, amount, label)."""
    text = Path(path).read_text(encoding="utf-8", errors="replace")
    units, deductions, names = [], [], []
    cur = None
    for raw in text.splitlines():
        m = UNIT_HEAD.match(raw)
        if m:
            names.append(m.group("label").strip())
            src = Path(path).parent.name
            units.append({"label": f"{src}:U{len(units) + 1}", "got": int(m.group("got")),
                          "max": int(m.group("max")), "source": src})
            cur = len(units) - 1
            continue
        if ANY_HEAD.match(raw) and len(ANY_HEAD.match(raw).group("hashes")) <= 2:
            # a non-scored h1/h2 ends the current unit's section
            cur = None
        if cur is None:
            continue
        comp = COMPONENT.match(raw)
        if not comp:
            continue                      # narrative prose restates losses; never re-count it
        got, mx = int(comp.group("got")), int(comp.group("max"))
        name = comp.group("name").strip()
        if got >= mx:
            continue
        body = raw[comp.end():]
        marked = [float(d.group("amt")) for d in DEDUCT.finditer(body) if float(d.group("amt")) > 0]
        labels = [b.group("text").strip() for b in BOLD.finditer(body)]
        labels = [l for l in labels if len(l) > 3] or labels
        if marked and abs(sum(marked) - (mx - got)) < 0.001:
            # itemized and self-consistent: keep each issue separately, with its own label
            for i, amt in enumerate(marked):
                label = labels[i] if i < len(labels) else (labels[0] if labels else body.strip()[:160])
                deductions.append({"unit": units[cur]["label"], "component": name,
                                   "amount": amt, "label": label.strip(),
                                   "norm": normalize(issue_name(label)), "inferred": False})
        else:
            # the markers do not add up to this line's own loss — trust the score, not the
            # prose, and say the label is inferred
            label = labels[0] if labels else body.strip()[:160]
            deductions.append({"unit": units[cur]["label"], "component": name,
                               "amount": mx - got, "label": label.strip(),
                               "norm": normalize(issue_name(label)), "inferred": True})
    return units, deductions, names


def redact(text, names):
    """A unit's own name never reaches the output, wherever it was written."""
    for n in sorted(names, key=len, reverse=True):
        for tok in [n] + [t for t in re.split(r"[\s,]+", n) if len(t) > 2]:
            text = re.sub(rf"(?<![A-Za-z0-9]){re.escape(tok)}(?![A-Za-z0-9])",
                          "[unit]", text, flags=re.IGNORECASE)
    return text


def cluster(deductions, threshold):
    clusters = []
    for d in deductions:
        if not d["norm"]:
            continue
        for c in clusters:
            if similar(d["norm"], c["norm"]) >= threshold:
                c["members"].append(d)
                break
        else:
            clusters.append({"norm": d["norm"], "members": [d]})
    return clusters


def main():
    ap = argparse.ArgumentParser(description="Cross-unit reconciliation audit for deductions.")
    ap.add_argument("files", nargs="+", help="evaluations.md file(s)")
    ap.add_argument("--threshold", type=float, default=0.62,
                    help="similarity above which two issues are the same issue (0-1)")
    ap.add_argument("--show-labels", action="store_true",
                    help="print issue text (already name-redacted); off by default")
    ap.add_argument("--emit-matrix", metavar="PATH",
                    help="write the family x unit deduction matrix (the cross-unit artifact)")
    ap.add_argument("--emit-rulings", metavar="PATH",
                    help="write the ruling-request queue: what the lead cannot decide alone")
    ap.add_argument("--self-test", action="store_true", help="fixture check; exits nonzero on failure")
    if "--self-test" in sys.argv[1:]:
        return self_test()
    args = ap.parse_args()

    all_units, all_ded, all_names = [], [], []
    for f in args.files:
        u, d, n = parse(f)
        all_units += u
        all_ded += d
        all_names += n
    if not all_units:
        print("no unit sections found (expected `## <label> — NN/NN`)")
        return 1

    print(f"units parsed        : {len(all_units)}")
    print(f"deductions extracted: {len(all_ded)}")
    lost = Counter()
    for d in all_ded:
        lost[d["unit"]] += d["amount"]
    inferred = len([d for d in all_ded if d.get("inferred")])
    print(f"units with >=1 deduction: {len(lost)} of {len(all_units)}")
    if inferred:
        print(f"labels inferred from the score (not itemized in the line): {inferred} "
              f"of {len(all_ded)} — those clusters are weaker evidence.")

    # A parser that silently mis-reads the corpus is worse than no parser. Reconcile what
    # was extracted against what each unit's own header says it lost.
    mismatched = [u for u in all_units
                  if abs(lost[u["label"]] - (u["max"] - u["got"])) > 0.001]
    if mismatched:
        print(f"PARSE FIDELITY: {len(mismatched)} of {len(all_units)} units do not reconcile "
              f"— component lines != (max - awarded).")
        for u in mismatched:
            print(f"  {u['label']}: header says -{u['max'] - u['got']:g}, "
                  f"components sum to -{lost[u['label']]:g}")
        print("  Two possible causes and this script cannot tell them apart: the parser missed")
        print("  a line, or the document's own arithmetic does not add up — which is itself a")
        print("  CONSISTENCY defect worth a look. Check these units by hand either way.")
    else:
        print(f"PARSE FIDELITY: all {len(all_units)} units reconcile "
              f"(extracted deductions == max - awarded).")
    print()

    clusters = cluster(all_ded, args.threshold)
    multi = [c for c in clusters if len({m["unit"] for m in c["members"]}) > 1]
    singles = [c for c in clusters if len({m["unit"] for m in c["members"]}) == 1]

    print(f"=== 1. Same issue, different price ({len(multi)} issue(s) span >1 unit) ===")
    flagged = 0
    for c in multi:
        amts = {m["unit"]: m["amount"] for m in c["members"]}
        if len(set(amts.values())) > 1:
            flagged += 1
            print(f"  INCONSISTENT  {amts}")
            if args.show_labels:
                for m in c["members"]:
                    print(f"      {m['unit']} -{m['amount']:g}  {redact(m['label'], all_names)[:110]}")
    print(f"  {flagged} issue(s) charged at different prices across units."
          if flagged else "  none — every cross-unit issue was charged the same.")
    print()

    print(f"=== 2. Deducted in exactly one unit ({len(singles)}) ===")
    print("  Each is either a genuinely unique defect or a consistency failure. Only a human")
    print("  reading the other units can tell which — this is the shortlist for that pass.")
    by_unit = defaultdict(int)
    for c in singles:
        by_unit[c["members"][0]["unit"]] += 1
    for u, n in sorted(by_unit.items()):
        print(f"    {u}: {n} singleton deduction(s)")
    if args.show_labels:
        for c in singles:
            m = c["members"][0]
            print(f"      {m['unit']} -{m['amount']:g}  {redact(m['label'], all_names)[:110]}")
    print()

    if args.emit_matrix:
        write_matrix(args.emit_matrix, all_units, clusters, all_names)
        print(f"matrix written: {args.emit_matrix}")
    if args.emit_rulings:
        n = write_rulings(args.emit_rulings, all_units, clusters, all_names)
        print(f"ruling requests written: {args.emit_rulings} ({n} question(s) for the human)")
    print("=== 3. Per-unit deduction inventory ===")
    print(f"  {'unit':6s} {'score':>9s} {'deductions':>11s} {'points lost':>12s}")
    for u in all_units:
        n = len([d for d in all_ded if d["unit"] == u["label"]])
        print(f"  {u['label']:6s} {u['got']:>5d}/{u['max']:<3d} {n:>11d} {lost[u['label']]:>12g}")
    return 0


def family_name(cluster, names):
    """A short label for the row: the shortest member issue, name-redacted."""
    txt = min((issue_name(m["label"]) for m in cluster["members"]), key=len)
    return redact(txt, names)[:70] or "(unlabelled)"


def write_matrix(path, units, clusters, names):
    """The cross-unit artifact. One row per defect family, one column per unit, one charge
    per cell. A row reading `-1 | -1 | -- | -2 | --` makes an inconsistency impossible to
    miss, which is the whole point: consistency becomes structural, not remembered."""
    labels = [u["label"] for u in units]
    rows = sorted(clusters, key=lambda c: (-len({m["unit"] for m in c["members"]}),
                                           -len(c["members"])))
    L = ["# Deduction matrix — cross-unit reconciliation (lead grader)", "",
         "One row per defect family. One charge per (family, unit) — **never per instance**;",
         "N instances of the same family in one unit is one charge, priced once in the Ruling",
         "column. A row with different numbers in different cells is either a justified",
         "difference or an unfairness, and it has to be one of the two, in writing.", "",
         "Generated from the drafted evaluations. The Ruling column is written by the lead",
         "grader and by the human — never by the generator.", "",
         "| # | Family | " + " | ".join(labels) + " | Ruling |",
         "|---|---|" + "---|" * (len(labels) + 1)]
    for i, c in enumerate(rows, 1):
        cells = []
        for lab in labels:
            amts = [m["amount"] for m in c["members"] if m["unit"] == lab]
            if not amts:
                cells.append("—")
            elif len(set(amts)) == 1 and len(amts) == 1:
                cells.append(f"−{amts[0]:g}")
            else:
                cells.append(f"−{sum(amts):g} ({len(amts)} inst.)")
        flag = ""
        charged = {m["unit"]: m["amount"] for m in c["members"]}
        if len(set(charged.values())) > 1:
            flag = " **← PRICE DIFFERS — arbitrate**"
        elif len(charged) < len(labels):
            flag = " ← not charged everywhere: justified or unfair?"
        L.append(f"| {i} | {family_name(c, names)} | " + " | ".join(cells) + f" |{flag} |")
    L += ["", "## Explicitly not deducted (record the decision, not just the silence)", "",
          "| Situation | Why no points | Applies to |", "|---|---|---|", "| | | |", "",
          "## Rulings", "",
          "Numbered, dated, attributed. Every ruling here becomes a write-back candidate.", "",
          "| # | Date | Question | Ruling | By |", "|---|---|---|---|---|", "| 1 | | | | |"]
    Path(path).write_text("\n".join(L), encoding="utf-8")


def write_rulings(path, units, clusters, names):
    """The questions for the human. Two kinds the lead must never settle silently: the same
    family priced differently across units, and a family charged in some units but not
    others. Both are fairness questions, and both are cheap to answer and expensive to guess."""
    labels = [u["label"] for u in units]
    qs = []
    for c in clusters:
        charged = {}
        for m in c["members"]:
            charged.setdefault(m["unit"], []).append(m["amount"])
        prices = {u: sum(v) for u, v in charged.items()}
        if len(set(prices.values())) > 1:
            qs.append(("SAME ITEM, DIFFERENT PRICE", family_name(c, names), prices,
                       "Two units were charged different amounts for what clusters as the "
                       "same defect. Which price is right for all of them?"))
        elif 0 < len(prices) < len(labels):
            missing = [u for u in labels if u not in prices]
            qs.append(("CHARGED HERE, NOT THERE", family_name(c, names), prices,
                       f"Not charged in {', '.join(missing)}. Is that a real difference in "
                       f"the work, or was it missed there?"))
    L = ["# Ruling requests — questions for the human grader", "",
         "The lead pass produced these because deciding them alone would set policy without",
         "authority. Each one is a fairness question across units. Answer once; the answer",
         "becomes a numbered ruling in the matrix and a write-back candidate.", ""]
    if not qs:
        L.append("_No cross-unit discrepancies found. Nothing to arbitrate this round._")
    for i, (kind, fam, prices, ask) in enumerate(qs, 1):
        L += [f"## Q{i} — {kind}", "", f"**Family:** {fam}", "",
              "| unit | charged |", "|---|---|"]
        L += [f"| {u} | −{p:g} |" for u, p in sorted(prices.items())]
        L += ["", f"**Question:** {ask}", "",
              "- [ ] price for all: ____", "- [ ] genuinely different, because: ____",
              "- [ ] waive everywhere, because: ____", ""]
    Path(path).write_text("\n".join(L), encoding="utf-8")
    return len(qs)


def self_test():
    """Fixture with a hand-computed answer. Prints real counts; nonzero exit on failure."""
    import tempfile
    checks, failures = 0, []

    def check(name, cond):
        nonlocal checks
        checks += 1
        if not cond:
            failures.append(name)

    doc = """# Evaluations

## Ada Lovelace — 98/100
- Task 1: 20/20 — no deduction.
- Task 2: 19/20 — **Unsupported cohort claim (-1).** Range covered Tasks 19-25 here.
- Task 3: 19/20 — **Missing degrees of freedom (-1).**

## Grace Hopper — 97/100
- Task 1: 18/20 — **Missing degrees of freedom (-2).**
- Task 2: 19/20 — **Unreproducible figure (-1).**

**What we owe you.** Restating: Communication -1 and clarity -1 were already charged above.
"""
    with tempfile.TemporaryDirectory() as tmp:
        f = Path(tmp) / "MP9" / "evaluations.md"
        f.parent.mkdir(parents=True)
        f.write_text(doc, encoding="utf-8")
        units, ded, names = parse(f)

        check("both units parsed", len(units) == 2)
        check("unit labels carry their source", all(u["label"].startswith("MP9:") for u in units))
        check("full-credit lines produce no deduction",
              not any(d["component"] == "Task 1" and d["unit"].endswith("U1") for d in ded))
        check("number range in prose is not a deduction",
              len(ded) == 4 and not any(d["amount"] in (19.0, 25.0) for d in ded))
        by_unit = Counter(d["unit"] for d in ded)
        check("deductions land on the right units",
              by_unit["MP9:U1"] == 2 and by_unit["MP9:U2"] == 2 + 1 - 1)
        for u in units:
            total = sum(d["amount"] for d in ded if d["unit"] == u["label"])
            check(f"{u['label']} reconciles", abs(total - (u["max"] - u["got"])) < 0.001)
        check("narrative restatement is not double-counted",
              sum(d["amount"] for d in ded) == 5)

        clusters = cluster(ded, 0.62)
        multi = [c for c in clusters if len({m["unit"] for m in c["members"]}) > 1]
        inconsistent = [c for c in multi
                        if len({m["amount"] for m in c["members"]}) > 1]
        check("the same issue across two units is clustered", len(multi) >= 1)
        check("the differently-priced issue is flagged", len(inconsistent) == 1)
        check("the flagged pair is the -1/-2 one",
              inconsistent and {m["amount"] for m in inconsistent[0]["members"]} == {1.0, 2.0})
        singles = [c for c in clusters if len({m["unit"] for m in c["members"]}) == 1]
        check("singletons are the rest", len(singles) == len(clusters) - len(multi))
        check("a unit name never survives into printed output",
              "Lovelace" not in redact("Ada Lovelace overclaimed", names)
              and "Ada" not in redact("Ada Lovelace overclaimed", names))

        # the matrix and ruling emitters: exercised end to end, because the first version
        # of them shipped with a NameError that a 13/13 self-test did not catch
        m = Path(tmp) / "matrix.md"; rq = Path(tmp) / "rulings.md"
        clusters = cluster(ded, 0.62)
        write_matrix(m, units, clusters, names)
        nq = write_rulings(rq, units, clusters, names)
        mt = m.read_text()
        check("matrix writes a row per family and a column per unit",
              all(u["label"] in mt for u in units) and "| Ruling |" in mt)
        check("matrix redacts unit identities", "Lovelace" not in mt and "Hopper" not in mt)
        check("matrix flags a family priced differently across units",
              "PRICE DIFFERS" in mt)
        check("matrix carries a rulings section", "## Rulings" in mt)
        check("matrix carries an explicitly-not-deducted section",
              "Explicitly not deducted" in mt)
        rt = rq.read_text()
        check("ruling queue raises the differently-priced family",
              nq >= 1 and "SAME ITEM, DIFFERENT PRICE" in rt)
        check("ruling queue offers a decision, not a verdict",
              "price for all" in rt and "waive everywhere" in rt)
        check("ruling queue names no person", "Lovelace" not in rt and "Ada" not in rt)
        # one family must occupy exactly ONE row even when its evidence differs per unit
        ev3 = Path(tmp) / "MPZ" / "evaluations.md"
        ev3.parent.mkdir()
        ev3.write_text(
            "# E\n\n## Ada Lovelace — 88/90\n"
            "- Investigation: 28/30 — **Unfilled named template fields (-2): the 1A blanks.**\n"
            "\n## Grace Hopper — 89/90\n"
            "- Investigation: 29/30 — **Unfilled named template fields (-1): the 3C header.**\n",
            encoding="utf-8")
        u3, d3, n3 = parse(ev3)
        c3 = cluster(d3, 0.62)
        fams = [f for f in c3 if "template" in family_name(f, n3).lower()]
        check("same family with different evidence collapses to ONE row", len(fams) == 1)
        check("that one row spans both units",
              fams and len({m["unit"] for m in fams[0]["members"]}) == 2)
        m3 = Path(tmp) / "m3.md"
        write_matrix(m3, u3, c3, n3)
        check("and the matrix flags its differing price", "PRICE DIFFERS" in m3.read_text())

    print(f"self-test: {checks - len(failures)}/{checks} checks passed")
    for f in failures:
        print(f"  FAIL: {f}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
