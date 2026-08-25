# Generation rules — from interview answers to working files

One source: generate from the plugin's `templates/` directory (CLAUDE.root.md,
CLAUDE.task.md, evaluation-report.template.md), substituting the user's confirmed answers
for the bracketed sections. Do not invent structure the templates don't have; do not leave
a bracket unfilled — anything the interview didn't cover gets asked, not guessed.

## What to write, where

```
<their project>/
├─ CLAUDE.md                    ← from templates/CLAUDE.root.md
├─ .gitignore                   ← per Q6 (see below)
└─ <task-name>/                 ← kebab-case from Q1 (e.g. lab-3/, q3-vendor-contracts/)
   ├─ CLAUDE.md                 ← from templates/CLAUDE.task.md
   ├─ inputs/                   ← empty, with a README line: material under review, read-only
   ├─ working-notes/            ← empty; one subdir per unit will appear during runs
   └─ output-template.md        ← from templates/evaluation-report.template.md
```

## Per-file rules

- **Root CLAUDE.md**: Q1 → "What this repository is" (include the unit definition from Q2
  and the authoritative output from Q3). Q3 → output format section (two-part split;
  subject-facing rules incl. anonymization from Q6). The discrete-findings rule, pre-send
  audit protocol, and precedents section come through from the template intact. Seed
  "Accumulated precedents" with the template's hard-won rules, marked `(seeded)` — the
  user's own will accumulate marked by date, and the file states the pilot-before-cohort
  default ("run the full loop on 2–3 units before the full set").
  Delete the three-contexts section unless the user's workflow ships an instruction file
  to a different audience (ask only if Q3 hinted at one; offer
  templates/CLAUDE.end-user-facing.md if yes).
- **Task CLAUDE.md**: Q1 → task description. Q5 → regime + criteria table, each criterion
  with its "judged from" artifact (the criteria audit's output — every row MUST name a
  file). Q4 → sources of truth. Q7 → the authoritative-for-the-subject list, with the
  never-deduct sentence. Q6 → waivers/gotchas as applicable. Precedents section starts
  empty.
- **Strictness section**: Q5b → the task CLAUDE.md's "Strictness and expected outcome"
  block — preset, both thresholds, the seeded price schedule for that preset, the expected
  average (or `none`), and the enforcement default. Leave the report threshold at "note and
  above" unless the user explicitly asked to suppress a class, and if they did, record which
  class and why.
- **.gitignore**: whenever the material involves people (or the user chose it in Q6):
  `<task>/inputs/` and `<task>/working-notes/` at minimum, plus anything else Q6 named. If
  the coded-units pass was accepted, add the coded copy too (`<task>/inputs-coded/` or
  whatever `--out` they chose) — coded is not de-identified, and the work is still in there.
  Add one comment line saying why: evaluation material stays out of version control shared
  beyond this machine.
- **output-template.md**: component names and the subject-facing rules substituted; the
  two-part structure and audit-status header kept verbatim.

## Conduct

- Existing files are never overwritten. Existing CLAUDE.md → show an appended,
  clearly-delimited section as a diff, or place the generated content one directory down;
  the user picks.
- Show every file as a diff/preview before writing; write only on confirmation.
- After writing, the walkthrough (SKILL.md step 5) — one paragraph per file, ending with:
  these files are yours; every rule in them is editable, and the write-back loop will
  propose additions, never make them silently.
