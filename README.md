# Grade it like an audit

**A field-tested method for instructing AI agents on recurring, high-stakes tasks — using
layered markdown, persistent memory, and a self-correcting write-back loop. Now an
installable Claude Code plugin with a guided setup, a blind-auditor fan-out, and a
12-to-18-minute demo that hunts planted defects in front of you.**

*No demo recording exists yet — rather than stage one, the site publishes real output from
recorded test runs instead: [what an auditor actually reports](https://henkaku-center.github.io/grade-it-like-an-audit/how-it-works.html#artifacts),
from `docs/test-runs/`.*

Most people instruct an AI agent by typing a prompt into a chat. That works for one-off
tasks and falls apart for anything you do repeatedly and can't afford to get wrong: the
instructions live in your head, drift between runs, and reset to zero every session.

This repository is a different approach, three ways at once: a **methodology** you can
read, a **template kit** you can copy by hand, and a **plugin** that automates the whole
workflow. It was built and hardened on a real grading workload, but nothing in the method
is specific to grading — it fits code review, security and compliance audits, report QA,
contract review: any task where a *plausible-but-wrong* result is expensive and the task
comes around again.

> **This repository contains no personal data about any student, subject, or evaluated
> person.** The only individuals named are the authors and, in the comparison survey,
> public maintainers of the projects surveyed. No submitted work, no evaluation
> outputs. Generic methodology, reusable templates, and synthetic demo data only. See
> [Privacy & scope](#privacy--scope).

---

## Try it without trusting it

The demo grades three **fictional** students whose draft evaluations contain **seven
planted defects** — a misquote, a wrong number, an overclaimed compliment, a
misattribution, broken arithmetic, an error hiding inside a previous "fix," and one defect
**no source can settle** — the harness flags it as unverifiable; only a human can rule on it. You watch independent auditors hunt the six (our
pre-ship test run caught all six — plus three blocker-class defects we hadn't planted),
then the answer key is unsealed, the seventh is revealed, and you learn why a human
stays in the loop. Twelve to eighteen minutes, measured twice. Zero real data.

```
/plugin marketplace add henkaku-center/grade-it-like-an-audit
/plugin install grade-it-like-an-audit
```

Then, in any empty folder:

```
/grade-audit demo
```

Still skeptical after the demo? Invert the trust arrow — two more rungs before the AI
drafts anything:

- **`/grade-audit check-mine`** — the harness fact-checks evaluations *you* wrote (your
  quotes, numbers, arithmetic, attributions). The AI never grades; it audits you.
- **`/grade-audit calibrate`** — you grade 3–5 units first; the harness grades them blind;
  a deterministic script reports the agreement (κ, ρ, mean absolute difference) so you see
  how it compares to *your* judgment before it touches anything real.

When you're ready: `/grade-audit setup` interviews you in plain language and generates
your whole workspace. From then on, `/grade-audit` alone always tells you where you are
and what's next.

> ⚠️ **Educators: know where your institution stands before real student work enters
> any AI tool — this one included.** Student submissions and grades are typically
> education records under FERPA (or your local equivalent: state student-privacy law,
> GDPR). Many institutions already have approved arrangements that cover AI services —
> yours may too — but that coverage comes from *your institution's* policies and
> agreements, not from this plugin or any provider's marketing. If you're not sure, ask
> your registrar, privacy office, or counsel before you start, and use the
> no-student-data rungs meanwhile (the demo is fully synthetic). The setup interview
> asks about this explicitly and records your answer; it will never block you — the
> decision and the responsibility are yours. Details:
> [data-handling guidance](skills/grade-audit-setup/references/data-handling.md). This
> is not legal advice, and the authors accept no liability for unauthorized or
> non-compliant use — see the [Disclaimer](#disclaimer).

## Never used Claude Code?

Claude Code is Anthropic's AI coding/agent tool; this plugin runs inside it. Two ways in:

- **Browser, nothing to install:** [claude.ai/code](https://claude.ai/code) (requires a
  Claude subscription). Plugins work there too.
- **Terminal:** `curl -fsSL https://claude.ai/install.sh | bash` (macOS/Linux/WSL) or
  `irm https://claude.ai/install.ps1 | iex` (Windows PowerShell), then run `claude` and
  sign in. Docs: [code.claude.com/docs](https://code.claude.com/docs).

Four words you'll meet, once each: a **skill** is a packaged instruction set you invoke by
typing `/its-name`; a **CLAUDE.md** is a plain markdown file of standing instructions the
agent reads automatically — in this method, *your* rulebook, which you own and edit; a
**subagent** is a helper with a fresh, isolated context (how the auditors are kept blind
— by construction; [LIMITS.md](LIMITS.md) spells out that boundary); **persistent memory**
is what lets a new session start knowing where the last one left off. That's all the
jargon there is.

**What it costs to run:** one audit round over N units spawns N auditor subagents plus one
consistency pass; budget 3–5 rounds (our two recorded runs took 5, and 9 with an early
stop). The demo is a fair small-scale
preview. Before your first real run, read **[LIMITS.md](LIMITS.md)** — this method
publishes what it cannot do with the same care as what it can.

## For skeptics — the honest numbers first

Across the method's two hardening runs: **14 audit rounds, 70 independent reviews — and
not one finding ever changed an outcome.** Every catch was a grounding or phrasing defect:
a misquote, a wrong number, an overclaim. The loop protects the *evidence and the prose*;
the *outcomes* were protected by the human's judgment plus the evidence discipline. And
one human reading the finished material cold found a defect that all nine rounds of the
run that produced it — forty-five reviews — had passed.

Those numbers are why the design works the way it does: every judgment must cite a source
you can open; every fix needs your approval; all state is plain files on your machine
("you can audit the auditor"); and the system tells you — in [LIMITS.md](LIMITS.md), in
the demo's final beat, in the convergence checklist — exactly where its blind spots are
and why the last reader must be human.

---

## Read it

**The website** — [henkaku-center.github.io/grade-it-like-an-audit](https://henkaku-center.github.io/grade-it-like-an-audit/)

| Page | What it covers |
|---|---|
| [Overview](https://henkaku-center.github.io/grade-it-like-an-audit/) | What it is, the honest numbers, and the three rungs before it touches anything real |
| [How it works](https://henkaku-center.github.io/grade-it-like-an-audit/how-it-works.html) | The workflow end to end, with real recorded output, and every option you can turn |
| [Limits & privacy](https://henkaku-center.github.io/grade-it-like-an-audit/limits.html) | What it cannot do, the comparative-disclosure limitation, and where responsibility rests |
| [How it compares](https://henkaku-center.github.io/grade-it-like-an-audit/compare.html) | The landscape, with the places others are ahead stated first |

**The source documents**

- **[`METHODOLOGY.md`](METHODOLOGY.md)** — the full method as an editable document.
- **[`DESIGN.md`](DESIGN.md)** — why the plugin is engineered the way it is, and the
  record of the harness being run on itself.
- **[`LIMITS.md`](LIMITS.md)** — blind spots, costs, and when *not* to use this.
- **[`COMPARISON.md`](COMPARISON.md)** — the landscape, surveyed honestly.

## Use it

Three paths, one source — the skills generate workspaces from the same templates you'd
copy by hand:

1. **The plugin** (above) — guided setup, automated audit rounds, demo, calibration.
2. **By hand** — the [`templates/`](templates/) starter kit:

   | File | What it is |
   |---|---|
   | [`CLAUDE.root.md`](templates/CLAUDE.root.md) | Root conventions — the rules true for *every* run of the task. |
   | [`CLAUDE.task.md`](templates/CLAUDE.task.md) | Per-instance specifics — criteria, sources of truth, gotchas. |
   | [`CLAUDE.end-user-facing.md`](templates/CLAUDE.end-user-facing.md) | Example of a *third* instruction context for a different audience. |
   | [`evaluation-report.template.md`](templates/evaluation-report.template.md) | A fixed two-part output format so every run is comparable. |
   | [`auditor-prompt.template.md`](templates/auditor-prompt.template.md) | The independent-reviewer prompt for the audit fan-out. |
   | [`memory-file.template.md`](templates/memory-file.template.md) | The one-fact-per-file persistent-memory format. |

3. **Beyond grading** — pre-filled task files in
   [`templates/quickstarts/`](templates/quickstarts/) for code review, compliance audit,
   and contract review, because the method never was grading-specific.

> The files are named `CLAUDE.md` because this method was built with
> [Claude Code](https://claude.com/claude-code), which auto-loads them into context. The
> *idea* is tool-agnostic — any agent that can be pointed at a repo of instructions works
> the same way. Rename to `AGENTS.md`, `.cursorrules`, or whatever your tool reads. (The
> plugin's automation is Claude Code-specific; the by-hand path is not.)

---

## The method in one screen

Three moving parts:

1. **Layered instruction files.** Markdown that auto-loads and overrides defaults,
   organized so the instructions get *more specific as you get closer to the work*:
   general conventions at the repo root, task specifics one level down. Most-specific
   wins; general fills the gaps.

2. **Persistent memory.** A per-user store that survives across sessions — an indexed set
   of single-fact files — so a fresh session already knows the last run's state and your
   standing preferences instead of starting from zero.

3. **The write-back loop.** The part that matters most. When a review catches a failure,
   the fix isn't just applied — a *rule* goes back into the docs, so that failure can't
   recur next time. **The instruction set compounds. Every run that catches something makes it stronger.** (In
   the plugin, a round is not closed until its lessons are written back.)

What those files *encode* is the working method:

- **A discrete-deduction discipline** — every judgment (every point removed, every finding
  raised) is a discrete, named, evidenced claim. If you can't name it, you don't claim it.
- **An independent audit harness** — one reviewer per unit of work, each reading *only*
  that unit, blind to the rest, so a claim can't be "confirmed" by another unit's data.
  Plus one lead pass across the set, for the consistency isolation can't see.
- **A loop to convergence — with a bound on it.** Audits find things, fixes get made,
  fixes get re-audited whole. It ends when a single pass is clean for the *entire set at
  once* — or, when that pass never comes, when a diff of the shipped material shows the
  loop has started auditing its own repairs rather than the work.

In one real run the loop took **five rounds**, and three of its catches were errors found
*inside a previous round's fix.* That is the loop earning its keep.

A second run took **nine rounds and never converged.** Blockers hit zero at round seven
and stayed there, while minor findings flattened and stopped falling — because seven of
round nine's ten findings were defects in round eight's *repairs*. The loop had stopped
measuring the work's error rate and started measuring its own edit rate. It was ended not
by a tenth round but by a diff: of the material that actually reaches a reader, two
sentences had changed, and both were verified in minutes.

Across both runs — **fourteen rounds, seventy independent reviews — not one finding
changed an outcome.** Every one was a grounding or phrasing defect. Then a single person
outside the loop read the finished material once and found a defect that all nine rounds
— forty-five reviews — of the run that produced it had passed.

Those three facts are the honest summary of what this method does, what it costs, and
where its blind spot is. See [`METHODOLOGY.md`](METHODOLOGY.md) for the detail, and
[`LIMITS.md`](LIMITS.md) for the full bill.

---

## How it compares

No other Claude Code skill did audit-style grading when we surveyed (2026-08): blind
per-unit fan-out + lead consistency pass + a bounded convergence loop + structural
write-back — and none we found, in any category, publishes failure-inclusive run
statistics. Commercial tools are far ahead on UI and LMS integration;
PrairieLearn on classroom-scale infrastructure; one apparently dormant skill's
κ-calibration idea was ahead of ours, so we adopted it and credited it. Full table, links, the searches
behind every absence claim, and where others beat us: **[COMPARISON.md](COMPARISON.md)**.

## Quick start (by hand, no plugin)

```
your-project/
├─ CLAUDE.md                  # ← start from templates/CLAUDE.root.md
├─ task-01/
│  ├─ CLAUDE.md               # ← start from templates/CLAUDE.task.md
│  ├─ inputs/                 # the material under review (read-only)
│  ├─ working-notes/<unit>/   # ledger · draft · audit-round{1..N}
│  └─ output.md               # ← format from templates/evaluation-report.template.md
└─ task-02/ …                 # same shape; precedents carry forward
```

1. Copy `templates/CLAUDE.root.md` to your repo root and fill in the bracketed sections.
2. For each instance of the task, copy `templates/CLAUDE.task.md` and name your
   ground-truth sources — the files or systems that settle a factual claim. Audit the
   criteria themselves before any work starts: every criterion names the artifact that
   will evidence it.
3. Draft with an evidence ledger (claim + source, written as you go).
4. Run the audit fan-out with `templates/auditor-prompt.template.md`, one reviewer per
   unit.
5. Loop: re-audit whole units after every revision; stop only on one clean pass over
   everything — and if blockers sit at zero while findings pile up in your own fixes,
   stop looping and diff what ships.
6. **Write every lesson back into `CLAUDE.md`.** This is the step that makes it worth
   doing.

---

## Privacy & scope

This repository is a **methodology, template kit, and plugin only**. It deliberately
contains:

- **No** names or identifying details of any student, subject, or evaluated person (the
  only real people named anywhere are the credited authors and the public maintainers
  of projects in the comparison survey). The demo's "students" and their work are
  synthetic, written for the demo.
- **No** submitted work, evaluations, scores, quotes, or transcripts.
- **No** illustration that reproduces anyone's actual work. Every anecdote is described
  by *shape* — "a paraphrase inside quotation marks," "a claim that predicted how the
  work would be received" — with the subject matter, wording and identifying specifics
  removed.

**Run statistics are real, and deliberately so.** Round counts, finding counts, how many
defects were hidden inside a previous round's fix, and the fact that no audit finding
ever changed an outcome — those are the actual numbers from real runs, because a
methodology page that invents its own evidence is worthless. They are aggregates about a
*process*: none is attached to a person, and no individual's score or work appears
anywhere.

*This bullet used to claim "no data from any real run." That was never accurate and the
page now says what is true instead — an overclaiming privacy notice is worse than an
honest one.*

If you adopt this method, keep your actual working files — inputs, evaluations, memory,
audit notes — in a **separate, private** repository; the plugin's setup gitignores them
by default and offers a coded-units pass (random unit codes, contents copied byte-for-byte
and scanned rather than rewritten, the name map kept outside the workspace — blind grading
and risk reduction, not compliance). Where your material involves
students or other people, read the data-handling guidance
([`skills/grade-audit-setup/references/data-handling.md`](skills/grade-audit-setup/references/data-handling.md))
— including the parts that are your institution's call, not a plugin's.

## Repository home

The canonical repository is
[henkaku-center/grade-it-like-an-audit](https://github.com/henkaku-center/grade-it-like-an-audit)
— it is where the install command points and where the illustrated guide is served from.
Edits land there; any other copy is a mirror (see [RELEASING.md](RELEASING.md)).

## Disclaimer

This project — the methodology, templates, plugin, and documentation — is provided **"as
is," without warranty of any kind**, express or implied. It is not legal advice, and
nothing in it establishes compliance with FERPA, GDPR, or any other law, regulation, or
institutional policy. **You are solely responsible for how you use it**: for confirming
that your use of any AI service on student work or other personal data complies with
applicable law and your institution's policies and agreements, and for the evaluative
decisions you ship. To the maximum extent permitted by law, the authors accept **no
liability for inappropriate, unauthorized, or non-compliant use** of this project or of
any AI service used with it. (The CC BY 4.0 license below carries the governing
warranty-and-liability terms; this section restates them in plain words for this
project's context.)

## Authors

Built and maintained by [Joseph Austerweil](https://github.com/josephausterweil)
([@josephausterweil](https://github.com/josephausterweil)), with Claude Code.

**Origin:** the approach started in the grading-workspace `CLAUDE.md` that
[Ira Winder](https://github.com/irawinder) ([@irawinder](https://github.com/irawinder))
wrote for the APS I course
([henkaku-center/aps-i-eval-2026](https://github.com/henkaku-center/aps-i-eval-2026)).
Everything since — the methodology writeup, templates, skills, agents, demo, evals, and
documentation — is Joseph's, who has carried it forward from there.

## License

Released under [CC BY 4.0](LICENSE) — use it, adapt it, share it. The license's
condition is attribution: give credit, link to the license, and note any changes.
