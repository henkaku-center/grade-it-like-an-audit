# Lab 3 report — Student B

## Methods

Rows with any missing measurement were dropped per the handout (11 rows; 333 remained).
To compare flipper length across species I used a permutation test on the difference in
group means (10,000 resamples) instead of a parametric test, because the group sizes are
unequal and I did not want to assume equal variances.

## Results

Mean flipper lengths: Adelie 190.0 mm, Chinstrap 195.8 mm, Gentoo 217.2 mm. The observed
spread between species means was larger than in all 10,000 permuted datasets (p < 0.0001),
so the species differences are not plausibly due to chance. Full computation is in
`analysis.py`.

![Flipper length by species](fig1.png)
*Figure 1: Violin plot of flipper length by species.*

![Permutation distribution](fig2.png)
*Figure 2: Permutation distribution of the between-species spread; observed value marked.*

## Limitation

The permutation test tells us the species differ somewhere, but not which pairs differ;
pairwise follow-ups with a multiple-comparison correction would be the next step.
