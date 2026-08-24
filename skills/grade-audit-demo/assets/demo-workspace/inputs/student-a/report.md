# Lab 3 report — Student A

## Methods

We removed the rows with missing values because they were fewer than three percent of the
data. That left 333 of 344 rows. We compared flipper length across the three species using
summary statistics and a one-way ANOVA, chosen because we are comparing one numeric
measurement across three groups.

## Results

Mean flipper length differed clearly by species: Adelie 190.0 mm, Chinstrap 195.8 mm,
Gentoo 217.2 mm. The ANOVA was significant (F = 594.8, p < 0.001), so we reject the null
hypothesis that species have equal mean flipper length.

![Flipper length by species](fig1.png)
*Figure 1: Boxplot of flipper length by species.*

![Flipper length histogram](fig2.png)
*Figure 2: Histogram of flipper length, colored by species.*

![Body mass vs flipper length](fig3.png)

## Limitation

Our data comes from three islands, and species are not evenly spread across them, so
island effects and species effects are partly confounded. A follow-up could compare within
a single island.
