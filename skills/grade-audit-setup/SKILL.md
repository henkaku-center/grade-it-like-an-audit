---
name: grade-audit-setup
description: Set up a grade-it-like-an-audit workspace through a plain-language interview — no template-filling by hand. Use when the user wants to start audit-style grading or evaluation for a real task, set up rubric-based review with audits, or says things like "set this up for my course/review/audit", "help me grade with this", "create the workspace".
---

# grade-audit-setup — the interview that replaces "fill in the brackets"

You build a working audit workspace from a conversation. The user needs no knowledge of
CLAUDE.md files, agents, or this methodology — your questions are in plain language, and
every generated file gets explained. Assume the user may be new to Claude Code entirely
and skeptical of AI: explain what you're doing as you do it, and never make a judgment
call that is theirs.

## Flow

1. **Detect context.** Look at the current directory: empty? an existing project? an
   existing `CLAUDE.md`? Never overwrite anything — for an existing CLAUDE.md, append a
   clearly-marked section or write the task file one level down, and show every diff
   before writing. If real submissions/material already exist here, note where, and treat
   them as read-only throughout.
2. **Interview — seven questions, ONE at a time.** Full scripts, plain-language phrasings,
   and the four-domain example table (grading / code review / compliance audit / contract
   review) are in `references/interview-guide.md`. The seven: the task; the unit of work;
   the output and its audience; the ground-truth sources; the criteria — with the
   criteria-audit inline (every criterion must name the artifact that will evidence it;
   this is where an unscoreable rubric gets caught, before any work exists); the
   never-events (privacy rules, which also generate the `.gitignore`); and what the
   subject was owed (sources the subject was told to follow, which you never deduct for
   following).
3. **Reflect back.** One summary table of their answers, concretized. Get an explicit
   confirmation (or corrections) before generating anything.
4. **Generate** per `references/generation-rules.md`: root `CLAUDE.md`, per-task
   `CLAUDE.md`, the output-format template, the directory tree, and a `.gitignore`
   covering inputs and working notes. Everything is generated from the plugin's
   `templates/` — one source — with the user's answers substituted for the brackets.
5. **Walk through what was written**, one file at a time, one paragraph each: what it is,
   why it exists, and that every rule in it is editable — these files are theirs, not the
   plugin's.
6. **Offer the fork**, with a recommendation: run `/grade-audit demo` first (if they
   haven't), then **pilot on 2–3 real units before the full set** — the pilot is the
   recommended default and is stated as such in the generated root file. Calibration
   (`/grade-audit calibrate`) is the right next step for anyone who wants the harness
   measured against their own grading before it drafts anything.

## Standing rules

- One question per message. No jargon in questions; jargon only in explanations, defined
  on first use.
- The criteria audit is not skippable: a criterion with no evidencing artifact is
  decoration — collect it or delete it, and partial capture is worse than none (say why:
  scoring from partial evidence makes the outcome depend on who got recorded).
- If the user's task involves personal data (students, employees, clients), the
  never-events question is where you surface `references/data-handling.md` — including
  the anonymize-before-grading option — and default everything sensitive to git-ignored,
  local-only paths.
