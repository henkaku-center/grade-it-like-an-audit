# Release checklist

One source of truth: the canonical repo is `henkaku-center/grade-it-like-an-audit` — it
hosts the marketplace, the plugin, and the GitHub Pages guide.
`josephausterweil/grade-it-like-an-audit` is a push mirror. Per the method's lesson 10,
the mirror is a step in this checklist, never a place to edit.

(Initial publication note: the plugin arrived as the `claude-code-plugin` pull request
on this repo, reviewed cold by Ira Winder — the human-outside-the-loop pass the
method requires. Merging that PR was the publication step.)

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
7. Push canonical (`henkaku-center`); push the mirror — one-time setup: `git remote add
   mirror git@github.com:josephausterweil/grade-it-like-an-audit.git`; then each
   release: `git push mirror main --tags`. Verify the README's Repository home section
   still names henkaku-center as canonical.
8. Fresh-environment install test: `/plugin marketplace add
   henkaku-center/grade-it-like-an-audit`, install, `/grade-audit demo` in an empty
   directory. Time it; the funnel promises ~10 minutes.
