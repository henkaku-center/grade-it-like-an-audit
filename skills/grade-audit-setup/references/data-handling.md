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
## Before any real student work: check with your institution

This part is not optional, and it is not a plugin setting. If you grade real student
work, you are handling educational records, and the rules that govern them are your
institution's, not this tool's. None of this document is legal advice.

- **FERPA (US):** student submissions, grades, and feedback are generally education
  records under the Family Educational Rights and Privacy Act. Whether they may be
  processed by a given AI service is determined by your institution's agreements with
  that provider — not by the provider's marketing, and not by this plugin. The same
  applies to state student-privacy laws, and to GDPR and national law for institutions
  outside the US.
- **So ask first.** Before real student data enters this workflow, contact whoever
  governs data at your institution — typically the registrar, privacy office, IT
  data-governance, or general counsel — and ask two questions: *Is this AI service
  approved for student educational records at our institution, under which agreement?*
  and *What data may I put into it — named records, de-identified records, or none?*
  Get the answer in writing, and record it (and its scope) in your task CLAUDE.md as a
  standing rule.
- **Until you have that answer**, stay on the rungs that involve no student data: the
  demo (fully synthetic), `check-mine` on evaluations stripped of identifiers, or an
  anonymized pilot using the coded-units option above — and treat even "anonymized" as
  a question to put to your institution, since de-identification standards are also
  theirs to set.
- The setup interview asks about this explicitly and will offer the synthetic and
  anonymized paths until you confirm institutional approval. That gate exists because
  the cost of guessing wrong falls on your students and your institution, not on a
  plugin.

## The one-line summary for a skeptic

Everything the harness produces is a local file you can read; what leaves your machine is
the same as any Claude session under your plan's terms — so set the workspace to
anonymized codes, keep inputs gitignored and the name map local, and the material that
reaches anyone is grading of unit codes against your rubric.
