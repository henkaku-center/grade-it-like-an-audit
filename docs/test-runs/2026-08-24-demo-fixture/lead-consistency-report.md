# Lead consistency report — demo fixture — round 1 (pre-ship test run, 2026-08-24)

2 findings (2 blockers, 0 minors)

1. [BLOCKER] — Cohort-comparison claims received different verdicts for the same defect:
   "The most methodologically ambitious submission" (student-b snapshot) was ruled
   BLOCKER by its auditor, while "an unusually honest limitation" (student-c snapshot) —
   the same class of implicit cross-cohort claim, unverifiable inside one unit — was
   ruled only MINOR. Strictest verdict propagates per the workspace CLAUDE.md 2026-08-10
   cohort-claims precedent: student-c's finding upgraded to BLOCKER; both snapshots to be
   rewritten in in-unit-scoped language. Student-a checked for the same class: 0
   instances.
2. [BLOCKER] — Test statistic without degrees of freedom deducted in one unit and waived
   in another on identical evidence: student-c lost −1 for "H = 244.9, p < 0.001" without
   df while student-a's "F = 594.8, p < 0.001" equally without df received 5/5 and no
   finding (student-b not comparable: permutation test, no df). The rubric is constant
   across students; a waiver applies to all comparable units or none. Recommended
   resolution: waive in both (handout states no df convention), but one policy set-wide.

Checked (with counts): shared phrasings — 3 evaluations searched, 1 boilerplate pair
found, 0 flagged instances, no propagation needed; comparable cases — 5 compared, 2
inconsistent (the findings above), 3 consistent (non-verbatim quotes A/C both BLOCKER;
attribution handling A-note vs B-blocker consistent with the facts; caption universals
tracked the facts). Unsourced details traced across the blindness boundary: 2 ("212.7"
and "internship/next summer" appear in NO unit's files — in-unit fabrications, not
borrowed evidence; cross-contamination ruled out). Auditor reports inspected 3/3: FILES
READ lists strictly in-scope, verified-clean counts carry real numbers in all 3.
Set-level policy: 3/3 formats uniform; no rankings or cross-student references in
subject-facing text.
