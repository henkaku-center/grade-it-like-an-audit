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

The running example is grading, because that is where the method was hardened. Every concrete
illustration is generic and invented; none reproduces any real person's work.

---

## Contents

1. [The layered instruction files](#1-the-layered-instruction-files)
2. [Persistent memory across sessions](#2-persistent-memory-across-sessions)
3. [The write-back loop](#3-the-write-back-loop)
4. [Encoded: the discrete-deduction discipline](#4-encoded-the-discrete-deduction-discipline)
5. [Encoded: the audit harness](#5-encoded-the-audit-harness)
6. [Encoded: the loop to convergence](#6-encoded-the-loop-to-convergence)
7. [In practice: five rounds to clean](#7-in-practice-five-rounds-to-clean)
8. [Set it up for your own work](#8-set-it-up-for-your-own-work)

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

Q3 run completed 2026-07-11. Five review rounds to converge; outcomes never moved.
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
Item 3: 18/20 — (−2) required section left blank; the checklist marks it "skipped."
  How to avoid: the template offered four testable options — completing one earns it back.
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

## 6. Encoded: the loop to convergence

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

### The six lessons that cost the most

Each of these is why a rule exists. If you take nothing else, take these.

1. **A fix is a new claim, and it inherits the counterexample.** Rewording a flawed sentence
   usually preserves what made it flawed. Re-verify every replacement from scratch, as if it had
   never been checked.
2. **Revisions introduce errors at a high rate.** Every round's fixes seed the next round's
   findings. This is the default behavior of editing under pressure, not sloppiness — which is
   why the re-audit step is non-negotiable.
3. **Praise universals die to a single counterexample.** "You did X *every* time" — one exception
   falsifies the whole sentence, and there's almost always one. Write "nearly every," "most," or
   name the instances.
4. **Attribution is a data-format trap.** Deciding who said something first, from a raw log, means
   reading the log's *actual* structure — a person's words can be recorded under a field you
   weren't searching. Verify against how the record is really shaped.
5. **Verify behavior against the shipped artifact, not the narrative.** What a system *did* is
   settled by its code and output, not by the story of the session.
6. **Independence needs a coherence pass on top.** Isolated reviewers are right for depth and for
   catching cross-contamination, but they cannot enforce consistency *between* units. Pair the
   fan-out with one lead pass. Neither alone is sufficient.

---

## 7. In practice: five rounds to clean

A real run over five units. The outcomes were settled early and **never moved** — every finding
was a grounding or phrasing defect, not an outcome error. Three defects were found *inside a
previous round's fix.* That's the loop, and the write-back rules, earning their keep.

| Round | What happened |
|---|---|
| **1** | Cleared too early — declared clean after four of five auditors reported; the fifth landed late and caught a real misquote. Lesson banked: convergence means *all* units in the same pass. |
| **2** | Four blockers the first pass had approved: a paraphrase inside quotation marks, credit for something the assistant actually prompted, and two praise universals — each falsifiable from the unit's own files. |
| **3** | One blocker *inside* a round-2 fix (a reworded sentence still carried its counterexample) — plus a reversal: a round-1 "correction" turned out to be the error, and was reversed against the raw record. |
| **4** | Same clause, third rewrite, still wrong — it kept implying a claim the shipped artifact couldn't back. Only when reduced to a plain, countable fact did it hold. |
| **5** | Clean for all five, in the same pass. Convergence. |

**5** rounds to converge · **3** defects hidden in prior fixes · **0** outcome changes from the
audits · **1** clean pass = done.

---

## 8. Set it up for your own work

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
4. **Fix the working-file shape.** An evidence ledger (claim + source, written as you draft), a
   defined output format, one review file per round. Make the reasoning recoverable.
5. **Turn on memory for continuity.** Let a fresh session start knowing the last run's state and
   your standing preferences, without re-explaining.
6. **Run the harness and the loop.** Independent reviewer per unit, blind to the rest; a lead pass
   for cross-unit consistency; re-review whole units; stop only on one clean pass over everything.
7. **Write every lesson back into the docs.** *This is the step that makes it worth doing.* Each
   failure becomes a rule; the instruction set gets stronger every run instead of resetting.
8. **Keep a human on the judgment calls, and keep the trail.** What changed, and what it changed
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
