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
import math
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

# `## Name — 97/100`  (em dash, en dash or hyphen; score optional on some headings)
UNIT_HEAD = re.compile(r"^##\s+(?P<label>.+?)\s*[—–-]\s*(?P<got>\d+(?:\.\d+)?)\s*/\s*(?P<max>\d+(?:\.\d+)?)\s*$")
ANY_HEAD = re.compile(r"^(?P<hashes>#{1,6})\s+(?P<label>.+?)\s*$")
# `- **Communication: 9/10** — …` or `- Task 5: 19/20 — …`
COMPONENT = re.compile(r"^\s*[-*]\s+\*{0,2}(?P<name>[^:*]{1,60}?):?\s*\*{0,2}\s*"
                       r"(?P<got>\d+(?:\.\d+)?)\s*/\s*(?P<max>\d+(?:\.\d+)?)")
# A deduction must be *enclosed*: `(-1)` or `(−1)`. Without the brackets this also matches
# every number range in the prose ("Tasks 19–25") and every hyphenated figure reference,
# which is how the first version reported 9 points lost from a 99/100 unit.
DEDUCT = re.compile(r"[(\[]\s*[-−–]\s*(?P<amt>\d+(?:\.\d+)?)\s*[)\]]")
BOLD = re.compile(r"\*\*(?P<text>.+?)\*\*")
# What remains of a component line after the score, with the component's own closing `**` and
# the em-dash separator removed — otherwise BOLD pairs the wrong asterisks.
LEAD = re.compile(r"^\s*\*{0,2}\s*[—–-]?\s*")
# Severity tiers are the method's existing vocabulary (BLOCKER / MINOR / note); presets
# attach thresholds and prices to them rather than inventing a taxonomy.
TIERS = ["note", "minor", "blocker"]          # ascending severity

# A preset is a coherent posture, not a mood. `report` is what gets written up at all;
# `charge` is what costs points. Note that `report` is "note" in every preset ON PURPOSE:
# lowering strictness DEMOTES a finding to a zero-point note, it never hides it. The letter
# still carries it, the student still learns from it, it simply does not cost marks.
PRESETS = {
    "lenient":  {"report": "note", "charge": "blocker",
                 "price": {"blocker": 1, "minor": 0, "note": 0},
                 "waiver": "waive where a rule plausibly applies"},
    "standard": {"report": "note", "charge": "minor",
                 "price": {"blocker": 2, "minor": 1, "note": 0},
                 "waiver": "waive where a rule states it"},
    "strict":   {"report": "note", "charge": "note",
                 "price": {"blocker": 3, "minor": 2, "note": 1},
                 "waiver": "waive only on an explicit written ruling"},
}

STOP = {"the", "a", "an", "and", "or", "but", "for", "of", "to", "in", "on", "is", "was",
        "it", "its", "this", "that", "with", "as", "at", "by", "from", "not", "no", "one",
        "two", "task", "point", "points", "deduction", "deducted", "added", "sweep"}


def apply_preset(findings, preset):
    """Price a set of findings under a preset. Returns one record per finding — the SAME
    finding set at every preset, which is the point: strictness changes `charged` and
    `amount`, never whether the finding exists."""
    if preset not in PRESETS:
        die(f"unknown preset '{preset}' (choose from: {', '.join(PRESETS)})")
    cfg = PRESETS[preset]
    charge_at = TIERS.index(cfg["charge"])
    report_at = TIERS.index(cfg["report"])
    out = []
    for f in findings:
        tier = str(f.get("severity", "minor")).strip().lower()
        if tier not in TIERS:
            tier = "minor"
        rank = TIERS.index(tier)
        charged = rank >= charge_at
        out.append({**f, "severity": tier,
                    "reported": rank >= report_at,
                    "charged": charged,
                    "amount": cfg["price"][tier] if charged else 0})
    return out


def round_half_away(x, q):
    """Round to the nearest multiple of `q`, breaking ties AWAY from zero.

    Python's round() is half-to-even, so a scaled price landing exactly on a half-quantum
    rounds DOWN — silently turning a charged finding into a free one. A residual is visible in
    the report; a finding that quietly stopped costing anything is not. Tie-break in the
    direction that keeps the finding priced, and let the residual carry the cost."""
    n = x / q
    return (math.floor(n + 0.5) if n >= 0 else math.ceil(n - 0.5)) * q


def price_quantum(amounts):
    """The granularity a schedule is actually written in.

    Rounding a scaled price to the nearest whole point is wrong on any rubric that does not
    use whole points: on a 6-point schedule priced in halves, scaling by 0.5 turns a −0.5 into
    0.25, which rounds away to nothing. Infer the step from the prices in front of us and
    round to that instead."""
    vals = [abs(a) for a in amounts if a]
    if not vals:
        return 1.0
    for q in (1.0, 0.5, 0.25, 0.2, 0.1, 0.05, 0.01):
        if all(abs(v / q - round(v / q)) < 1e-9 for v in vals):
            return q
    return 0.01


def target_analysis(units, deductions, target, basis=None, quantum=None):
    """What uniform tariff multiplier would bring the cohort average to `target`?

    Scaling the schedule is the only enforcement route that keeps attribution intact: every
    deduction still names its issue, and only the price moves — identically for everyone.
    Prices are discrete, so the target is often unreachable exactly; the residual is reported,
    never absorbed.
    """
    if not units:
        return {"ok": False, "why": "no units parsed"}
    maxes = [u["max"] for u in units]
    mean_max = sum(maxes) / len(maxes)
    if basis:
        mean_max = float(basis)
    lost = {u["label"]: 0.0 for u in units}
    for d in deductions:
        if d["unit"] in lost:
            lost[d["unit"]] += d["amount"]
    mean_lost = sum(lost.values()) / len(lost)
    # `actual` is what was actually AWARDED (the units' own scores), not what the extractor
    # managed to find. Those differ whenever a document's components do not sum to its
    # header, and building the target math on the extraction would silently mis-state the
    # cohort. The multiplier still has to scale the extracted set, so when the two disagree
    # the multiplier is approximate and the caller is told so rather than left to assume.
    if basis:
        # normalise to the requested basis instead of mixing scales
        actual = sum(u["got"] / u["max"] for u in units) / len(units) * mean_max
        mean_lost = sum(lost[u["label"]] / u["max"] for u in units) / len(units) * mean_max
    else:
        actual = sum(u["got"] for u in units) / len(units)
    extracted_implies = mean_max - mean_lost
    reconciles = abs(actual - extracted_implies) < 0.01
    res = {"ok": True, "units": len(units), "basis": mean_max, "actual": actual,
           "target": float(target), "gap": float(target) - actual, "mean_lost": mean_lost,
           "reconciles": reconciles, "extracted_implies": extracted_implies}
    if mean_lost <= 0:
        res.update({"ok": False, "why": "no deductions to scale — a target cannot be reached "
                                        "by re-pricing when nothing was charged"})
        return res
    if float(target) > mean_max:
        res.update({"ok": False, "why": f"target {target} exceeds the basis {mean_max:g} — "
                                        "unreachable without awarding points for nothing"})
        return res
    k = (mean_max - float(target)) / mean_lost
    # apply the multiplier, rounding to the schedule's own granularity rather than to whole
    # points, then measure what that actually achieves
    q = quantum or price_quantum([d["amount"] for d in deductions])
    rounded, vanished = {u["label"]: 0.0 for u in units}, 0
    for d in deductions:
        if d["unit"] not in rounded:
            continue
        new = round_half_away(d["amount"] * k, q)
        if d["amount"] > 0 and new == 0:
            vanished += 1
        rounded[d["unit"]] += new
    achieved = mean_max - sum(rounded.values()) / len(rounded)
    res.update({"multiplier": k, "achieved": achieved, "quantum": q,
                "residual": float(target) - achieved, "vanished": vanished})
    return res


ALREADY_CODED = re.compile(r"^(unit-[a-z]+|U\d+)$", re.I)


def label_regex(label):
    """Match a unit label as a whole token. Underscore counts as a separator, not a word
    character, for the same reason it does in the coding pass: `unit-a` must be found in
    `unit-a_notes` and must NOT be found inside `unit-ab`."""
    return re.compile(r"(?<![A-Za-z0-9])" + re.escape(label) + r"(?![A-Za-z0-9])", re.I)


def cross_reference_check(per_file):
    """Every round, deterministically: does any unit's own evaluation name another unit?

    Referencing one subject's work inside another's feedback is a never-event. The blind
    auditors are asked to catch it and the lead pass looks for it, but both are judgment; this
    is arithmetic. Catching it in round 1 costs a line — catching it at delivery costs the
    whole grading pass, and missing it costs a student's privacy.

    Only meaningful when each file IS one unit. A single evaluations.md covering the whole
    cohort mentions every unit by construction and is not a letter.
    """
    labels = [lab for lab, _ in per_file]
    hits = []
    for lab, text in per_file:
        for other in labels:
            if other == lab:
                continue
            for m in label_regex(other).finditer(text):
                hits.append({"unit": lab, "names": other,
                             "line": text.count("\n", 0, m.start()) + 1})
    return hits


def code_unit_labels(units, deductions):
    """Column headers must never be identities — but do not invent a SECOND code for labels
    that are already coded.

    In the one-file-per-unit layout a unit's label is its directory name, which in a real
    workspace is a person's name. Those must be relabelled. But when the workspace was built
    by `code-units.py` the directories are already `unit-a`, `unit-b`, … — non-identifying,
    and durably mapped back to people in that pass's `map.json`. Renaming those to `U1..Un`
    adds a second hop whose legend lives only in a terminal, so the instructor holds a matrix
    saying `U1`, a letter saying `unit-a`, and no saved link between them. Leave coded labels
    alone.
    """
    if all(ALREADY_CODED.match(u["label"] or "") for u in units):
        return {}                                  # already non-identifying; one hop is enough
    legend = {}
    for i, u in enumerate(units, 1):
        coded = f"U{i}"
        legend[coded] = u["label"]
        u["label"] = coded
    back = {v: k for k, v in legend.items()}
    for d in deductions:
        d["unit"] = back.get(d["unit"], d["unit"])
    return legend


def die(msg):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(2)


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
            units.append({"label": f"{src}:U{len(units) + 1}", "got": float(m.group("got")),
                          "max": float(m.group("max")), "source": src})
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
        got, mx = float(comp.group("got")), float(comp.group("max"))
        name = comp.group("name").strip()
        if got >= mx:
            continue
        body = LEAD.sub("", raw[comp.end():])
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
            label = labels[0] if labels else f"(unnamed issue in {name})"
            deductions.append({"unit": units[cur]["label"], "component": name,
                               "amount": mx - got, "label": label.strip(),
                               "norm": normalize(issue_name(label)), "inferred": True})
    if not units:
        return parse_file_as_unit(path, text)
    return units, deductions, names


def parse_file_as_unit(path, text):
    """One file per unit — the layout this method's own workspaces use
    (`working-notes/<unit>/draft-evaluation.md`). There is no `## Name — 96/100` heading to
    find because the unit is the directory, so the label comes from the path and the unit
    total is the sum of its component lines."""
    p = Path(path)
    label = p.parent.name if p.parent.name not in ("", ".", "/") else p.stem
    got = mx = 0
    deductions = []
    for raw in text.splitlines():
        comp = COMPONENT.match(raw)
        if not comp:
            continue
        g, m = float(comp.group("got")), float(comp.group("max"))
        got += g
        mx += m
        if g >= m:
            continue
        body = LEAD.sub("", raw[comp.end():])
        marked = [float(d.group("amt")) for d in DEDUCT.finditer(body)
                  if float(d.group("amt")) > 0]
        labels = [b.group("text").strip() for b in BOLD.finditer(body)]
        labels = [l for l in labels if len(l) > 3] or labels
        name = comp.group("name").strip()
        if marked and abs(sum(marked) - (m - g)) < 0.001:
            for i, amt in enumerate(marked):
                lab = labels[i] if i < len(labels) else (labels[0] if labels else body.strip()[:160])
                deductions.append({"unit": label, "component": name, "amount": amt,
                                   "label": lab, "norm": normalize(issue_name(lab)),
                                   "inferred": False})
        else:
            lab = labels[0] if labels else f"(unnamed issue in {name})"
            deductions.append({"unit": label, "component": name, "amount": m - g,
                               "label": lab, "norm": normalize(issue_name(lab)),
                               "inferred": True})
    if mx == 0:
        return [], [], []
    return ([{"label": label, "got": got, "max": mx, "source": p.parent.name}],
            deductions, [label])


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
    ap.add_argument("--target-average", type=float, metavar="N",
                    help="expected cohort average; reports the gap and the uniform tariff "
                         "multiplier that would close it. Reports; never decides.")
    ap.add_argument("--basis", type=float, metavar="N",
                    help="score basis for the target (default: the units' own max)")
    ap.add_argument("--tolerance", type=float, default=None, metavar="N",
                    help="gap below which the target is treated as met "
                         "(default: 1%% of the basis — 1.0 on a /100 rubric, 0.06 on a /6 one)")
    ap.add_argument("--show-preset", metavar="NAME",
                    help="print a strictness preset's schedule and exit")
    ap.add_argument("--self-test", action="store_true", help="fixture check; exits nonzero on failure")
    if "--self-test" in sys.argv[1:]:
        return self_test()
    if "--show-preset" in sys.argv[1:]:
        name = sys.argv[sys.argv.index("--show-preset") + 1]
        if name not in PRESETS:
            die(f"unknown preset '{name}' (choose from: {', '.join(PRESETS)})")
        c = PRESETS[name]
        print(f"preset: {name}")
        print(f"  report threshold : {c['report']} and above  (nothing below this is hidden — "
              f"it is demoted to a zero-point note)")
        print(f"  charge threshold : {c['charge']} and above")
        print(f"  prices           : blocker −{c['price']['blocker']}  "
              f"minor −{c['price']['minor']}  note −{c['price']['note']}")
        print(f"  waiver posture   : {c['waiver']}")
        print("  fixed at every preset: if no specific issue can be named, the points are "
              "awarded. That is the attribution guarantee, not a setting.")
        return 0
    args = ap.parse_args()

    all_units, all_ded, all_names, per_file = [], [], [], []
    for f in args.files:
        u, d, n = parse(f)
        if len(u) == 1:                      # one file, one unit -> a letter-shaped artifact
            per_file.append((u[0]["label"],
                             Path(f).read_text(encoding="utf-8", errors="replace")))
        all_units += u
        all_ded += d
        all_names += n
    if not all_units:
        print("no unit sections found (expected `## <label> — NN/NN`)")
        return 1
    xrefs = cross_reference_check(per_file)
    if xrefs:
        print(f"** NEVER-EVENT: {len(xrefs)} cross-reference(s) — a unit's own evaluation names")
        print("   another unit. No subject may be named or identifiable in another subject's")
        print("   feedback. Fix these before anything is delivered:")
        for h in xrefs[:20]:
            print(f"     {h['unit']}  names  {h['names']}  at line {h['line']}")
        if len(xrefs) > 20:
            print(f"     …and {len(xrefs) - 20} more")
        print()
    legend = code_unit_labels(all_units, all_ded)
    if legend:
        print("These units were NOT already coded, so they were relabelled for the written")
        print("artifacts. Keep this legend — nothing else records it:")
        for coded, orig in legend.items():
            print(f"  {coded} = {orig}")
        print("  (Grading coded units instead — see the setup skill's coded-units pass — "
              "avoids this second mapping entirely.)")
        print()

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
    unnamed = len([d for d in all_ded if d["label"].startswith("(unnamed issue in ")])
    if unnamed:
        print(f"** {unnamed} of {len(all_ded)} deduction(s) NAME NO ISSUE. The method's central "
              f"rule is that every point removed is tied to a specific named issue; a "
              f"deduction that names none cannot be clustered, cannot be compared across "
              f"units, and cannot be defended to the subject. Fix the drafts, not the matrix.")

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

    tol = args.tolerance if args.tolerance is not None else (args.basis if args.basis else 100) / 100.0
    if args.target_average is not None:
        ta = target_analysis(all_units, all_ded, args.target_average, args.basis)
        tol = args.tolerance if args.tolerance is not None else ta.get("basis", 100) / 100.0
        print("=== Expected average ===")
        if not ta.get("ok"):
            print(f"  actual {ta.get('actual', float('nan')):.2f} vs target "
                  f"{args.target_average:g} — cannot re-price: {ta['why']}")
        else:
            print(f"  units {ta['units']}  ·  basis {ta['basis']:g}  ·  "
                  f"actual {ta['actual']:.2f}  ·  target {ta['target']:g}  ·  "
                  f"gap {ta['gap']:+.2f}")
            if not ta["reconciles"]:
                print(f"  CAUTION: the extracted deductions imply "
                      f"{ta['extracted_implies']:.2f}, not the awarded {ta['actual']:.2f} — "
                      f"the extraction is incomplete, so the multiplier below is approximate. "
                      f"Fix the parse or price by hand.")
            if abs(ta["gap"]) <= tol:
                print(f"  within tolerance ({tol:g}, 1% of basis) — no re-pricing indicated.")
            else:
                print(f"  uniform tariff multiplier that would close it: "
                      f"x{ta['multiplier']:.3f}")
                print(f"  after rounding to the schedule's own step ({ta['quantum']:g}) it "
                      f"achieves {ta['achieved']:.2f} (residual {ta['residual']:+.2f})")
                if ta["vanished"]:
                    print(f"  WARNING: {ta['vanished']} deduction(s) would round to zero — "
                          f"they become notes, so say so in the letters.")
                print("  THIS SCRIPT DOES NOT APPLY IT. The enforcement choice is the "
                      "human's; see the ruling queue.")
        print()
    if args.emit_matrix:
        write_matrix(args.emit_matrix, all_units, clusters, all_names)
        print(f"matrix written: {args.emit_matrix}")
    if args.emit_rulings:
        n = write_rulings(args.emit_rulings, all_units, clusters, all_names,
                          target_analysis(all_units, all_ded, args.target_average, args.basis)
                          if args.target_average is not None else None,
                          tol)
        print(f"ruling requests written: {args.emit_rulings} ({n} question(s) for the human)")
    print("=== 3. Per-unit deduction inventory ===")
    print(f"  {'unit':6s} {'score':>9s} {'deductions':>11s} {'points lost':>12s}")
    for u in all_units:
        n = len([d for d in all_ded if d["unit"] == u["label"]])
        print(f"  {u['label']:6s} {u['got']:>5g}/{u['max']:<3g} {n:>11d} {lost[u['label']]:>12g}")
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
        charged = {}
        for m in c["members"]:
            charged[m["unit"]] = charged.get(m["unit"], 0) + m["amount"]
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


def write_rulings(path, units, clusters, names, target=None, tolerance=1.0):
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
    if target and target.get("ok") and abs(target["gap"]) > tolerance:
        L += ["## Q0 — EXPECTED AVERAGE NOT MET", "",
              f"Cohort average is **{target['actual']:.2f}** against a target of "
              f"**{target['target']:g}** (gap {target['gap']:+.2f}, basis "
              f"{target['basis']:g}).", "",
              "Three ways to respond. This is your decision, not the harness's:", "",
              f"- [ ] **Scale the schedule** — multiply every family's price by "
              f"**x{target['multiplier']:.3f}**, re-derive every grade. Achieves "
              f"{target['achieved']:.2f} after rounding (residual "
              f"{target['residual']:+.2f})."
              + (f" **{target['vanished']} deduction(s) would round to zero** and become "
                 f"notes." if target["vanished"] else "")
              + " Attribution survives: each deduction still names its issue, only the price "
                "moves, identically for everyone.",
              "- [ ] **Adjust individual grades** to hit the number exactly. This **breaks "
              "the discrete attributable deduction rule** — points would move without a "
              "named issue behind them. Available, but the cost is real and it should be "
              "recorded in the matrix.",
              "- [ ] **Advisory only** — record the gap as evidence the schedule may be "
              "miscalibrated and change nothing.", "",
              "Before choosing: a cohort can genuinely be excellent or weak. Forcing the "
              "average then misreports them, and the evidence in these units is the better "
              "guide to which is happening.", ""]
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

        # one-file-per-unit layout: what this method's own workspaces actually produce
        wn = Path(tmp) / "working-notes" / "student-a"
        wn.mkdir(parents=True)
        (wn / "draft-evaluation.md").write_text(
            "# Draft evaluation\n\n"
            "- **Data cleaning: 5/5** — crisp.\n"
            "- **Analysis correctness: 4/5** — **Missing degrees of freedom (-1).**\n"
            "- **Figures: 5/5** — all captioned.\n", encoding="utf-8")
        fu, fd, fn = parse(wn / "draft-evaluation.md")
        check("a per-unit file parses without a `## Name — NN/NN` heading", len(fu) == 1)
        check("the unit label comes from its directory", fu[0]["label"] == "student-a")
        check("the unit total is the sum of its components",
              fu[0]["got"] == 14 and fu[0]["max"] == 15)
        check("its deduction is found and attributed to that unit",
              len(fd) == 1 and fd[0]["amount"] == 1 and fd[0]["unit"] == "student-a")
        check("full-credit component lines produce no deduction",
              all(d["component"] != "Data cleaning" for d in fd))

        # the never-event, checked deterministically every round rather than left to judgment
        xr = cross_reference_check([("unit-a", "Unlike unit-b, this stalled.\nmore\n"),
                                    ("unit-b", "Clean work.\n")])
        check("a unit's evaluation naming another unit is caught", len(xr) == 1)
        check("and it reports which unit, which other, and where",
              xr[0]["unit"] == "unit-a" and xr[0]["names"] == "unit-b" and xr[0]["line"] == 1)
        check("a clean set produces no cross-reference finding",
              cross_reference_check([("unit-a", "Good.\n"), ("unit-b", "Good.\n")]) == [])
        check("a label is matched as a whole token, so unit-a is not found inside unit-ab",
              cross_reference_check([("unit-ab", "discussing my own unit-ab work\n"),
                                     ("unit-a", "x\n")]) == [])
        check("but a genuine mention of a longer label is still caught",
              len(cross_reference_check([("unit-a", "see unit-ab elsewhere\n"),
                                         ("unit-ab", "x\n")])) == 1)
        check("underscore counts as a separator when matching a label",
              len(cross_reference_check([("unit-a", "unit-b_notes\n"), ("unit-b", "x\n")])) == 1)

        # a deduction that names no issue must say so, not borrow a sentence of prose
        unnamed_ws = Path(tmp) / "unnamed" / "alpha"
        unnamed_ws.mkdir(parents=True)
        (unnamed_ws / "draft-evaluation.md").write_text(
            "- **Write-up clarity: 4/5** — methods and results were thoughtful but the "
            "confounding discussion drifted.\n", encoding="utf-8")
        uu, ud, un = parse(unnamed_ws / "draft-evaluation.md")
        check("an unnamed deduction is labelled as unnamed, not given a prose fragment",
              len(ud) == 1 and ud[0]["label"] == "(unnamed issue in Write-up clarity)")
        check("and it names the component so the row is still meaningful",
              "Write-up clarity" in ud[0]["label"])

        # regressions for the defects the release dogfood found
        check("die() exists, so a bad preset is a message not a NameError",
              callable(globals().get("die")))
        bold = Path(tmp) / "bold" / "alpha"
        bold.mkdir(parents=True)
        (bold / "draft-evaluation.md").write_text(
            "- **Data cleaning: 5/5** — fine.\n"
            "- **Analysis correctness: 4/5** — **Missing degrees of freedom (-1).**\n",
            encoding="utf-8")
        bu, bd, bn = parse(bold / "draft-evaluation.md")
        check("a bolded component line does not swallow the issue label",
              len(bd) == 1 and issue_name(bd[0]["label"]) == "Missing degrees of freedom")
        already = [{"label": "unit-a", "got": 5, "max": 6}, {"label": "unit-b", "got": 6, "max": 6}]
        check("a workspace that is already coded is NOT coded a second time",
              code_unit_labels(already, []) == {}
              and [u["label"] for u in already] == ["unit-a", "unit-b"])
        bl = code_unit_labels(bu, bd)
        check("unit labels are coded, never the directory name",
              bu[0]["label"] == "U1" and bl["U1"] == "alpha")
        check("deductions follow the relabel", bd[0]["unit"] == "U1")
        mb = Path(tmp) / "bold-matrix.md"
        write_matrix(mb, bu, cluster(bd, 0.62), bn)
        check("and the written matrix carries no directory name",
              "alpha" not in mb.read_text() and "| U1 |" in mb.read_text())

        multi = [{"unit": "U1", "component": "A", "amount": 1.0, "label": "Missing df",
                  "norm": normalize("Missing df")},
                 {"unit": "U1", "component": "B", "amount": 2.0, "label": "Missing df",
                  "norm": normalize("Missing df")},
                 {"unit": "U2", "component": "A", "amount": 2.0, "label": "Missing df",
                  "norm": normalize("Missing df")}]
        mu = [{"label": "U1", "got": 7, "max": 10}, {"label": "U2", "got": 8, "max": 10}]
        mm = Path(tmp) / "multi.md"
        write_matrix(mm, mu, cluster(multi, 0.62), [])
        check("a price difference is flagged even when one unit has two instances",
              "PRICE DIFFERS" in mm.read_text())

        # small-basis rubrics: a 6-point schedule priced in halves must not be rounded to
        # whole points, and a tie must not silently waive a charged finding
        check("the schedule's own step is inferred, not assumed to be 1",
              price_quantum([1.0, 0.5, 1.5]) == 0.5
              and price_quantum([1, 2, 3]) == 1.0
              and price_quantum([0.25, 0.75]) == 0.25
              and price_quantum([]) == 1.0)
        check("a tie rounds away from zero, so a charged finding stays charged",
              round_half_away(0.25, 0.5) == 0.5 and round_half_away(-0.25, 0.5) == -0.5)
        small_u = [{"label": "U1", "got": 5.0, "max": 6}, {"label": "U2", "got": 5.5, "max": 6},
                   {"label": "U3", "got": 4.5, "max": 6}]
        small_d = [{"unit": "U1", "amount": 1.0}, {"unit": "U2", "amount": 0.5},
                   {"unit": "U3", "amount": 1.5}]
        st = target_analysis(small_u, small_d, 5.5)
        check("a half-point schedule keeps its granularity", st["quantum"] == 0.5)
        check("and no charged finding rounds away to nothing", st["vanished"] == 0)
        check("the miss is reported as residual, not absorbed",
              abs(st["residual"] - 0.1667) < 0.01)
        big = target_analysis([{"label": "U1", "got": 98, "max": 100},
                               {"label": "U2", "got": 97, "max": 100}],
                              [{"unit": "U1", "amount": 2.0}, {"unit": "U2", "amount": 3.0}], 95)
        check("whole-point schedules are unaffected by the change",
              big["quantum"] == 1.0 and abs(big["achieved"] - 95.0) < 0.001)

        bt = target_analysis([{"label": "U1", "got": 18, "max": 20}],
                             [{"unit": "U1", "amount": 2.0}], 92, basis=100)
        check("--basis rescales the actual average, not just the maximum",
              abs(bt["actual"] - 90.0) < 0.001 and abs(bt["gap"] - 2.0) < 0.001)

        # --- strictness presets -------------------------------------------------------
        # The load-bearing property: the SAME finding set at every preset. Strictness must
        # change what a defect costs, never whether it was seen.
        synth = [{"severity": "blocker", "issue": "a"}, {"severity": "minor", "issue": "b"},
                 {"severity": "note", "issue": "c"}]
        priced = {name: apply_preset(synth, name) for name in ("lenient", "standard", "strict")}
        totals = {k: sum(x["amount"] for x in v) for k, v in priced.items()}
        check("every preset yields the identical finding set",
              all(len(v) == 3 for v in priced.values())
              and all([x["issue"] for x in v] == ["a", "b", "c"] for v in priced.values()))
        check("no preset hides a finding from the report",
              all(all(x["reported"] for x in v) for v in priced.values()))
        check("preset totals are ordered lenient < standard < strict",
              totals["lenient"] < totals["standard"] < totals["strict"])
        check("hand-computed preset totals", (totals["lenient"], totals["standard"],
                                              totals["strict"]) == (1, 3, 6))
        check("lenient demotes a minor to a zero-point note, it does not drop it",
              [x for x in priced["lenient"] if x["severity"] == "minor"][0]["amount"] == 0
              and [x for x in priced["lenient"] if x["severity"] == "minor"][0]["reported"])
        check("an unrecognised severity defaults to minor, never to free",
              apply_preset([{"severity": "wat", "issue": "z"}], "strict")[0]["amount"] == 2)

        # --- expected-average calibration ----------------------------------------------
        # fixture: Ada 98/100 (lost 2), Grace 97/100 (lost 3) -> mean_lost 2.5, actual 97.5
        ta = target_analysis(units, ded, 95)
        check("actual cohort average computed", abs(ta["actual"] - 97.5) < 0.001)
        check("multiplier is hand-computable: (100-95)/2.5 = 2.0",
              abs(ta["multiplier"] - 2.0) < 0.001)
        check("scaling by that multiplier lands exactly on target",
              abs(ta["achieved"] - 95.0) < 0.001 and abs(ta["residual"]) < 0.001)
        check("nothing vanishes when scaling up", ta["vanished"] == 0)

        up = target_analysis(units, ded, 99)
        check("raising the target shrinks the tariff: (100-99)/2.5 = 0.4",
              abs(up["multiplier"] - 0.4) < 0.001)
        check("discrete rounding leaves a reported residual, not a fudge",
              abs(up["achieved"] - 99.5) < 0.001 and abs(up["residual"] + 0.5) < 0.001)
        check("deductions that round to zero are counted and surfaced", up["vanished"] == 3)

        check("actual is what was awarded, not what the extractor found",
              abs(ta["actual"] - 97.5) < 0.001 and ta["reconciles"] is True)
        skew = [dict(d) for d in ded][:-1]          # drop a deduction: extraction now short
        bad = target_analysis(units, skew, 95)
        check("an incomplete extraction is flagged, not silently used",
              bad["reconciles"] is False
              and abs(bad["actual"] - 97.5) < 0.001
              and bad["extracted_implies"] > bad["actual"])
        check("a target above the basis is refused, not approximated",
              target_analysis(units, ded, 105)["ok"] is False)
        check("with no deductions there is nothing to scale",
              target_analysis(units, [], 90)["ok"] is False)

        rq2 = Path(tmp) / "rulings-target.jsonl.md"
        write_rulings(rq2, units, cluster(ded, 0.62), names, target_analysis(units, ded, 95), 1.0)
        rt2 = rq2.read_text()
        check("a missed target becomes Q0 in the ruling queue", "EXPECTED AVERAGE NOT MET" in rt2)
        check("Q0 offers all three enforcement routes",
              "Scale the schedule" in rt2 and "Adjust individual grades" in rt2
              and "Advisory only" in rt2)
        check("Q0 states the cost of the attribution-breaking route",
              "breaks the discrete attributable deduction rule" in rt2)
        check("Q0 warns that a cohort may genuinely differ from the target",
              "genuinely be excellent or weak" in rt2)
        rq3 = Path(tmp) / "rulings-ontarget.md"
        write_rulings(rq3, units, cluster(ded, 0.62), names, target_analysis(units, ded, 97), 1.0)
        check("a target within tolerance raises no question",
              "EXPECTED AVERAGE NOT MET" not in rq3.read_text())

    print(f"self-test: {checks - len(failures)}/{checks} checks passed")
    for f in failures:
        print(f"  FAIL: {f}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
