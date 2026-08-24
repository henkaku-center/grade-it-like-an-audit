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
## Real student work: know where your institution stands

If you grade real student work, you are handling educational records, and the rules that
govern them are your institution's, not this tool's. None of this document is legal
advice, and this tool never verifies or enforces compliance — it warns, asks, and
records; **the decision and the responsibility are yours** (see the README's
Disclaimer).

- **FERPA (US):** student submissions, grades, and feedback are generally education
  records under the Family Educational Rights and Privacy Act. Whether they may be
  processed by a given AI service is determined by your institution's policies and
  agreements with that provider — not by the provider's marketing, and not by this
  plugin. The same applies to state student-privacy laws, and to GDPR and national law
  for institutions outside the US.
- **You may already be covered.** Many institutions have arrangements that permit AI
  services on student records — an enterprise or education agreement, a zero-data-
  retention contract, an approved deployment. This tool cannot see those arrangements;
  if you know yours covers this use, you're the one in a position to say so, and the
  setup interview will record your answer and get out of your way.
- **If you're not sure, ask first.** Contact whoever governs data at your institution —
  typically the registrar, privacy office, IT data-governance, or general counsel — with
  two questions: *Is this AI service approved for student educational records at our
  institution, under which agreement?* and *What data may I put into it — named records,
  de-identified records, or none?* An answer in writing is worth having. Record it (and
  its scope) in your task CLAUDE.md as a standing rule.
- **While you wait**, the rungs that involve no student data are all fully usable: the
  demo (synthetic), `check-mine` on evaluations stripped of identifiers, or an
  anonymized pilot using the coded-units option above — and note that de-identification
  standards are also your institution's to set, so "anonymized" is worth including in
  the questions you ask them.
- The setup interview raises all of this explicitly whenever the material is student
  work, records your answer, and never blocks you. It asks because the cost of guessing
  wrong falls on your students and your institution — but it defers to you, because
  your institution's arrangements are yours to know, not this plugin's to police.

## The one-line summary for a skeptic

Everything the harness produces is a local file you can read; what leaves your machine is
the same as any Claude session under your plan's terms — so set the workspace to
anonymized codes, keep inputs gitignored and the name map local, and the material that
reaches anyone is grading of unit codes against your rubric.
