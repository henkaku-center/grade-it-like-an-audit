# Release checklist

One source of truth: the canonical repo is `henkaku-center/grade-it-like-an-audit` — it
hosts the marketplace, the plugin, and the GitHub Pages guide.
`josephausterweil/grade-it-like-an-audit` is a push mirror. Per the method's lesson 10,
the mirror is a step in this checklist, never a place to edit.

(Publication note, corrected 2026-08-25. An earlier version of this file said the plugin
arrived as a pull request "reviewed cold by Ira Winder — the human-outside-the-loop pass
the method requires." That was not true and the repository's own history says so:
`git log --merges` is empty, and commit `415ee1f` records a **simulated** cold read — a
model session standing in for the reviewer. The plugin first reached this repo's `main`
by direct push on 2026-08-25. **The human-outside-the-loop pass has not been performed.**
`LIMITS.md` carries it as the one box the harness cannot tick for itself, and it is still
unticked. Correcting this is itself an instance of the rule the method exists to enforce:
a claim nothing can verify does not ship because it flatters the project.)

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
7. Push canonical (`henkaku-center`); push the mirror: `git push origin main --tags` (the mirror is already configured as
   `origin`; canonical is the separately-named `henkaku-center` remote). Verify the README's Repository home section
   still names henkaku-center as canonical.
8. Fresh-environment install test: `/plugin marketplace add
   henkaku-center/grade-it-like-an-audit`, install, `/grade-audit demo` in an empty
   directory. Time it; measured at 12 and 18 minutes (2026-08-25), which is what the README
   now states.
