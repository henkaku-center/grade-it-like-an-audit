#!/usr/bin/env python3
"""Structural validation for the plugin — runs in CI with no dependencies.

Checks the things `claude plugin validate` checks that we can verify statically,
plus this repo's own conventions (sealed answer key, eval case shape). Exits
nonzero with a list of failures; prints real counts either way.
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
failures = []
checked = 0


def fail(msg):
    failures.append(msg)


def frontmatter(path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        return None
    fields = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith((" ", "\t", "#")):
            k, v = line.split(":", 1)
            fields[k.strip()] = v.strip().strip('"')
    return fields


# --- manifests ---
for name, required in [("plugin.json", ["name", "description", "version"]),
                       ("marketplace.json", ["name", "plugins"])]:
    p = ROOT / ".claude-plugin" / name
    checked += 1
    if not p.exists():
        fail(f"missing {p}")
        continue
    try:
        data = json.loads(p.read_text())
    except json.JSONDecodeError as e:
        fail(f"{name}: invalid JSON: {e}")
        continue
    for field in required:
        if field not in data:
            fail(f"{name}: missing required field '{field}'")

# --- skills ---
skill_dirs = sorted(d for d in (ROOT / "skills").iterdir() if d.is_dir())
if not skill_dirs:
    fail("no skills found")
for d in skill_dirs:
    checked += 1
    sk = d / "SKILL.md"
    if not sk.exists():
        fail(f"{d.name}: no SKILL.md")
        continue
    fm = frontmatter(sk)
    if fm is None:
        fail(f"{d.name}/SKILL.md: no frontmatter block")
        continue
    for field in ("name", "description"):
        if not fm.get(field):
            fail(f"{d.name}/SKILL.md: missing frontmatter '{field}'")
    if fm.get("name") and fm["name"] != d.name:
        fail(f"{d.name}/SKILL.md: name '{fm['name']}' != directory name")
    desc = fm.get("description", "")
    if len(desc) > 1536:
        fail(f"{d.name}/SKILL.md: description {len(desc)} chars (cap 1536)")
    body_lines = sum(1 for _ in sk.open()) if sk.exists() else 0
    if body_lines > 130:
        fail(f"{d.name}/SKILL.md: {body_lines} lines — keep SKILL.md short; move depth to references/")

# --- agents ---
agent_files = sorted((ROOT / "agents").glob("*.md"))
if not agent_files:
    fail("no agents found")
for a in agent_files:
    checked += 1
    fm = frontmatter(a)
    if fm is None:
        fail(f"agents/{a.name}: no frontmatter block")
        continue
    for field in ("name", "description"):
        if not fm.get(field):
            fail(f"agents/{a.name}: missing frontmatter '{field}'")
    if a.stem in ("unit-auditor", "lead-consistency", "fresh-reader"):
        tools = fm.get("tools", "")
        if set(t.strip() for t in tools.split(",")) - {"Read", "Grep", "Glob"}:
            fail(f"agents/{a.name}: auditor agents must be read-only (tools: Read, Grep, Glob) — found '{tools}'")

# --- evals ---
case_dirs = [d for d in (ROOT / "evals").iterdir()
             if d.is_dir() and d.name != "results"]
for c in sorted(case_dirs):
    checked += 1
    if not (c / "prompt.md").exists():
        fail(f"evals/{c.name}: no prompt.md")
    graders = list((c / "graders").glob("*.md")) if (c / "graders").is_dir() else []
    if not graders:
        fail(f"evals/{c.name}: no graders/*.md")
for te in sorted(ROOT.glob("skills/*/evals/trigger_eval.json")):
    checked += 1
    try:
        cases = json.loads(te.read_text())
        flags = {c["should_trigger"] for c in cases}
        if flags != {True, False}:
            fail(f"{te.relative_to(ROOT)}: needs both should_trigger true and false cases")
    except (json.JSONDecodeError, KeyError, TypeError) as e:
        fail(f"{te.relative_to(ROOT)}: {e}")

# --- sealed answer key: never inside the demo workspace ---
checked += 1
ws = ROOT / "skills/grade-audit-demo/assets/demo-workspace"
leaks = [p for p in ws.rglob("*") if "answer" in p.name.lower()]
if leaks:
    fail(f"answer key material inside demo workspace: {leaks}")

# --- report, with counts ---
print(f"checked {checked} items: {checked - len(failures)} passed, {len(failures)} failed")
for f in failures:
    print(f"  FAIL: {f}")
sys.exit(1 if failures else 0)
