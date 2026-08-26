# Interview guide — seven questions, plain language

*(Plus four follow-ups: Q5b strictness, Q6a institutional coverage, Q6b coded units,
Q6c disclosure to subjects.)*

Ask in order, one per message. Each entry gives: the question (adapt wording to their
context, keep the substance), why it's asked (say this in one sentence if the user seems
unsure), and example answers across four domains so the user can answer by analogy.
Follow up until the answer is concrete enough to generate from — vague answers produce
bracket-shaped files, which is what this interview exists to prevent.

Domains for the example tables: **G** = grading, **CR** = code review, **CA** = compliance
audit, **CO** = contract review.

## Q1 — The task

"What's the job, in a sentence or two? What lands on your desk, and what are you supposed
to produce from it?"

Why: becomes the "What this repository is" section — the agent's one-paragraph orientation.

G: "Grade 25 lab reports against my rubric each week." · CR: "Review every PR touching the
payments service." · CA: "Quarterly check of our data-retention practices against policy."
· CO: "Review vendor contracts before signature."

## Q2 — The unit of work

"When you do this job, what's the natural 'one of them'? The thing you'd finish and set
aside before picking up the next?"

Why: the unit defines auditor scope — one independent auditor reads one unit, blind to the
rest. Everything downstream hangs on this boundary being right.

G: one student's submission. · CR: one pull request. · CA: one policy control. · CO: one
contract.

Follow-up if fuzzy: "If two of these got mixed together, would that be a problem?" (If
no — the unit is probably bigger than they said.)

## Q3 — The output and its audience

"What do you deliver at the end, and who reads it? Is there a difference between what you
keep for your records and what the person being evaluated sees?"

Why: fixes the two-part output format (internal audit record vs subject-facing text) and
its rules — tone, anonymization, no cross-unit comparisons.

G: grade + feedback letter to each student; gradebook entry for records. · CR: review
comments to the author; approval status for the team. · CA: findings memo to leadership;
remediation list to control owners. · CO: risk summary to the deal owner; markup to the
counterparty's counsel.

**Q3b — who the feedback is from.** "How should the feedback be signed, and how formal?"
One line, recorded in the task CLAUDE.md. Ask because otherwise the sign-off is inferred from
whatever personal writing rules the operator happens to have — invisible when it works,
inconsistent when it does not, and absent for anyone whose setup carries none. Capture the
name as it should appear, the register (first-name and warm / formal / departmental), and
where a reply should go.

## Q4 — Ground-truth sources

"When there's a factual disagreement — a number, a quote, what something did — what
settles it? Name the actual files or systems."

Why: auditors verify every claim against these, never against memory or the evaluation's
own prose. No named source, no checkable claim.

G: the submission itself, the assignment handout, the autograder output. · CR: the diff,
the CI results, the spec. · CA: the logs, the config exports, the policy text. · CO: the
contract text, the playbook, the term sheet.

## Q5 — The criteria (with the criteria audit, inline)

"What are you judging, component by component, and how much does each count? This stays
fixed for every unit."

Then, for EACH criterion, immediately: **"Which artifact will show you this? Name the
file."** This is the criteria audit, run before any work exists:

- No artifact will be collected → the criterion is decoration: collect it or delete it,
  now. The cost of an unscoreable criterion falls on the assessor, not the subjects.
- Artifact collected for only SOME units → do not use the criterion; partial evidence
  looks scoreable, which is exactly the danger.
- Tell the user plainly when this catches something: "this just saved you a dispute" — it
  is the earliest value the method delivers.

G: "Effort" with no defined evidence → decoration; "Analysis /5, judged from report.md" →
scoreable. · CR: "code quality" (vague) vs "no new lint violations, judged from CI run". ·
CA: "control is effective" vs "retention config matches policy §3, judged from config
export". · CO: "acceptable liability" vs "cap ≥ 12 months fees, judged from §9".

## Q5b — Strictness and the expected outcome

Ask AFTER the criteria exist — strictness is meaningless before there is a rubric to be
strict about. Two questions, both skippable.

**"How hard do you grade?"** Offer the three presets with one consequence each:

- **lenient** — only blockers cost points; minors and notes are written up as feedback.
- **standard** — blockers and minors cost points; notes are feedback. *(default)*
- **strict** — everything named costs something.

Say the part that stops this being a way to hide problems: **a lower preset never suppresses
a finding.** It moves it from charged to noted; the subject still reads it in their letter.
The only way to stop something being reported at all is to raise the report threshold
deliberately, and the run will then tell you how many findings that suppressed.

**"Do you have an expected average?"** Optional, default none. If they give one, ask whether
to *enforce* it or treat it as *advisory*, and say what enforcing costs before they answer:
the honest route re-prices every defect family by one uniform multiplier and re-derives every
grade, so attribution survives; the exact route moves individual grades, which breaks the
rule that every point removed names an issue. Either way the choice is offered again at the
run that hits the gap — record the default here, not a commitment.

Also say once: a cohort can genuinely be excellent or weak, and forcing an average then
misreports them.

Record both answers in the task CLAUDE.md's "Strictness and expected outcome" section.

## Q6 — Never-events (privacy and red lines)

**State the defaults first, then ask what to add.** Two never-events are not the user's to
invent, and asking for them invites a workspace that lacks them. Say them as already applied:

- **No subject is ever named in another subject's feedback** — no names, no quotes, no
  "unlike another submission", no rankings, no cohort comparisons that identify anyone.
- **An outcome is visible only in that subject's own delivery** — never in another's letter,
  never in a shared file, never in a class-wide message.

These are already enforced: the auditors carry them as a POLICY check, and the
lead-consistency pass verifies them across the whole set. Then ask:

"Those two are already in place. What *else* must never happen with this material? Think:
leaves this machine, ends up in a public repo, gets quoted somewhere."

Why: generates the `.gitignore` (inputs and working notes ignored by default whenever the
material involves people), the anonymization rules in the output format, and the
data-handling defaults. If the material is about people — students, employees, clients —
walk them through the plugin's `references/data-handling.md` guidance now, and default to
the strictest option they'll accept. Also set where working files live (private repo vs
local-only).

**Q6b — the coded-units offer (whenever the material is about people).** "Do you want to
grade coded units instead of named ones? I can copy the submissions into a workspace where
each person is `unit-a`, `unit-b`, … , with the map kept in a directory this session cannot
read." Sell it on the methodological ground first — it takes the name off the work before
the judgment forms, which is what blind grading means — and on exposure reduction second.
**State the limit in the same breath:** it codes the container, not the content; file
contents are copied byte-for-byte and scanned, never rewritten, so a name written inside a
submission is still there, and the scan report tells you where. It is pseudonymization, not
anonymization, and it establishes no compliance with anything. If they accept, run
`scripts/code-units.py` as a dry run, walk them through the scan report (especially "Needs
your eyes" and the attestation of fields already blank in the source), then `--apply`.
Record the choice and the `--keys` location in the generated task CLAUDE.md, and add the
printed `deny` rule to `.claude/settings.json` so the separation is enforced, not promised.

**Q6a — the institutional question (ALWAYS ASKED when the material is student work;
NEVER a blocker).** Ask directly: "Is your use of this AI service on student work covered
by your institution's policies or agreements? (Many institutions have approved
arrangements — an enterprise or education agreement, an approved deployment; you may
well be covered in a way this tool can't see.)" Student submissions and grades are
typically FERPA-covered education records (or the local equivalent — state law, GDPR),
and coverage is determined by the institution's arrangements, which the user knows and
this plugin cannot.

- **If they say they're covered:** take their word for it, record their answer (what
  covers it, in their words, with the date) in the generated task CLAUDE.md, and proceed
  with the full workflow. Their institution's arrangements are theirs to know; this
  interview is not an audit of them.
- **If no or unsure:** warn plainly and prominently — **check with your university before
  real student work enters this workflow** (registrar, privacy office, or counsel; the
  data-handling reference lists the two questions to ask) — then proceed with whatever
  the user chooses. Recommend the no-student-data rungs (synthetic demo, de-identified
  `check-mine`, anonymized pilot) in the meantime, and offer — as an option, not a
  requirement — to record a reminder in the task CLAUDE.md ("institutional coverage
  unconfirmed as of [date]; confirm before scaling up"). The decision, and the
  responsibility, are the user's — say that last part in so many words.
- In all cases, note once: this conversation is not legal advice, and use of the tool on
  student data is at the user's responsibility (see the Disclaimer in the README).

**Q6c — disclosure to the subjects (ASKED whenever the subjects are students or other
people receiving the feedback; NEVER a blocker).** "Will you tell students that an
AI-assisted pass was part of how their feedback was produced — and if so, where: the
syllabus, the assignment, or a line in the feedback itself?"

Ask it because the recurring position across institutional AI guidance is that people
being evaluated have an interest in knowing an automated system was involved, and because
the same guidance holds the instructor accountable for explaining the basis of any
decision. This tool is unusually well placed to satisfy both: every judgment already names
its issue and cites a source, so an instructor who discloses has something concrete to
disclose.

- **If yes:** record where and in what words in the task CLAUDE.md. Offer the suggested
  syllabus paragraph and one-line feedback footer from the data-handling reference as a
  starting point — theirs to edit, not to adopt verbatim.
- **If no, or not yet:** record that too, with the date, and move on. Say once that this is
  the user's call: disclosure norms vary by institution and by course, and some
  institutions set this centrally rather than leaving it to the instructor.
- **Do not editorialize either way.** Ask, record, proceed. The one thing worth saying
  plainly, once: whatever they choose, the claim they can defend is that a human set the
  criteria, approved every judgment, and decided every grade — because on this workflow
  that is true.

## Q7 — What the subject was owed

"What were the people being evaluated told — handouts, specs, docs, playbooks? If your
own instructions told them X, they can't lose points for doing X, even where the system
actually does Y."

Why: separates *authoritative-for-the-subject* sources from *merely true* ones. This
distinction prevents the most corrosive class of unfair deduction.

G: the assignment handout and course docs. · CR: the style guide and CONTRIBUTING.md. ·
CA: the published policy version employees were trained on. · CO: the negotiation playbook
the other side was shown.

## After Q7

Reflect all answers back as one table (question → their answer, concretized). Ask for
corrections. Only then generate, per `generation-rules.md`.
