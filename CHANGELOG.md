# Changelog

## 0.3.2 — 2026-08-26

Record-keeping only; no behaviour change.

- **The loop closed.** Four rounds on real submissions reached convergence and **write-back
  fired** — the mechanism this method is named for, and the last path never exercised. Two
  dated precedents were appended, both traced to the human's own rulings. `LIMITS.md` and
  `DESIGN.md` carry the full trajectory, including the two caveats that stop a clean round
  being over-read: round 4 ran on a smaller model and on a deliberately narrowed scope.
- **`matrix cells moved` was 0 in all four rounds**, with charges identical throughout. The
  outcome was settled at round 1 and four rounds of work went into the prose and the evidence
  — which is what this loop is for, and what the matrix was added to make visible.
- **The cross-unit view found bugs in the assignment, not the work.** Three units had
  inherited the same two errors from the course's own stencils; none was charged, under the
  standing rule that you never deduct for following an instruction you were given. Recorded in
  `DESIGN.md`: one student misreading a scaffold is a defect, three doing it identically is a
  scaffold bug, and only a cross-unit view can tell those apart.

## 0.3.1 — 2026-08-26

Two defects found by the first fresh-environment install test, plus the measurement that test
happened to produce.

- **The lead report's filename was never specified.** Two live runs produced
  `audit-round1-lead.md` and `lead-round1.md`; anything referencing the lead report by path
  breaks on one of them. Fixed at `working-notes/audit-round<N>-lead.md`.
- **Both agents' verdict lines came back as prose.** The output spec asks for `CLEAN` or
  `N findings (B blockers, M minors, K notes)` as the first line; live runs produced "CLEAN
  verdict: not applicable — findings below" and "CONSISTENT verdict does not apply", which are
  neither form and cannot be counted. Both specs now say exactly one of the two forms, nothing
  else, and quote the observed failure.
- **The sonnet default is no longer unmeasured.** A fresh install running the demo at the
  default caught **6 of 6 catchable planted defects, all as blockers**, flagged the seventh
  (uncatchable by design) as unverifiable, caught two known unplanted extras, and its lead
  pass made the cross-unit catch blind auditors structurally cannot — plus one the earlier
  larger-model run missed. Parity on this fixture; n=1 on a small synthetic corpus, so LIMITS
  says that rather than claiming general equivalence.

## 0.3.0 — 2026-08-25

- **The ruling queue now has memory.** A live four-round run showed it re-asking questions
  already settled: the underlying matrix rows still differ after a ruling ("justified
  difference" is an answer, not a change), so the generator asked again every round and by
  round three the queue was noise a human learns to skip. `--prior-matrix` reads the existing
  matrix and suppresses any family whose Ruling cell a human or the lead has filled — an
  auto-flag does not count as a ruling. On the real workspace this cut the queue from 3
  questions to the 1 genuinely open. The same run also showed a question the lead raised at
  round 3 never reaching the queue file, because the merge was an instruction to the
  orchestrator rather than a mechanism.
- **Agents default to `sonnet`, and the model is configurable per task.** The bundled agents
  declared no model, so they inherited whatever the operator's session was running — which on
  a large-model session makes an N-auditors-per-round fan-out expensive and slow for no stated
  reason. All three now declare `sonnet`, and both task templates carry a "Models and cost"
  block the run skill reads and passes at spawn time. Stated in LIMITS rather than glossed:
  this is a **cost decision, not a measured equivalence** — every finding count recorded in
  that file was produced by a larger model than the shipped default, so those counts are an
  upper bound until someone measures the gap. The lead pass is one call doing the hardest
  reasoning, so it is the first worth raising.
- **The letter's sign-off is recorded, not inferred.** A live run signed every letter "Joe" —
  correctly, but by accident: the plugin has no signature field, and the name came from the
  operator's own global writing-style rules. That works invisibly for one person and produces
  an improvised or absent sign-off for anyone else, and can vary between rounds. Both task
  templates now carry a "Who the feedback is from" block (name as it should appear, register,
  reply-to), the interview asks for it (Q3b), and the report template tells the drafter to use
  the recorded value rather than improvise — a cohort receiving differently-signed letters
  reads as carelessness about the thing they care most about.
- **A default workspace, so `CLAUDE.md` is not the user's problem.**
  `templates/quickstarts/student-grading.CLAUDE.task.md` is a complete, defensible grading
  workspace — layout, never-events, the discrete-attributable-deduction rule, strictness
  preset, sources of truth, what-the-subject-was-owed, data-handling slots and seeded
  precedents. The run skill's preflight no longer stops when no task file exists; it supplies
  this one, fills in what it can see, and shows it. The front door offers "just start" ahead
  of the demo and the interview, and the setup skill gains a fast path for people who do not
  want ten questions. Grading was the one flagship case with no ready-made task file, while
  code-review, compliance-audit and contract-review all had one.
  **The rubric is the deliberate exception** — the plugin will not guess criteria. Grading
  against an invented rubric is the one failure the rest of the machinery cannot catch, since
  every judgment would be evidenced, internally consistent, and measured against a standard
  nobody chose. Where a handout exists the skills propose a rubric from it for approval; where
  it does not, they ask. Nothing is drafted or audited until the criteria are approved.
- **Referencing another student inside a student's feedback is now checked mechanically,
  every round.** It was already forbidden — the auditors carry it as a POLICY check and the
  lead pass looks for it — but both are judgment. The matrix build now searches each unit's
  own evaluation for any other unit's label and prints a NEVER-EVENT block before anything
  else; `--personalize` runs the same check at delivery and refuses to write while one is
  outstanding. Catching it in round 1 costs a line; catching it at delivery costs the grading
  pass; missing it costs a student's privacy. Worth stating plainly because it is easy to
  mistake for a naming problem: **no coding scheme prevents this.** The defect is in the
  sentence, not the label — rename the unit and the letter still points at another student.
  And it is not a guarantee that no student is ever referenced: it searches for *labels*. Of
  four ways one student can surface in another's letter it covers three — a unit code
  always, a real name at delivery only (the grading session is denied the map by design, so it
  cannot search names; `--personalize` has it legitimately and refuses on names too), and a
  **verbatim quote of another unit's work** via `--verify-quotes`, which checks every quoted
  span of 25+ characters against the submissions on disk: sourced in its own unit (silent),
  found only in another unit (borrowed evidence, a never-event), or found nowhere (the
  paraphrase-in-quotes defect). Shared material — handout, reference solution, stencils — is
  excluded, since every subject quotes from it legitimately. The one remaining form is an
  identifying description carrying no name and no quote; it has no token to match and stays
  with the auditors and the lead pass. Documented in LIMITS.md rather than left to be assumed.
- **`--personalize` puts the real names back into the letters, locally.** Reads the coded
  letters and the map, writes named copies, sends nothing — no script this plugin ships
  imports `socket`, `http`, `urllib` or `requests`, and that is checkable with one grep.
  Greeting placeholders become the name; **unit codes in the body are left alone by default**
  and reported with line numbers, because a code in the body refers to the work and
  substituting a name turns "your work on unit-a" into "your work on Ada Lovelace"
  (`--code-phrase "your submission"` replaces them, with the wording your choice). It
  maps letters to units by **exact filename stem or containing folder**, so one filename
  cannot claim two units and a stray README is skipped as not-a-letter rather than stopping a
  delivery. One condition does halt the whole run: **a letter that names another unit inside
  it** — which is not a mapping ambiguity and no naming scheme prevents, but the never-event
  rule firing (no subject named or identifiable in another subject's feedback). Nothing is
  written while one is outstanding, because a mis-delivered letter is indistinguishable from a
  correct one until a student replies. Output must go somewhere other than the coded letters,
  which it enforces.
- **Getting the names back is now a documented, one-command step.** The tooling could code a
  student to `unit-a` but nothing said how to go back, and the 0.2.0 fix for identity-bearing
  matrix columns had quietly created a *second* coding layer: `unit-a` was relabelled to `U1`
  for written artifacts, with that legend printed only to a terminal. An instructor could end
  up holding a matrix saying `U1`, a letter saying `unit-a`, and no saved link between them.
  Now: already-coded workspaces are never re-coded, so there is one hop and the map file is
  the only lookup ever needed; `code-units.py --decode <run>.map.json` prints the
  code → identity table (run outside the grading session, which is denied read access to the
  map by design) and warns to hand-check a row before a batch send; and the round trip is
  written into the data-handling reference and both task templates.
- **Expected-average calibration works on small-basis rubrics.** Found by a live workspace
  that graded out of 6 points with half-point prices. Three defects, all fixed: scaled prices
  were rounded to whole points, which waived 2 of 3 findings outright; ties rounded
  half-to-even, so a price landing exactly half-way **silently became free**; and the
  tolerance was a fixed 1.0, which is 1% of a /100 rubric but 17% of a /6 one. The step is now
  inferred from the schedule's own prices, ties round away from zero so a charged finding
  stays charged and the miss surfaces as a reported residual instead, and the tolerance is 1%
  of the basis. Whole-point /100 schedules are unaffected. `reconcile-deductions.py` self-test
  60 → 66.
- Demo timing corrected in the demo skill's own description and cost line: 12–18 minutes,
  measured twice in live sessions, replacing an unmeasured "10 minutes".

## 0.2.1 — 2026-08-25

One correction, found by running 0.2.0 against real student submissions within the hour.

- **The scan report claimed "only the top-level folder was renamed" while `--rename-files`
  had just renamed every file.** The same false claim was caught by the release dogfood and
  fixed in the auditor agent and the prompt template — and missed in the report itself, which
  is the one place a grader actually reads it. The attestation is now conditional on the flag,
  and when filenames were coded it adds the rule that follows: a cross-reference broken by a
  coded filename is a tooling artefact, never the subject's error. Regression covers both
  branches; `code-units.py` self-test 49 → 51.

Also recorded from that run, which was the first use of the coded-units pass on real student
work: zero real names reached the scan report, byte-identity held 3/3, the PDF was reported as
*uninspected* rather than clean, and the notebooks carried no identity inside their contents.

## 0.2.0 — 2026-08-25

Cross-unit fairness, a privacy pass that cannot corrupt the evidence, and a strictness dial.
Validated against a real cohort's issued grades before shipping; the numbers and their
caveats are in `LIMITS.md`.

- **Coded units** (`skills/grade-audit-setup/scripts/code-units.py`): codes each person's
  container to a random unit code, copies contents **byte-for-byte** (hash-verified,
  timestamps preserved) and *scans* rather than rewrites them. An earlier rewriting version
  broke the method's own ATTRIBUTION check by folding collaborators into the subject's code;
  the shipped one observes and reports. Records identity template fields already blank in the
  source, before grading, so an anonymization pass can never be mistaken for the cause of a
  subject's blank. Map kept outside the workspace with a printed `deny` rule.
- **Deduction matrix — cross-unit reconciliation.** A family x unit artifact built each
  round (`reconcile-deductions.py --emit-matrix`), with the binding rule **one charge per
  (family, unit), never per instance**. Clustering runs on the named issue rather than the
  label plus its evidence, so one defect family occupies one row and an inconsistent price
  is impossible to miss. The `lead-consistency` agent arbitrates what the instruction files
  authorize, flags analogy-based extensions for reversal, and refuses the rest.
- **Ruling requests — questions for the human grader** (`--emit-rulings`): raised whenever
  two units are charged differently for the same item, a family is charged unevenly with no
  evidence for the difference, a defect class has no precedent, a finding sits on a policy
  boundary, or a waiver's scope is unclear. Each carries three ready dispositions. Answers
  become numbered rulings and write-back candidates.
- **Recursion to convergence extended to the matrix**: a round is done when no unit blocks
  AND the matrix has no unarbitrated flag and no cell moved. `round-metrics.md` gains
  `matrix cells moved` and `open ruling requests`; oscillating cell movement means two
  rulings are fighting, which is a question for the human. The human closes the loop, not
  the counter.
- **Strictness presets** (`lenient` / `standard` / `strict`): coherent bundles of charge
  threshold, per-severity price, and waiver posture, set once at setup (interview Q5b) in the
  task CLAUDE.md and read back at run time. `--show-preset NAME` prints any of them.
  Deliberately *not* adjustable by preset: the report threshold stays at `note`, so a lower
  setting demotes a finding to a zero-point note that still reaches the subject rather than
  hiding it; and an unnamed issue is awarded at every setting.
- **Expected-average calibration** (`--target-average N --basis N`): reports the awarded
  cohort average, the gap, the uniform tariff multiplier that would close it, and the residual
  after discrete rounding — and applies nothing. A gap beyond tolerance becomes `Q0` in the
  ruling queue offering three routes (scale the schedule / adjust individual grades / advisory
  only), each with its cost stated, including that adjusting grades breaks the discrete
  attributable deduction rule. The average is computed from what was **awarded**, not from
  what the parser extracted, and the two disagreeing is reported loudly rather than absorbed.
- **`compare-runs.py`** — compares a finished run against grades already issued: aligns
  units, proposes finding-pairs by component, emits an adjudication worksheet and tabulates
  recorded verdicts. It proposes pairings and never decides them, because lexical
  similarity demonstrably cannot.
- **Attribution:** Ira Winder recorded as originator, Joseph Austerweil as author and
  maintainer.

## 0.1.0 — 2026-08-24

First release of the plugin (the methodology and templates predate it).

- Four skills: `grade-audit` (front door/router), `grade-audit-setup` (plain-language
  interview → generated workspace), `grade-audit-run` (audit rounds with blind fan-out,
  convergence + bounding, structural write-back; `calibrate` and `check-mine` modes),
  `grade-audit-demo` (synthetic workspace, seven planted defects, sealed answer key).
- Three read-only agents: `unit-auditor`, `lead-consistency`, `fresh-reader` (labeled
  weak proxy for the human outside reader).
- Calibration metrics script (`agreement.py`, stdlib-only: weighted κ, Spearman ρ, MAD,
  small-n caveat).
- Eval suite: 3 plugin-level cases, trigger evals for the front-door and demo skills;
  runner early-access at release — see `evals/README.md` for exact verification status.
- New documents: `LIMITS.md`, `DESIGN.md`, `COMPARISON.md`, data-handling reference,
  cross-domain quickstarts; README rewritten around the skeptic funnel; CI structural
  validation.
