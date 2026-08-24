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
   your memory of the session.
2. **Lead normalize.** Skim all drafts for structural conformance to the output format
   (sections present, tables well-formed). Fix format only — never content — and note what
   you touched.
3. **Fan out.** One `unit-auditor` subagent per unit, in parallel, each prompted with ONLY
   its own unit's paths. Construction rules in `references/fan-out-protocol.md` — follow the
   path-isolation rules exactly; they are the blindness guarantee.
4. **Lead consistency pass.** After all reports return, one `lead-consistency` subagent over
   the full set plus the round's reports. Apply the strictest verdict anywhere to every
   instance of a shared phrasing.
5. **Findings table → human.** Each auditor's verbatim report is already saved as
   `working-notes/<unit>/audit-round<N>.md` (per the fan-out protocol). Merge the findings
   into one set-level table (unit, severity, exact text, ground truth, proposed fix) saved
   as `working-notes/findings-round<N>.md`. Present the table and ask the human to
   approve, reject, or amend EACH fix. Never apply an unapproved fix; never finalize an
   outcome yourself.
6. **Apply approved fixes**, then **re-audit every revised unit, whole** — a fresh
   `unit-auditor` per revised unit, told it is re-auditing (a fix is a new claim; the auditor
   must re-check everything, not just the flagged spot).
7. **Convergence check.** Update `working-notes/round-metrics.md` and evaluate BOTH rules in
   `references/convergence-and-bounding.md`: converged (one pass clean for ALL units at
   once) → ship path; bounding triggered (blockers at zero, findings concentrating in prior
   fixes) → stop looping, diff what ships, verify only changed shipped text. Otherwise →
   another round, with the human's go-ahead.
8. **Write-back — the round is not closed without it.** Propose dated precedent lines for
   every new failure mode this round caught, per `references/write-back.md`. Show as a diff
   to the task (or root) `CLAUDE.md`; append only what the human approves.
9. **Round report.** Verdict per unit, the metrics table (trajectory across rounds), what
   was written back, and what happens next. If the run has converged: remind the user of the
   one box you cannot tick — **book one human reader outside the loop** (the `fresh-reader`
   agent is available as a labeled weak proxy, never a substitute).

## Standing rules

- Costs are stated up front: N units ≈ N auditor subagents per round; budget 3–5 rounds
  (the recorded runs took 5, and 9 with an early stop). Say this before round 1.
- Praise is audited as strictly as criticism. When a claim fails twice, propose deletion,
  not narrowing — subtraction is the only edit that cannot inherit a counterexample.
- Everything you produce lands in `working-notes/` as files. The user can audit the auditor.
