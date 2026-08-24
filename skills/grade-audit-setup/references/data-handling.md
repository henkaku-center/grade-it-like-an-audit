# Data handling — where does the student work go?

The first question a careful adopter asks, answered in two halves: what stays on your
machine (which you control), and what reaches the model provider (which you configure).
Written 2026-08; the provider half changes — the links are the authority, not this page.

## Half 1 — your machine, your rules (what this plugin does)

- Setup gitignores `inputs/` and `working-notes/` by default whenever the material
  involves people. Submissions, evaluations, ledgers, and audit reports stay out of any
  repo you might push. The public artifact is your method; the material is not.
- Nothing is sent anywhere by the plugin itself beyond the model calls that power the
  session — no telemetry, no third-party services, no uploads. All working state is plain
  files you can open.
- The methodology's own repo demonstrates the stance: it publishes run *statistics* and
  templates, and not one person's data. Hold your workspace to the same line: keep real
  material in a separate, private (or non-)repo.
- **Anonymize-before-grading option** (offered at setup): replace names with codes
  (student-a, …) in a copy of the inputs and grade the copy; keep the code→name map in a
  local file the workspace never reads. The audit harness never needs real names — units
  are units.

## Half 2 — the model provider (what to check, where)

Model calls go to the provider behind the user's Claude Code login. As of this writing
(verify against the linked pages — they are the authority):

- **Commercial terms** (API, Team, Enterprise, Claude for Education): not used for model
  training under the commercial terms/DPA; API inputs/outputs deleted from the backend
  within ~30 days, with Zero Data Retention agreements available to qualifying
  organizations. See https://platform.claude.com/docs/en/manage-claude/api-and-data-retention
  and https://www.anthropic.com/legal/commercial-terms
- **Consumer plans** (Free/Pro/Max on claude.ai): training on conversations depends on a
  user-controlled setting — check it before grading real work, and prefer a
  commercial/education plan for institutional use. See
  https://www.anthropic.com/news/updates-to-our-consumer-terms and your account's privacy
  settings.
- **Institutional obligations (e.g. FERPA):** compliance is an institution-level question
  — an agreement between your institution and the provider, not a property a plugin can
  confer. Ask your institution which AI services are approved for student records, and
  put that answer in the task CLAUDE.md as a never-event. When in doubt, use the
  anonymize-before-grading option above: coded units with the name map kept local answer
  most review-board concerns at the source.

## The one-line summary for a skeptic

Everything the harness produces is a local file you can read; what leaves your machine is
the same as any Claude session under your plan's terms — so set the workspace to
anonymized codes, keep inputs gitignored and the name map local, and the material that
reaches anyone is grading of unit codes against your rubric.
