---
name: qa-review
description: >-
  QA review of code and skills in this repo using the Octopus multi-model review
  (/octo:review) plus this project's own skill checklist. Use when asked to
  review, QA, check or audit changes, a skill folder, a script or a PR ("review
  this", "QA the new skill", "is this ready?", "check my changes"), and at the
  end of the develop skill. It reports findings and does not fix them unless the
  user asks.
---

# QA Review (via Octopus)

Two passes: the Octopus multi-model code review, then the checks specific to
this project. Report findings. Don't edit files unless the user asks for fixes.

`OCTO="$HOME/.claude-octopus/plugin"`

## 1. Decide what to review

Pick the target from the request: a skill folder (`skills/<name>/`), specific
files, the current git diff, or a PR number. If it isn't clear, review what
changed most recently and say which files you chose.

## 2. Project checklist (run first, it's quick)

For each skill in scope:

```bash
for d in skills/*/; do
  f="$d/SKILL.md"; n=$(basename "$d")
  [ -f "$f" ] || { echo "FAIL $n: no SKILL.md"; continue; }
  head -1 "$f" | grep -q '^---$' || echo "FAIL $n: no frontmatter"
  grep -q "^name: $n\$" "$f" || echo "FAIL $n: name != folder"
  grep -q '^description:' "$f" || echo "FAIL $n: no description"
  echo "INFO $n: $(wc -l < "$f") lines"
done
```

Then check by reading:

- **Description:** it says what the skill does *and* when to trigger it, with
  concrete phrases, and doesn't overlap with another skill.
- **Body:** imperative instructions, a clear workflow and output format, under
  ~500 lines, and long material moved to `references/`.
- **Scripts:** each one runs (`python3 scripts/x.py --help` or a sample input),
  exits non-zero on failure, and has no network calls, secrets or absolute paths
  (`grep -nE 'requests|urllib|curl|wget|http|/home/|API_KEY' scripts/*`).
- **Author content:** keeps the author's voice, marks unverified facts and
  quotes, and contains no real manuscripts or long copyrighted excerpts.
- **Index:** `README.md` lists the skill.

## 3. Octopus multi-model review

```bash
test -x "$OCTO/scripts/orchestrate.sh" && echo "octo:ok" || echo "octo:missing"
```

Write the review prompt with the `prompt-master` skill first (target: review agents; name the target files, what to check, and the output format). Then, if Octopus is available, read `$OCTO/commands/review.md` and follow it for the
target from step 1. It runs `orchestrate.sh code-review` across the available
providers. Don't call `/octo:review` with the Skill tool; follow the file.
If it's missing, say so, give only the checklist results and suggest
`/octo:setup`.

## 4. Report

Merge both passes, remove duplicates, and rank by severity:

```
## QA verdict: PASS | PASS WITH NOTES | FAIL

### Blocking
- `path:line` — problem → failure scenario → suggested fix

### Should fix
- …

### Nits
- …

### Checked
- checklist: <n> skills, <n> scripts run
- Octopus providers: <from its agent summary>, or "not run: <reason>"
```

Include only findings you can point to in the code. Mark anything uncertain as
"unverified" rather than leaving it out or overstating it.
