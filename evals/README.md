# Eval suite

Evals for the plugin, in two layers — authored per the method's own rule: record what was
actually verified, with counts, never "all verified."

## Plugin-level cases (`evals/<case>/prompt.md` + `graders/*.md`)

| Case | What it tests |
|---|---|
| `demo-defect-recall` | The demo catches all 6 catchable planted defects (proportional score), keeps the answer key sealed, keeps auditors blind, reveals the 7th defect honestly, and respects the approval boundary. |
| `setup-interview` | The setup interview asks one question at a time, runs the criteria audit (it must challenge the unevidenced "overall scholarly effort" rubric line), defaults student data to gitignored/local, and confirms before writing. |
| `check-mine-facts` | Reverse-audit finds a planted wrong number and a paraphrase-in-quotes, reports verified claims with real counts, keeps judgment calls out of scope, and applies nothing uninvited. |

## Skill-level trigger evals (`skills/*/evals/trigger_eval.json`)

Should/shouldn't-trigger query sets for the front door (16 queries) and the demo
(8 queries), following the format used by official Anthropic plugin skills.

## Verification status — honest counts

- Authored: 3 cases (4 grader rubrics), 2 trigger sets (24 queries). Structural layout
  follows the `claude plugin eval` documented format (`evals/<case>/prompt.md +
  graders/*.md`).
- Executed with `claude plugin eval`: **0 of 3** — the runner is in early access and not
  enabled for this environment. Re-verified at the 0.2.0 release by running
  `claude plugin eval . --threshold 0.8` on **2026-08-25 against Claude Code 2.1.245**: it
  exits with `` `plugin eval` is currently in early access ``. The subcommand is present in
  the CLI's help output, which is why this was retried; presence is not access. Run it once
  the gate lifts.
- Executed manually: **1 of 3** — the demo-defect-recall scenario's machinery (blind
  fan-out + lead pass over the fixture) ran on 2026-08-24 and satisfied the recall
  grader 6/6 and the blindness and sealed-key clauses of the honesty grader; reports in
  `docs/test-runs/2026-08-24-demo-fixture/`. The setup-interview and check-mine cases
  have not been executed.
- `LIMITS.md` → "Dogfood and test record" carries the running counts as further runs
  happen; this file states the method and the status at release.
