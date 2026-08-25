<!--
DEFAULT WORKSPACE — dropped in by grade-audit when no task CLAUDE.md exists.

Everything here is a defensible default you can use as-is. ONE section is deliberately
unfilled: the rubric. That is not an oversight and it is not something this plugin will
guess for you — a criterion nobody chose is decoration, and grading against an invented
rubric produces confident, well-evidenced, wrong outcomes. Fill in "Criteria / rubric",
then run.

Delete this comment once you've read it.
-->

# CLAUDE.md — [assignment name]

## What this repository is

A grading workspace for [assignment]. One folder per student under `inputs/`; the
authoritative output is one evaluation per student in `working-notes/<unit>/`, and the
subject-facing letter extracted from it.

This is NOT a working copy of the assignment. The assignment source lives in `solution/`
or wherever you keep it.

```
inputs/<unit>/           # the submission — read-only
working-notes/<unit>/    # evidence ledger · draft evaluation · audit-round{1..N}
working-notes/deduction-matrix.md    # cross-unit reconciliation, one row per defect family
output.md                # authoritative output
```

## Never-events — applied by default

Enforced by the auditors and verified across the set by the lead pass:

- **No student is named in another student's feedback.** No names, no quotes, no rankings,
  no cohort comparison that identifies anyone, no "unlike another submission".
- **A grade appears only in that student's own delivery** — never in another's letter, never
  in a shared file, never in a class-wide message.

## The core rule: discrete, attributable findings

**Every point removed is tied to a specific, named issue**, with the evidence that shows it
and a one-line "how to avoid it next time". If no specific issue can be named, the points are
awarded. This holds at every strictness setting; it is the guarantee the whole method rests
on, not a preference.

One charge per defect family per student — never per instance. Three blanks in one workbook
is one *unfilled fields* charge, not three.

## Strictness and expected outcome

- **Preset:** standard  *(lenient = only blockers cost points · strict = everything named costs)*
- **Report threshold:** note and above — a lower preset demotes a finding to a zero-point
  note that still reaches the student; it never hides it
- **Charge threshold:** minor and above
- **Price schedule (seed):** blocker −2 · minor −1 · note −0  *(the deduction matrix's Ruling
  column overrides this per family)*
- **Expected average:** none
- **Enforcement:** ask each run

## Models and cost

[The auditors are the bill: one subagent per unit per round. They default to `sonnet`, which
is the cost driver handled. Raise one if its work suffers — and see the caveat below before
assuming a smaller model finds the same defects.]

- **Unit auditors:** [sonnet | opus] — N per round, so this is the number that matters
- **Lead consistency pass:** [sonnet | opus] — 1 per round; it does the hardest reasoning
  (cross-unit arbitration), so it is the first one worth raising
- **Fresh reader:** [sonnet | opus] — 1, and already a labelled weak proxy

## Who the feedback is from

[Recorded once so every letter signs the same way. Without this the sign-off is inferred from
whatever personal writing rules the operator happens to have — which works by accident for
one person and varies or vanishes for anyone else. A grade letter is a formal communication;
name its sender.]

- **Signed:** [the name as it should appear, e.g. "Joe" or "Prof. Okonkwo"]
- **Register:** [first-name and warm / formal / departmental — pick one and hold it]
- **Reply-to:** [office hours, email, or "reply to this message"]

## Criteria / rubric — YOU MUST FILL THIS IN

**This plugin will not guess your rubric.** Grading against invented criteria is the one
failure the rest of this machinery cannot catch: every judgment will be evidenced, internally
consistent, and measured against a standard nobody chose.

If you have an assignment handout or rubric in this workspace, ask the setup skill to propose
a rubric from it — it will show you a draft and wait for your approval. Otherwise write it
here. A table works well:

| Component | Weight | Judged from |
|---|---|---|
| [name] | [/N] | [which file or behaviour evidences it] |

**The criteria audit, which is not skippable:** for each row, name the artifact that
evidences it. A criterion whose evidence was never collected is decoration — collect it or
delete the row. Partial evidence is worse than none, because the outcome then depends on who
happened to get recorded.

## Sources of truth — verify every claim here, not from memory

- **The submission itself** (`inputs/<unit>/`) — authoritative for what the student did.
- **[the assignment handout / spec / starter code]** — authoritative *for the student*. If it
  disagrees with reality, that is a documentation bug, not the student's error, and it is
  never a deduction.
- **[the reference solution, if any]** — a comparison, not a target. Divergence is not error.

## What the student was owed

Never deduct for following an instruction you gave them. If the handout said X and the
system does Y, the student who did X is correct for the purposes of this grade.

## Data handling and institutional coverage

- **Institutional coverage:** [what covers this use, in your own words] — recorded [date]
- **Coded units:** [yes / no]; `--keys` directory: [absolute path, outside this workspace]
- **Deny rule added to `.claude/settings.json`:** [yes / no]

**Delivery:** `code-units.py --personalize <letters> --map <keys>/<run>.map.json --out
<somewhere-else>` puts the real names into the greetings, locally, refusing any letter it
cannot map unambiguously. Dry run first.

**Getting names back at delivery:** letters are addressed to unit codes; the map says who
each is. Run `python3 <plugin>/skills/grade-audit-setup/scripts/code-units.py --decode
<keys>/<run>.map.json` outside the grading session, and hand-check one row before sending the
batch.

`inputs/` and `working-notes/` are gitignored by default. See the plugin's data-handling
reference before real student work enters this workflow.

## Accumulated precedents

Every caught failure becomes a durable rule here, dated. Seeded with ones learned the hard
way; yours accumulate below.

- Write cohort claims without factual universals — one counterexample fails the audit.
- Revisions introduce errors at a high rate — re-audit whole units, not the flagged spot.
- A fix is a new claim and inherits the counterexample. Re-verify replacements from scratch.
- Verify behaviour claims against the shipped artifact, not the session narrative.
- When reading a raw log for attribution, scan its *actual* structure (queued input,
  attachments), not just the obvious "user" field, or you will under-credit the student.
- [YOUR-DATE] [your next hard-won rule]
