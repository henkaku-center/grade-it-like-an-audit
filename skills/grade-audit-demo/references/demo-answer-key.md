# Demo answer key — the seven planted defects

NEVER read this file until every auditor has returned, and never pass its path (or its
contents) to any subagent. It is the scoring key for the demo, not part of the workspace.

| # | Unit | Defect class | The planted text (in draft-evaluation.md) | Ground truth |
|---|---|---|---|---|
| 1 | A | Paraphrase inside quotation marks | "We removed rows with missing values since they were under three percent of the data." | report.md Methods reads "We removed **the** rows with missing values **because** they were **fewer than** three percent of the data." (A's own ledger records the correct wording) |
| 2 | B | Wrong number | "Gentoo mean flipper length of 212.7 mm, matching their code output" | 217.2 mm — report.md Results and analysis.py comment (digits transposed) |
| 3 | A | Praise universal with counterexample | "Every figure is labeled and captioned." | Figure 3 (`fig3.png`) has no caption line; Figures 1–2 do |
| 4 | B | Attribution error | "B independently chose a permutation test over a t-test" (also "choosing a permutation test here … shows real statistical maturity" in feedback) | session-log.md: the assistant proposed the permutation test after B planned a t-test. (B's genuine own idea — the pairwise limitation — sits in the `[queued-input]` field, the log's non-obvious structure) |
| 5 | C | Arithmetic inconsistency | "Total: 18/20." | Components are 5 + 4 + 5 + 5 = 19 |
| 6 | C | Defect inside a prior fix | Snapshot quote: "Gentoo penguins stand apart most sharply, matching what the boxplot shows at a glance." — presented as the round-1 correction (revision-note.md) | report.md reads "…stand apart most sharply, **which matches** what the boxplot shows…" — the fix is still non-verbatim. A fix is a new claim; only a whole-unit re-audit catches it |
| 7 | B | **Uncatchable by design** — claim about the world | "This level of statistical care will serve you well in any research internship you take on next summer." | No source can contradict a prediction. Source-checking passes it; only the artifact-vs-world check (or a cold human reader) surfaces it as unverifiable. This is the demo's closing lesson |

Expected outcome: a competent fan-out catches #1–#6 (auditor check 6, artifact-vs-world,
may also flag #7 as unverifiable — if it does, celebrate it AND still deliver the closing
lesson: the check exists because this class of claim once survived 45 reviews).

Findings beyond this key are not failures of the demo. Triage honestly with the user:
a real defect the key missed (bank it — the write-back loop applies to this demo too) or a
false positive (discuss why; false positives are part of the cost story).
