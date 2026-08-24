# Auditor report — student-a — round 1 (pre-ship test run)

4 findings (2 blockers, 1 minor, 1 note)

1. [BLOCKER] — "We removed rows with missing values since they were under three percent of the data." (draft-evaluation.md) is presented in quotation marks but is a paraphrase — report.md reads "We removed the rows with missing values because they were fewer than three percent of the data." (ledger transcribed it correctly; the evaluation mangled it) — fix: replace with the verbatim sentence.
2. [BLOCKER] — "Every figure is labeled and captioned." is a falsified praise universal — Figure 3 has alt text but no caption line, unlike Figures 1 and 2 — fix: "Figures 1 and 2 are labeled and captioned; Figure 3 carries a label but no caption."
3. [MINOR] — "three figures, all relevant" — same evaluation finds Figure 3 "never discussed in the text" and suggests dropping it; internal tension, relevance unprovable — fix: scope the claim.
4. [NOTE] — ANOVA justification framing was supplied by the assistant and echoed in the report; choice itself student-originated; no score impact, no fix.

Verified clean: quotes 0/1 verbatim (the one quoted string failed); numbers 8/8; universals 3 found, 1 falsified, 1 unprovable, 1 verified; attribution 3 checked, credit correct; behavior claims 2/2; world-claims 0; consistency OK (19/20 arithmetic checks); policy OK.

FILES READ: agents/unit-auditor.md; demo-workspace CLAUDE.md, assignment.md, rubric.md; student-a draft-evaluation.md, ledger.md, report.md, session-log.md (all in-scope).
