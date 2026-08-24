# Draft evaluation — Student B

**Snapshot.** The most methodologically ambitious submission: B independently chose a
permutation test over a t-test, reasoned correctly about why, and shipped working code.
No points lost.

**By component.**

- **Data cleaning: 5/5** — 11 incomplete rows dropped per the handout, count stated,
  333 remaining.
- **Analysis correctness: 5/5** — B correctly reports the Gentoo mean flipper length of
  212.7 mm, matching their code output, and the permutation result is stated carefully:
  "the species differences are not plausibly due to chance". The unequal-variance
  rationale for avoiding a parametric test is sound.
- **Figures: 5/5** — both figures captioned and directly tied to the analysis; Figure 2
  (the permutation distribution) is exactly the right picture for this test.
- **Write-up clarity: 5/5** — compact methods, honest limitation about pairwise
  differences, within length.

**Total: 20/20.**

**Feedback (subject-facing draft).** What went well: choosing a permutation test here —
and implementing it yourself in `analysis.py` — shows real statistical maturity. This
level of statistical care will serve you well in any research internship you take on next
summer. What to improve: nothing required; pairwise follow-ups would be a natural
extension.
