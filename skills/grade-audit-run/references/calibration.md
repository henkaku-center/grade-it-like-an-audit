# Calibration mode — the harness earns trust against the human, quantitatively

Before the harness grades anything that counts, the human grades 3–5 units themselves; the
harness grades the same units blind; a deterministic script reports how well they agree.
The direction of trust is the point: the harness is measured against the human's judgment,
not the other way around. Do not suggest proceeding to real grading until the human has
seen the numbers.

Related: to compare a finished harness run against grades that were already issued — a
fidelity check rather than a calibration — use `scripts/compare-runs.py`. It aligns units,
proposes finding-pairs by component, and emits a worksheet for adjudication; it never
decides a pairing itself, because lexical similarity demonstrably cannot.

## Procedure

1. **Intake.** The human picks 3–5 units they have graded (or will grade now) and confirms
   the rubric/criteria and ground-truth sources. Their scores go in a file the harness must
   NOT see yet — ask them to keep it out of the workspace, or write it to
   `working-notes/calibration/human-scores.csv` only AFTER step 2 completes.
2. **Blind grading.** Draft an evaluation for each calibration unit exactly as a real run
   would (evidence ledger included), with one hard rule: nothing in any prompt or context
   names or contains the human's scores. Auditor-style isolation applies — if the human's
   scores are anywhere in the workspace already, do not open that file, and say so in the
   report ("the blind-grading claim is itself a claim; here is what I did and did not
   read").
3. **Compare.** Write `working-notes/calibration/scores.csv` with header `unit,human,ai`,
   then run:

   ```
   python3 "<this skill's directory>/scripts/agreement.py" working-notes/calibration/scores.csv --scale-min 0 --scale-max <top of scale>
   ```

   The script prints per-unit diffs, mean absolute difference, exact agreement, Spearman
   rho, and quadratic-weighted kappa with an interpretation band — computed, not asserted.
   Pass `--scale-min/--scale-max` so the printed scale is honest and out-of-range scores are
   caught. Note what it does *not* do: quadratic-weighted kappa here is invariant to the
   declared range (the weight normalizer cancels, and expected agreement is built from the
   observed marginals), so the coefficient itself will not move.
4. **Report.** Show: the script output verbatim; for every unit where scores differ, BOTH
   rationales side by side (the human can see exactly where the harness reads the rubric
   differently); and the script's own small-n caveat. Then ask the human how to proceed:
   - **Good agreement, acceptable reasoning** → proceed to real runs; save the calibration
     result in `working-notes/calibration/` as the baseline.
   - **Systematic disagreement** (harness consistently harsher/softer, or misreading a
     criterion) → the disagreement is calibration data: tighten the task `CLAUDE.md`
     (criteria wording, waivers, "what the subject was owed"), then re-calibrate on the
     same units. Rubric fixes discovered here are write-back material.
   - **Scattershot disagreement** → the criteria may be unscoreable (the twelve-point-spread
     signature). Route to the criteria audit before anything else: for each criterion, does
     the evidence it grades actually exist in the collected artifacts?

## Rules

- The human's scores are never training data and never quoted into instruction files —
  calibration output stays in `working-notes/calibration/`.
- Re-run calibration after any substantial rubric change, and once per new cohort/task if
  the runs are recurring. State the cost honestly: one calibration ≈ one mini-run over 3–5
  units.
- Never smooth the numbers. If kappa comes back "fair," the report says fair.
