<!--
  QUICKSTART — a pre-filled per-task CLAUDE.md for a COMPLIANCE AUDIT. Copy into your
  audit task directory as CLAUDE.md and adjust the bracketed leftovers.
-->

# CLAUDE.md — [Q_] compliance audit: [policy/framework name]

Task-specific guidance. Shared conventions live in the root `CLAUDE.md` — the
discrete-findings rule and the pre-send audit loop apply to audit findings exactly as to
grades: a finding is a discrete, named, evidenced claim.

## What this task is

Assess each control in [policy §§] against current practice. A unit of work = one control
(its policy text, its evidence artifacts, its owner's attestation).

## Regime — what counts toward the outcome

A control's status (effective / deficient / not assessable) is settled by collected
evidence only. Attestations without artifacts are recorded but cannot make a control
"effective." **Run the criteria audit first:** a control whose evidence was never
collected is *not assessable* — that finding falls on the audit program, not the owner.

## Criteria

| Component | Bar | Judged from |
|---|---|---|
| [Control ID] | config matches policy §[n] | [config export path / screenshot dir] |
| [Control ID] | log review performed [cadence] | [review log path] |

## Sources of truth — verify every claim here, not from memory

- **Exported configs / logs at [path]** — authoritative for what systems do. Dated;
  quote the export, not the console from memory.
- **Policy text [version, path]** — authoritative for what's required.
- **Authoritative *for control owners* (never a deficiency for following it):** the
  procedure version owners were trained on [path]. Procedure-vs-policy gaps are program
  findings, not owner findings.

## Per-task gotchas

- Evidence has timestamps; a claim about the audit period verifies against evidence FROM
  that period. Partial-period evidence is flagged, not extrapolated.
- Numbers ("all 14 systems", "0 exceptions") verify against the export row count.

## Precedents set in this task

- [DATE] [first precedent goes here]
