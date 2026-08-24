"""Lab 3 analysis — Student B. Permutation test on species flipper-length means."""
import csv
import random

random.seed(3)

rows = [r for r in csv.DictReader(open("penguins.csv"))
        if r["flipper_length_mm"] and r["species"]]
# 333 rows after dropping missing (11 removed)

groups = {}
for r in rows:
    groups.setdefault(r["species"], []).append(float(r["flipper_length_mm"]))

means = {sp: sum(v) / len(v) for sp, v in groups.items()}
print(means)  # {'Adelie': 190.0, 'Chinstrap': 195.8, 'Gentoo': 217.2}


def spread(ms):
    return max(ms) - min(ms)


observed = spread(means.values())
pooled = [x for v in groups.values() for x in v]
sizes = [len(v) for v in groups.values()]

count = 0
for _ in range(10_000):
    random.shuffle(pooled)
    it = iter(pooled)
    perm_means = [sum(chunk) / n for n in sizes
                  if (chunk := [next(it) for _ in range(n)])]
    if spread(perm_means) >= observed:
        count += 1

print("p =", count / 10_000)  # p = 0.0 -> report as p < 0.0001
