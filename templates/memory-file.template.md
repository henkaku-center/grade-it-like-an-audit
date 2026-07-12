<!--
  TEMPLATE — one persistent-memory file. Persistent memory is a per-user store that survives
  across sessions, separate from the repo's CLAUDE.md files. Keep it as: one INDEX file that
  lists every memory (loaded each session), plus one file per memory. This is a single memory.

  Rules:
    - One file, ONE fact. Don't bundle.
    - Update the matching file instead of creating a duplicate; delete what turns out wrong.
    - Don't store what the repo/code/history already records — memory is for the non-obvious.
    - `description` is what a future session matches on to decide relevance; make it a good hook.
    - `type`: user (who they are) | feedback (how to work) | project (ongoing state) | reference.
    - Link related memories with [[their-name]].
-->

---
name: [short-kebab-case-slug]
description: [one line — the hook a future session uses to decide this is relevant]
metadata:
  type: project        # user | feedback | project | reference
---

[The fact, stated plainly. Convert relative dates to absolute ("last week" → 2026-07-01).]

<!-- For `feedback` and `project` types, follow with these two lines: -->

**Why:** [why this matters / the reasoning behind the preference or decision]
**How to apply:** [what to actually do differently because of it]

Related: [[another-memory-slug]]
