# Release checklist

One source of truth: the canonical repo is `josephausterweil/grade-it-like-an-audit`;
`henkaku-center/grade-it-like-an-audit` is a push mirror kept for the GitHub Pages URL.
Per the method's lesson 10, the mirror is a step in this checklist, never a place to edit.

1. `python3 scripts/validate-structure.py` and `claude plugin validate --strict .` — green.
2. `claude plugin eval . --threshold 0.8` if the runner is enabled; otherwise run the
   three cases manually in a session and update the counts in `evals/README.md` and
   `LIMITS.md` (real counts, never "all verified").
3. Dogfood: run one audit round of the harness over the changed docs/skills; write back
   lessons; update the record in `DESIGN.md`.
4. Update `CHANGELOG.md`; bump `version` in `.claude-plugin/plugin.json` (semver).
5. Demo recording, if the demo changed: record `/grade-audit demo` (asciinema or GIF) →
   `docs/demo.gif`, referenced from the README's placeholder comment.
6. Commit; `claude plugin tag` to create the release tag.
7. Push canonical; push the mirror — one-time setup: `git remote add henkaku-center
   git@github.com:henkaku-center/grade-it-like-an-audit.git`; then each release:
   `git push henkaku-center main --tags`. Verify the mirror README banner still points
   at the canonical repo.
8. Fresh-environment install test: `/plugin marketplace add
   josephausterweil/grade-it-like-an-audit`, install, `/grade-audit demo` in an empty
   directory. Time it; the funnel promises ~10 minutes.
