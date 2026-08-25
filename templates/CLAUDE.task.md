<!--
  TEMPLATE — per-task specifics. Copy into ONE task directory as CLAUDE.md and fill the
  [BRACKETS]. This layer holds what is true for THIS task only; shared conventions live in
  the root CLAUDE.md and are inherited. When they conflict, this file wins.
-->

# CLAUDE.md — [TASK NAME]

Task-specific guidance. Shared reviewer conventions live in the root `CLAUDE.md` and carry over
in full — especially the discrete-findings rule, the output format, and the pre-send audit loop.

## What this task is

[One or two sentences: what the subject was asked to do, and what they submitted.]

## Regime — what counts toward the outcome

[State it explicitly BEFORE grading. Examples: "deliverables only, process logs are qualitative
feedback"; or "process logs are scored — here's the weight." Name any floors or caps. Deciding
what counts after seeing the work is how bias enters.]

## Strictness and expected outcome

[Set once here; the run skill reads it back. `standard` and no target is the default — an
indifferent adopter does not have to choose. See
`skills/grade-audit-run/references/deduction-matrix.md` for what each field does.]

- **Preset:** [lenient | standard | strict]
- **Report threshold:** note and above  ← *leave this; no preset hides a finding*
- **Charge threshold:** [blocker | minor | note] and above
- **Price schedule (seed):** blocker −[N] · minor −[N] · note −[N]
  *(a seed only — the deduction matrix's Ruling column overrides it per family)*
- **Expected average:** [none | N/BASIS]
- **Enforcement:** [ask each run | advisory only]

**Fixed at every preset, never a setting:** if no specific issue can be named, the points are
awarded. That is the attribution guarantee this whole method rests on. Lowering strictness
demotes a finding to a zero-point note — it never hides it, and the subject still sees it.

## Criteria / rubric

[The fixed point split or pass/fail bar, held constant across every unit. A table works well.]

| Component | Weight | Judged from |
|---|---|---|
| [name] | [/N] | [which file / which behavior] |

## Sources of truth — verify every claim here, not from memory

[List the exact files or systems that SETTLE a factual claim. This is what auditors check
against. Example:]

- **[path/to/reference]** — [what it is authoritative for].
- **[the engine/spec/code]** — verify all numeric and behavioral claims here.
- **Authoritative *for the subject* (never deduct for following it):** [the docs/README/spec you
  handed them]. If it disagrees with the system, that's a doc bug, not the subject's error.

## Waivers / special rules

[Any this-task-only exceptions, with the trigger that justifies each. Apply them
everywhere-or-nowhere — a rule that waives one unit's issue waives it for all comparable units.]

## Per-task gotchas

[The things that bite: known tooling bugs whose symptoms you must NOT deduct for, quirks in the
inputs, naming conventions for the submissions, anything an auditor could misread.]

## Precedents set in this task

<!-- Append here as this run teaches you something reusable; promote the general ones to root. -->

- [YOUR-DATE] [precedent]
