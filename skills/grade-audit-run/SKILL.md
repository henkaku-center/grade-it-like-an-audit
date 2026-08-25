---
name: grade-audit-run
description: Run one audit round (or a calibration or reverse-audit pass) in a grade-it-like-an-audit workspace. Use when the user wants to audit draft evaluations or grades, run the pre-send audit, re-audit revised units, check convergence, calibrate the harness against their own grading, or have their hand-written evaluations fact-checked. Requires a workspace set up by grade-audit-setup (or equivalent CLAUDE.md structure).
argument-hint: "[round | calibrate | check-mine]"
---

# grade-audit-run — one audit round, end to end

You orchestrate the audit harness. You do not audit units yourself — independence is by
construction: fresh subagents, each handed only its own unit. The human owns every judgment
call; you own the ceremony.

Modes: default = an audit round over drafted evaluations. `calibrate` = agreement check
against human-graded units (read `references/calibration.md`). `check-mine` = audit
evaluations the human wrote (read `references/reverse-audit.md`).

## Protocol for an audit round

1. **Preflight.** Read the root and task `CLAUDE.md`. Confirm: units are drafted; each unit
   has an evidence ledger; the criteria were audited at setup (each criterion names the
   artifact that evidences it). Anything missing → stop and tell the user what to produce
   first; do not audit undrafted work. Determine the round number from
   `working-notes/*/audit-round*` files — all state lives in inspectable files, never in
   your memory of the session. **If the inputs are coded units**, confirm the coding pass's
   byte-identity line (`N/N copied files hash-match their source`) in its scan report before
   fanning out. Without that proof you cannot tell a student's blank field from one the
   tooling removed — and the auditors will be asked to charge it. No proof → re-run the
   coding pass or grade the originals; do not guess.
2. **Lead normalize.** Skim all drafts for structural conformance to the output format
   (sections present, tables well-formed). Fix format only — never content — and note what
   you touched.
3. **Fan out.** One `unit-auditor` subagent per unit, in parallel, each prompted with ONLY
   its own unit's paths **and the task's two strictness thresholds** (report / charge, from
   the task CLAUDE.md's strictness block; default `standard` if absent). State the rule in
   the prompt: below the charge threshold, report as a zero-point note with evidence — demote,
   never drop. Construction rules in `references/fan-out-protocol.md` — follow the
   path-isolation rules exactly; they are the blindness guarantee.
4. **Build the deduction matrix.** Blind auditors cannot police fairness across units, so
   consistency is made structural instead. Run
   `python3 "<this skill's directory>/scripts/reconcile-deductions.py" working-notes/*/draft-evaluation.md --emit-matrix
   working-notes/deduction-matrix.md --emit-rulings working-notes/ruling-requests.md`.
   One row per defect family, one column per unit. **One charge per (family, unit) — never
   per instance.** Seed the price schedule from the task's preset
   (`--show-preset <name>` prints it); a ruling on any family overrides the seed. Protocol in `references/deduction-matrix.md`; that one rule is worth more
   accuracy than everything else in this skill combined.
5. **Lead consistency pass.** One `lead-consistency` subagent over the full set, the round's
   reports, AND the matrix. It arbitrates every flagged row it has authority to settle
   (normalize a price the instruction files fix; propagate a waiver everywhere-or-nowhere;
   collapse instances), flags analogy-based extensions for reversal, applies the strictest
   verdict anywhere to every instance of a shared phrasing — and refuses the rest. It is
   read-only; you write its decisions into the matrix. **The lead will raise ruling requests
   the generator did not** — questions it found by reading across units that no single row
   flags. Append those to `working-notes/ruling-requests.md` before showing the human, or
   they exist only inside the lead's report and the human never answers them. Observed live:
   a run where the generator wrote 2 questions and the lead added a third.
5b. **Expected-average check (only if the task sets one).** After the matrix is priced, run
   `python3 "<this skill's directory>/scripts/reconcile-deductions.py" … --target-average N --basis N`. It reports the awarded cohort
   average, the gap, the uniform multiplier that would close it and the residual after
   rounding — and applies nothing. A gap beyond tolerance becomes `Q0` in the ruling queue
   with three routes (scale the schedule / adjust individual grades / advisory only). Present
   them with their costs, including that adjusting grades breaks the discrete attributable
   deduction rule, and that **a cohort can genuinely be excellent or weak, in which case
   forcing the average misreports them**. The human chooses; you record it in the matrix.
6. **Two things → human, together.** (a) The findings table (unit, severity, exact text,
   ground truth, proposed fix), saved as `working-notes/findings-round<N>.md`. (b) The
   **ruling requests** — the fairness questions the lead would not settle: same item priced
   differently in two units, a family charged unevenly with no evidence for the difference, a
   defect class with no precedent, a policy boundary (including any uncertainty an auditor
   flagged about itself), an unclear waiver scope. Each carries three ready dispositions, so
   answering costs a sentence. Ask the human to approve/reject/amend EACH fix and to rule on
   EACH question. Never apply an unapproved fix; never answer a ruling request yourself.
7. **Apply approved fixes and rulings.** Write each ruling into the matrix numbered, dated
   and attributed; re-price the affected cells. Then **re-audit every revised or re-priced
   unit, whole** — a fresh `unit-auditor` per unit, told it is re-auditing (a fix is a new
   claim; re-check everything, not just the flagged spot).
8. **Rebuild the matrix and diff it.** Regenerate and count `cells moved` against last
   round. A ruling can re-price one row into a discrepancy on another — that is a new
   question, not a finished round.
9. **Convergence check.** Update `working-notes/round-metrics.md` (blockers, minors,
   findings-in-prior-fixes, **matrix cells moved**, **open ruling requests**) and evaluate
   the rules in `references/convergence-and-bounding.md`. Converged = one pass where no unit
   blocks, the matrix has no unarbitrated flag, **no ruling request is open**, and no cell
   moved (the rule is stated once, in `references/convergence-and-bounding.md`; this is a
   restatement, not a second definition). Bounding triggered →
   stop looping, diff what ships. Otherwise → another round, with the human's go-ahead.
   **The human closes the loop, not the counter:** once cell movement is small and blockers
   are zero, show the diff of what moved and offer the close explicitly — the recorded runs
   ended at round 9 on "the latest changes seem minor," with round 10 never run.
10. **Write-back — the round is not closed without it.** Every ruling the human gave is a
   precedent that would have prevented this round's discrepancy; propose it as a dated line
   per `references/write-back.md`, alongside precedents for new failure modes. Show as a diff
   to the task (or root) `CLAUDE.md`; append only what the human approves. Measured: a run
   carrying prior rulings matched the issued grades to 3.0 points; the same harness without
   them diverged by 11.4 and moved one outcome band.
11. **Round report.** Verdict per unit, the matrix (rows, arbitrated, open questions, cells
   moved), the metrics table (trajectory across rounds), what was written back, and what
   happens next. If the run has converged: remind the user of the
   one box you cannot tick — **book one human reader outside the loop** (the `fresh-reader`
   agent is available as a labeled weak proxy, never a substitute).

## Standing rules

- Costs are stated up front: N units ≈ N auditor subagents per round; budget 3–5 rounds
  (the recorded runs took 5, and 9 with an early stop). Say this before round 1.
- Praise is audited as strictly as criticism. When a claim fails twice, propose deletion,
  not narrowing — subtraction is the only edit that cannot inherit a counterexample.
- Everything you produce lands in `working-notes/` as files. The user can audit the auditor.
- Never set a price by acting. A price chosen because nobody objected becomes a precedent
  nobody chose — ask, and let the answer become the rule.
