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
basis** — larger than every other cause combined, including missing precedents.

Instances still belong in the evidence; they justify the charge and they belong in the
letter. They do not each carry a price.

## Building it

```
python3 scripts/reconcile-deductions.py working-notes/*/draft-evaluation.md \
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
`working-notes/ruling-requests.md`. Each one carries the family, the per-unit charges, and
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
- the rebuilt matrix has no unarbitrated flag and no cell moved since the previous round.

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
