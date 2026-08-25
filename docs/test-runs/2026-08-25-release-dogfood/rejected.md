# Findings checked and rejected

The method's own rule is that an auditor's report is a claim, not a verdict. One finding did
not survive verification.

## Top-level scope, finding 2 — "the internal arithmetic does not close"

**Claim:** "MAD 11.4 × n=5 = 57 total absolute deviation, not 63 … the denominator behind
'63 points' cannot be derived from any published figure."

**Verified:** the arithmetic does close. 63 is the total of the *fresh run's* deductions; 57
is the total of the *score deltas*. They differ by 6, which is exactly the issued run's
in-scope deductions:

```
issued  90 88 90 90 86
fresh   80 77 84 83 63
deltas  10 11  6  7 23  -> 57, MAD 11.4
63 fresh deductions - 6 issued in-scope = 57
```

**Kept anyway:** the auditor reached a wrong conclusion because the numbers it needed were
not in the repository. That is the finding's own argument for preserving artifacts, and it
stands even though the arithmetic critique does not.
