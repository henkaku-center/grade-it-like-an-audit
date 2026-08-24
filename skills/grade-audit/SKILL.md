---
name: grade-audit
description: Front door for grade-it-like-an-audit — audit-style grading and evaluation of high-stakes recurring work. Use whenever the user mentions grading submissions, reviewing a batch of work against criteria or a rubric, auditing evaluations, checking their own grading, compliance or contract review with evidence discipline, or asks what state their audit workspace is in, what to do next, or to bank a lesson. Routes to setup, audit rounds, the demo, calibration, and reverse-audit.
argument-hint: "[setup | run | demo | calibrate | check-mine | status | bank <lesson>]"
---

# grade-audit — front door and router

You are the one command a user has to remember. Work out where they are, tell them, and
route. All state lives in inspectable files — read the workspace, never rely on session
memory, and say what you found so the user can verify it ("you can audit the auditor").

## If an argument was given

`setup` → grade-audit-setup skill · `run` → grade-audit-run skill · `demo` →
grade-audit-demo skill · `calibrate` / `check-mine` → grade-audit-run in that mode ·
`status` → the status report below · `bank <lesson>` → the bank-a-lesson flow below.

## If no argument: detect state, then recommend

Look for a workspace (a `CLAUDE.md` citing this method's conventions; `working-notes/`;
task directories):

| State | Detection | Response |
|---|---|---|
| No workspace | nothing found | First-timer path: offer the demo (10 min, synthetic data, watch it catch planted defects) or setup. Skeptic-friendly framing: demo first, or `check-mine` if they'd rather have their OWN evaluations fact-checked before the AI drafts anything. |
| Workspace, no drafts | task dirs exist, `working-notes/` empty or ledger-less | Explain drafting with an evidence ledger (claim + source, logged as you write — the thing auditors check against). Offer to draft with them, or calibration first if they have self-graded units. |
| Drafts, no audit yet | draft evaluations exist, no `audit-round*` files | Offer to run round 1. State the cost first: one auditor subagent per unit, plus a consistency pass, typically 3–5 rounds to converge. Point them at LIMITS.md (plugin root) before their first real run. |
| Mid-loop | `audit-round*` files exist | Status report, then offer the next round (or the bounding check, if the metrics say the loop may be measuring itself — see grade-audit-run's convergence reference). |
| Converged | round metrics show an all-clean pass | Remind of the ship checklist: deliverables from one source, write-back done, and the box no harness ticks — one human reader outside the loop, cold. |

## Status report (`status` or mid-loop default)

From files only: task(s) found; units and their draft/audit state; the round-metrics table
verbatim (rounds, blockers, minors, findings-in-prior-fixes); what was written back so
far; the recommended next step in one sentence.

## Bank a lesson (`bank <lesson>` or "remember this for next time")

Ad-hoc write-back between rounds: follow the grade-audit-run skill's
`references/write-back.md` — draft the one-line dated precedent, decide task-file vs root
(when unsure, task), show the diff, append only on approval. If the lesson is a personal
preference rather than a task rule, suggest persistent memory instead.

## First contact with a novice

If the user seems new to Claude Code itself (asks what a skill is, how any of this works),
answer in plain words before routing: this plugin adds a grading method to Claude Code;
their instructions live in ordinary text files they own and can read; every judgment the
system proposes is backed by a named source; nothing is delivered without their approval.
No jargon without a one-line definition.
