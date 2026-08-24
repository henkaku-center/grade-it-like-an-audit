# LIMITS.md — what this does not do, what it costs, and when not to use it

Read this before your first real run. A methodology page that only advertises itself is
worthless; this one publishes its blind spots and its bill, because they were paid for.

## The honest headline numbers (real runs, real counts)

- Across the method's two hardening runs: **14 audit rounds, 70 independent reviews, 0
  outcome changes.** Every finding was a grounding or phrasing defect — a misquote, a
  wrong number, an overclaim. The loop is excellent at protecting the *prose and the
  evidence*. On this record it has never once changed a *grade*.
- One run **converged in 5 rounds**; three of its catches were errors inside a previous
  round's fix. One run **ran 9 rounds and never converged** — it was ended by a diff of
  what ships, not by a clean pass, after the loop started finding defects mostly in its
  own repairs.
- After all of it, **one human reading the finished material cold found a defect that
  all nine rounds — forty-five reviews — of the run that produced it had passed** — a
  claim about the world, which no source can contradict.

Size your expectations accordingly: if you want the outcomes protected, that protection
is the human's judgment plus the evidence discipline — not the loop count.

## Blind spots, by design

1. **Claims about the world.** Predictions, reception claims, "this will serve you well"
   — nothing in any source can falsify them, so source-checking passes them. The auditors
   carry an explicit artifact-vs-world check now, but the durable fix is structural: one
   human reader outside the loop, reading cold, at the end. The harness cannot tick that
   box and will tell you so.
2. **The criteria themselves.** The deduction discipline defends every judgment against
   the rubric; it never questions the rubric. Run the criteria audit at setup (the
   interview forces it): a criterion whose evidence was never collected is decoration,
   and partial evidence is worse than none.
3. **Shared model blind spots.** The auditors, the lead pass, and the bundled
   `fresh-reader` agent are the same class of system. A harness converges on the failure
   modes it was built to catch and grows blind to the rest in proportion to how well it
   works. More subagents is not the fix; a human outside the loop is.
4. **Blindness is by construction, not enforcement.** Auditor isolation comes from what
   their prompts contain — there is no per-unit filesystem sandbox. Each auditor reports
   the files it read, and the lead pass checks those reports; but per the method's own
   lesson 4, a "files I read" line is itself a claim. The eval suite includes a
   blindness-compliance check for exactly this reason.

## What it costs

- One audit round over N units ≈ **N auditor subagent runs + 1 lead pass**. Budget
  **3–5 rounds** — and note the honest caveat that the two recorded hardening runs took
  5, and 9 with an early stop; budget for re-audits of revised units on top. The demo
  (3 units, 1 round) is a fair small-scale preview of the per-round cost.
- Calibration ≈ one mini-run over 3–5 units. Cheap relative to a wrong outcome; not free.
- The write-back and the ledgers cost minutes per round and are what make round N+1
  cheaper than round N. Skipping them keeps the price and drops the compounding.

## When NOT to use this

- **One-off, low-stakes evaluation.** The machinery pays for itself on recurring work
  where a plausible-but-wrong result is expensive. For a single casual pass, it is
  overhead.
- **When the evidence doesn't exist.** If submissions/logs/artifacts weren't collected,
  no audit can check claims against them. Fix collection first (the criteria audit will
  tell you).
- **As an outcome oracle.** The harness proposes; the human disposes. If you want a
  system to *decide* grades unsupervised, this is not it, on purpose.
- **As a substitute for institutional approval.** Data-handling questions (FERPA and
  kin) are answered by your institution's agreements, not by a plugin — see
  `skills/grade-audit-setup/references/data-handling.md`.

## Dogfood and test record

Kept honest with counts, updated as runs happen:

- `agreement.py` verified against a hand-computed example (quadratic-weighted κ = 0.900
  reproduced exactly; degenerate inputs handled). CI re-runs this check on every push.
- Plugin structure: `claude plugin validate --strict` passes (manifest, skills, agents);
  `scripts/validate-structure.py` 15/15 checks pass.
- Eval cases executed with `claude plugin eval`: 0 of 3 (runner in early access at
  authoring time — see `evals/README.md`).
- **Fan-out + lead pass executed for real against the demo fixture (2026-08-24):** 3
  blind auditors + 1 lead pass. All 6 catchable planted defects caught, all as blockers;
  the 7th (the world-claim) was flagged as unverifiable by the artifact-vs-world check;
  **3 additional real defects the author had not planted were found** — 2 by unit
  auditors (a cohort superlative, an implicit comparison), 1 by the lead pass alone (the
  same statistic-without-df deducted in one unit and silently waived in another —
  invisible to blind auditors by construction). Blindness held: 3 of 3 FILES READ lists
  strictly in-scope; the stray number was traced across all units and ruled a
  transposition, not contamination. The full interactive demo (narration beats,
  write-back demonstration) has not yet been executed in a user session — the machinery
  under it has. Primary artifacts (the auditor reports and lead report) are preserved in
  `docs/test-runs/2026-08-24-demo-fixture/`.
- **Docs dogfood executed (2026-08-24):** 3 scope-isolated auditors over the plugin's own
  documentation found 30 findings (5 blockers, 11 minors, 14 notes) — including a license
  contradiction and a fourteen-rounds overclaim that both predate the plugin, and wrong
  counts in this file's own companion records. Fixes applied; record and written-back
  lessons in `DESIGN.md`; reports preserved in `docs/test-runs/2026-08-24-docs-dogfood/`.
