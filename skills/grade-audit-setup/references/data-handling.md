# Data handling — where does the student work go?

The first question a careful adopter asks, answered in two halves — what stays on your
machine (which you control), and what reaches the model provider (which you configure) —
with the coded-units pass in between, which shrinks what reaches anyone at all.
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
- **Coded-units pass** (offered at setup): grade a copy in which each person is a random
  unit code, with the map kept outside the workspace. The audit harness never needs real
  names — units are units. Run it with `scripts/code-units.py`; the section below is what it
  does and, more importantly, what it does not.

## The coded-units pass — what it buys, and what it does not

`skills/grade-audit-setup/scripts/code-units.py` copies each person's material to
`unit-a/`, `unit-b/`, … , keeps the code→identity map **outside** the workspace, and
**scans** the contents rather than rewriting them. Stdlib only, dry-run by default.

```
python3 code-units.py --inputs inputs/ --roster roster.csv \
        --out inputs-coded/ --keys ~/.grade-audit-keys/f26-mp1/
# read the scan report it prints, then:
python3 code-units.py ... --apply
```

`roster.csv` is one row per person with a `path` (or `folder`/`file`) column naming their
submission and an optional `role` column; every other cell is an identifier to search for.
No roster? `--roster-from-dirs` derives candidates from each submission's own folder name.

### It never rewrites your files, and that is the point

An earlier version redacted file contents. Tested against a raw session log, it broke the
method's own ATTRIBUTION check — it folded collaborators into the subject's code, so a log
reading "Sam suggested antithetic variates" came out as the subject suggesting it: the exact
BLOCKER the method exists to catch, manufactured by the privacy feature and undetectable
afterwards. It also destroyed `@property` decorators and `github.com/numpy/numpy`
citations. **A redaction pass rewrites the same files the evidence discipline depends on.**

So this one observes and reports. Copies are byte-for-byte and hash-verified, timestamps
preserved, and the report carries the proof (`N/N copied files hash-match their source`).
It also records identity template fields **already blank in the source, before grading**, so
a student's blank can never be mistaken for something the tool removed — the units *not*
listed are the control.

### The reason to do it that has nothing to do with law

Blind grading. The method already commits to auditor blindness and no cross-unit comparison;
coded units serve that by taking the name off the work before the judgment forms. That is a
pedagogical claim you can defend without a lawyer, and it is the claim this feature rests on.

### The headline limit: it codes the container, not the content

If a submission says "By Jane Doe" inside, it still does. On a real cohort, **5 of 5 units
carried identity findings inside their file contents** — and 5,628 of 5,629 of them sat in
the agent session transcripts, not the deliverables. The scan tells you where; the fixes are
upstream: anonymous export from your LMS, or an assignment instruction to keep names in the
LMS field and out of the file.

### The privacy benefit is real and strictly secondary

- **GDPR: pseudonymization is not anonymization.** Recital 26 — if a key exists that can
  re-attribute the data, it is still personal data and the Regulation applies in full. You
  keep the key, because you have to return grades to real people. This is an Article 32
  security measure, not an exemption.
- **FERPA: the content is the education record, not just the name on it.** The
  de-identification provision (34 CFR §99.31(b)) needs indirect identifiers gone *and* a
  reasonable determination that identity is not ascertainable. On student prose you cannot
  make that determination, and in your own hands nothing is de-identified — you hold the
  roster.
- **Why codes and not hashes.** Hashing a name is reversible against a class roster in
  microseconds, and the same FERPA provision requires a code *not based on* the student's
  own information. Codes here are random, shuffled, and fresh per run — a code reused across
  assignments is a linkable profile.

### Getting the names back at delivery

This is the step people forget to plan for, so plan for it here. Your letters are addressed
to `unit-a`, `unit-b`, …; the map says who those are. One command, run **outside** the
grading session (that session is denied read access to the map, which is the whole point):

```
python3 code-units.py --decode ~/.grade-audit-keys/f26-mp1/<run>.map.json
```

It prints one row per unit — code, source folder, and whatever identity columns your roster
carried — and reminds you to hand-check one before sending the batch. A mis-sent grade is not
a recoverable error.

Two things that keep this simple, and are worth not undoing:

- **One hop, not two.** The audit tooling deliberately does not re-code units that are already
  coded. A workspace built by this pass keeps `unit-a` all the way through to the letter, so
  the map file is the only lookup you ever need. (If you grade uncoded folders, the matrix
  relabels them for its own output and prints that legend once, to the terminal — keep it, or
  better, code the units and avoid the second mapping.)
- **The map is the only copy.** Nothing else records the link, by design. Back it up with the
  same care you would give a gradebook, and delete it when the grades are final and appealed.

### Putting the names back into the letters — locally

`--decode` tells you who each unit is. `--personalize` does the delivery step itself, on this
machine:

```
python3 code-units.py --personalize working-notes/letters/ \
        --map ~/.grade-audit-keys/f26-mp1/<run>.map.json \
        --out ~/letters-to-send/ --code-phrase "your submission"
```

Dry run first, always — it prints which letter maps to which person before writing anything.
It reads local files and writes local files; there is no network code in any script this
plugin ships, and you can check that yourself with a grep for `urllib`, `requests`, `socket`
and `http`.

What it does and deliberately does not do:

- **Greeting placeholders become the name.** `Dear [student],` → `Dear Ada Lovelace,`.
- **Unit codes in the body are left alone by default**, and reported with line numbers. A code
  in the body refers to the *work* — substituting a name turns "your work on unit-a" into "your
  work on Ada Lovelace". Pass `--code-phrase "your submission"` if you want them replaced, and
  choose the wording yourself.
- **Mapping is exact, not fuzzy.** A letter belongs to the unit whose code is its filename
  stem (`unit-a.md`) or its containing folder (`unit-a/letter.md`). Nothing else is guessed at,
  so one filename cannot claim two units, and a file that resolves to no unit — a README, a
  cohort summary — is simply skipped as not-a-letter rather than stopping the batch.
- **One thing does stop the whole run: a letter that names another unit inside it.** That is
  not a mapping problem and no naming scheme prevents it; it is the never-event rule firing —
  no subject may be named or identifiable in another subject's feedback. Fix the letter, not
  the mapping. Nothing is written for any letter while one is outstanding, because a
  mis-delivered letter is indistinguishable from a correct one until a student replies.
- **Output goes somewhere separate** from the coded letters, and it refuses to overwrite them.
  Those files now carry identities: keep them out of version control, and hand-check one
  against the map before sending the batch.

### Keep the key out of reach — and enforce it

The map goes in a directory the script refuses to place inside the workspace — checked
against the workspace root, not merely the directory you ran from — `chmod 700`, map at
`0600`. The in-workspace report carries counts and unit codes, and redacts any roster
identity from the paths it prints.

The script also prints a `deny` rule for `.claude/settings.json`. Be precise about what that
buys: it denies the **Read tool** and **`cat`** on that path. It does not stop `head`,
`grep`, `less`, or a Python one-liner, and the map sits under the same UID as the session. It
is a guardrail that makes casual access fail loudly, **not a sandbox**. The real separation is
that the directory is outside the workspace, and you can keep it on different media entirely.

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

## Telling students — suggested language you should edit

Institutional AI guidance converges on two points that pull in the same direction: people
being evaluated have an interest in knowing an automated system was involved, and the
instructor remains accountable for explaining the basis of any decision. Setup asks about
this at Q6c and records your answer; whether and how to disclose is yours to decide, and
some institutions decide it centrally.

If you do disclose, the useful thing about this workflow is that you have something
concrete to say. Two drafts to adapt — **do not paste these unread**, they make factual
claims about your course that only you can confirm:

**For a syllabus or assignment page:**

> Feedback in this course is written and graded by me. I use an AI-assisted review pass to
> check my own drafts before I send them: it verifies that quotations are accurate, that
> numbers match your submitted work, that arithmetic adds up, and that any credit or
> criticism I give is supported by something in what you actually turned in. It flags
> problems for me; I decide every point and every grade. If you would like to know more
> about how your feedback was produced, ask me.

**For a one-line footer on the feedback itself:**

> Written and graded by [name]. An automated pass checked the quotations, figures, and
> arithmetic in this letter before it was sent.

Three things to keep true if you rewrite them. First, do not describe the tool as grading
your students -- it drafts and prices, and you approve, so "I decide every point" is the
claim to keep. Second, do not promise the check is exhaustive; it covers what leaves a
trace, and [LIMITS.md](../../../LIMITS.md) says which forms those are. Third, if you tell
students their work is de-identified before it reaches the model, make sure that is
actually true of your setup (the coded-units pass codes the container, and the scan report
tells you what identity the contents still carry).

## The one-line summary for a skeptic

Everything the harness produces is a local file you can read; what leaves your machine is
the same as any Claude session under your plan's terms — so set the workspace to
anonymized codes, keep inputs gitignored and the name map local, and what reaches anyone is
your rubric applied to coded units — **plus whatever identity the submissions themselves
still contain**, which this pass reports and does not remove.
