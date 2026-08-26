# Launch checklist — where to put this, in what order

*Drafted 2026-08-26. Nothing here has been done yet; it is a list for you to work through.*

The repository is at **0 stars and 0 forks**, which is the honest starting position. Two things
are worth knowing before spending effort on any of this.

First, for a Claude Code skill the thing people actually judge is the `SKILL.md` and the
README, not the star count. The recurring advice in every "how to pick a skill" guide is the
same: read the SKILL.md, check for recent commits, look at whether issues get answered. A repo
with modest stars and real activity reads better than a padded one, so there is no reason to
chase numbers.

Second, and more important for this project: **the academic channels matter more than the
developer ones.** The people this was built for do not browse awesome-lists. They hear about
tools from a teaching centre, a colleague, or a disciplinary listserv.

---

## 1. Repository hygiene first (an hour, and it gates everything else)

- [ ] Set the GitHub **description** and **topics**. Suggested topics: `claude-code`,
      `claude-skill`, `grading`, `rubric`, `assessment`, `higher-education`, `pedagogy`,
      `ai-ethics`, `feedback`. Topics are how GitHub search finds you at all.
- [ ] Set the repo **homepage** field to the site.
- [ ] Confirm GitHub Pages is serving the new four-page site.
- [ ] Pin the repo on your GitHub profile.
- [ ] Open two or three issues yourself describing known gaps (the missing demo recording, the
      unticked human-outside-the-loop box). An issue tracker with real, honestly-scoped issues
      is a credibility signal; an empty one is ambiguous.

## 2. The academic channels (highest value, slowest)

- [ ] **Your own teaching centre.** At Chiba Tech and, if you still have the contact, at
      UW-Madison. Centres for teaching and learning are exactly the intermediary that decides
      whether a tool reaches faculty, and they are the audience most likely to appreciate a
      limits page written like this one.
- [ ] **POD Network** (podnetwork.org) — the professional body for educational development in
      higher ed, ~1,500 members, with a webinar series and an annual conference. A conference
      submission or a PODLive session would reach precisely the right people. Note the lead
      times are long, so start now if you want it this cycle.
- [ ] **Disciplinary listservs and societies** — cognitive science, psychology teaching,
      computational social science. A short plain-text post with the limits page linked, not
      the landing page.
- [ ] **Your lab site**, which is the durable home. The project entry and news post exist; make
      sure both are live before any social post goes out, so links resolve.
- [ ] Consider a short write-up for a teaching-and-learning outlet. The honest-failures framing
      is genuinely unusual in this space and is the angle an editor would want.

## 3. The Claude Code ecosystem (fast, low effort, modest return)

- [ ] Submit to the awesome-lists this project already documents grepping for grading skills
      and finding none — which makes the submission easy to justify:
      - `hesreallyhim/awesome-claude-code`
      - `travisvn/awesome-claude-skills`
      - `karanb192/awesome-claude-skills`
      - `BehiSecc/awesome-claude-skills`
- [ ] Submit to the **SkillsMP marketplace** (searched during the survey; still no student-work
      grading skills there).
- [ ] Consider `StudentSuite/awesome-skills-plugins-for-students` — adjacent rather than exact,
      since that list is student-facing and this is instructor-facing. Worth one message asking
      whether an instructor section would fit.

## 4. Social (do last, after the site and lab pages are live)

- [ ] LinkedIn — `linkedin.md` in this directory.
- [ ] Bluesky — `bluesky.md`. Bluesky is where the education community reassembled after the
      Twitter migration, and there are education starter packs worth being added to. Ask.
- [ ] Neither draft is scheduled or sent. Both need your read before they go anywhere.

## 5. What NOT to do

- **Do not post to Hacker News or r/programming.** Wrong audience twice over: they will
  evaluate it as a developer tool, and the ensuing thread about whether ai should grade
  anything at all will be tiresome and will not reach a single instructor.
- **Do not claim it does not grade.** It proposes grades. The whole positioning depends on
  being precise about this, and a skeptic disproves the overclaim in thirty seconds.
- **Do not soften the limits page for a launch.** It is the strongest asset in the repository
  for this audience, and it only works if it is the same page tomorrow.
- **Do not chase stars.** See above.

---

## The one-sentence pitch, if you need it verbally

> It is a grading tool whose purpose is feedback: it proposes a grade, but every point deducted
> has to name an issue and cite a source you can open, and in fourteen audit rounds it has never
> once changed a grade — every catch improved what the student actually reads.
