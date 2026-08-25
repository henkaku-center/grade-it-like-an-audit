# DESIGN.md — why the plugin is built the way it is

The methodology (METHODOLOGY.md) says what the method is. This file records the
engineering decisions that turned it into a plugin, so a reader can audit the design the
way the design audits everything else.

Provenance: the approach originated in Ira Winder's grading-workspace `CLAUDE.md` for
the APS I course (`henkaku-center/aps-i-eval-2026`); Joseph Austerweil developed it from
there into this methodology and plugin and maintains it. The conversion itself (skills,
agents, demo, evals, 2026-08 docs) was built with Claude Code — anything wrong in the
packaging is on this layer, not on the origin.

## Decisions

**One front door, three working skills.** A novice remembers exactly one thing:
`/grade-audit`. It reads the workspace and routes; the heavy phases (setup interview,
audit rounds, demo) are separate skills because they are different jobs with different
context needs. Every SKILL.md stays short; the three working skills keep their depth in
`references/` — progressive disclosure keeps the always-loaded token cost low and the
deep material one Read away.

**Write-back is structural, not optional.** The methodology's central thesis is that the
instruction set compounds — every caught failure becomes a durable rule. So write-back is
the mandatory closing phase of every audit round ("a round is not closed until its lessons
are written back"), not a separate skill someone can skip. The tool improves its host
project's CLAUDE.md over time, always by shown diff, always with human approval.

**Auditors are least-privilege by construction.** The `unit-auditor` and `lead-consistency`
agents carry read-only tools (`Read, Grep, Glob`). An auditor that cannot write cannot
"fix" what it should only report, and a reviewer reading the agent definition can verify
the guarantee in one line.

**Blindness is by construction-of-context — and we say so.** Subagents start with fresh
context and see only the paths their prompt names; the fan-out protocol forbids passing
any multi-unit path. There is no per-unit filesystem sandbox, so the design adds
compensating checks (each auditor reports its files-read list; the lead pass audits those
lists and hunts cross-contamination signals) and LIMITS.md states the boundary plainly.
Honest architecture over implied guarantees — the method's own lesson 4 applied to
ourselves: a "files I read" line is a claim.

**The human owns every judgment.** No fix is applied unapproved, no outcome finalized by
the harness, no precedent appended silently. The convergence checklist ends with a box the
harness explicitly cannot tick — one human reader outside the loop — and the bundled
`fresh-reader` agent is labeled a weak proxy in its own definition, because subagents
share the model's blind spots (METHODOLOGY §7).

**All state is inspectable files.** Rounds, findings, metrics, ledgers — everything lands
in `working-notes/` as plain markdown; the front door reconstructs state by reading files,
never from session memory. You can audit the auditor, and a session that dies mid-round
loses nothing.

**The demo plants its own failure.** Seven defects: six catchable, one — a claim about
the world — uncatchable by design, revealed from a sealed answer key at the end. A tool
that demonstrates its own blind spot on request is the honest version of a sales demo,
and it teaches the single most important structural rule (keep a human outside the loop)
by demonstration.

**One source, every format.** The repo is simultaneously the white paper, the by-hand
template kit, and the installable plugin — because the method's lesson 10 ("generate
every format from one source") applies to the method's own packaging. The skills generate
workspaces from the same `templates/` a by-hand adopter copies.

**Calibration points the trust arrow at the human.** Before the harness grades anything
real, it grades units the human already graded — blind — and a deterministic stdlib
script (`skills/grade-audit-run/scripts/agreement.py`) computes κ/ρ/MAD. Computed, not
asserted; and the script prints its own small-n caveat rather than letting a coefficient
overclaim.

**A green self-test is not evidence the feature works.** The 0.2.0 dogfood found 18 blockers
while every script suite passed — a dry run writing real names to disk, a report printing a
name it had dropped as a common word, a key-directory guard checking the working directory
instead of the workspace, matrix columns carrying directory names, a documented flag raising
`NameError`. Each had a passing test beside it, because the suites tested what the code did
rather than what the documentation promised, and none of them ran the documented commands as
written. Three separate defects this session were caught by executing the thing instead of
reading it. The rule written back: **a self-test that never runs the documented command is
not testing the feature**, and covering new code is part of adding it.

**A strictness dial must not become a way to stop looking.** Adopters need to grade harder or
softer than the templates imply — measured, the same harness produced 96–100 under one
rulebook and 63–84 under another. The obvious design makes auditors less sensitive at lower
settings, and it is wrong: it hides defects rather than pricing them, so the subject loses the
feedback precisely where the grader had decided not to charge for it. So strictness is split
in two. A **report threshold** governs what is written up and stays at `note` in every preset;
a **charge threshold** governs what costs points and is the only thing a preset moves. Lenient
means a minor becomes a zero-point note in the letter, not a minor nobody mentions. The same
logic drives the expected-average feature: enforcing a target by scaling the whole price
schedule keeps every deduction tied to its named issue, while adjusting individual grades does
not — both are offered, only one is recommended, and the difference is stated where the choice
is made rather than in a footnote.

**Consistency is a structure, not a memory.** A blind auditor cannot police fairness across
units — it cannot know unit B was charged −1 for the thing it just charged −3 — so asking it
to be consistent asks for what its isolation forbids. The deduction matrix moves the charge
decision to the only place with cohort sight: one row per defect family, one column per
unit, one charge per cell. A row reading `−1 | −1 | — | −2 | —` is self-evidently a question,
which is the point; run against a real cohort it surfaced one family charged −1, −2, −2, —
and −3 across five units. The lead pass arbitrates what the instruction files authorize and
**refuses the rest**, because a price set by acting becomes a precedent nobody chose. What it
refuses becomes a numbered question for the human, and the answer becomes a written
precedent — the same write-back loop, now fed by fairness questions and not only by caught
defects.

**Deviations from the original plan, recorded.** (1) No `commands/` alias was shipped:
skills are already user-invocable as `/grade-audit`, and a same-named command would
collide rather than help. (2) `claude plugin eval` was early-access-gated in the build
environment, so the eval suite ships authored-but-runner-unexecuted, with exact counts in
`evals/README.md`.

## Dogfood record

The harness is run on this plugin's own material before each release. Per the method:
counts, not adjectives — the table records each run, and the primary artifacts (auditor
and lead reports) are preserved under `docs/test-runs/`.

| Run | Units | Rounds | Blockers | Minors | Written back | Notes |
|---|---|---|---|---|---|---|
| 2026-08-24 demo-fixture test (fan-out + lead over the demo workspace) | 3 | 1 | 9 (6 planted, 3 unplanted — 2 found by unit auditors incl. 1 upgraded from minor by the lead, 1 lead-pass only) | 2 | known-extras section added to the demo answer key | All 6 catchable planted defects caught; world-claim flagged by artifact-vs-world; 3 blocker-class unplanted defects found (a 4th, minor-level, is in the preserved reports), kept in the fixture deliberately and documented. Blindness 3/3. Artifacts: `docs/test-runs/2026-08-24-demo-fixture/`. |
| 2026-08-24 docs dogfood (3 scope-isolated auditors over README / meta-docs / skills+agents, repo as ground truth) | 3 | 1 | 5 | 11 (+14 notes) | 3 lessons below | Caught a license contradiction and a fourteen-rounds overclaim that predate the plugin, wrong counts in our own "honest counts" records, a path collision in the run protocol, and a one-source violation (a promised template sentence that didn't exist). All blockers and minors fixed same day. Artifacts: `docs/test-runs/2026-08-24-docs-dogfood/`. |
| 2026-08-24 docs dogfood, round 2 (diff-scoped re-audit of round 1's fixes — a fix is a new claim) | diff of the round-1 commit | 1 | 0 | 7 (+3 notes) | — | 43 of 50 changed facts verified clean; all 5 round-1 blocker fixes held. The 7 minors were residue of the fixes themselves: a leftover of the corrected phrasing in one skill, the license fix still overstating (attribution = credit + license link + change-notes), a condensation tally short by two, a fourth unplanted fixture catch the counts missed, and a paraphrase-in-quotes inside a preserved report. Fixed in prose; preserved artifacts annotated, never edited. |
| 2026-08-25 release dogfood (3 scope-isolated auditors over the 0.2.0 diff: run skill / setup+agents+templates / top-level docs, each running the commands the docs describe) | 3 scopes | 1 | 18 | 29 (+16 notes) | 1 lesson below | **Stopped the release.** Every script self-test was green throughout while a dry run wrote real names to disk, the report could print a name dropped as a common word, `--keys` guarded the working directory instead of the workspace, matrix columns carried directory names, `die()` was undefined, family labels collapsed for the format the demo itself uses, and the LICENCE did not cover the shipped code. One finding verified and rejected (arithmetic that did close). All 18 fixed with regressions; suites 42→49 and 51→60. Artifacts: `docs/test-runs/2026-08-25-release-dogfood/`. |
| 2026-08-25 live user session (first end-to-end run of `grade-audit-run` outside the authors' scripts, 3-unit demo workspace) | 3 | 1 | — | — | 2 fixes | Blindness held 3/3 — every `FILES READ` in scope, real counts, no bare universals. The lead arbitrated the matrix, escalated 2 rows and **added a third question of its own**. Two defects only a live run could surface: the lead's added ruling requests were never merged into `ruling-requests.md`, and the fixture's own drafts deduct **without naming an issue**, which the matrix now reports as the discipline failure it is. Demo timed at 12 and 18 minutes, correcting a README claim of 10. |

## Lessons banked from the dogfood (the write-back, applied to ourselves)

- 2026-08-24 A pointer to evidence is itself a verification claim — never write
  "recorded there" before the record exists; create the record first or say "to be
  recorded."
- 2026-08-24 When stating a count of your own artifacts, count the artifacts, not your
  memory of authoring them — the wrong count sat in the section titled "honest counts."
- 2026-08-24 Preserve the primary artifacts of any run you cite (auditor reports, lead
  report) in the repo; an unfalsifiable self-report of a clean run is the pattern lesson
  4 warns about.
