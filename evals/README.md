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

- Authored: 3 cases (5 grader rubrics), 2 trigger sets (24 queries). Structural layout
  follows the `claude plugin eval` documented format (`evals/<case>/prompt.md +
  graders/*.md`).
- Executed with `claude plugin eval`: **0 of 3** — the runner is in early access and not
  enabled for this environment at authoring time. Run
  `claude plugin eval . --threshold 0.8` once enabled.
- Executed manually (the scenario run end-to-end in a session and checked against the
  grader rubrics by hand): see `LIMITS.md` → "Dogfood and test record" for the current
  counts; that file is updated as runs happen, this one states the method.
