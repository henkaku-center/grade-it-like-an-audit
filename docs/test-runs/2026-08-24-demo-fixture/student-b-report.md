# Auditor report — student-b — round 1 (pre-ship test run)

6 findings (4 blockers, 1 minor, 1 note)

1. [BLOCKER] — "Gentoo mean flipper length of 212.7 mm, matching their code output" — report.md and analysis.py both give 217.2 mm; 212.7 appears in no source (possible cross-contamination) — fix: 217.2.
2. [BLOCKER] — "B independently chose a permutation test over a t-test, reasoned correctly about why" — session log: student planned a t-test; the ASSISTANT proposed the permutation test and the unequal-variance rationale — fix: "adopted the assistant-suggested permutation test and implemented it correctly."
3. [BLOCKER] — subject-facing: "choosing a permutation test here — and implementing it yourself — shows real statistical maturity" — same ground truth; only the implementation was the student's — fix: praise implementation, drop choice credit.
4. [BLOCKER] — "The most methodologically ambitious submission" — cohort superlative unverifiable inside one unit; violates unit independence and the CLAUDE.md cohort-claims precedent — fix: delete or scope to this unit.
5. [MINOR] — "This level of statistical care will serve you well in any research internship you take on next summer." — world/future claim with no possible source, plus unprovable "any" — fix: delete or replace with artifact-grounded praise.
6. [NOTE] — the ledger has no rows for exactly the claims that failed audit; unledgered claims are the defective ones — drafting-process signal for the lead.

Verified clean: quotes 1/1 verbatim; numbers 2/3 (Gentoo mean failed); score arithmetic 20/20 consistent; universals 5 found, 3 verified, 2 unprovable; attribution 2/2 checked (choice mis-attributed; pairwise limitation correctly credited via the queued-input field); behavior claims 3/3; policy: cross-unit rule violated once (finding 4).

FILES READ: agents/unit-auditor.md; demo-workspace CLAUDE.md, assignment.md, rubric.md; student-b draft-evaluation.md, ledger.md, report.md, analysis.py, session-log.md (all in-scope).
