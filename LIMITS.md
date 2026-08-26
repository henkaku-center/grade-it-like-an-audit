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
5. **The cross-reference check is deterministic for codes, not for references.** Naming one
   student inside another's feedback is a never-event, and the harness now checks for it
   mechanically every round rather than only at delivery. But it searches for unit *labels*.
   Of four ways one student can appear in another's letter, three are now mechanical: a unit
   code (every round), a real name (at delivery, where the map is legitimately in hand — the
   grading session is denied it by design), and a verbatim quote of another unit's work
   (`--verify-quotes`, which also catches quotes sourced nowhere). The fourth — an identifying
   description carrying no name and no quote, "the only submission that used a permutation
   test" — has no token to match and stays with the auditors' cross-contamination check and
   the lead pass. Do not read the mechanical checks as a guarantee that no student is ever
   referenced: they cover the forms that leave a trace.
6. **Strictness is a real axis, and the presets do not settle it for you.** The same harness
   on the same submissions produced **96–100** under one rulebook and **63–84** under a
   stripped-back one. The presets (`lenient`/`standard`/`strict`) make that axis explicit
   rather than leaving it to whatever the templates implied, but they only *seed* prices — the
   matrix's rulings still decide, and a preset cannot tell you which posture your course
   should have. Two things the presets deliberately cannot do: **suppress a finding** (a lower
   preset demotes it to a zero-point note that still reaches the subject; only an explicit
   report-threshold change hides anything, and the round report then says how much), and
   **license a vague deduction** (an unnamed issue is awarded at every setting).
7. **An enforced average is a policy choice with a cost, and the harness will not make it for
   you.** Scaling the price schedule by one uniform multiplier keeps attribution intact —
   every deduction still names its issue, only the tariff moves. Adjusting individual grades
   to hit a number does not, and the harness says so before offering it. Neither route can
   tell whether a cohort is genuinely strong or the schedule is simply miscalibrated; that
   judgment is the human's, and forcing an average onto a cohort that really is excellent (or
   really is weak) misreports them. The residual after discrete rounding is reported, never
   absorbed.
8. **Blindness is by construction, not enforcement.** Auditor isolation comes from what
   their prompts contain — there is no per-unit filesystem sandbox. Each auditor reports
   the files it read, and the lead pass checks those reports; but per the method's own
   lesson 4, a "files I read" line is itself a claim. The eval suite includes a
   blindness-compliance check for exactly this reason.

## What it costs

- The bundled agents default to **`sonnet`**, and the task file can raise any of them. That
  default is a cost decision, and it has now been measured **once**, on the one corpus with
  ground truth: a fresh marketplace install running the demo at the sonnet default caught
  **6 of 6 catchable planted defects, all as blockers**, flagged the seventh (uncatchable by
  design) as unverifiable, caught two of the known unplanted extras, and — the part that
  matters — its lead pass made the cross-unit catch blind auditors structurally cannot,
  the degrees-of-freedom inconsistency charged in one unit and waived in another, plus a
  second inconsistency the earlier larger-model run did not report. That is parity on this
  fixture, not proof in general: n=1, on a small synthetic corpus whose defects were planted
  to be findable. The other counts in this file were produced at a higher tier and remain
  upper bounds.
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
- **Release dogfood before 0.2.0 (2026-08-25): 63 findings — 18 blockers, 29 minors, 16
  notes** from three scope-isolated auditors over the changed docs and the shipped scripts.
  It stopped the release. Every script self-test was green throughout while a dry run was
  writing real names to disk, the report could print a name it had dropped as a common word,
  `--keys` was guarded against the current directory rather than the workspace, matrix
  columns were raw directory names, `die()` was undefined, family labels collapsed for the
  format the demo itself uses, and the LICENCE did not cover the code being shipped. One
  finding was verified and rejected. Record and the written-back lesson:
  `docs/test-runs/2026-08-25-release-dogfood/`.
- Script self-tests, all in CI, all fixtures with hand-computed answers:
  `code-units.py` **49/49**, `reconcile-deductions.py` **58/58**, `compare-runs.py` **13/13**
  (up from 42/51/13 — the added checks are regressions for the dogfood's blockers).
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
- **The method has been tested on material it had never seen.** The two arms below ran
  against two real assignments from a course the harness had no prior exposure to — the
  instructor's own course, graded on their own machine, with no submission content published
  here; the institutional-coverage question this file asks you to settle is theirs to answer,
  and this run is not evidence that it can be skipped — and were
  compared against grades a human had already issued. With the task's own rulebook supplied
  it reproduced those grades to **3.0 points on a /90 basis with no outcome-band change**,
  and independently rediscovered the judgment-heavy defects the human had found. That is a
  real external validation, not a self-consistency check, and it is the strongest external evidence here — on **n=5 units with 3 comparable issued
  findings, no same-condition control arm, and finding-pairs adjudicated by hand**.
  **What it does not cover:** those runs exercised the *grading judgment*, not the shipped
  orchestration. They used general-purpose subagents with hand-written prompts, not the
  bundled `unit-auditor` definition, and they graded in one shot rather than running the
  skill's actual round (preflight → lead normalize → fan-out → lead-consistency → findings
  table → human approval → re-audit → convergence → write-back). A single `/grade-audit run`
  in a live session would close that gap, and nothing else here does.
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
- Eval cases executed with `claude plugin eval`: **0 of 3**. Retried at the 0.2.0 release
  (2026-08-25, Claude Code 2.1.245) — the runner is still gated and exits with an
  early-access notice. Manually executed: 1 of 3 (the demo-defect-recall machinery, 2026-08-24).
  See `evals/README.md`.
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
- **Coded units run on real student work for the first time (2026-08-25).** Three real
  submissions (two notebooks, one PDF): **zero real names reached the scan report**,
  byte-identity 3/3, the PDF correctly reported as *uninspected* rather than clean, and both
  scanned units carried no identity inside their contents. It also found one defect — the
  attestation claimed only the folder was renamed while `--rename-files` had coded every
  filename — which is the same false claim the dogfood caught in two other files and this one
  had kept. Fixed in 0.2.1.
- **The full audit round executed in a live user session (2026-08-25)** — the first time,
  and it exercised the machinery this file previously listed as unrun. A 3-unit round
  produced per-unit auditor reports, a lead-consistency pass, a deduction matrix and a
  ruling queue. **Blindness held 3/3**: every `FILES READ` list was in-scope, with real
  counts and no bare universals. The lead arbitrated the matrix, escalated 2 rows it would
  not settle, and **added a third question of its own** that no single row flagged. Two
  defects the run exposed, both fixed: the lead's added questions were never merged into
  `ruling-requests.md` (so the human would not see them), and the drafts' deductions **name
  no issue at all**, which the matrix now reports as the discipline failure it is rather
  than dressing a prose fragment up as a defect family.
- **Demo executed in a live user session (2026-08-25):** run twice end to end by a user
  against the plugin directory, taking **12 and 18 minutes**. The README previously promised
  "10 minutes" on no measurement; it now states the measured range. This closes, for the demo
  skill only, the gap LIMITS has carried since 0.1.0.
- **The recursion ran, on real work: three full rounds (2026-08-25/26).** The first observed
  convergence trajectory, on a live 3-unit workspace of real submissions:

  | round | blockers | minors | notes | findings in prior fixes | matrix cells moved |
  |---|---|---|---|---|---|
  | 1 | 6 | 10 | 7 | — | 0 |
  | 2 | 1 | 10 | 5 | ~5 | 0 |
  | 3 | 1 | 1 | 7 | 1 family | 0 |

  Blockers fell 6 → 1 → 1; round 2's findings were mostly defects introduced by round 1's own
  fixes, which is the pattern METHODOLOGY predicts and the bounding rule exists for. The lead
  scoped round 4 minimally by itself (fix and re-audit one unit whole; verify the others
  byte-unchanged), which is the discipline working without being asked.

  **The most useful number is the one that never moved.** `matrix cells moved` was 0 in every
  round and the charges were identical across all three (5.5 / 6 / 4). The grades were stable
  from round 1; what kept churning was the prose. That is exactly the separation the matrix
  was added to make visible, and it says the loop was protecting the writing, not the outcome
  — consistent with this file's headline record of 0 outcome changes in 14 earlier rounds.

  Two defects only a multi-round run could expose, both fixed: the ruling queue **re-asked
  questions already settled** (the underlying rows still differ, so the generator had no
  memory of the matrix's Ruling column — by round 3 the queue was noise), and a question the
  lead raised at round 3 **never reached the queue file at all**, because the merge was an
  instruction to the orchestrator rather than a mechanism.

  **Confound, recorded rather than hidden:** the operator switched to a smaller model at round
  4, so round 4's counts are not comparable with rounds 1–3 and are excluded from the table
  above. Rounds 1–3 ran on one tier throughout.
- **The loop closed. Four rounds, convergence reached, write-back fired (2026-08-26).** The
  full method has now run end to end on real work, which it had never done:

  | round | blockers | minors | notes | findings in prior fixes | matrix cells moved |
  |---|---|---|---|---|---|
  | 1 | 6 | 10 | 7 | — | 0 |
  | 2 | 1 | 10 | 5 | ~5 | 0 |
  | 3 | 1 | 1 | 7 | 1 family | 0 |
  | 4 | **0** | **0** | 0 | none — CLEAN | 0 |

  Convergence by Rule 1: clean for the whole set on one pass, matrix stable, no open ruling
  requests. **Write-back fired**, appending two dated precedents traced to the human's own
  rulings — family granularity is a human call, and marked ellipses in quoted cites are
  acceptable iff every retained fragment verifies. That is the mechanism the method is named
  for, and until this run it had never executed.

  **The number that never moved is still the most useful one.** `matrix cells moved` was 0 in
  all four rounds and the charges were identical throughout (5.5 / 6 / 4). The outcome was
  settled at round 1; four rounds of work went into the prose and the evidence. That matches
  the headline record of 0 outcome changes across 14 earlier rounds, and it is the clearest
  statement of what this loop is for: it protects the writing and the grounding, not the grade.

  **Two caveats on the clean round, because a clean pass is the easiest thing to over-read.**
  Round 4 ran on a smaller model than rounds 1–3, and it was deliberately scoped to one unit
  with the other two byte-frozen. A CLEAN verdict from a weaker model on a narrowed scope is
  the ambiguous case, not the triumphant one. Mitigating it: the lead pass independently
  re-verified that unit's CLEAN rather than accepting the auditor's checklist, and said so in
  its report.
- **Fresh-environment install test (2026-08-26)** — `RELEASING.md` step 8, never previously
  performed. `/plugin marketplace add henkaku-center/grade-it-like-an-audit` → install → demo,
  in an empty directory, from the published `v0.3.0` rather than a local `--plugin-dir`. The
  marketplace manifest resolved, all four skills and three agents registered, the front door
  routed an empty directory correctly, and the demo reported the corrected **12–18 minute**
  figure — confirming the installed artifact was the fixed one. Two defects it exposed, both
  fixed: the lead report's filename was never specified (two live runs produced
  `audit-round1-lead.md` and `lead-round1.md`), and both agent specs' verdict lines came back
  as prose — "CLEAN verdict: not applicable — findings below" — instead of the machine-readable
  form the output spec asks for.
- **Headless load test (2026-08-24):** `claude --plugin-dir . -p` confirmed a live Claude
  Code session sees all 4 skills and all 3 agents under the plugin's namespace.
