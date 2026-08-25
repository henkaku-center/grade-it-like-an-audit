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
4. **Pricing, not detection, is where a run goes wrong.** Measured against a real cohort's
   issued grades, the harness found substantially the same defects — but charging every
   instance instead of one charge per defect family moved the mean absolute error from
   **3.6 to 11.4 points on a /90 basis**, more than every other cause combined. The
   deduction matrix exists for exactly this: a run can be evidence-perfect and still unfair,
   because fairness is a property of the set and no blind auditor can see the set. And a run
   carrying the prior rounds' rulings matched the issued grades to **3.0**, while the same
   harness without them diverged by 11.4 and moved one outcome band — the measured argument
   for write-back.
5. **Strictness is a real axis, and the presets do not settle it for you.** The same harness
   on the same submissions produced **96–100** under one rulebook and **63–84** under a
   stripped-back one. The presets (`lenient`/`standard`/`strict`) make that axis explicit
   rather than leaving it to whatever the templates implied, but they only *seed* prices — the
   matrix's rulings still decide, and a preset cannot tell you which posture your course
   should have. Two things the presets deliberately cannot do: **suppress a finding** (a lower
   preset demotes it to a zero-point note that still reaches the subject; only an explicit
   report-threshold change hides anything, and the round report then says how much), and
   **license a vague deduction** (an unnamed issue is awarded at every setting).
6. **An enforced average is a policy choice with a cost, and the harness will not make it for
   you.** Scaling the price schedule by one uniform multiplier keeps attribution intact —
   every deduction still names its issue, only the tariff moves. Adjusting individual grades
   to hit a number does not, and the harness says so before offering it. Neither route can
   tell whether a cohort is genuinely strong or the schedule is simply miscalibrated; that
   judgment is the human's, and forcing an average onto a cohort that really is excellent (or
   really is weak) misreports them. The residual after discrete rounding is reported, never
   absorbed.
7. **Blindness is by construction, not enforcement.** Auditor isolation comes from what
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
- **Before your institution has approved it — for real student work, full stop.**
  Student submissions and grades are typically FERPA-covered education records (state
  student-privacy law and GDPR raise the same question elsewhere), and no plugin can
  confer compliance. Check with your university — registrar, privacy office, or counsel
  — and get the approval in writing before identifiable student data enters this
  workflow; the setup interview gates on exactly this. Until then: synthetic demo,
  de-identified `check-mine`, anonymized pilot only. See
  `skills/grade-audit-setup/references/data-handling.md`. Not legal advice; your
  institution's rules govern.

## Dogfood and test record

Kept honest with counts, updated as runs happen:

- `agreement.py` verified against a hand-computed example (quadratic-weighted κ = 0.900
  reproduced exactly; degenerate inputs handled). CI re-runs this check on every push.
- Script self-tests, all in CI, all fixtures with hand-computed answers:
  `code-units.py` **42/42**, `reconcile-deductions.py` **51/51**, `compare-runs.py` **13/13**.
  The strictness work added hand-computed cases in both directions — a cohort of known average
  with targets above and below it, the asserted multiplier and the residual left by discrete
  rounding, the count of deductions that round away to notes, and the two degenerate cases
  (nothing to scale; a target above the basis). Plus the property that matters most: the same
  finding set at all three presets, with only the charges differing.
  Two of those suites exist because a feature shipped broken under a green self-test that did
  not exercise it — the matrix emitters raised a `NameError` on first real use. Coverage of
  new code is now part of adding it.
- **Two defects found by running the new code rather than reading it (2026-08-25):** the
  expected-average math was computing the cohort average from what the *parser extracted*
  rather than what was *awarded* — on a real file whose components do not sum to its header
  those differ, and the target would have been set against the wrong number; it now uses the
  awarded scores and says so loudly when the two disagree. And the deduction matrix could not
  parse `working-notes/<unit>/draft-evaluation.md` — the one-file-per-unit layout this
  method's own workspaces produce — despite the documentation instructing exactly that
  command. Both are covered by tests now.
- **Validated against a real cohort's issued grades (2026-08-25), two arms.** Primed (the
  task's own precedents supplied): MAD **3.0 points on a /90 basis**, no outcome-band change.
  Unprimed (precedents withheld, policy and waiver kept): MAD **11.4**, one outcome-band
  change, 38 fresh deductions against 3 issued in-scope findings. Diagnosis: **both arms
  found substantially the same defects** — the divergence is pricing. Re-aggregating the
  unprimed run's own findings into the issued run's defect families, one charge per (family,
  unit), returns MAD to **3.6**. The withheld rulings account for 17 of 63 points; family
  aggregation accounts for most of the rest. Caveats that limit all of it: n=5 units, only 3
  issued in-scope findings (2 unlabelled and excluded as uncomparable), no
  same-condition control arm, and the adjudication of finding-pairs was done by hand after
  lexical matching produced false pairs.
- Plugin structure: `claude plugin validate --strict` passes (manifest, skills, agents);
  `scripts/validate-structure.py` 15/15 checks pass.
- Eval cases executed with `claude plugin eval`: 0 of 3 (runner in early access at
  authoring time — see `evals/README.md`).
- **Fan-out + lead pass executed for real against the demo fixture (2026-08-24):** 3
  blind auditors + 1 lead pass. All 6 catchable planted defects caught, all as blockers;
  the 7th (the world-claim) was flagged as unverifiable by the artifact-vs-world check;
  **3 additional blocker-class defects the author had not planted were found** — 2 by
  unit auditors (a cohort superlative, an implicit comparison), 1 by the lead pass alone
  (the same statistic-without-df deducted in one unit and silently waived in another —
  invisible to blind auditors by construction); a 4th, minor-level unplanted catch is in
  the preserved reports. Blindness held: 3 of 3 FILES READ lists
  strictly in-scope; the stray number was traced across all units and ruled a
  transposition, not contamination. The full interactive demo (narration beats,
  write-back demonstration) has not yet been executed in a user session — the machinery
  under it has. Primary artifacts (the auditor reports and lead report) are preserved in
  `docs/test-runs/2026-08-24-demo-fixture/`.
- **Docs dogfood executed (2026-08-24):** 3 scope-isolated auditors over the plugin's own
  documentation found 30 findings (5 blockers, 11 minors, 14 notes) — including a license
  contradiction and a fourteen-rounds overclaim that both predate the plugin, and wrong
  counts in this file's own companion records. Fixes applied; a **round-2 diff-scoped
  re-audit of those fixes** (a fix is a new claim) found 0 blockers and 7 minors — all
  residue of the fixes themselves — which were fixed in prose and annotated (never
  silently edited) in the preserved artifacts. Record and written-back lessons in
  `DESIGN.md`; reports in `docs/test-runs/2026-08-24-docs-dogfood/`.
- **Headless load test (2026-08-24):** `claude --plugin-dir . -p` confirmed a live Claude
  Code session sees all 4 skills and all 3 agents under the plugin's namespace.
