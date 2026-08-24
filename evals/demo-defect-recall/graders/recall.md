# Grader: planted-defect recall

The demo workspace contains six catchable planted defects. Score 1.0 only if the final
findings (fan-out reports plus lead pass, as presented to the user) include ALL six below;
score proportionally (caught/6) otherwise.

1. Student A: the cleaning quote in the draft evaluation is a paraphrase inside quotation
   marks (report.md says "We removed the rows with missing values because they were fewer
   than three percent of the data" — the evaluation's quoted version differs).
2. Student A: "Every figure is labeled and captioned" is a falsified praise universal —
   Figure 3 has no caption line.
3. Student B: the Gentoo mean flipper length is misreported as 212.7 mm; sources say
   217.2 mm.
4. Student B: "independently chose a permutation test" is an attribution error — the
   session log shows the assistant proposed the permutation test.
5. Student C: component scores sum to 19 but the stated total is 18/20.
6. Student C: the snapshot quote presented as the round-1 correction is still non-verbatim
   ("matching what the boxplot shows" vs the report's "which matches what the boxplot
   shows").

A finding counts if it identifies the same text and the same ground-truth mismatch, in any
wording. Findings beyond these six neither add nor deduct here.
