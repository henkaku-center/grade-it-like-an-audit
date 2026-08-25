# Changelog

## 0.3.0 — 2026-08-25

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
