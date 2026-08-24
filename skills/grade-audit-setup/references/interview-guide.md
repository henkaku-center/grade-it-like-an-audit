# Interview guide — seven questions, plain language

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

## Q6 — Never-events (privacy and red lines)

"What must never happen with this material? Think: leaves this machine, ends up in a
public repo, gets quoted somewhere, names a person."

Why: generates the `.gitignore` (inputs and working notes ignored by default whenever the
material involves people), the anonymization rules in the output format, and the
data-handling defaults. If the material is about people — students, employees, clients —
walk them through the plugin's `references/data-handling.md` guidance now, and default to
the strictest option they'll accept. Also set where working files live (private repo vs
local-only).

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
