# Dogfood audit — unit: skills/*/SKILL.md, skills/*/references/*, agents/* — 2026-08-24

Verdict: 7 findings (0 blockers, 3 minors, 4 notes). Ground truth: the repository itself.

1. [MINOR] — grade-audit-run/SKILL.md step 5 and fan-out-protocol.md assigned two
   different contents (merged findings table vs verbatim auditor report) to the same path
   `working-notes/<unit>/audit-round<N>.md`. FIXED: verbatim reports keep that path; the
   merged table now goes to `working-notes/findings-round<N>.md`.
2. [MINOR] — demo-script.md attributed "two" unplanted catches to "the harness" while the
   answer key and LIMITS record three (two by auditors, one lead-pass-only). FIXED:
   "the blind auditors caught two … and the lead pass caught a third."
3. [MINOR] — setup promised "the pilot is the recommended default and is stated as such
   in the generated root file," but templates/CLAUDE.root.md contained no pilot sentence
   — a one-source violation (generation-rules forbids inventing structure the templates
   lack). FIXED: pilot-before-cohort line added to the root template.
4. [NOTE] — front-door skill called the ledger "the thing auditors check against,"
   inverting its role (auditors check claims against sources, using the ledger as the
   map). FIXED.
5. [NOTE] — the demo fixture ships no image/CSV binaries; a literal behavior-claims
   auditor could flag the absent files. FIXED: pre-triaged in the answer key as fixture
   scope.
6. [NOTE] — setup SKILL summary stated the .gitignore unconditionally where
   generation-rules conditions it on Q6/people. FIXED: condition added to the summary.
7. [NOTE] — setup said calibration precedes the harness "drafting anything"; calibration
   itself drafts blind evaluations. FIXED: "anything that counts."

Verified clean (auditor's counts): cross-references 19/19 paths resolve, 3/3 agent names
match, described contents match 18/19 (exception = finding 3); protocol pairs 9 compared,
7 consistent (sealed-key rule consistent 4/4 statements; write-back consistent across 3
citing sites); template fidelity 13/14 generation-rules claims verified; demo integrity
7/7 planted defects exist exactly as the key describes, 12/12 answer-key quoted strings
verified character-for-character, 3/3 known-extras texts verified incl. the A-vs-C df
asymmetry; numbers 26/26 traced; universals/world-claims 11 examined, 0 falsified.
