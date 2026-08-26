# LinkedIn — draft, not posted

*Lead: the general method, with grading as the proving ground. Nothing here is scheduled or
sent; edit freely and post it yourself.*

---

Most people instruct an AI agent by typing a prompt into a chat. That works fine for one-off
tasks, and it falls apart for anything you do repeatedly and cannot afford to get wrong: the
instructions live in your head, they drift between runs, and they reset to zero every session.

I spent a good while working out what to do instead, and the answer turned out to be
pleasingly low-tech. Put the instructions in plain markdown files. Give the agent persistent
memory. Then make every caught mistake write itself back into the rulebook, so the same
mistake cannot happen twice.

I hardened it on grading, because grading is where being *plausibly* wrong is most expensive
and least detectable. A misquote sitting inside quotation marks, a compliment that overreaches
by exactly one counterexample, a total that does not add up (these ship, and nobody catches
them, including me).

What came out is a Claude Code plugin called "Grade it like an audit." Three things I would
want to know if someone else were telling me about it:

First, it is a grading tool whose purpose is feedback. It does propose grades and I am not
going to pretend otherwise, but a proposed grade here is arithmetic: what is left after every
deduction has named a specific issue and cited a source you can open. Nothing is subtracted
for a general impression, because a general impression has nothing to cite.

Second, the headline number is the one most tools would bury. Across 14 audit rounds and 70
independent reviews, not a single finding has ever changed a student's grade. Every catch
improved the evidence or the wording instead. That is the design rather than a disappointment,
because the thing worth protecting is what the student reads.

Third, it publishes its failures at the same length as its successes. One run went nine rounds
and never converged; it had started finding defects mostly in its own repairs. After all nine
of those rounds (45 separate reviews) one human reading the finished material cold found a
defect every one of them had passed. That is the permanent hole in the method, and it is why
the last reader has to be a person.

I know many colleagues are wary of ai anywhere near assessment, and I think that wariness is
mostly well-founded rather than reflexive. The literature is genuinely not reassuring: the
same essay scored differently on different runs, leniency that tracks the writer's first
language, agreement between models that is only moderate. So this is built the other way
round. It hands you the evidence instead of the verdict, everything it produces is a plain
file you can read, and setup now asks whether you intend to tell your students an automated
pass was involved (with suggested wording, which you are meant to edit rather than paste).

It is free and CC BY. There is a 12-to-18-minute demo that runs on fully synthetic data, plants
seven defects for itself to hunt, and then shows you the one it cannot catch.

Site: https://henkaku-center.github.io/grade-it-like-an-audit/
Code: https://github.com/henkaku-center/grade-it-like-an-audit

Originated with Ira Winder, who had the first version of the idea. I would be glad to hear
where it breaks -- especially from people who would rather it did not work.

---

## Notes on this draft

- One typed ` -- ` in the whole post (the last line). Everything else uses parentheses.
- Enumerated as First / Second / Third rather than a bulleted list, which reads better in the
  LinkedIn feed and matches how you write.
- No bold anywhere, no emoji, no hype verbs.
- The failure paragraph is deliberately third rather than buried at the end. For this audience
  it is the most persuasive paragraph in the post.
- If you want it shorter, cut the fourth paragraph (the "three things" preamble) and the
  literature sentence. The failure paragraph should be the last thing cut, not the first.
