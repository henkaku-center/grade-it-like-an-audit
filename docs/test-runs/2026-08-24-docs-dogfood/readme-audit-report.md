# Dogfood audit — unit: README.md — 2026-08-24

Verdict: 12 findings (1 blocker, 5 minors, 6 notes). Ground truth: the repository itself.

1. [BLOCKER] — "a credit link back is appreciated but not required" — LICENSE is CC BY
   4.0, whose defining condition is mandatory attribution; the README stated the opposite
   of the shipped license. FIXED: "the license's one condition is attribution, and a
   credit link back satisfies it."
2. [MINOR] — "found a defect all fourteen rounds had passed" (×2) — METHODOLOGY: the
   cold-read defect survived nine rounds / forty-five reviews of the run that produced
   it; run A never audited that material. FIXED in both places (and in LIMITS.md, which
   shared the overclaim).
3. [MINOR] — "no competitor publishes its run statistics" exceeded COMPARISON.md's
   support (LLM-AES is peer-reviewed). FIXED: "none we found publishes failure-inclusive
   run statistics."
4. [MINOR] — "dormant" (homework-grader) unsourced in-repo. FIXED: dormancy evidence
   (repo created and last pushed same day, 2026-02-22) added to COMPARISON.md.
5. [MINOR] — "You watch independent auditors find the six" predicted every future run,
   contradicting the demo's own honest-miss rule. FIXED: "hunt the six (our pre-ship test
   run caught all six — plus three defects we hadn't planted)."
6. [MINOR] — "no personal data of any kind" died to the Authors section, LICENSE
   copyright line, and plugin.json. FIXED: scoped to "no personal data about any student,
   subject, or evaluated person — the only people named are the authors."
7. [NOTE] — "nothing in it is specific to grading" vs the grading-named skills. FIXED:
   "nothing in the method."
8. [NOTE] — "mean difference" vs the script's mean absolute difference. FIXED.
9. [NOTE] — "genuinely blind" stated flatly where LIMITS hedges. FIXED: "kept blind — by
   construction; LIMITS.md spells out that boundary."
10. [NOTE] — "typically take 3–5 rounds" vs recorded runs of 5 and 9. FIXED: "budget 3–5
    rounds (our two recorded runs took 5, and 9 with an early stop)."
11. [NOTE] — the italic correction note quotes a pre-repo README version unverifiable in
    this git history. LEFT AS IS (predates the repo's history by design).
12. [NOTE] — external-world claims (install commands, browser availability, subscription
    requirement) have no in-repo source. LEFT AS IS (inherently external; verified against
    vendor docs at authoring time).

Verified clean (auditor's counts): numbers 20/22 verified; in-repo link targets 12/12;
commands 7/7; universals 25 found, 19 held; behavior claims 12/12 substantively verified;
README↔LIMITS↔DESIGN consistent except the shared finding-2 overclaim.
