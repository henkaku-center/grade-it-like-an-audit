<!--
  QUICKSTART — a pre-filled per-task CLAUDE.md for CODE REVIEW, proving the method is not
  grading-specific. Copy into your review task directory as CLAUDE.md and adjust the
  bracketed leftovers. Pairs with the root template as usual.
-->

# CLAUDE.md — PR review: [service/area name]

Task-specific guidance. Shared reviewer conventions live in the root `CLAUDE.md` —
especially the discrete-findings rule, the output format, and the pre-send audit loop.

## What this task is

Review each pull request against the team's standards before merge. A unit of work = one
PR (its diff, description, CI results, and linked issue).

## Regime — what counts toward the outcome

The verdict (approve / request changes) is settled by the diff and CI only. Commit history
hygiene and description quality are feedback, never blockers, unless [your policy].

## Criteria

| Component | Bar | Judged from |
|---|---|---|
| Correctness | no demonstrable bug in changed lines | the diff + tests |
| Tests | changed behavior has a changed/new test | the diff, CI run |
| Style | no new lint violations | CI lint job |
| Scope | diff matches the stated intent | diff vs PR description + issue |

## Sources of truth — verify every claim here, not from memory

- **The diff itself** — authoritative for what changed. Quote it verbatim.
- **CI results** — authoritative for test/lint claims; never assert "tests pass" from
  reading the code.
- **Authoritative *for the author* (never a finding for following it):** CONTRIBUTING.md
  and the style guide at [path]. If the linter and the style guide disagree, that's a
  tooling bug to file, not the author's error.

## Per-task gotchas

- A review claim about runtime behavior verifies against code and CI output, not the PR
  description's narrative.
- Praise is audited too: "great test coverage" needs the tests named.

## Precedents set in this task

- [DATE] [first precedent goes here]
