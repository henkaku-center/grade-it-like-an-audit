# The markdown is the program

*How to instruct an AI agent for recurring, high-stakes work — the full method.*

High-stakes evaluative work fails in one predictable way: a claim that is *almost* right
ships anyway. A number sourced to the wrong place. Praise that overreaches by one
counterexample. A quote that is close but not verbatim. You do not beat that by being more
careful. You beat it with structure.

This document describes that structure in three layers of instruction infrastructure —
**layered files, persistent memory, and a self-correcting write-back loop** — and the three
things those files encode: a **deduction discipline**, an **audit harness**, and a **loop to
convergence**. It closes with a setup recipe you can follow for your own work.

The running example is grading, because that is where the method was hardened. No illustration
here reproduces anyone's actual work — each is described by shape, with the subject matter and
identifying specifics removed. The **run statistics** (round counts, finding counts, defects
found inside prior fixes, outcomes changed) are real, because a method page that invents its
own evidence is worthless; every one is an aggregate about a process, attached to no person.

---

## Contents

1. [The layered instruction files](#1-the-layered-instruction-files)
2. [Persistent memory across sessions](#2-persistent-memory-across-sessions)
3. [The write-back loop](#3-the-write-back-loop)
4. [Encoded: the discrete-deduction discipline](#4-encoded-the-discrete-deduction-discipline)
5. [Encoded: the audit harness](#5-encoded-the-audit-harness)
6. [Encoded: the loop to convergence — and when it stops converging](#6-encoded-the-loop-to-convergence--and-when-it-stops-converging)
7. [What the harness cannot catch](#7-what-the-harness-cannot-catch)
8. [In practice: two runs](#8-in-practice-two-runs)
9. [Set it up for your own work](#9-set-it-up-for-your-own-work)

---

## 1. The layered instruction files

You don't configure the agent in code; you *instruct* it in markdown. Every session, the agent
reads the instruction files in scope before it does anything, and treats them as **overriding
its defaults**. The files are plain markdown, checked into the repo, and organized so that the
instructions get more specific as you get closer to the work.

```
your-project/
├─ CLAUDE.md                  ◆ root conventions — shared by every run of the task
├─ task-01/
│  ├─ CLAUDE.md               ◆ this instance's specifics — criteria, sources, gotchas
│  ├─ end-user/CLAUDE.md        — (optional) an instruction file for a different audience
│  ├─ inputs/                   — the material under review (read-only)
│  ├─ working-notes/<unit>/     — ledger · draft · audit-round{1..N} (working files)
│  ├─ output.md               ◆ authoritative output — a fixed format
│  └─ deliverables/             — final, cleared artifacts (produced only after the audit passes)
└─ task-02/ …                  — same shape; precedents carry forward
```

**The load rule, stated out loud:** the most specific file in scope wins; more general files
fill in whatever it doesn't say. The root file carries what's true for *all* runs — the
deduction rule, the output format, the audit protocol. The per-task file carries what's true
for *this* run — the criteria, which files are the source of truth for verifying a claim, the
per-task gotchas.

### The trap: several files named `CLAUDE.md`, each with a different job

If the same filename appears at more than one layer — and it will — an agent can import a rule
from the wrong layer and apply it to the wrong reader. Name the contexts explicitly, in the
files themselves. A grading setup, for example, can have three:

| Scope | Job | Audience |
|---|---|---|
| **Repo root** | Reviewer meta-conventions: the deduction rule, output format, audit loop, accumulated precedent. | The agent, as reviewer. |
| **Per-task** | Task specifics: criteria, source-of-truth files, waivers, input conventions. | The agent, as reviewer. |
| **Shipped-with-the-work** | A tutor prompt that goes *to the end user* and tells the agent to guide without giving answers. | The agent, as tutor — a different role entirely. |

When you're reviewing, you are not the end user's tutor, so "never give answers" does not apply
to *your* questions. The docs have to say so, or the agent will guess wrong.

### Output and working files are specified too

The docs don't just set policy — they fix the **shape of the work**. The authoritative output
has a mandated format (for grading: an internal audit section, then the reader-facing letters),
so every run is comparable. The `working-notes/<unit>/` folders hold the agent's artifacts — an
evidence ledger, a draft, one audit report per round — all versioned, so the reasoning behind a
result is recoverable long after the fact.

---

## 2. Persistent memory across sessions

The `CLAUDE.md` files are shared and per-repo. Memory is the complement: a **per-user store
that persists across sessions and projects**, so a brand-new session doesn't start from zero.
It's how the agent begins already knowing "the last run took four review rounds," "this one is
finished," or "the lead prefers to make the borderline calls personally."

The mechanics are deliberately boring, which is what makes them reliable:

- An **index file** is loaded into context every session — one line per memory, so the agent
  knows what it knows.
- Each memory is **one file holding one fact**, with frontmatter that says what it is and how
  to recall it.
- A `type` field sorts memories into: *who the user is*, *how they want you to work*, *ongoing
  project state*, and *pointers to outside resources.*

```markdown
---
name: task-2026-q3-complete
description: Q3 run finished — outcome, where things live, lessons
metadata:
  type: project        # user | feedback | project | reference
---

Q3 run completed 2025-10-14. Five review rounds to converge; outcomes never moved.
Lesson banked: a fix is a new claim — re-verify replacements from scratch.
Related: [[task-2026-q2-complete]]
```

The discipline that keeps it useful: **one fact per file; update instead of duplicating; delete
what turns out wrong; and don't store what the repo already records.** Memory is for what you
couldn't reconstruct from the code and the history — not a second copy of it.

---

## 3. The write-back loop

This is the property that makes the whole thing worth the effort. When a review catches a
mistake, you don't just fix the mistake. **You add a rule to the docs so that class of mistake
can't recur** — on this run or the next one. The instruction set is not written once; it is
edited by its own failures.

> Every rule in a mature root file exists because something went wrong once. The docs are scar
> tissue from past mistakes — which is exactly why the next run doesn't repeat them.

The cycle:

1. **A run hits a failure mode.** For instance, a reviewer credits the subject with an idea the
   assistant actually suggested — a real, subtle attribution error.
2. **The immediate fix is applied and re-reviewed.** That unit is corrected and re-checked whole.
3. **A durable rule is written back into the docs.** *"Verify who originated an idea against the
   raw record — and read the log's actual structure, not just the obvious field."* Now it's
   standing policy.
4. **The next run's agents are pre-warned.** They read that rule before they start. The mistake
   that cost a round last time costs nothing this time.

You can watch institutional knowledge accumulate in the file itself. A mature root file grows
lines like these, each traceable to the run that earned it:

```
# excerpts — each is a scar from a prior run
• Write cohort claims without factual universals — one counterexample fails review.
• Revisions introduce errors at a high rate; re-review whole units, not the flagged spot.
• Praise is checked as strictly as criticism.
• Verify behavior claims against the shipped artifact, not the session narrative.
• A fix is a new claim, and inherits the counterexample.
```

A prompt you retype each session can't do this. A file can. That's the case for treating
instructions as version-controlled infrastructure rather than conversation.

---

## 4. Encoded: the discrete-deduction discipline

One rule the files impose on every judgment: **every point you remove (or every finding you
raise) is tied to a discrete, named issue, with a one-line "how to avoid."** If you can't name
the specific thing the subject did or failed to do, the points are awarded — the finding isn't
raised. A judgment is a claim, and a claim needs evidence.

```
Item 3: 16/20 — (−4) two required fields left empty; the summary sheet marks them "n/a."
  How to avoid: either field accepts one line — "not measured, because X" scores full.
  // no nameable issue on the other 18 points → they are earned, not "given"
```

Three moves make the discipline hold up under pressure:

- **Praise is audited as strictly as criticism.** The counterintuitive lesson from checking the
  method's own output: most errors were *overclaimed praise*, not wrong criticism — the
  criticism was evidenced from the start; the compliments drew on impression. So every quote and
  superlative in the positive section is logged with its source, exactly like a deduction.
- **Ground truth beats memory, always.** Every number or behavioral claim is verified against
  the source — the actual code, file, or record — never against recollection.
- **"What you were owed."** If your own instructions told the subject X, you don't penalize them
  for X, even when the system actually does Y. Decide up front which sources are *authoritative
  for the subject* and which are merely *true*.

Two things are fixed in writing before any work starts: the **regime** (what counts toward the
result) and the **criteria** (held constant across everyone). Deciding what counts *after* you've
seen the work is how bias enters.

---

## 5. Encoded: the audit harness

The person who writes an evaluation is the worst person to check it — they will re-confirm their
own reasoning. So drafting and auditing are separate jobs, and the auditors are independent *by
construction*, not by good intentions.

**One unit of work per auditor — blind to the rest.** Each auditor is handed exactly one unit
and reads *only* that unit's files. They cannot see the other evaluations, the other inputs, or
each other's findings. This isolation is the whole point: a claim can't be "confirmed" by
another unit's data, and a detail borrowed from the wrong place has nowhere to hide.

```
                    ┌─────────────────────────┐
                    │  Lead: drafts + normalizes │
                    └────────────┬────────────┘
        ┌──────────┬─────────────┼─────────────┬──────────┐
    Auditor A   Auditor B    Auditor C     Auditor D   Auditor E
   reads only  reads only   reads only    reads only  reads only
       A           B            C             D           E
        └──── independent · fresh eyes each round · no shared context ────┘
```

Two supports make the fan-out work:

- **The evidence ledger**, written *as the draft is written*, logs every claim beside its source
  line. Auditing then means checking each claim against what it cites — not re-deriving the whole
  evaluation — and flagging anything that cites nothing.
- **A lead pass catches what isolation can't: cross-unit consistency.** In one run, an identical
  praise line was flagged in one unit and passed in another *in the same round*, because each
  auditor saw only their own. The lead greps the whole set for shared phrasings and applies the
  strictest verdict anyone reached to every instance. Fan out for depth; one pass for coherence.

---

## 6. Encoded: the loop to convergence — and when it stops converging

Audits find things; fixes get made; and then — this is the part everyone gets wrong — the fixes
get audited *again*. The loop does not stop when each unit has been clean at some point. It stops
on one strict condition:

> **One pass comes back clean for the entire set at the same time.**

```
draft+ledger → normalize(lead) → audit(fan-out) → revise → re-audit WHOLE unit
      ↑                                                              │
      └──────────── if any unit fails, the set isn't clean ─────────┘
                              ↓  (clean for all at once)
                             ship
```

Two rules keep the loop from lying to you:

- **Re-audit the whole unit, not the flagged spot.** A revision changes the surrounding text and
  how it reads; checking only the edited line misses what the edit broke elsewhere.
- **The human stays in the loop.** Every round surfaces its findings and what changed; the
  judgment calls — borderline deductions, tone, whether a fix is acceptable — are the human's,
  not the harness's.

### The stopping rule tells you when you *may* stop. It does not tell you when to stop trying.

This is the correction a later run forced, and it is the most important thing on this page.

That run took **nine rounds** over five units and never satisfied the rule. Blockers — findings
that would change what shipped — hit zero at round seven and stayed there. Minor findings did
not fall. They flattened at eight to eleven per round and stayed flat. The loop was not
converging. It was idling at a constant rate, and a tenth round was queued on the assumption
that a clean pass was one more round away. It was not.

**The diagnostic is a single question:**

> What fraction of this round's findings are in text that did not exist before the last round?

On round nine, seven of ten were. The loop had stopped measuring the artifact's error rate and
started measuring **its own edit rate**. Every round produced fixes; every fix was new text; new
text is where findings come from. A process that manufactures its own work does not converge,
and running it again is not a plan.

**The resolution was not another round. It was to scope the exposure.** Instead of asking "what
is still wrong?", ask "what actually changed in the material that ships?" — and diff it.

That diff took minutes and collapsed the problem. Most of the round's findings sat in text that
never leaves the building: internal notes, working commentary, per-unit reasoning. Of the
material that actually reaches the reader, **exactly two sentences had changed** since the
previous round. One was a deletion, which cannot introduce a new claim. The other introduced a
single new noun, which was checked against the source artifact in one search.

Nine rounds of process, replaced by one diff and one check.

```
if (blockers == 0 for N rounds) and (findings mostly land in the previous round's own fixes):
        stop looping · diff what ships · verify only what changed there
else:
        loop
```

**The rule:** before convening another round, diff the shipped artifact against the last
audited version. If this round's findings concentrate in text the reader will never see, the
loop is auditing itself. **Audit what ships.**

Two cautions, so this is not read as permission to quit early:

- **This applies only after blockers have gone to zero and stayed there.** A loop still finding
  substantive errors is converging, however slowly, and the stopping rule stands.
- **Scoping is a verification step, not a skip.** The two changed sentences were still checked
  against sources. What was dropped was the *ceremony* of a full pass, not the checking.

### The lessons that cost the most

Each of these is why a rule exists. If you take nothing else, take these.

1. **A fix is a new claim, and it inherits the counterexample.** Rewording a flawed sentence
   usually preserves what made it flawed. Re-verify every replacement from scratch, as if it had
   never been checked.
2. **When a claim fails twice, delete it — do not narrow it.** This is the resolution to lesson
   1, and it took four rounds on one claim to learn. The instinct on a failed claim is to add a
   qualifier, restrict the scope, hedge the verb. Each narrowing is a new claim that usually
   inherits the same counterexample. One claim produced a finding in four consecutive rounds;
   each round narrowed it; the fourth found that the previous narrowing had landed on the wrong
   side of a dash, leaving the original conclusion standing in adjective form. **Subtraction is
   the only edit that cannot inherit a counterexample.** It held every time it was used;
   narrowing did not hold once.
3. **Revisions introduce errors at a high rate.** Every round's fixes seed the next round's
   findings. This is the default behavior of editing under pressure, not sloppiness — which is
   why the re-audit step is non-negotiable, and why lesson 2 matters so much.
4. **A verification assertion is itself a claim, and it can be false.** "Every reference was
   checked." "All sources verified." These read as process notes; they are claims, and nothing
   checks them. One round's record asserted that every cross-reference in it had been opened and
   verified. A later reviewer opened them: five did not resolve, and two pointed into a
   different unit's material. **Record the count you actually checked** — "six of eight
   verified, two not" is worth more than "all verified," and unlike "all verified" it can be
   true.
5. **A record can interfere with its own instrument.** One note recorded that a search over the
   project history returned exactly one result — a reproducible verification, correctly
   performed. Committing the note made it false, because the note *quoted the search string* and
   so became a second result. **Record what you found and where, not the command that found
   it**, whenever the command searches text the record will then quote.
6. **Praise universals die to a single counterexample.** "You did X *every* time" — one exception
   falsifies the whole sentence, and there's almost always one. Write "nearly every," "most," or
   name the instances.
7. **Attribution is a data-format trap.** Deciding who said something first, from a raw log, means
   reading the log's *actual* structure — a person's words can be recorded under a field you
   weren't searching. Verify against how the record is really shaped.
8. **Verify behavior against the shipped artifact, not the narrative.** What a system *did* is
   settled by its code and output, not by the story of the session.
9. **Independence needs a coherence pass on top.** Isolated reviewers are right for depth and for
   catching cross-contamination, but they cannot enforce consistency *between* units. Pair the
   fan-out with one lead pass. Neither alone is sufficient.
10. **Generate every format from one source.** If the same content ships as a document *and* a
    message *and* a summary, generate them all from one file. On one run a late correction
    reached two of six copies, and three different wordings of the same sentence went out to
    different readers. It surfaced a month later, by accident, and by then the archive no longer
    matched what people had actually received.

---

## 7. What the harness cannot catch

Sections 4–6 are the machinery. This section is its blind spots — both found the hard way, and
neither fixable by running the machinery harder.

### Audit the standard, not just the output

The discrete-deduction discipline makes every judgment defensible *against the criteria*. It
never questions the criteria.

One run surfaced three criteria that could not be scored at all — not because the work was weak,
but because **the evidence each criterion graded had never been collected.** A criterion was
published, weighted, and counted toward the outcome; nobody had gathered the material it judged.

The signature is unmistakable once you know it. Independent reviewers, handed identical
evidence, scored one such criterion across a **twelve-point spread on a twenty-point scale.**
That is not disagreement about quality. It is disagreement about what is even being read — and
it is what an unscoreable criterion looks like from the inside.

The resolution generalizes to one test, applied to your own standard rather than to the work:

> **Did the instructions explicitly ask for this, and did we collect what we asked for?**

Where the answer is no, **the cost falls on the assessor, not the subject.** Criteria that
failed the test were dropped and the remainder rescaled; a component nobody had collected was
awarded in full to everyone. Subjects are held to what they were told to do — not to what you
wish you had told them.

Run this *before* the work starts:

- For each criterion, name the artifact that will evidence it. Not "we'll see it" — the file.
- If no artifact gets collected, the criterion is decoration. Collect it or delete it.
- **Partial capture is worse than none.** If a criterion's evidence is captured for some
  instances and not others, do not use it. Partial evidence *looks* scoreable, which is exactly
  the danger: scoring from it makes the outcome depend on who happened to get recorded rather
  than on what they did. A reviewer will reach for it precisely because it is there.

### Independent reviewers share blind spots — and more of them will not help

The fan-out in section 5 catches what one reviewer misses. It cannot catch what all of them are
looking away from.

On one run, a single sentence survived **nine rounds and forty-five independent reviews.** One
round examined that exact sentence and passed it, with a note explaining why it was fine. A
second person then read the finished material once, cold, with no knowledge of the process, and
flagged it immediately.

The sentence predicted the work's future influence in the world. Every reviewer had checked it
the way they checked everything: is it sourced, is the attribution right, does it contradict the
record? It passed all three — because **a claim about what will happen later has no source to
contradict it.**

The reviewers were calibrated for one failure mode and blind to another. Two fixes, and you want
both:

1. **Add the check explicitly**, because it is not implied by "verify every claim":
   > Is this claim about the artifact, or about the world? A claim about the world cannot be
   > verified against the artifact, and no amount of source-checking will surface it.
2. **Keep one reader outside the loop.** Not a better auditor — a *different* one, arriving
   once, at the end, without the process in their head. Forty-five reviewers inside the harness
   were worth less on this specific defect than one person reading it fresh. Budget for that
   person.

The general form is worth stating plainly, because it applies to any review system you build:
**a harness converges on the failure modes it was built to catch, and grows blind to the rest in
proportion to how well it works.** The better your loop gets, the more you need someone outside
it.

---

## 8. In practice: two runs

Two runs of the same harness over five units each. In **both**, the outcomes were settled early
and **never moved** — across fourteen rounds and seventy independent reviews, not one finding
changed an outcome. Every one was a grounding or phrasing defect. That is the strongest single
piece of evidence for the method and the strongest argument for bounding it: the loop is very
good at prose defects and, on this evidence, unnecessary for outcomes.

### Run A — converged in five rounds

| Round | What happened |
|---|---|
| **1** | Cleared too early — declared clean after four of five auditors reported; the fifth landed late and caught a real misquote. Lesson banked: convergence means *all* units in the same pass. |
| **2** | Four blockers the first pass had approved: a paraphrase inside quotation marks, credit for something the assistant actually prompted, and two praise universals — each falsifiable from the unit's own files. |
| **3** | One blocker *inside* a round-2 fix (a reworded sentence still carried its counterexample) — plus a reversal: a round-1 "correction" turned out to be the error, and was reversed against the raw record. |
| **4** | Same clause, third rewrite, still wrong — it kept implying a claim the shipped artifact couldn't back. Only when reduced to a plain, countable fact did it hold. |
| **5** | Clean for all five, in the same pass. Convergence. |

**5** rounds · **3** defects hidden in prior fixes · **0** outcome changes · **1** clean pass = done.

### Run B — nine rounds, and it never converged

Same harness, harder material, and the run that produced section 6's correction and section 7
entire.

| Round | Blockers / minors | What happened |
|---|---|---|
| **1–5** | 3 / 18 at the low point | Substantive findings, including the inverse of run A's failure: text *softer* and more flattering than the reasoning behind it. Real convergence. |
| **6** | 1 / 10 | The one blocker was round 5's own blocker, surviving inside round 5's replacement for it. Third consecutive round where the defect was the repair. |
| **7** | 0 / 11 | First round with no blocker anywhere. What it found instead: the *countermeasure* from round 6 had failed three times — bad cross-reference counts, a tally short by two. |
| **8** | 0 / 8 | Findings now one level inside the process: a clause correctly narrowed in round 7 whose following inference was left unnarrowed. |
| **9** | 0 / 10 | **Seven of ten findings were defects in round 8's repairs, or in the record describing them.** Count rising, not falling. |
| **—** | — | **Stopped by diff, not by another round.** Two sentences of shipped text had changed since round 8; both verified directly. See section 6. |

**9** rounds · **45** independent reviews · **0** outcome changes · **0** clean passes ·
**stopped by scoping.**

Then the part that matters most: a second person read the finished material once, cold, and
found a defect that all nine rounds had passed — and one round had explicitly approved. See
section 7.

### What the two runs together say

- **The loop is worth running.** Run A's three-defects-inside-fixes and run B's rounds 1–5 are
  real errors caught before they reached anyone.
- **The loop must be bounded.** Run B shows it does not always terminate on its own, and that a
  process generating its own findings can look identical to a process still finding things.
- **Neither run's audits changed an outcome.** Fourteen rounds. If your loop is meant to protect
  the *result*, measure whether it ever has; if it only ever protects the *prose*, size it
  accordingly.
- **Keep someone outside it.** The cheapest defect-per-hour on either run was one fresh reader
  at the end.

---

## 9. Set it up for your own work

None of this is specific to grading. It fits any recurring, high-stakes task you hand to an AI
agent — code review, a compliance or security audit, report QA, contract review, release notes —
anywhere a plausible-but-wrong result is expensive and the task comes around again.

1. **Stand up the file tree.** One repo, a root instruction file, a folder per instance of the
   task, working-file and output conventions. Version everything.
2. **Seed the root conventions.** Write what's true for every run: the standard for a finding, the
   output format, the review protocol. Keep it general; specifics go one layer down.
3. **Write the per-task file — and name your ground-truth sources.** The criteria for this task,
   and exactly which files or systems are authoritative for verifying a claim. Separate what's
   authoritative from what your subject was entitled to rely on.
   **Then audit the criteria themselves, before any work starts** (section 7): for each one,
   name the artifact that will evidence it, and delete or fix any criterion whose evidence you
   will not actually collect — or will collect only for some instances.
4. **Fix the working-file shape.** An evidence ledger (claim + source, written as you draft), a
   defined output format, one review file per round. Make the reasoning recoverable.
5. **Turn on memory for continuity.** Let a fresh session start knowing the last run's state and
   your standing preferences, without re-explaining.
6. **Run the harness and the loop — and bound it.** Independent reviewer per unit, blind to the
   rest; a lead pass for cross-unit consistency; re-review whole units; stop on one clean pass
   over everything. **And decide in advance what you will do if that pass never comes** (section
   6): once blockers sit at zero and the findings are mostly landing in the previous round's own
   repairs, stop looping, diff what actually ships, and verify only what changed there.
7. **Book one reader outside the loop.** A person who arrives once, at the end, who has not
   watched the process and is not calibrated by it. This is the cheapest defect-per-hour in the
   whole method (section 7).
8. **Write every lesson back into the docs.** *This is the step that makes it worth doing.* Each
   failure becomes a rule; the instruction set gets stronger every run instead of resetting.
9. **Keep a human on the judgment calls, and keep the trail.** What changed, and what it changed
   *from*, is the audit record — it's how a later reader trusts the result.

### Working solo, or without a multi-agent setup?

The instruction files and memory work with a single agent — the layering and the write-back loop
are the valuable parts, and neither needs a fleet. You can even be your own auditor: draft, let it
rest, and return as a stranger who must verify every claim against its source with no memory of
writing it. The ledger is what makes that honest — "re-checking" means checking sources, not
re-reading your own reasoning.

---

*Built with [Claude Code](https://claude.com/claude-code). The method is tool-agnostic — any
agent you can point at a repo of instructions works the same way.*
