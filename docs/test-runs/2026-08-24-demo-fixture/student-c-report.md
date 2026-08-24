# Auditor report — student-c — round 1, re-audit framing (pre-ship test run)

4 findings (2 blockers, 1 minor, 1 note)

1. [BLOCKER] — Snapshot quote "Gentoo penguins stand apart most sharply, matching what the boxplot shows at a glance." is not verbatim — report.md reads "…stand apart most sharply, which matches what the boxplot shows at a glance." The round-1 fix replaced one non-verbatim quote with another — fix: quote exactly, including "which matches".
2. [BLOCKER] — "Total: 18/20." contradicts the component lines: 5+4+5+5 = 19; only one documented −1 exists — fix: 19/20 (or name the second deduction discretely).
3. [MINOR] — "an unusually honest limitation" — implicit cohort comparison, no in-unit source, subject-facing — fix: "a candid limitation."
4. [NOTE] — the −1 for missing df rests on a convention the handout never states; defensible grader discretion; flagged for lead awareness of "what the subject was owed."

Verified clean: quotes 0/1 verbatim; numbers 3/3; universals 1 found, verified; attribution 2/2 (island figure student-originated per log; Kruskal-Wallis correctly not credited as originated); behavior claims 3/3; artifact-vs-world: 1 flagged (finding 3); consistency: arithmetic fails (finding 2); policy otherwise OK; ledger 7/7 rows map to real sources though the opening-quote row masks the non-verbatim transcription.

FILES READ: agents/unit-auditor.md; demo-workspace CLAUDE.md, assignment.md, rubric.md; student-c draft-evaluation.md, revision-note.md, ledger.md, report.md, session-log.md (all in-scope).
