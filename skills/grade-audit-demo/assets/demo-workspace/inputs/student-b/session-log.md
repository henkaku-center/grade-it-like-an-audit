# Course-assistant session log — Student B (auto-submitted)

[user] planning to run a t-test between the species for flipper length
[assistant] A t-test compares two groups — you have three species. Also your group sizes
are unequal. Have you considered a permutation test on the spread of the group means? It
avoids the equal-variance assumption entirely.
[user] oh good point. how many resamples is standard?
[assistant] 10,000 is a common choice for a lab like this.
[user] ok doing the permutation test with 10000 resamples
[queued-input from user, delivered with next message] btw I also want to mention in the
limitation that this doesn't tell us WHICH species differ — that part is my own thought,
adding it to the report.
[assistant] Good limitation to note. Pairwise tests with a correction would be the
follow-up.
