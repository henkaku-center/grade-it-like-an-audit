# CLAUDE.md — Demo: Lab 3 grading (synthetic data)

Everything in this workspace is synthetic. No real students, no real work. It exists so a
new user can watch the audit harness run before trusting it with anything real.

## What this is

Grading for "Lab 3: Penguin measurements" in a fictional intro data-science course. A unit
of work = one student's submission in `inputs/<student>/`. The authoritative output is each
unit's draft evaluation in `working-notes/<student>/draft-evaluation.md`.

## Regime — what counts

Deliverables only (`report.md` and any code) are scored. Session logs are NOT scored; they
are read only for attribution and integrity checks.

## Criteria

See `rubric.md`. Four components, 5 points each, 20 total. Held constant across all three
students.

## Sources of truth

- **`inputs/<student>/report.md`** (and `analysis.py` where present) — authoritative for
  every quote, number, and behavior claim about that student's work.
- **`assignment.md`** — authoritative *for the student*: never deduct for following it.
  If it disagrees with anything else, that is a handout bug, not the student's error.
- **`inputs/<student>/session-log.md`** — authoritative for who originated an idea. Read
  its actual structure, including bracketed non-turn fields, not just the speaker labels.
- **The evidence ledger** `working-notes/<student>/ledger.md` — the drafter's claim-by-claim
  source log; auditors check the evaluation against sources, using the ledger as the map.

## The core rule: discrete, attributable findings

Every point removed is tied to a specific, named issue with a one-line "how to avoid."
Praise is audited as strictly as criticism. Ground truth over memory, always.

## Accumulated precedents

- 2026-08-10 Write cohort claims without factual universals — one counterexample fails the
  audit.
- 2026-08-17 A fix is a new claim; re-audit revised units whole, not just the flagged spot.
