# DESIGN.md — why the plugin is built the way it is

The methodology (METHODOLOGY.md) says what the method is. This file records the
engineering decisions that turned it into a plugin, so a reader can audit the design the
way the design audits everything else.

Provenance: the methodology and templates are joint work by Joseph Austerweil and Ira
Winder, hardened on real runs. The plugin conversion recorded here (skills, agents,
demo, evals, 2026-08 docs) was authored by Joseph Austerweil with Claude Code; the
design decisions below draw on the shared methodology but predate co-author review —
anything wrong in the packaging is on this layer, not on the method.

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

## Lessons banked from the dogfood (the write-back, applied to ourselves)

- 2026-08-24 A pointer to evidence is itself a verification claim — never write
  "recorded there" before the record exists; create the record first or say "to be
  recorded."
- 2026-08-24 When stating a count of your own artifacts, count the artifacts, not your
  memory of authoring them — the wrong count sat in the section titled "honest counts."
- 2026-08-24 Preserve the primary artifacts of any run you cite (auditor reports, lead
  report) in the repo; an unfalsifiable self-report of a clean run is the pattern lesson
  4 warns about.
