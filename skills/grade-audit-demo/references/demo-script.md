# Demo script — narration beats

The demo exists to convert a skeptic by demonstration, not persuasion. The tone throughout:
show, count, and be candid about cost and limits. Never oversell — the audience is someone
waiting for the AI to overclaim.

## Beat 0 — set the stage (before anything runs)

Say, in about five sentences: this workspace is synthetic (no real students anywhere);
three draft evaluations contain planted defects; the real audit harness — the same one used
on real work — will now try to find them; this will spawn 3 independent auditor subagents
plus 1 consistency pass and takes a few minutes. State the honest frame up front: "I know
where the defects are, but the auditors don't — they start fresh and each sees only its own
student's files. At the end I'll show you the answer key, including one defect the harness
cannot catch by design."

Do NOT reveal defect locations, classes, or counts-per-unit. The one pre-announced fact:
seven planted, one uncatchable.

## Beat 1 — the fan-out (run it for real)

Copy `assets/demo-workspace/` into the working directory (default
`./grade-audit-demo-workspace/`, or where the user asks; never overwrite an existing
directory — pick a fresh name instead). Then follow the grade-audit-run fan-out protocol
exactly: one `unit-auditor` per student, paths for that student only; Student C's prompt
includes the re-audit framing (revision-note.md documents a prior fix — re-audit the WHOLE
unit). The answer key's path never appears in any prompt. While auditors run, explain what
blindness buys in one sentence: a claim can't be "confirmed" by another student's data.

## Beat 2 — reports land

Run the `lead-consistency` pass, then show the merged findings table exactly as a real run
would: unit, severity, exact text, ground truth, proposed fix. Point at the FORM of one
finding: "notice it names the text, cites the source line, and proposes a one-line fix —
that's the discrete-findings rule. No finding, no deduction."

## Beat 3 — the reveal

NOW read `references/demo-answer-key.md` and score the run against it, in a table:
caught / missed per planted defect. Be exact: "6 of 7" (or whatever actually happened —
if an auditor missed a planted defect, say so plainly; the honest miss is worth more to a
skeptic than a perfect score).

Then the seventh: show the internship-prediction sentence and ask the user — "what source
could contradict this?" Let the answer land: none. A claim about the world has no artifact
to check it against. This is why the method keeps one HUMAN reader outside the loop, and
why a real sentence of this class once survived nine rounds and forty-five reviews before
a person reading cold caught it in one pass.

Then tell the known-extras story (answer key, "Known extras" section): the harness caught
two defects its own author hadn't planted, in the fixture written to demonstrate
defect-catching. Triage any further findings per the answer key's last paragraph.

## Beat 4 — the write-back (show the compounding)

Take one caught defect (the attribution error is the most striking) and walk the write-back:
draft the one-line dated precedent, show the diff against the demo workspace's CLAUDE.md
"Accumulated precedents" section, append on the user's approval. Close the point: "next
run's auditors read that rule before they start. The mistake that cost a round today costs
nothing tomorrow. Your instruction files accumulate scar tissue — that's the whole method."

## Beat 5 — close honestly

Three sentences, roughly: what they watched cost N subagent runs over ~10 minutes on 3
units — real runs are that, times rounds. The harness protects the prose and the evidence;
across the method's real runs (14 rounds, 70 reviews) it never changed an outcome — the
human owns those. Offer the two next steps: `/grade-audit setup` to build a workspace for
their real task, or `/grade-audit check-mine` if they'd rather have the harness fact-check
evaluations THEY wrote before letting it draft anything. Then delete or keep the demo
workspace, their choice.
