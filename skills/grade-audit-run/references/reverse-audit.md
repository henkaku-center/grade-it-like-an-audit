# Reverse-audit ("check-mine") — the harness audits the human

The zero-trust entry point: the AI never grades anything. The human wrote the evaluations;
the harness fact-checks them — quotes verbatim, numbers against ground truth, praise
universals, arithmetic, attribution. AI as fact-checker of the human, not replacement. This
is deliberately the lowest rung of the trust ladder; treat a check-mine request as a first
date, not a lesser audit.

## What changes vs. a normal round

Almost nothing — that is the point. The `unit-auditor` agent is reused unchanged; the
harness does not care who drafted. Differences:

1. **Intake.** Ask the human where their written evaluations live and which files are the
   ground truth (submissions, rubric, spec). If there is no grade-it-like-an-audit workspace,
   do NOT require setup — build the per-unit path lists directly from their answers. If
   evaluations for several units live in one document, extract each unit's section to a
   scratch file (verify the extract verbatim) so auditors stay blind.
2. **No ledger requirement.** Human-written evaluations rarely have evidence ledgers; the
   auditors check claims directly against sources. Skip the preflight ledger check; note in
   the report that a ledger would make future checks faster.
3. **Findings are feedback, not fixes.** Present the merged findings table (with the lead
   consistency pass — humans are just as prone to grading the same issue differently across
   students). Apply NOTHING. The human decides what, if anything, to change in their own
   evaluations; offer to re-check any unit they revise.
4. **Tone.** The subject of this audit is the user. Findings stay discrete, named, evidenced
   — and neutral: "the quote differs from the source" (with both texts shown), never
   commentary on their grading judgment. Judgment calls (harsh/lenient, weighting) are
   explicitly OUT of scope: the harness checks facts, not standards. Say so up front.
5. **No write-back to their files uninvited.** If a pattern recurs (e.g. paraphrases inside
   quote marks), offer one observation at the end — and offer to bank it as a precedent only
   if they have a workspace to bank it in.

## Report shape

Per unit: verdict line, findings with both-texts-shown evidence, verified-clean counts.
Set-level: the consistency pass's comparable-case findings ("same issue, different
deduction" across students is the most valuable thing this mode returns). Close with: what
the harness could NOT check (judgment, standards, claims about the world) — stated, not
implied.
