# Lab 3 report — Student C

## Methods

I dropped the 11 incomplete rows as the handout allows, leaving 333. I compared flipper
length across species with a Kruskal-Wallis test, because it does not assume the
measurements are normally distributed within each group.

## Results

The species clearly separate on flipper length (Adelie 190.0 mm, Chinstrap 195.8 mm,
Gentoo 217.2 mm; H = 244.9, p < 0.001). Gentoo penguins stand apart most sharply, which
matches what the boxplot shows at a glance.

![Flipper length by species](fig1.png)
*Figure 1: Boxplot of flipper length by species.*

![Flipper length by island](fig2.png)
*Figure 2: Flipper length by island, showing the confounding between island and species.*

## Limitation

I did not check the within-group distributions before choosing the test; Kruskal-Wallis
was a safe default rather than a justified choice, and with distributions this separated
almost any reasonable test would have agreed.
