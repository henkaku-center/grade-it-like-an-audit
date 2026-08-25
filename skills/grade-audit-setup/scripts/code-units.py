#!/usr/bin/env python3
"""Code each person's submission to a unit code, and scan — never rewrite — the contents.

What this does: assigns every person a random unit code, copies their material into a
coded workspace **byte-for-byte**, keeps the code->identity map OUTSIDE that workspace,
and reports every identifier it can find inside the files so you can decide what to do.

What this does NOT do: modify file contents. An earlier version rewrote them and broke the
audit method's ATTRIBUTION check — a privacy pass runs over the same files the evidence
discipline depends on. This one observes and reports. See ../references/data-handling.md.

It is also not anonymization, de-identification, or compliance with any law: you keep the
key, so the material remains personal data and an education record. Not legal advice.

Stdlib only. Dry-run by default; --apply writes.
"""

import argparse
import csv
import fnmatch
import hashlib
import json
import os
import re
import secrets
import shutil
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

TEXT_EXT = {
    ".md", ".markdown", ".txt", ".rst", ".tex", ".org",
    ".py", ".js", ".mjs", ".ts", ".tsx", ".jsx", ".java", ".c", ".h", ".cpp", ".hpp",
    ".cs", ".go", ".rs", ".rb", ".php", ".swift", ".kt", ".m", ".r", ".rmd", ".jl",
    ".sql", ".sh", ".bash", ".zsh", ".ps1",
    ".csv", ".tsv", ".json", ".jsonl", ".yml", ".yaml", ".toml", ".ini", ".cfg",
    ".html", ".htm", ".css", ".scss", ".xml", ".svg", ".ipynb", ".gitignore", "",
}

# Metadata-bearing formats: copied, never opened. Named in the report so you know the
# author field is still in there.
METADATA_EXT = {
    ".pdf", ".doc", ".docx", ".odt", ".xls", ".xlsx", ".ppt", ".pptx", ".pages",
    ".jpg", ".jpeg", ".png", ".tif", ".tiff", ".heic", ".mp3", ".mp4", ".mov", ".zip",
}

# Identity-class patterns: shapes that are hard to confuse with coursework content.
IDENTITY = [
    ("EMAIL", re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b")),
    ("PROFILE-URL", re.compile(
        r"\b(?:https?://)?(?:www\.)?"
        r"(?:linkedin\.com/in|twitter\.com|x\.com|instagram\.com|facebook\.com|"
        r"medium\.com/@|orcid\.org|youtube\.com/@|about\.me)/[\w.\-@]+", re.I)),
    ("PHONE", re.compile(
        r"(?<![\w.])(?:\+\d{1,3}[\s.-]?)?(?:\(\d{3}\)[\s.-]?|\d{3}[\s.-])\d{3}[\s.-]\d{4}(?![\w])")),
]

# `@name` is a handle in prose and `@property` in source. Prose only, code spans masked.
HANDLE = ("HANDLE", re.compile(r"(?<![\w./@])@[A-Za-z][\w.-]{2,}\b"))

# Citation-class, reported separately: github.com/numpy/numpy is a source, not a person.
CODE_HOST = ("CODE-HOST-URL", re.compile(
    r"\b(?:https?://)?(?:www\.)?(?:github\.com|gitlab\.com|bitbucket\.org)/[\w.\-/]+", re.I))

# Flagged for a human, never counted as identity: a capitalized pair is as likely to be
# "Central Limit Theorem" as a person.
NAMEISH = ("NAME-SHAPED", re.compile(r"\b[A-Z][a-z]{1,15}\s+[A-Z][a-z]{1,15}\b"))

CODE_EXT = {
    ".py", ".js", ".mjs", ".ts", ".tsx", ".jsx", ".java", ".c", ".h", ".cpp", ".hpp",
    ".cs", ".go", ".rs", ".rb", ".php", ".swift", ".kt", ".m", ".r", ".rmd", ".jl",
    ".sql", ".sh", ".bash", ".zsh", ".ps1", ".ipynb", ".json", ".jsonl", ".yml",
    ".yaml", ".toml", ".xml", ".svg", ".css", ".scss", ".html", ".htm",
}

FENCED = re.compile(r"```.*?```|~~~.*?~~~|`[^`\n]+`", re.S)

# Identity-shaped template fields that are ALREADY empty in the source. Recorded before any
# grading happens, so nobody can later mistake a student's blank for something this tool did.
IDENTITY_FIELD = re.compile(
    r"^[\s>*_-]*\**\s*(student\s*name|name|author|date|submitted\s*by)\s*\**\s*[::]"
    r"\s*\**\s*(?P<value>.*?)\s*\**\s*$", re.I | re.M)
BLANK_VALUE = re.compile(r"^(_{3,}|\.{3,}|-{3,}|\[\s*\]|)$")

COMMON_WORDS = {
    "al", "an", "art", "bill", "bob", "case", "chance", "dan", "drew", "grace", "green",
    "guy", "hope", "jean", "joy", "king", "lane", "may", "mark", "miles", "mine", "page",
    "rose", "sky", "son", "stone", "sun", "van", "will", "wood",
}

# Words that show up in submission filenames and are not names.
FILENAME_NOISE = {
    "final", "project", "projects", "report", "reports", "submission", "submissions",
    "paper", "research", "draft", "version", "assignment", "solution", "presentation",
    "slides", "notes", "code", "data", "analysis", "aps", "and", "the", "for", "with",
}

RESIDUAL_RISK = """\
## What this pass cannot do

Structural limits, not bugs. They are why this is risk reduction and blind grading, not
compliance.

- **It codes the container, not the content.** File contents are copied byte-for-byte. If
  a submission says "By Jane Doe" inside, it still does — the scan tells you where, and the
  fix is upstream: anonymous export from your LMS, or an assignment instruction to keep
  names in the LMS field and out of the file.
- **You hold the key.** The map exists (you have to return grades to real people), so
  nothing here is de-identified in your hands, and under GDPR this is pseudonymized
  personal data, not anonymous data.
- **The scan's recall is not 100%.** It searches the terms you supply plus a narrow set of
  structured patterns. Nicknames, misspellings, initials, and third parties are missed
  unless you list them. Self-identifying content — a hometown, a distinctive topic — is not
  a name and cannot be found this way at all.
- **Binary formats are not inspected.** PDF/Office author fields, EXIF, and revision
  history are copied untouched. Affected files are listed by unit code.
- **Two copies of the material now exist.** Gitignore both; delete the coded tree when the
  grading is done.
"""


def die(msg):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(2)


def unit_code(i):
    """0 -> unit-a ... 25 -> unit-z, 26 -> unit-aa. Order is assigned after a shuffle."""
    label = ""
    i += 1
    while i:
        i, rem = divmod(i - 1, 26)
        label = chr(ord("a") + rem) + label
    return f"unit-{label}"


def assign_codes(people):
    """Random codes, not hashes: a hash of a name is reversible against a class roster in
    microseconds, and FERPA's coded-record provision (34 CFR 99.31(b)(2)) requires a code
    not based on the student's own information. Shuffle so the code carries no ordering."""
    order = list(range(len(people)))
    secrets.SystemRandom().shuffle(order)
    for rank, idx in enumerate(order):
        people[idx]["code"] = unit_code(rank)
    return people


def name_variants(value):
    """first/last/full -> the spellings that actually show up in submitted work."""
    out = {value}
    parts = [p for p in re.split(r"[\s,]+", value.strip()) if p]
    if len(parts) >= 2:
        first, last = parts[0], parts[-1]
        out |= {first, last, f"{first} {last}", f"{last}, {first}", f"{last} {first}"}
        for sep in (".", "_", "-", ""):
            out.add(f"{first}{sep}{last}")
        out.add(f"{first[0]}{last}")
        out.add(f"{first[0]}.{last}")
    return {v for v in (s.strip() for s in out) if v}


def terms_from_path_name(name):
    """Derive candidate identifiers from a submission's own file/folder name.

    `mp1-rosalind-vega` -> rosalind, vega, rosalind-vega, rosalindvega …
    Noise words (report, final, submission) are dropped; what survives is a candidate, and
    candidates are never printed — only counted.
    """
    stem = Path(name).stem
    stem = re.sub(r"^(?:mp|hw|lab|assignment|final)[\s_-]*\d*[\s_-]*", "", stem, flags=re.I)
    raw = [t for t in re.split(r"[^A-Za-z]+", stem) if t]
    tokens = [t for t in raw if len(t) >= 3 and t.lower() not in FILENAME_NOISE]
    out = set(tokens)
    if len(tokens) >= 2:
        out |= name_variants(f"{tokens[0]} {tokens[1]}")
    return out


def term_regex(term):
    r"""Underscore is a separator here, not a word character. `\w` includes `_`, so a
    boundary built on it silently misses `Ellery_Who_Should_Protect.pdf` and
    `jane_doe` — which is how names most often appear in filenames and identifiers."""
    return re.compile(r"(?<![A-Za-z0-9])" + re.escape(term) + r"(?![A-Za-z0-9])",
                      re.IGNORECASE)


def slug_role(value):
    s = re.sub(r"[^a-z0-9]+", "-", value.strip().lower()).strip("-")
    return "person" if not s or s.startswith("unit") else s


def filter_terms(terms, allow_short, skipped):
    keep = set()
    for t in terms:
        if not allow_short and (len(t) < 3 or t.lower() in COMMON_WORDS):
            skipped.append(t)
            continue
        keep.add(t)
    return keep


def load_roster(path, allow_short):
    """Every cell except `path` and `role` is an identifier to search for."""
    with open(path, newline="", encoding="utf-8-sig") as fh:
        rows = list(csv.DictReader(fh))
    if not rows:
        die(f"roster {path} has no data rows")
    headers = [h for h in rows[0] if h]
    path_col = next((h for h in headers if h.strip().lower() in
                     ("path", "folder", "dir", "file", "submission")), None)
    role_col = next((h for h in headers if h.strip().lower() == "role"), None)
    people, skipped = [], []
    for row in rows:
        terms = set()
        for col, val in row.items():
            if not col or col in (path_col, role_col) or not val or not val.strip():
                continue
            val = val.strip()
            terms |= name_variants(val) if " " in val else {val}
        people.append({
            "path": (row.get(path_col) or "").strip() if path_col else "",
            "role": slug_role((row.get(role_col) or "") if role_col else ""),
            "terms": sorted(filter_terms(terms, allow_short, skipped), key=len, reverse=True),
            # unfiltered: what the roster actually knows. Used for redacting output, because a
            # name dropped from the SEARCH set as too short or too common still must not be
            # printed into a report the grading session reads.
            "identity_terms": sorted(terms, key=len, reverse=True),
            "identity": {k: v for k, v in row.items() if k and v},
        })
    return people, sorted(set(skipped))


def roster_from_dirs(inputs, excludes, allow_short):
    """No roster CSV: each immediate child of --inputs is a unit, and its own name is the
    source of candidate identifiers. Honest about being a guess — everything it derives is
    reported as a count, never printed."""
    people, skipped = [], []
    for child in sorted(inputs.iterdir()):
        name = child.name
        if name.startswith(".") or any(fnmatch.fnmatch(name, pat) for pat in excludes):
            continue
        raw = terms_from_path_name(name)
        people.append({"path": name, "role": "student",
                       "terms": sorted(filter_terms(raw, allow_short, skipped),
                                       key=len, reverse=True),
                       "identity_terms": sorted(raw, key=len, reverse=True),
                       "identity": {"path": name}})
    return people, sorted(set(skipped))


def is_text(p):
    if p.suffix.lower() in METADATA_EXT or p.suffix.lower() not in TEXT_EXT:
        return False
    try:
        chunk = p.open("rb").read(8192)
    except OSError:
        return False
    if b"\x00" in chunk:
        return False
    try:
        chunk.decode("utf-8")
    except UnicodeDecodeError:
        return False
    return True


def mask_code_spans(text):
    """Hide fenced and inline code so prose rules do not fire inside a code sample."""
    spans = []

    def stash(m):
        spans.append(m.group(0))
        return "\x00" * len(m.group(0))

    return FENCED.sub(stash, text), spans


def line_of(text, pos):
    return text.count("\n", 0, pos) + 1


def blank_identity_fields(text, relpath, attest):
    """Record identity template fields found in the source, blank or filled, before coding.

    Both states matter: the blanks are what a grader might otherwise blame on this tool, and
    the filled ones are the control that proves the tool did not blank anything. A unit with
    no such field at all is a third state and must not be counted as either."""
    for m in IDENTITY_FIELD.finditer(text):
        blank = bool(BLANK_VALUE.match(m.group("value") or ""))
        attest.append({"file": relpath, "line": line_of(text, m.start()),
                       "field": m.group(1).strip().lower(),
                       "blank": blank,
                       "state": ("empty in the source, before this tool touched anything"
                                 if blank else "filled in by the author")})


def scan_text(text, relpath, plan, is_code, findings):
    """Report, never replace. `plan` is [{label, terms}] — labels, not names, reach the
    report; the matched string is carried for the private detail log only."""
    for entry in plan:
        for term in entry["terms"]:
            for m in term_regex(term).finditer(text):
                findings.append({"kind": "ROSTER-TERM", "class": "identity",
                                 "file": relpath, "line": line_of(text, m.start()),
                                 "label": entry["label"], "match": m.group(0)})
    for kind, pattern in IDENTITY:
        for m in pattern.finditer(text):
            findings.append({"kind": kind, "class": "identity", "file": relpath,
                             "line": line_of(text, m.start()), "match": m.group(0)})
    if not is_code:
        masked, _ = mask_code_spans(text)
        kind, pattern = HANDLE
        for m in pattern.finditer(masked):
            findings.append({"kind": kind, "class": "identity", "file": relpath,
                             "line": line_of(text, m.start()), "match": m.group(0)})
    for kind, pattern in (CODE_HOST, NAMEISH):
        for m in pattern.finditer(text):
            findings.append({"kind": kind,
                             "class": "citation" if kind == "CODE-HOST-URL" else "flag",
                             "file": relpath, "line": line_of(text, m.start()),
                             "match": m.group(0)})
    return findings


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(65536), b""):
            h.update(block)
    return h.hexdigest()


def build_plan(subject, people):
    """Labels, not names. The unit's own person is their code; everyone else the roster
    knows gets a token of their own, numbered per unit and shuffled so the numbering means
    nothing across units. Nobody is ever folded into the subject."""
    subject_terms = set(subject["terms"])
    others = [p for p in people if p is not subject and p["terms"]]
    secrets.SystemRandom().shuffle(others)
    plan = [{"label": subject["code"], "terms": sorted(subject_terms, key=len, reverse=True)}]
    seen = Counter()
    for other in others:
        terms = set(other["terms"]) - subject_terms
        if not terms:
            continue
        seen[other["role"]] += 1
        plan.append({"label": f"{other['role']}-{seen[other['role']]}",
                     "terms": sorted(terms, key=len, reverse=True)})
    return plan


def deny_rule_snippet(keys):
    return f"""
Enforce the separation — add to the grading workspace's `.claude/settings.json` so the
session cannot read the map even if it tries (a prompt-level promise is not enforcement):

  {{
    "permissions": {{
      "deny": [
        "Read({keys}/**)",
        "Bash(cat {keys}/**)"
      ]
    }}
  }}
"""


def sanitize(text, terms):
    """No path reaches the report with an identifier still in it — a filename carries a
    name as readily as the text does."""
    for term in sorted(terms, key=len, reverse=True):
        text = term_regex(term).sub("[id]", text)
    return text


def render_report(run_id, mode, units, per_unit, findings, path_leaks, skipped_terms,
                  missing, copy_verified, all_terms, attest=(), renamed_files=False):
    ident = [f for f in findings if f["class"] == "identity"]
    cites = [f for f in findings if f["class"] == "citation"]
    flags = [f for f in findings if f["class"] == "flag"]
    units_with_identity = sorted({f["file"].split("/")[0] for f in ident})

    L = [
        "# Coded units — scan report",
        "",
        f"Run `{run_id}` · {len(units)} unit{'s' if len(units) != 1 else ''} · mode: {mode}",
        "",
        "**No real names appear in this file** — unit codes, categories, and `file:line`",
        "locations only. Matched strings go to the private detail log beside the map.",
        "",
        "> Contents were **not modified**. This pass codes the container and reports what is",
        "> inside it. It is pseudonymization, not anonymization, and establishes no",
        "> compliance with FERPA, GDPR, or your institution's policy.",
        "",
        "## The number that decides whether container coding is enough",
        "",
    ]
    unscanned = sorted(c for c in per_unit if per_unit[c]["text"] == 0)
    scanned_units = len(per_unit) - len(unscanned)
    if unscanned:
        L += [f"**{len(unscanned)} of {len(units)} units had NOTHING to scan** — every file in",
              "them is a format this pass does not open (PDF, Office, image). A zero here is",
              "**not a clean result, it is an uninspected one**; the author metadata inside",
              "those files was never looked at, and their filenames are listed below.",
              f"Units: {', '.join(unscanned)}", ""]
    if scanned_units:
        L += [f"**{len(units_with_identity)} of {scanned_units} scanned units carry at least one "
              f"identity finding inside their file contents** ({len(ident)} findings total).",
              ""]
        if units_with_identity:
            L += ["Coding the folder does not blind those units — the name is still in the",
                  "text. Fix it upstream (anonymous LMS export, or tell students to keep names",
                  "out of the file) or accept that grading is not blind for them.", ""]
        else:
            L += ["No identity findings in anything that could be read. For the readable part",
                  "of this corpus, coding the container is the whole intervention.", ""]

    L += ["## Findings by category", "", "| category | class | count |", "| --- | --- | --- |"]
    for kind, n in sorted(Counter((f["kind"], f["class"]) for f in findings).items(),
                          key=lambda kv: -kv[1]):
        L.append(f"| {kind[0]} | {kind[1]} | {n} |")
    if not findings:
        L.append("| (none) | — | 0 |")

    L += ["", "## Per unit", "",
          "| unit | files | text scanned | not inspected | identity | citation-class | flags | .git |",
          "| --- | --- | --- | --- | --- | --- | --- | --- |"]
    for code in sorted(per_unit):
        u = per_unit[code]
        mine = [f for f in findings if f["file"].split("/")[0] == code]
        L.append(f"| {code} | {u['files']} | {u['text']} | {len(u['binary'])} "
                 f"| {len([f for f in mine if f['class'] == 'identity'])} "
                 f"| {len([f for f in mine if f['class'] == 'citation'])} "
                 f"| {len([f for f in mine if f['class'] == 'flag'])} "
                 f"| {'yes' if u['git'] else '—'} |")

    L += ["", "## Needs your eyes", ""]
    binaries = [(c, f) for c in sorted(per_unit) for f in per_unit[c]["binary"]]
    if binaries:
        L.append(f"- **{len(binaries)} file(s) not inspected** — PDF/Office author fields and "
                 f"EXIF are intact inside them:")
        for c, f in binaries[:40]:
            L.append(f"  - `{sanitize(f'{c}/{f}', all_terms)}`")
        if len(binaries) > 40:
            L.append(f"  - …and {len(binaries) - 40} more")
    else:
        L.append("- No uninspectable files.")
    gits = [c for c in sorted(per_unit) if per_unit[c]["git"]]
    if gits:
        L.append(f"- **{len(gits)} unit(s) carry a `.git` directory** — commit authorship is "
                 f"readable identity, and is also the raw record an attribution check wants. "
                 f"`--exclude-git` drops it; you cannot have both: {', '.join(gits)}")
    if path_leaks:
        L.append(f"- **{len(path_leaks)} path(s) still carry an identifier** after coding — a "
                 f"filename, not the folder. `--rename-files` renames them; leaving them is a "
                 f"choice, not an oversight:")
        for p in path_leaks[:20]:
            L.append(f"  - `{sanitize(p, all_terms)}`")
    else:
        L.append("- No coded path carries an identifier.")
    L.append(f"- **{len(cites)} citation-class URL(s)** (`github.com/…` and friends) reported "
             f"separately from identity: a repo link is usually a source, occasionally an "
             f"account. Yours to judge.")
    phones = [f for f in ident if f["kind"] == "PHONE"]
    if phones:
        L.append(f"- **{len(phones)} phone number(s)** — in academic writing these are usually "
                 f"the *cited institution's* switchboard, not the author's. Check before "
                 f"treating them as the subject's identity.")
    L.append(f"- **{len(flags)} name-shaped phrase(s) flagged** — capitalized pairs the roster "
             f"did not explain. Could be a classmate, a TA, or a theorem. Never counted as "
             f"identity — and on a transcript corpus this count is noise-dominated "
             f"(\"Central Limit\", \"Read Tool\"); read it as a haystack size, not a signal.")
    if skipped_terms:
        L.append(f"- **{len(skipped_terms)} candidate term(s) skipped as too short or too "
                 f"common** to search for safely. `--allow-short` includes them.")
    if missing:
        L.append(f"- **{len(missing)} roster path(s) not found** under `--inputs`.")
    if copy_verified is not None:
        L.append(f"- Byte-identity: **{copy_verified[0]}/{copy_verified[1]} copied files "
                 f"hash-match their source**." if copy_verified[0] == copy_verified[1] else
                 f"- **BYTE-IDENTITY FAILURE: only {copy_verified[0]}/{copy_verified[1]} "
                 f"copied files hash-match their source. Do not grade this copy.**")
    if ident:
        byfile = Counter(f["file"] for f in ident)
        L += ["", "## Where the identity actually is", "",
              "Aggregated by file, worst first — in a corpus of agent transcripts a handful of",
              "files usually account for nearly all of it, and that changes what you do next.",
              "", "| file | identity findings |", "| --- | --- |"]
        for fname, n in byfile.most_common(25):
            L.append(f"| `{sanitize(fname, all_terms)}` | {n} |")
        if len(byfile) > 25:
            L.append(f"| …and {len(byfile) - 25} more files | "
                     f"{sum(n for _, n in byfile.most_common()[25:])} |")
        L += ["", "Line numbers and matched strings are in the private detail log, not here."]
    L += ["", "## Attestation — this pass did not blank anything", "",
          "File **contents were copied byte-for-byte** and hash-verified. A blank name field, a",
          "missing date or an empty section in a coded unit was blank in the submission.",
          "**Never attribute one to this tool** — and if you believe content was altered, that is",
          "a tooling finding, not a subject defect.", ""]
    if renamed_files:
        L += ["Filenames **were** coded in this run (`--rename-files`), so a cross-reference that",
              "no longer resolves is a tooling artefact — never charge a subject for it. Only the",
              "top-level folder is renamed without that flag.", ""]
    else:
        L += ["Only the top-level folder was renamed; filenames are untouched.", ""]
    blanks = [a for a in attest if a.get("blank")]
    filled = [a for a in attest if not a.get("blank")]
    with_field = {a["file"].split("/")[0] for a in attest}
    scanned_units = {c for c in per_unit if per_unit[c]["text"] > 0}
    no_field = sorted(scanned_units - with_field)
    unscanned = sorted(c for c in per_unit if per_unit[c]["text"] == 0)
    if blanks:
        byu = sorted({a["file"].split("/")[0] for a in blanks})
        L += [f"Identity fields already empty in the source, recorded before grading "
              f"({len(blanks)} in {len(byu)} unit(s)):", "",
              "| unit | field | location |", "| --- | --- | --- |"]
        for a in blanks[:40]:
            L.append(f"| {a['file'].split('/')[0]} | {a['field']} | "
                     f"`{sanitize(a['file'], all_terms)}:{a['line']}` |")
        if len(blanks) > 40:
            L.append(f"| …and {len(blanks) - 40} more | | |")
        L.append("")
    else:
        L += ["No identity template field was empty in the source.", ""]
    L += ["The control, stated exactly — three states, not two:", "",
          f"- **{len({a['file'].split('/')[0] for a in filled})} unit(s)** had such a field and "
          f"it was **filled in**. If this tool blanked fields, these would be blank too.",
          f"- **{len(no_field)} scanned unit(s)** contain no such field at all"
          + (f" ({', '.join(no_field)})" if no_field else "")
          + " — neither blank nor filled; nothing can be inferred about them.",
          f"- **{len(unscanned)} unit(s)** had nothing scannable"
          + (f" ({', '.join(unscanned)})" if unscanned else "")
          + " — not inspected, so not evidence either way.", ""]
    L += ["", RESIDUAL_RISK]
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(
        description="Code submissions to unit codes and scan their contents. "
                    "Contents are never modified. Risk reduction, not compliance.")
    ap.add_argument("--inputs", help="directory whose immediate children are submissions")
    ap.add_argument("--out", help="directory to write coded units into")
    ap.add_argument("--roster", help="CSV; one row per person, a path/folder/file column")
    ap.add_argument("--roster-from-dirs", action="store_true",
                    help="no CSV: derive candidate identifiers from each submission's own name")
    ap.add_argument("--keys", help="directory for the code->identity map; must be OUTSIDE "
                                   "the workspace. Required with --apply.")
    ap.add_argument("--exclude", action="append", default=[],
                    help="glob of immediate children that are not submissions (repeatable)")
    ap.add_argument("--apply", action="store_true", help="write files (default: dry run)")
    ap.add_argument("--scan-only", action="store_true", help="scan in place; copy nothing")
    ap.add_argument("--rename-files", action="store_true",
                    help="also rename files whose names carry an identifier")
    ap.add_argument("--exclude-git", action="store_true", help="do not copy .git directories")
    ap.add_argument("--allow-short", action="store_true",
                    help="also search terms under 3 chars / common words")
    ap.add_argument("--report", help="write the scan report here (default: <out>/scan-report.md)")
    ap.add_argument("--self-test", action="store_true", help="run the built-in fixture check")
    ap.add_argument("--decode", metavar="MAP.json",
                    help="print the code -> identity table from a run's map file. This is how "
                         "you get the names back at delivery; run it OUTSIDE the grading "
                         "session, since that session is denied read access to the map.")
    if "--self-test" in sys.argv[1:]:
        return self_test()
    if "--decode" in sys.argv[1:]:
        return decode(sys.argv[sys.argv.index("--decode") + 1])
    args = ap.parse_args()

    if not args.inputs:
        die("--inputs is required")
    inputs = Path(args.inputs).resolve()
    if not inputs.is_dir():
        die(f"--inputs {inputs} is not a directory")
    if not args.roster and not args.roster_from_dirs:
        die("give --roster CSV or --roster-from-dirs")
    if args.apply and args.scan_only:
        die("--apply and --scan-only are contradictory")
    out = Path(args.out).resolve() if args.out else None
    if not args.scan_only and out is None:
        die("--out is required unless --scan-only")
    keys = Path(args.keys).resolve() if args.keys else None
    if args.apply and keys is None:
        die("--apply requires --keys: the map has to go somewhere outside the workspace")
    if keys:
        for label, target in (("--out", out), ("--inputs", inputs)):
            if target and (keys == target or keys in target.parents or target in keys.parents):
                die(f"--keys {keys} overlaps {label} {target}. The map must not live with "
                    f"the material.")
        # The workspace is the tree the grading session works in — the common ancestor of the
        # material and the coded copy — not whatever directory you happened to run from.
        workspace = (Path(os.path.commonpath([str(inputs), str(out)])) if out
                     else inputs.parent)
        if keys == workspace or workspace in keys.parents:
            die(f"--keys {keys} is inside the workspace ({workspace}). Put it where the "
                f"grading session cannot reach it — that is the point of the map.")
    if args.apply and out.exists() and any(out.iterdir()):
        die(f"--out {out} exists and is not empty; refusing to write into it")

    if args.roster:
        people, skipped_terms = load_roster(args.roster, args.allow_short)
    else:
        people, skipped_terms = roster_from_dirs(inputs, args.exclude, args.allow_short)
    units = [p for p in people if p["path"]]
    if not units:
        die("no roster row names a submission path — nothing to code")
    assign_codes(units)

    findings, per_unit, missing, path_leaks, attest = [], {}, [], [], []
    copied, verified = 0, 0

    for person in units:
        src = inputs / person["path"]
        if not src.exists():
            missing.append(person["path"])
            continue
        code = person["code"]
        plan = build_plan(person, people)
        # the path-leak check uses the unfiltered set too, so the report cannot claim
        # "no coded path carries an identifier" while listing one
        all_terms = sorted({t for p in people for t in p.get("identity_terms", p["terms"])},
                           key=len, reverse=True)
        u = per_unit[code] = {"files": 0, "text": 0, "binary": [], "git": False}
        files = [src] if src.is_file() else sorted(p for p in src.rglob("*") if p.is_file())
        for f in files:
            rel = f.name if src.is_file() else str(f.relative_to(src))
            in_git = ".git" in Path(rel).parts
            if in_git:
                u["git"] = True
                if args.exclude_git:
                    continue
            u["files"] += 1
            renamed = rel
            if args.rename_files:
                for entry in plan:
                    for term in entry["terms"]:
                        renamed = term_regex(term).sub(entry["label"], renamed)
            coded_rel = f"{code}/{renamed}"
            for term in all_terms:
                if term_regex(term).search(renamed):
                    path_leaks.append(coded_rel)
                    break
            if is_text(f):
                u["text"] += 1
                text = f.read_text(encoding="utf-8", errors="replace")
                scan_text(text, coded_rel, plan, f.suffix.lower() in CODE_EXT, findings)
                blank_identity_fields(text, coded_rel, attest)
            else:
                u["binary"].append(renamed)
            if args.apply:
                target = out / code / renamed
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, target)     # contents and mtime, untouched
                copied += 1
                if sha256(f) == sha256(target):
                    verified += 1

    run_id = f"{datetime.now().strftime('%Y-%m-%dT%H-%M-%S')}-{secrets.token_hex(3)}"
    mode = "APPLIED" if args.apply else ("SCAN ONLY" if args.scan_only else "DRY RUN")
    every_term = sorted({t for p in people for t in p.get("identity_terms", p["terms"])},
                        key=len, reverse=True)
    report = render_report(run_id, mode, units, per_unit, findings, sorted(set(path_leaks)),
                           skipped_terms, missing,
                           (verified, copied) if args.apply else None, every_term, attest,
                           args.rename_files)

    if keys and (args.apply or args.scan_only):
        keys.mkdir(parents=True, exist_ok=True)
        os.chmod(keys, 0o700)
        if args.apply:
            keymap = keys / f"{run_id}.map.json"
            keymap.write_text(json.dumps(
                {"run": run_id, "inputs": str(inputs), "out": str(out),
                 "units": [{"code": p["code"], "path": p["path"], "identity": p["identity"]}
                           for p in units]}, indent=2), encoding="utf-8")
            os.chmod(keymap, 0o600)
    if keys and (args.apply or args.scan_only):
        detail = keys / f"{run_id}.detail.jsonl"
        with detail.open("w", encoding="utf-8") as fh:
            for rec in findings:
                fh.write(json.dumps(rec) + "\n")
            for leak in sorted(set(path_leaks)):
                fh.write(json.dumps({"kind": "PATH-CARRIES-IDENTIFIER", "path": leak}) + "\n")
        os.chmod(detail, 0o600)

    report_path = Path(args.report).resolve() if args.report else (
        out / "scan-report.md" if args.apply else None)
    if report_path:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(report, encoding="utf-8")

    print(report)
    if keys and (args.apply or args.scan_only):
        print(f"\nPrivate detail log (real matched strings): {keys}/{run_id}.detail.jsonl")
    if args.apply:
        print(f"Map: {keys}/{run_id}.map.json")
        print(f"At delivery, get the names back with:\n"
              f"  python3 {Path(__file__).name} --decode {keys}/{run_id}.map.json\n"
              f"Run that OUTSIDE the grading session — that session is denied read access to "
              f"the map, which is the point.")
        print(deny_rule_snippet(keys))
        if verified != copied:
            print(f"!! byte-identity failed on {copied - verified} file(s). Do not grade "
                  f"this copy.")
            return 1
    elif not args.scan_only:
        print("\n--- DRY RUN. Nothing written — not even the private detail log. Review the "
              "above, then re-run with --apply, or --scan-only --keys DIR to record the "
              "matched strings without copying anything. ---")
    return 0


def decode(mapfile):
    """Print the code -> identity table. The round trip the instructor actually needs: the
    letters are addressed to unit codes, and this is what says who each one belongs to."""
    path = Path(mapfile)
    if not path.exists():
        die(f"no map file at {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    units = data.get("units", [])
    if not units:
        die(f"{path} records no units")
    width = max(len(u["code"]) for u in units)
    print(f"run {data.get('run', '?')} — {len(units)} unit(s)")
    print(f"coded from : {data.get('inputs', '?')}")
    print()
    for u in sorted(units, key=lambda x: x["code"]):
        ident = u.get("identity", {})
        who = " · ".join(f"{k}={v}" for k, v in ident.items() if k.lower() != "path")
        print(f"  {u['code']:<{width}}  {u.get('path', '')}" + (f"    {who}" if who else ""))
    print()
    print("Send each unit's letter to the person on its row. Check one by hand before sending")
    print("the batch — a mis-sent grade is not a recoverable error.")
    return 0


def self_test():
    """Fixture with a known answer — run in CI, prints real counts, exits nonzero on any
    failure. The central guarantee (contents are untouched) is checked by hash."""
    import contextlib
    import io
    import tempfile
    checks, failures = 0, []

    def check(name, cond):
        nonlocal checks
        checks += 1
        if not cond:
            failures.append(name)

    def run(argv):
        old = sys.argv
        sys.argv = ["code-units.py"] + argv
        try:
            with contextlib.redirect_stdout(io.StringIO()) as buf:
                rc = main()
            return rc, buf.getvalue()
        finally:
            sys.argv = old

    with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as keydir:
        tmp, keydir = Path(tmp), Path(keydir)
        sub = tmp / "inputs" / "mp1-quilla-brandsmith"
        sub.mkdir(parents=True)
        essay = sub / "quilla-brandsmith-essay.md"
        essay.write_text(
            "By Quilla Brandsmith (quilla.brandsmith@uni.edu, 608-555-0100).\n"
            "Quilla analyzed the Central Limit Theorem. Ping @quillab for data.\n"
            "Profile: linkedin.com/in/quillabrandsmith\n"
            "```python\n@property\ndef rate(self): ...\n```\n", encoding="utf-8")
        (sub / "model.py").write_text(
            "import functools\nclass S:\n    @property\n    def r(self): ...\n"
            "    @functools.lru_cache\n    def draw(self): ...\n"
            "# ref: https://github.com/numpy/numpy\n", encoding="utf-8")
        (sub / "figure.png").write_bytes(b"\x89PNG\x00fake")
        old_mtime = 1_500_000_000
        for f in sub.rglob("*"):
            os.utime(f, (old_mtime, old_mtime))
        roster = tmp / "roster.csv"
        roster.write_text("path,name,email,role\n"
                          "mp1-quilla-brandsmith,Quilla Brandsmith,quilla.brandsmith@uni.edu,student\n"
                          ",Li Wei,,peer\n", encoding="utf-8")

        people, skipped = load_roster(roster, allow_short=False)
        subject = next(p for p in people if p["path"])
        terms = {t.lower() for t in subject["terms"]}
        check("name variants expand", {"quilla brandsmith", "brandsmith, quilla", "quilla.brandsmith"} <= terms)
        check("role is not itself a search term", "student" not in terms)

        derived = terms_from_path_name("mp1-rosalind-vega")
        check("assignment prefix stripped from derived terms",
              not any(t.lower().startswith("mp1") for t in derived))
        check("derived terms include both name parts",
              {"rosalind", "vega"} <= {t.lower() for t in derived})
        check("filename noise words dropped",
              not ({"report", "submission"} & {t.lower()
                   for t in terms_from_path_name("Marlowe_Research_Paper_submission")}))

        assign_codes([subject])
        plan = build_plan(subject, people)
        check("subject label is the unit code", plan[0]["label"] == subject["code"])
        check("others get their own label, never the unit code",
              all(not e["label"].startswith("unit-") for e in plan[1:]))

        f1 = []
        scan_text(essay.read_text(), "unit-a/essay.md", plan, False, f1)
        kinds = Counter(f["kind"] for f in f1)
        check("roster name found", kinds["ROSTER-TERM"] >= 3)
        check("email found", kinds["EMAIL"] == 1)
        check("phone found", kinds["PHONE"] == 1)
        check("profile URL found", kinds["PROFILE-URL"] == 1)
        check("prose @handle found", kinds["HANDLE"] == 1)
        check("markdown code fence not treated as a handle",
              not any(f["match"] == "@property" for f in f1))
        check("name-shaped phrase flagged, not identity",
              any(f["kind"] == "NAME-SHAPED" and f["class"] == "flag" for f in f1))
        check("line numbers are right",
              any(f["kind"] == "EMAIL" and f["line"] == 1 for f in f1)
              and any(f["kind"] == "PROFILE-URL" and f["line"] == 3 for f in f1))

        f2 = []
        scan_text((sub / "model.py").read_text(), "unit-a/model.py", plan, True, f2)
        check("python decorators are not handles",
              not any(f["kind"] == "HANDLE" for f in f2))
        check("code-host URL is citation-class, not identity",
              any(f["kind"] == "CODE-HOST-URL" and f["class"] == "citation" for f in f2))
        check("no identity finding invented in clean code",
              not any(f["class"] == "identity" for f in f2))

        # guard: the map may not live with the material
        out, keys = tmp / "coded", keydir / "keys"        # keys live OUTSIDE the workspace
        try:
            run(["--inputs", str(tmp / "inputs"), "--roster", str(roster),
                 "--out", str(out), "--keys", str(out / "k"), "--apply"])
            check("keys-inside-out is refused", False)
        except SystemExit as e:
            check("keys-inside-out is refused", e.code == 2)

        rc, _ = run(["--inputs", str(tmp / "inputs"), "--roster", str(roster),
                     "--out", str(out), "--keys", str(keys), "--apply"])
        check("apply run succeeds", rc == 0)
        coded = next(d for d in out.iterdir() if d.is_dir())
        pairs = [(f, coded / f.relative_to(sub)) for f in sorted(sub.rglob("*")) if f.is_file()]
        check("every file copied", all(dst.exists() for _, dst in pairs))
        check("copies are byte-identical (the central guarantee)",
              all(sha256(s) == sha256(d) for s, d in pairs))
        check("mtimes preserved", all(int(d.stat().st_mtime) == old_mtime for _, d in pairs))
        check("contents genuinely unmodified",
              (coded / "quilla-brandsmith-essay.md").read_text() == essay.read_text())
        report = (out / "scan-report.md").read_text()
        check("report names nobody",
              not any(n in report for n in ("Quilla", "Brandsmith", "quillab", "Li Wei")))
        check("report counts the units that are not blind",
              "1 of 1 scanned units carry at least one identity" in report.replace("\n", " "))
        check("filename carrying a name is reported, with the name masked",
              "path(s) still carry an identifier" in report and "[id]-essay.md" in report)
        keyfile = next(keys.glob("*.map.json"))
        check("map is 0600", oct(keyfile.stat().st_mode)[-3:] == "600")
        check("map still carries the real identity", "Quilla Brandsmith" in keyfile.read_text())
        # the round trip the instructor needs at delivery
        old_argv = sys.argv
        sys.argv = ["code-units.py", "--decode", str(keyfile)]
        try:
            with contextlib.redirect_stdout(io.StringIO()) as buf:
                drc = main()
            dout = buf.getvalue()
        finally:
            sys.argv = old_argv
        check("--decode prints the code -> identity table", drc == 0
              and "Quilla Brandsmith" in dout and "unit-" in dout)
        check("--decode warns before a batch send", "mis-sent grade" in dout)
        check("detail log holds the matched strings",
              "Quilla Brandsmith" in next(keys.glob("*.detail.jsonl")).read_text())

        # --- the privacy defects the release dogfood found, each with its reproduction ---
        try:
            run(["--inputs", str(tmp / "inputs"), "--roster", str(roster),
                 "--out", str(out), "--keys", str(tmp / "inside-keys"), "--apply"])
            check("a key directory inside the workspace is refused", False)
        except SystemExit as e:
            check("a key directory inside the workspace is refused", e.code == 2)

        dryws = tmp / "dry"
        (dryws / "inputs" / "mp1-quilla-brandsmith").mkdir(parents=True)
        (dryws / "inputs" / "mp1-quilla-brandsmith" / "e.md").write_text(
            "By Quilla Brandsmith.\n", encoding="utf-8")
        drykeys = keydir / "drykeys"
        rc6, out6 = run(["--inputs", str(dryws / "inputs"), "--roster", str(roster),
                         "--out", str(dryws / "coded"), "--keys", str(drykeys)])
        check("a dry run writes NOTHING — not the coded copy, not the detail log",
              rc6 == 0 and not drykeys.exists() and not (dryws / "coded").exists())
        check("and the dry-run message says so accurately", "not even the private" in out6)

        # a name the SEARCH set drops as too common must still be redacted from the report
        common = tmp / "common"
        (common / "inputs" / "bob-smith").mkdir(parents=True)
        (common / "inputs" / "bob-smith" / "Bob_Report.md").write_text("Draft.\n",
                                                                       encoding="utf-8")
        crost = tmp / "common-roster.csv"
        crost.write_text("path,name\nbob-smith,Bob Smith\n", encoding="utf-8")
        rc7, out7 = run(["--inputs", str(common / "inputs"), "--roster", str(crost),
                         "--out", str(common / "coded"), "--keys", str(keydir / "ck"),
                         "--apply"])
        rep7 = (common / "coded" / "scan-report.md").read_text()
        check("a common-word name never reaches the report verbatim",
              "Bob" not in rep7 and "[id]" in rep7)
        check("and the path-leak line cannot contradict itself",
              not ("No coded path carries an identifier" in rep7
                   and "still carry an identifier" in rep7))

        # scan-only writes nothing
        out2 = tmp / "never"
        rc2, _ = run(["--inputs", str(tmp / "inputs"), "--roster", str(roster), "--scan-only"])
        check("scan-only succeeds", rc2 == 0)
        check("scan-only writes nothing", not out2.exists())

        # a corpus with no identifiers reports none
        clean = tmp / "clean" / "unit-x"
        clean.mkdir(parents=True)
        (clean / "report.md").write_text(
            "[user] planning a t-test\n[assistant] consider a permutation test\n",
            encoding="utf-8")
        rc3, out3 = run(["--inputs", str(tmp / "clean"), "--roster-from-dirs", "--scan-only"])
        check("clean corpus reports zero identity findings",
              rc3 == 0 and "No identity findings in anything that could be read" in out3)

        # regressions for the three defects a real-corpus run exposed
        check("underscore is a boundary, not a word character",
              bool(term_regex("Ellery").search("Ellery_Who_Should_Protect.pdf"))
              and bool(term_regex("jane").search("jane_doe_final.md")))
        check("a term still cannot match inside a longer word",
              not term_regex("ane").search("jane") and not term_regex("Kot").search("Ellery"))

        binonly = tmp / "binonly" / "mp1-ellery-tanaka"
        binonly.mkdir(parents=True)
        (binonly / "Ellery_Report.pdf").write_bytes(b"%PDF-1.4 fake")
        rc4, out4 = run(["--inputs", str(tmp / "binonly"), "--roster-from-dirs", "--scan-only"])
        check("binary-only unit is reported as uninspected, never as clean",
              rc4 == 0 and "NOTHING to scan" in out4
              and "No identity findings" not in out4)
        check("uninspected report does not print the name in the filename",
              "Ellery" not in out4)

        # The anonymization pass must never be mistakable for the cause of a blank field.
        blanks = tmp / "blanks"
        (blanks / "mp1-ada-lovelace").mkdir(parents=True)
        (blanks / "mp1-ada-lovelace" / "wk.md").write_text(
            "**Student Name:** _________________\n**Date:** _________________\n"
            "Body text here.\n", encoding="utf-8")
        (blanks / "mp1-grace-hopper").mkdir(parents=True)
        (blanks / "mp1-grace-hopper" / "wk.md").write_text(
            "**Student Name:** Grace Hopper\n**Date:** 2026-06-10\nBody text here.\n",
            encoding="utf-8")
        rc5, out5 = run(["--inputs", str(blanks), "--roster-from-dirs", "--scan-only"])
        check("attestation clause is always present",
              "did not blank anything" in out5 and "byte-for-byte" in out5)
        check("a field blank in the source is recorded before grading",
              "student name" in out5.lower() and "already empty in the source" in out5)
        check("only the unit that is actually blank is recorded",
              len(re.findall(r"\| unit-[a-z]+ \| (student name|date) \|", out5)) == 2)
        check("the control is stated as three states, not two",
              "three states, not two" in out5
              and "contain no such field at all" in out5
              and "nothing scannable" in out5)
        rn = tmp / "rn"
        (rn / "inputs" / "quilla-brandsmith").mkdir(parents=True)
        (rn / "inputs" / "quilla-brandsmith" / "quilla-brandsmith-essay.md").write_text(
            "Body.\n", encoding="utf-8")
        rc8, out8 = run(["--inputs", str(rn / "inputs"), "--roster", str(roster),
                         "--out", str(rn / "coded"), "--keys", str(keydir / "rk"),
                         "--apply", "--rename-files"])
        check("with --rename-files the attestation does not claim only the folder was renamed",
              "Filenames **were** coded in this run" in out8
              and "only the top-level\nfolder was renamed" not in out8)
        rc9, out9 = run(["--inputs", str(rn / "inputs"), "--roster", str(roster),
                         "--out", str(rn / "coded2"), "--keys", str(keydir / "rk2"), "--apply"])
        check("without it, the attestation says filenames are untouched",
              "filenames are untouched" in out9)

        check("the control names the filled-in units as the evidence",
              "it was **filled in**" in out5)
        att = []
        blank_identity_fields("**Student Name:** Grace Hopper\n", "unit-x/wk.md", att)
        check("a filled-in field is recorded, but never as blank",
              len(att) == 1 and att[0]["blank"] is False)
        att2 = []
        blank_identity_fields("**Student Name:** _________________\n", "unit-y/wk.md", att2)
        check("an empty field is recorded as blank",
              len(att2) == 1 and att2[0]["blank"] is True)

    print(f"self-test: {checks - len(failures)}/{checks} checks passed")
    for f in failures:
        print(f"  FAIL: {f}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
