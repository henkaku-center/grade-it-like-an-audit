# How this compares — the landscape, honestly surveyed

Surveyed 2026-08-24 (GitHub stats from that day). Per this method's own discipline, the
absence claims at the bottom list the searches that backed them, and the places
competitors are *ahead* of us are stated as plainly as the places they are not.

## Direct competitors (things you could install or adopt instead)

✓ = present · ~ = partial · ✗ = absent/not documented · ? = could not verify from public docs

| Project | Type | Rubric support | Evidence-cited judgments | Independent audit pass | Write-back of instructions | Memory across sessions | Human-in-the-loop | Published validation |
|---|---|---|---|---|---|---|---|---|
| **Grade it like an audit** (this) | Methodology + Claude Code plugin | ✓ + pre-flight criteria audit | ✓ every judgment named + evidenced; praise audited too | ✓ blind subagent per unit + lead consistency pass + explicit convergence bound | ✓ every caught failure → durable rule | ✓ persistent memory + state-in-files | ✓ per-fix approval + one human reader outside the loop | ✓ honest run stats (incl. failures) |
| [homework-grader](https://github.com/ChantillyAn/homework-grader) | Claude Code skill | ✓ YAML, weights, anchors | ✓ mandatory quote per dimension | ~ bias controls + κ-calibration vs teacher samples; single grader, no second reviewer | ~ manual rubric refinement | ✗ | ✓ teacher calibrates + reviews flags | ~ built-in κ/ρ/MAD machinery, no external stats |
| [teaching-skills](https://github.com/YujxZJCN/teaching-skills) | Claude Code skill suite | ✓ rubric/blueprint builder | ✓ evidence-bound outputs | ~ deterministic gates; no blind fan-out | ~ per-term IMPROVE record | ✓ "Course Passport" | ✓ professor checkpoints | ✗ |
| [claude-edu-plugins](https://github.com/rudini/claude-edu-plugins) | Claude Code plugin (Moodle/Kahoot) | ~ quiz-based | ? | ✗ | ✗ | ✗ | ~ | ✗ |
| [LLM-AES](https://github.com/Xiaochr/LLM-AES) | Research framework (essay scoring) | ✓ | ✗ score-oriented | ~ dual-process (LLM + supervised model) | ✗ | ✗ | ✓ | ✓ peer-reviewed (LAK25) |
| [PrairieLearn AI grading](https://docs.prairielearn.com/aiGrading/) | Open-source course-platform feature | ✓ instructor rubric | ~ per-submission rationale + full prompt transparency | ✗ human review/override instead | ✗ | n/a | ✓ human grade always wins | ~ instructor-reported accuracy |

Notably: Anthropic's official [k12-teacher-skills](https://github.com/anthropics/k12-teacher-skills)
(394★) covers lesson planning and differentiation and **does not grade** — official
adjacent interest, unoccupied niche.

## Where others are genuinely ahead

- **Commercial products** — [Gradescope](https://guides.gradescope.com/hc/en-us/articles/24838908062093-AI-assisted-grading-and-answer-groups)
  (AI answer-grouping at institutional scale), [CoGrader](https://cograder.com) (K-12
  essays vs state rubrics, FERPA-positioned), [EssayGrader.ai](https://essaygrader.ai),
  [Brisk](https://www.briskteaching.com), [Class Companion](https://www.classcompanion.com),
  [TimelyGrader](https://www.timelygrader.ai) (Canvas rubric import + grade passback) —
  are ahead on UI, LMS integration, certification, and classroom scale. This project is a
  methodology/rigor layer, not a convenience rival. (EssayGrader users report
  same-essay-different-score inconsistency — exactly the failure mode a convergence rule
  with a bound exists to catch.)
- **PrairieLearn** is ahead on battle-tested infrastructure and a human-override workflow
  proven at course scale.
- **homework-grader**'s quantitative teacher-calibration was ahead of this project's
  original design; this plugin's calibration mode (`/grade-audit calibrate`) exists
  because that was the right idea — credited here. (The project appears dormant: at
  survey time its GitHub repo was created and last pushed on the same day, 2026-02-22,
  at 7★ — which is why the idea needed a maintained home.)

## Adjacent, not competing

LLM-as-judge harnesses ([promptfoo](https://promptfoo.dev), [DeepEval](https://github.com/confident-ai/deepeval),
[Ragas](https://github.com/explodinggradients/ragas), the wound-down OpenAI Evals) judge
*model* outputs in dev pipelines, not human work; none found markets itself for grading
student submissions.

## What is unique here, on the evidence above

The combination of: a blind per-unit auditor fan-out **plus** a cross-unit lead pass
**plus** an explicit convergence bound (including detection of a loop auditing its own
repairs) **plus** a structural write-back loop — and, in any category, published honest
run statistics including the failures (a 9-round non-convergence; a defect that survived
45 reviews).

## The searches behind the absence claims

Claiming "no existing Claude Code skill does audit-style grading" requires showing the
searches that failed to find one (2026-08-24):

1. Four awesome-lists (hesreallyhim/awesome-claude-code, travisvn/awesome-claude-skills,
   karanb192/awesome-claude-skills, BehiSecc/awesome-claude-skills) grepped for
   grade/grading/grader/rubric/essay/homework/teacher/assess — zero student-work grading
   entries.
2. GitHub API repo searches: `claude skill grading`, `claude grader`, `claude-code
   rubric`, `claude skill essay grading` (by stars) — no audit-style grading skill; the
   only additional grading skill surfaced was a 2★ single-purpose IELTS scorer.
3. Web search for blind/independent per-submission subagent grading with Claude Code —
   generic subagent tutorials only.
4. SkillsMP marketplace, query "grading" — no student-work grading skills.
5. The official anthropics/skills repo — 17 skills, none education/grading (verified via
   secondary walkthroughs; marked high-confidence, not file-by-file).

Caveats: homework-grader and teaching-skills capabilities are taken from their READMEs,
not code inspection; commercial claims are vendor claims. If you find a competitor this
table misses, open an issue — the table follows the same rule as everything else here:
it gets corrected, and the correction is the point.
