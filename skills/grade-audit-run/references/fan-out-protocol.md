# Fan-out protocol — constructing blind auditors

The blindness guarantee is by construction of context, not by sandbox: an auditor subagent
starts with a fresh context and sees only what its prompt names. These rules are what make
that guarantee real. Violating any of them silently voids the round.

## Per-auditor prompt construction

For each unit, spawn one `unit-auditor` subagent whose prompt contains exactly:

1. **The unit's name** and, if this is a re-audit, the sentence: "This unit was revised in
   response to a prior finding. Re-audit the WHOLE unit from scratch; a prior clean verdict
   is not evidence."
2. **This unit's file paths only:**
   - the draft evaluation for this unit (the unit's section of the output file, or its draft
     file in `working-notes/<unit>/`)
   - this unit's inputs/deliverables directory
   - this unit's evidence ledger
3. **The shared, unit-neutral context:** the root `CLAUDE.md`, the task `CLAUDE.md`, and the
   ground-truth sources named in the task file (spec, engine code, reference docs). Shared
   sources are allowed because they contain no other unit's work.
4. **What to return** — the agent definition already fixes the report format; do not add
   requirements that conflict with it.

## Strictness thresholds in the prompt

Every auditor prompt carries the two thresholds from the task CLAUDE.md's strictness block
(default `standard` when the task file has none):

- **report threshold** — normally `note`: everything the auditor can name and evidence.
- **charge threshold** — `blocker`, `minor` or `note` and above, per the preset.

State the rule verbatim in the prompt, because it is the difference between a lenient setting
and a blind one:

> Below the charge threshold, report the finding as a NOTE with its evidence and zero points.
> Demote it; never drop it.

And carry the fixed guarantee unchanged at every preset: if no specific issue can be named,
the points are awarded.

## Path-isolation rules

- NEVER pass a directory that contains multiple units' work (e.g. the whole `inputs/` or
  `working-notes/` root). Pass the unit's own subdirectory.
- NEVER pass the combined output file if it holds all units' evaluations — extract this
  unit's section to a scratch file in `working-notes/<unit>/` and pass that. (Extraction is
  mechanical; verify the extract matches the master verbatim.)
- NEVER pass another auditor's report, a previous round's findings for OTHER units, or the
  round-metrics file.
- NEVER mention other units' names, scores, or findings in the prompt.
- The demo answer key, if present anywhere, is never passed and never named.

## Collecting reports

- Run auditors in parallel; wait for ALL to return before any verdict. "Clean" declared
  before the last report lands is the round-1 failure from the method's own history — all
  units, same pass.
- Save each report verbatim as `working-notes/<unit>/audit-round<N>.md`.
- An auditor that read out-of-scope files (check its `FILES READ:` line) has a voided
  verdict: note it, and re-run that unit's audit with a corrected prompt. The lead pass also
  checks this line — it is a claim, not a guarantee.

## Lead pass

After all unit reports are in, spawn one `lead-consistency` subagent with: every unit's
evaluation (the full set), every report from this round, and the instruction files. It alone
may read across units. Apply its strictest-verdict propagation to the findings table before
showing the human.
