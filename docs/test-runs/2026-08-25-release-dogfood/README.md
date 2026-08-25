# Release dogfood — 0.2.0 pre-tag audit (2026-08-25)

Three scope-isolated auditors over the changed documentation and the shipped scripts, run
before tagging 0.2.0. Each was told to run the commands the docs describe, because a
documented command that does not work is a blocker.

**Verdict: 63 findings — 18 blockers, 29 minors, 16 notes.** The release was stopped.

| scope | findings | blockers |
|---|---|---|
| run skill (SKILL.md, deduction-matrix, fan-out, convergence, calibration) | 21 | 7 |
| setup skill, agents, templates | 26 | 7 |
| top-level docs, manifests, licence | 16 | 4 |

## What it caught that the self-tests did not

Every script self-test was green throughout — 42/42, 51/51, 13/13 — while all of the
following was true:

- A **dry run wrote real names to disk** (`<run>.detail.jsonl`) while printing "Nothing
  written." The documented first command.
- The **in-workspace report could print a real name**: `sanitize()` masked only the *search*
  terms, so a first name dropped as a common word ("Bob") reached the report verbatim — and
  the same report asserted "No coded path carries an identifier" four lines below one.
- **`--keys` was guarded against the current directory, not the workspace.** Run from
  anywhere else, the map landed inside the tree it exists to stay out of.
- **Matrix column headers were raw directory names** — student names in any real workspace.
- The **deny-rule claim was false**: it emits `Read()` and `Bash(cat …)` only; `head`, `grep`,
  `less` and Python read the map fine. The doc called it *enforced*.
- **Family labels collapsed to `(unlabelled in source)`** for the bolded component format the
  demo workspace itself uses — one meaningless matrix row for an entire cohort.
- **`die()` was called and never defined** — a documented flag raised a raw `NameError`.
- **`PRICE DIFFERS` missed multi-instance rows**, so a run could be declared converged on a
  live, unflagged fairness discrepancy.
- **`--basis` never rescaled the average**, so the gap and multiplier were garbage whenever
  the flag did anything.
- **`--self-test` aborted entirely** when run from any ancestor of `TMPDIR`.
- The **LICENCE covered only the methodology, guide and templates** while the manifest
  declared CC BY 4.0 over a release containing four scripts, four skills and three agents.
- **`RELEASING.md` asserted a named person performed a cold read.** `git log --merges` is
  empty and commit `415ee1f` records a *simulated* one.

## The pattern, written back

Each of these had a passing self-test beside it. The suites tested what the code did, not
what the documentation promised, and never ran the documented commands as written. Three
separate defects this session were found by *running* the thing rather than reading it. The
rule that follows: **a self-test that does not execute the documented command is not testing
the feature, and coverage of new code is part of adding it, not a follow-up.**

## Provenance

Findings below are reproduced from the three auditors' returned reports. Each finding was
independently re-verified before being acted on; one was rejected (see `rejected.md`). The
full agent transcripts were not committed — they are session-local and contain no material
that is not summarised here.
