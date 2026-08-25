# Convergence and bounding — when to stop, and when to stop trying

Two rules. The first says when you MAY stop. The second says when continuing has stopped
measuring the work and started measuring the loop itself. Evaluate both at the end of every
round, from the metrics file — never from impression.

## The metrics file (the convergence dashboard)

Append one row to `working-notes/round-metrics.md` at the end of every round:

```markdown
| Round | Blockers | Minors | Notes | Findings in prior round's fixes | Units clean this pass | Matrix cells moved | Open ruling requests |
|---|---|---|---|---|---|---|---|
| 1 | 4 | 12 | 7 | — | 2/5 | — | 6 |
| 2 | 1 | 9 | 5 | 3/10 (30%) | 3/5 | 7 | 2 |
| 3 | 0 | 3 | 4 | 2/3 (67%) | 2/5 | 1 | 0 |
```

"Findings in prior round's fixes" = of this round's findings, how many sit in text that did
not exist before the previous round's revisions. Compute it by checking each finding's
location against what the previous round changed — this is the bounding rule's input, so
count it honestly, per finding, not by feel.

"Notes" counts findings reported at zero points — everything below the charge threshold. A
lenient preset creates these by demotion, so without the column the ledger silently loses the
findings the subject still receives, and a run can look quiet while it is only cheap.

"Matrix cells moved" = how many (family, unit) charges changed since the previous round,
after rulings were applied. "Open ruling requests" = fairness questions still unanswered.
Both come from `references/deduction-matrix.md`.

Render the full table in every round report. The trajectory IS the argument: falling
blockers and falling minors = converging; blockers at zero with minors flat and the
prior-fix fraction climbing = the loop is auditing its own repairs; **cell movement that
oscillates instead of falling = two rulings are fighting**, and that is a question for the
human, not another round.

## Rule 1 — convergence (when you may stop)

> One pass comes back clean for the ENTIRE set at the same time, **and the matrix is
> stable**: no unarbitrated flag, no open ruling request, no cell moved this round.

- "Each unit was clean at some point" is not convergence. All units, same pass.
- Any revision after the clean pass voids it — the revised unit is re-audited whole, and the
  set needs a new all-clean pass.
- **Clean units are not enough.** Every unit can pass its own audit while the set is still
  unfair, because a blind auditor cannot see that the same defect cost another unit twice as
  much. The matrix is the only place that shows up, so it converges too or nothing has.
- A ruling applied this round re-prices cells, which can open a discrepancy on a different
  row. That is a new question, not a finished loop.
- On convergence: outputs are cleared to deliver. Final checklist to the human: deliverables
  generated from the one master source (never hand-copied); the write-back done; and the one
  box the harness cannot tick — **a human reader outside the loop reads the finished
  material once, cold.** Offer the `fresh-reader` agent only with its limitation stated: it
  shares the model's blind spots; it supplements the human reader, never replaces them.

## Rule 2 — bounding (when to stop trying)

Trigger: **blockers have been zero for two consecutive rounds AND the majority of this
round's findings sit in text introduced by the previous round's own fixes.**

When triggered, do not convene another round. Instead:

1. **Diff what ships.** Compare the subject-facing material (only that — not notes, not
   internal sections) against the last audited version.
2. **Verify only what changed there**, each change against its ground-truth source. A
   deletion cannot introduce a new claim; new or altered text is checked from scratch.
3. Report to the human: the diff, the verifications, and the recommendation to stop. The
   decision is theirs.

**The human closes the loop, not the counter.** Once blockers are zero and cell movement is
small, put the close on the table explicitly: show what moved since last round and ask
whether it is worth another pass. The recorded runs ended exactly this way — round 9 closed
on *"the latest changes seem minor and so I'm not concerned"*, and round 10 was never run.
Offering the close is part of the job; deciding it is not.

Two cautions, verbatim from the method's history:

- This applies ONLY after blockers are at zero and stay there. A loop still finding
  substantive errors is converging, however slowly — Rule 1 stands.
- Scoping is a verification step, not a skip. The changed sentences are still checked; what
  is dropped is the ceremony of a full pass, not the checking.

## Editing rules the loop depends on

- **A fix is a new claim and inherits the counterexample.** Every replacement is re-verified
  from scratch by the re-audit; never mark a fix "done" on application.
- **When a claim fails twice, propose deletion, not narrowing.** Narrowing (qualifiers,
  scope restrictions, hedged verbs) usually inherits the same counterexample; subtraction
  cannot. Say this to the human when a finding recurs on the same claim.
- **Record real counts** ("6 of 8 verified"), never bare universals ("all verified") — in
  your round reports as much as in the auditors'.
