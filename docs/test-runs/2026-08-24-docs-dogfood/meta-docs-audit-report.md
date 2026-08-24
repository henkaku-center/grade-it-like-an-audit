# Dogfood audit — unit: LIMITS.md, DESIGN.md, CHANGELOG.md, RELEASING.md, evals/README.md — 2026-08-24

Verdict: 11 findings (4 blockers, 3 minors, 4 notes). Ground truth: the repository itself.

1. [BLOCKER] — LIMITS.md "a defect all 14 rounds had passed" — same overclaim as the
   README's; METHODOLOGY records nine rounds / forty-five reviews. FIXED.
2. [BLOCKER] — evals/README.md "3 cases (5 grader rubrics)" — the repo contains exactly
   4 grader files. A wrong count in the section titled "honest counts." FIXED: 4.
3. [BLOCKER] — DESIGN.md blocker tally "10 (6 planted, 2 unplanted, 2 lead-pass incl. 1
   upgrade)" double-counted the upgraded finding. FIXED: "9 (6 planted, 3 unplanted — 2
   found by unit auditors incl. 1 upgraded from minor by the lead, 1 lead-pass only)."
4. [BLOCKER] — LIMITS.md pointed to a DESIGN.md dogfood record that was an empty
   placeholder ("findings and write-backs are recorded there") — a false verification
   assertion per the method's lesson 4. FIXED: the docs-dogfood row is now filled and the
   artifacts preserved under docs/test-runs/.
5. [MINOR] — DESIGN.md "The harness was run on this plugin's own documentation before
   shipping" contradicted its own unfilled table row. FIXED: present-tense process
   statement + filled rows.
6. [MINOR] — DESIGN.md "Every SKILL.md stays short with depth in references/" — the
   front-door skill has no references/. FIXED: "the three working skills keep their depth
   in references/."
7. [MINOR] — CHANGELOG.md "per-skill trigger evals" — only 2 of 4 skills have them.
   FIXED: "trigger evals for the front-door and demo skills."
8. [NOTE] — the eval-runner early-access claim might be stale given the CLI's full help
   text. RE-VERIFIED BY EXECUTION same day: the runner still refuses with an early-access
   notice; evals/README.md now records the re-verification.
9. [NOTE] — the fixture-run's verification assertions rested on self-reports with no
   preserved primary artifacts. FIXED: reports preserved in
   docs/test-runs/2026-08-24-demo-fixture/; lesson banked in DESIGN.md.
10. [NOTE] — RELEASING.md's mirror-push command failed as written (no remotes
    configured). FIXED: one-time remote-add setup documented.
11. [NOTE] — "Typical runs take 3–5 rounds" weakly supported by the two recorded runs
    (5, and 9 with an early stop). FIXED: reworded as a budget with the recorded runs
    stated.

Verified clean (auditor's counts): 22 stated counts checked, 16 verified (incl. by
executing validate-structure.py, agreement.py, and claude plugin validate), 2 falsified
(fixed), 1 irreconcilable (fixed), 1 unfalsifiable (now falsifiable via preserved
artifacts); paths 19/20 (docs/demo.gif explicitly future); cross-file quotes 2/2
verbatim; bare "all verified" assertions found: 0; DESIGN behavior claims vs actual
skills/agents: 9/9 supported.
