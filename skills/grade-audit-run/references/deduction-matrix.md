# The deduction matrix — cross-unit reconciliation, and the questions it raises

The blind fan-out is what makes each judgment honest. It is also what makes the set
*unfair*, and no amount of per-unit rigour fixes that: an auditor that cannot see unit B
cannot know that unit B was charged −1 for the thing it just charged −3. Consistency is not
something a blind auditor can be asked to remember. It has to be a structure.

The structure is a **family × unit matrix**, built once per round, after the fan-out.

## The one rule that does most of the work

> **One charge per (family, unit) — never per instance.**

Three blanks in one workbook is one *unfilled fields* charge, not three. This is not
leniency; it is the difference between grading a defect and grading how many times a defect
happened to surface. Measured on a real cohort, charging per instance instead of per family
moved the mean absolute error against the issued grades from **3.6 to 11.4 points on a /90
basis** on the one cohort this was measured against. Withheld precedents accounted for a
comparable share of the same gap; the two overlap and cannot be attributed independently.

Instances still belong in the evidence; they justify the charge and they belong in the
letter. They do not each carry a price.

## The cross-reference check — run before anything else

Every time the matrix is built, each unit's own evaluation is searched for any *other* unit's
label. A hit is a **never-event**: no subject may be named or identifiable in another
subject's feedback, and a comparison like "unlike unit-b, the derivation stalled" carries a
pointer to another student's work into this student's letter.

This is deliberately mechanical. The blind auditors are told to catch it and the lead pass
looks for it, but both are judgment; this is arithmetic, it runs every round, and it costs
nothing. The same check runs again at delivery in `code-units.py --personalize`, which refuses
to write any letter while one is outstanding — but catching it in round 1 costs a line, and
catching it at delivery costs the whole grading pass.

No naming scheme prevents this, which is worth being clear about: the defect is in the
sentence, not the label. Rename the unit and the letter still points at another student.

**What this check does NOT catch — state it plainly rather than let it be assumed.** It
searches for other units' *labels*. Measured against four ways one student can appear in
another's feedback, it catches one:

| how the reference appears | caught here? |
| --- | --- |
| names another unit's code — "unlike unit-b" | **yes** |
| names the student — "unlike Grace's proof" | no, here; **yes at delivery**, where the map is in hand |
| identifies without naming — "the only submission that used a permutation test" | **no** |
| quotes another student's work verbatim | **no** |

The last two are judgment, which is what the auditors' cross-contamination check and the lead
pass are for; the harness cannot mechanise them and does not pretend to. The name case is
deliberately split: at matrix time the grading session is denied the map — that is the point
of keeping it outside the workspace — so it cannot search for names; `--personalize` has the
map legitimately and refuses on real names as well as codes.

## Strictness: the preset seeds the schedule, the ruling overrides it

The task CLAUDE.md carries a preset. It sets two thresholds and a starting price per severity
tier:

| preset | charge threshold | blocker / minor / note | waiver posture |
|---|---|---|---|
| `lenient` | blocker only | −1 / 0 / 0 | waive where a rule plausibly applies |
| `standard` | minor and above | −2 / −1 / 0 | waive where a rule states it |
| `strict` | note and above | −3 / −2 / −1 | waive only on an explicit written ruling |

`python3 "<this skill's directory>/scripts/reconcile-deductions.py" --show-preset strict` prints any of them.

Two properties that are not negotiable by preset:

- **The report threshold stays at `note`.** A lower preset moves a finding from *charged* to
  *noted*; it never removes it from the letter. Strictness governs what a defect costs, not
  whether the harness looked. If a user raises the report threshold to cut noise, the round
  report states what that suppressed and how many.
- **An unnamed issue is always awarded.** At every preset. That is the attribution guarantee.

These are seeds. The moment a ruling prices a family, the ruling wins and the schedule row
records it — that is the whole point of having a Ruling column.

## Expected average — a calibration signal, not a constraint

If the task sets an expected average, run the check after the matrix is priced:

```
python3 "<this skill's directory>/scripts/reconcile-deductions.py" \
    working-notes/*/draft-evaluation.md \
    --target-average 92 --basis 100 --emit-rulings working-notes/ruling-requests.md
```

It reports the cohort average (computed from what was **awarded**, not from what the parser
extracted — and it says so loudly when those disagree), the gap, and the uniform tariff
multiplier that would close it, with the residual left after rounding. **It applies nothing.**

Two things it gets right that are easy to get wrong on a small rubric. It rounds to **the
schedule's own step**, inferred from the prices in front of it — a 6-point rubric priced in
half-points stays in half-points instead of being rounded to whole points, which would waive
most of its findings. And it breaks ties **away from zero**, so a scaled price landing exactly
half-way keeps the finding charged: a residual is visible in the report, a finding that
quietly stopped costing anything is not. The tolerance is 1% of the basis, not a fixed point,
because 1.0 is 1% of a /100 rubric and 17% of a /6 one. A gap beyond tolerance becomes `Q0` in the ruling queue with three routes:

- **Scale the schedule** — one multiplier, every family, re-derive every grade. Attribution
  survives: each deduction still names its issue and only the price moves, identically for
  everyone. This is calibration, not curving.
- **Adjust individual grades** — hits the number exactly and breaks the discrete attributable
  deduction rule, because points then move without a named issue behind them. It is offered,
  with that cost stated, and the choice is recorded in the matrix.
- **Advisory only** — record the gap as evidence the schedule may be miscalibrated.

Say the quiet part when you present it: **a cohort can genuinely be excellent or weak, and
forcing the average then misreports them.** The evidence in the units is the better guide to
which is happening than the distance from a number set before anyone read the work.

## Building it

```
python3 "<this skill's directory>/scripts/reconcile-deductions.py" \
    working-notes/*/draft-evaluation.md \
    --emit-matrix working-notes/deduction-matrix.md \
    --emit-rulings working-notes/ruling-requests.md
```

The generator clusters deductions into families **by their named issue**, not by their
evidence — the evidence differs in every unit by construction, and clustering on it splits
one family across several rows, which is exactly the state the matrix exists to make
visible. It fills the cells. It never fills the **Ruling** column: that is the lead grader's
and the human's.

Rows are flagged automatically in two ways, and both are questions, not verdicts:

- **`PRICE DIFFERS — arbitrate`** — the same family charged different amounts in different
  units. Either a justified difference or an unfairness, and it must be one of the two, in
  writing.
- **`not charged everywhere`** — charged in some units, absent in others. Either those units
  genuinely do not have the defect, or nobody looked. The blind auditors cannot tell you
  which.

## Arbitration — what the lead may settle alone

The lead grader may:

- **Normalize a price** where the instruction files already fix it, citing the rule.
- **Propagate a waiver** under everywhere-or-nowhere discipline, per family, naming both
  units.
- **Collapse instances** into their family charge.
- **Record an explicit non-deduction** — the "Explicitly not deducted" table. A defect
  found and deliberately not charged must be written down as a decision; silence reads as
  an oversight to the next round and to the next assignment.

The lead grader may **not** invent a price the instruction files do not support, and may not
decide a fairness question by preference. When it extends a ruling by analogy, it records
the extension and **flags it for reversal** — the real runs do this verbatim: *"waived by
consistency extension (lead-grader call — FLAGGED, revert if he sees a distinction)."*

## The ruling queue — questions for the human

Everything the lead may not settle becomes a numbered question in
`working-notes/ruling-requests.md`. The generator writes the questions it can see from the
matrix alone; **the lead adds the ones only a cross-unit read reveals**, and the orchestrator
appends them to the same file — otherwise they live only in the lead's report and never reach
the human who has to answer them. Each one carries the family, the per-unit charges, and
three pre-drafted dispositions (price for all / genuinely different / waive everywhere) so
answering costs a sentence.

Ask the human when:

1. **Two units were charged differently for the same item.** The most common and the most
   important — this is the fairness question, and it is cheap to answer and expensive to
   guess.
2. **A family is charged in some units and not others**, and the difference is not visible
   in the evidence.
3. **A defect class has no precedent** — nothing in the instruction files prices it. Do not
   set the price by acting; a price set by accident becomes a precedent nobody chose.
4. **A finding sits on a policy boundary** — is a session-log gap a disclosure failure or a
   different thing entirely? Auditors flag their own uncertainty here; treat those flags as
   queue items, not noise.
5. **A waiver's scope is unclear** — does it cover a whole absent section, or only a blank
   field?

Answers come back as numbered, dated rulings in the matrix, and every ruling is a write-back
candidate (`references/write-back.md`). That is the loop that made the difference: a run
given the prior rounds' rulings agreed with the issued grades to **3.0 points**; the same
harness without them diverged by **11.4** and changed one outcome band.

## Recursion — the matrix is part of what must converge

A round is not done when the units are clean. It is done when the units are clean **and the
matrix is stable**. Applying a ruling re-prices cells, which can create a new discrepancy
elsewhere, which is a new question. So:

```
fan out → build matrix → arbitrate → ask the human → apply rulings
   → re-audit every re-priced unit, whole → rebuild matrix → compare
```

Stop when **both** hold on the same pass:

- no unit produces a blocker, **and**
- the rebuilt matrix has no unarbitrated flag, **no open ruling request**, and no cell moved
  since the previous round.

That is a restatement of the one rule in `references/convergence-and-bounding.md`; if they
ever disagree, that file wins.

Record `matrix cells moved` and `open ruling requests` as columns in
`working-notes/round-metrics.md`, alongside blockers and minors. A cell-movement count that
falls to zero is the convergence signal; one that oscillates means two rulings are fighting,
and that is itself a question for the human.

**The human closes the loop, not the counter.** The recorded runs ended at round 9 on the
human's judgment — *"the latest changes seem minor and so I'm not concerned"* — with round
10 not run. Offer that close explicitly once cell movement is small and no blockers remain:
show the diff of what moved, and let the human decide whether it is worth another pass.
Bounding still applies (`references/convergence-and-bounding.md`): if the matrix is only
moving because previous rulings keep re-opening each other, stop and diff what ships.
