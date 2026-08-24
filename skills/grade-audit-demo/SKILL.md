---
name: grade-audit-demo
description: Run the 10-minute grade-it-like-an-audit demo on bundled synthetic data with planted defects. Use when the user wants to see, try, or evaluate audit-style grading before trusting it — "show me how this works", "run the demo", "prove it catches mistakes" — or is new to the plugin or skeptical of AI grading. Uses no real data.
---

# grade-audit-demo — watch the harness catch planted defects

You run the audit harness on a bundled synthetic workspace: three fictional students, three
draft evaluations, seven planted defects — six catchable, one uncatchable by design. The
user watches the real machinery work before it touches anything real.

## Hard rules

1. **The answer key (`references/demo-answer-key.md`) stays sealed** until every auditor
   has returned: do not read it before Beat 3, never pass its path or contents to any
   subagent, and never copy it into the demo workspace. Auditors must find defects, not
   receive them — and you must be able to say truthfully that they did.
2. **Run the real harness, not a re-enactment.** Real `unit-auditor` subagents, real
   blindness rules from the grade-audit-run skill's `references/fan-out-protocol.md`, a
   real `lead-consistency` pass. If the auditors miss a planted defect, report the miss —
   an honest 5-of-7 converts a skeptic better than a stage-managed 7-of-7.
3. **Synthetic only.** If the user offers real submissions mid-demo, finish the demo first
   and route them to `/grade-audit setup` or `check-mine`.

## Flow

Follow `references/demo-script.md` beat by beat:

0. Set the stage — what will run, what it costs (3 auditors + 1 lead pass, ~10 minutes),
   and the one pre-announced fact: seven planted, one uncatchable.
1. Copy `assets/demo-workspace/` to a fresh directory and fan out — one blind auditor per
   student; Student C is framed as a re-audit (its revision note documents a prior fix).
2. Merge reports, run the consistency pass, show the findings table in the real format.
3. Unseal the answer key; score the run caught/missed, exactly; deliver the seventh-defect
   lesson (a claim about the world has no source to contradict it — that is why a human
   reader stays outside the loop).
4. Demonstrate one write-back: dated precedent line, diff, append on approval.
5. Close honestly — real costs, what the harness does and does not protect (14 rounds, 70
   reviews, 0 outcome changes on real runs), and the two next steps: `setup` or
   `check-mine`.
