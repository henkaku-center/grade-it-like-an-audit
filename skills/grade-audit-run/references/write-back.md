# Write-back — the step that makes the whole thing worth doing

A round is not closed until its lessons are written back. When the audit catches a mistake,
the fix repairs this run; the RULE prevents the next one. The instruction set is edited by
its own failures — that compounding is the method's core property, so write-back is a
mandatory phase of every round, not an optional cleanup.

## What earns a precedent line

A NEW failure mode — a class of mistake the instruction files do not already guard. Not
every finding earns one: the third praise-universal caught this round is the existing rule
working, not a new rule. Ask per finding: "would a one-line rule have prevented this class,
and is that rule absent from the docs?" Only a yes-and-yes writes back.

## How to write the rule

- One line, dated, imperative, general enough to catch the class, concrete enough to act on:
  `- 2026-08-24 Verify who originated an idea against the raw record — read the log's actual structure, not just the obvious field.`
- Name the failure shape, not the instance. No unit names, no subject details, no scores —
  precedent lines survive into a long-lived file and must stay clean of personal data.
- Where it goes: the **task** `CLAUDE.md` "Precedents set in this task" section by default;
  promote to the **root** `CLAUDE.md` "Accumulated precedents" only if the rule is true for
  every run of the task, not just this one. When unsure, task file — promotion can happen
  later; demotion never does.

## Procedure

1. Draft the candidate lines (usually 0–3 per round; more suggests you are logging findings,
   not extracting rules).
2. Show the human a diff of exactly what would be appended, where. Include your
   task-vs-root reasoning in one sentence each.
3. Append only approved lines. Never rewrite or delete existing precedent lines during
   write-back — they are other rounds' scar tissue; editing them is a separate, human-led
   decision.
4. Record in the round report which lines were banked and which findings produced them.

## Bank-a-lesson (outside a formal round)

The front-door skill routes ad-hoc "remember this for next time" moments here. Same
procedure, one line at a time: draft, place (task vs root), show the diff, append on
approval. If the lesson is about the user's standing preferences rather than the task,
suggest persistent memory as the home instead of the repo files.
