<!--
  TEMPLATE — root conventions for an AI-agent review/evaluation workflow.
  Copy to the ROOT of your working repo as CLAUDE.md and fill in the [BRACKETS].
  This layer holds what is true for EVERY run of the task. Task-specific details go in
  a per-task CLAUDE.md one directory down (see CLAUDE.task.md).
  Delete these HTML comments before use, or keep them — the agent ignores them.
-->

# CLAUDE.md — [PROJECT NAME] (root conventions)

This file provides guidance to the AI agent for all work in this repository. **These
instructions override default behavior; follow them exactly.** More specific `CLAUDE.md`
files deeper in the tree win where they conflict; this file fills the gaps.

## What this repository is

[One paragraph: what the repo is for, what a "unit of work" is (one submission? one file? one
PR?), and what the authoritative output is. State plainly that this is NOT [whatever it might be
mistaken for].]

## Repository layout

```
[task-01]/
  inputs/            # the material under review — read-only
  working-notes/<unit>/   # ledger · draft · audit-round{1..N}
  output.md          # authoritative output (format below)
CLAUDE.md            # this file
```

## The three instruction contexts — don't confuse them

<!-- Keep this section only if your setup ships an instruction file to a different audience. -->

1. **This file (root)** — reviewer meta-conventions, shared across all tasks.
2. **`[task]/CLAUDE.md`** — specifics for one task (criteria, sources of truth, gotchas).
3. **`[…]/CLAUDE.md` that ships to the end user** — a *different role* (e.g. a tutor/assistant
   prompt). When you are the reviewer, do NOT apply the end-user-facing rules to the questions
   the operator asks you here.

## The core rule: discrete, attributable findings

Every judgment is a discrete, named, evidenced claim:

- **Every point removed (or finding raised) is tied to a specific, named issue**, with a
  one-line "how to avoid." If you cannot name the concrete thing the subject did or failed to
  do, the points are awarded / the finding is not raised.
- **Praise is audited as strictly as criticism.** Log every quote and superlative in the
  positive section with its source, exactly like a deduction. (Overclaimed praise is the most
  common error — guard it hardest.)
- **Ground truth over memory.** Verify every number and behavioral claim against the source
  named in the per-task file — never against recollection.
- **"What the subject was owed."** If our own instructions/docs told the subject X, do not
  penalize them for X even if the system does Y. [Name your authoritative-for-the-subject
  sources in the per-task file.]

## Output format

[Define the authoritative output's fixed structure so every run is comparable. Example, adapt:]

- **Internal section** — the reasoning and evidence: an outcome table, and per-unit findings,
  each `Finding: … — (severity) … How to avoid: …`.
- **Subject-facing section** — what actually gets delivered. [State any rules: no cross-unit
  comparisons, cite the deliverable not the process log, anonymize where required, etc.]

## The pre-send audit (required before anything is delivered)

Fan out **one fresh, independent auditor per unit**, each reading **only that unit's files**, so
a claim can't be confirmed by another unit's data and cross-contamination can't hide.

- Each auditor checks: every quoted string verbatim against the source; every number against the
  named ground truth; every praise universal against one counterexample; attribution against the
  raw record.
- **Re-audit every revised unit, whole** — not just the flagged spot. A fix is a new claim.
- **Loop until one pass is clean for ALL units in the same pass.** "Each was clean once" is not
  convergence.
- A **lead pass** greps the full set for shared phrasings/consistency (which per-unit auditors
  can't see) and applies the strictest verdict anywhere to every instance.
- Record the trail: what changed and what it changed *from*.

## Accumulated precedents

<!--
  THE MOST IMPORTANT SECTION OVER TIME. Every time the audit catches a NEW failure mode,
  append a dated one-line rule here so it can't recur. This is how the instruction set
  compounds. Seed it with the ones below (learned the hard way on real runs); add your own.
-->

- Write cohort/aggregate claims without factual universals — one counterexample fails the
  audit. Prefer "nearly every" / "most," and make illustrative lists true of *someone*.
- Revisions introduce errors at a high rate — re-audit whole units, not the flagged spot.
- A fix is a new claim, and inherits the counterexample. Re-verify replacements from scratch.
- Verify UI/behavior claims against the shipped artifact, not the session narrative.
- When reading a raw log for attribution, scan the log's *actual* structure (queued input,
  attachments), not just the obvious "user" field, or you will under-credit the subject.
- [YOUR-DATE] [your next hard-won rule goes here]
