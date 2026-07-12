# Grade it like an audit

**A field-tested method for instructing AI agents on recurring, high-stakes tasks — using layered markdown, persistent memory, and a self-correcting write-back loop.**

Most people instruct an AI agent by typing a prompt into a chat. That works for one-off
tasks and falls apart for anything you do repeatedly and can't afford to get wrong: the
instructions live in your head, drift between runs, and reset to zero every session.

This repository describes a different approach. You treat the agent's instructions as
**infrastructure** — version-controlled markdown files that load into the agent's context
automatically, layered from general to specific, refined every time the work is done. The
method was built and hardened on a real grading workload, but nothing in it is specific to
grading. It fits code review, security and compliance audits, report QA, contract review —
any task where a *plausible-but-wrong* result is expensive and the task comes around again.

> **This repository contains no personal data of any kind.** No student names, no submitted
> work, no evaluation outputs — nothing that identifies any individual. Everything here is
> generic methodology and reusable templates. See [Privacy & scope](#privacy--scope).

---

## Read it

- **[The illustrated guide](https://henkaku-center.github.io/grade-it-like-an-audit/)** —
  a single-page walkthrough (summary + full detail). *(Live once GitHub Pages is enabled; the
  source is [`docs/index.html`](docs/index.html) and renders offline too.)*
- **[`METHODOLOGY.md`](METHODOLOGY.md)** — the same content as an editable markdown document.

## Use it

The [`templates/`](templates/) directory is a starter kit you can copy into your own repo:

| File | What it is |
|---|---|
| [`CLAUDE.root.md`](templates/CLAUDE.root.md) | Root conventions — the rules true for *every* run of the task. |
| [`CLAUDE.task.md`](templates/CLAUDE.task.md) | Per-instance specifics — criteria, sources of truth, gotchas. |
| [`CLAUDE.end-user-facing.md`](templates/CLAUDE.end-user-facing.md) | Example of a *third* instruction context that ships to a different audience. |
| [`evaluation-report.template.md`](templates/evaluation-report.template.md) | A fixed two-part output format so every run is comparable. |
| [`auditor-prompt.template.md`](templates/auditor-prompt.template.md) | The independent-reviewer prompt for the audit fan-out. |
| [`memory-file.template.md`](templates/memory-file.template.md) | The one-fact-per-file persistent-memory format. |

> The files are named `CLAUDE.md` because this method was built with
> [Claude Code](https://claude.com/claude-code), which auto-loads `CLAUDE.md` from the working
> directory into the model's context. The *idea* is tool-agnostic — any agent that can be
> pointed at a repo of instructions works the same way. Rename to `AGENTS.md`, `.cursorrules`,
> or whatever your tool reads.

---

## The method in one screen

Three moving parts:

1. **Layered instruction files.** Markdown that auto-loads and overrides defaults, organized
   so the instructions get *more specific as you get closer to the work*: general conventions
   at the repo root, task specifics one level down. Most-specific wins; general fills the gaps.

2. **Persistent memory.** A per-user store that survives across sessions — an indexed set of
   single-fact files — so a fresh session already knows the last run's state and your standing
   preferences instead of starting from zero.

3. **The write-back loop.** The part that matters most. When a review catches a failure, the
   fix isn't just applied — a *rule* goes back into the docs, so that failure can't recur next
   time. **The instruction set compounds. Every run makes it stronger.**

What those files *encode* is the working method:

- **A discrete-deduction discipline** — every judgment (every point removed, every finding
  raised) is a discrete, named, evidenced claim. If you can't name it, you don't claim it.
- **An independent audit harness** — one reviewer per unit of work, each reading *only* that
  unit, blind to the rest, so a claim can't be "confirmed" by another unit's data.
- **A loop to convergence** — audits find things, fixes get made, fixes get re-audited whole.
  It ends only when a single pass is clean for the *entire set at once.*

In one real run this loop took **five rounds** — and three of its catches were errors found
*inside a previous round's fix.* That is the loop earning its keep.

See [`METHODOLOGY.md`](METHODOLOGY.md) for the detail behind each of these.

---

## Quick start

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
2. For each instance of the task, copy `templates/CLAUDE.task.md` and name your ground-truth
   sources — the files or systems that settle a factual claim.
3. Draft with an evidence ledger (claim + source, written as you go).
4. Run the audit fan-out with `templates/auditor-prompt.template.md`, one reviewer per unit.
5. Loop: re-audit whole units after every revision; stop only on one clean pass over everything.
6. **Write every lesson back into `CLAUDE.md`.** This is the step that makes it worth doing.

---

## Privacy & scope

This repository is a **methodology and template kit only**. It deliberately contains:

- **No** names or identifying details of any person.
- **No** submitted work, evaluations, scores, quotes, or transcripts.
- **No** data from any real run — only generic, invented illustrations described by *shape*
  (e.g. "a paraphrase inside quotation marks"), never by content.

If you adopt this method, keep your actual working files — inputs, evaluations, memory,
audit notes — in a **separate, private** repository. The whole point of the discipline is to
handle sensitive material carefully; the public artifact is the method, not the material.

## Authors

Built by [Joseph Austerweil](https://github.com/josephausterweil)
([@josephausterweil](https://github.com/josephausterweil)) and
[Ira Winder](https://github.com/irawinder) ([@irawinder](https://github.com/irawinder)).

## License

Released under [CC BY 4.0](LICENSE) — use it, adapt it, share it; a credit link back is
appreciated but not required.
