---
name: develop
description: >-
  Build or change code in this repo through the Octopus (octo) develop workflow.
  Use when asked to implement, build, create or refactor something: a new author
  skill under skills/, a helper script, or any multi-file change ("create a skill
  for…", "implement…", "add a script that…", "refactor…"). Not for one-line fixes
  or typos (edit those directly), not for reviews (use qa-review) and not for
  research (use search).
---

# Develop (via Octopus)

This project's first rule (see `AGENTS.md`, rule 0) is that heavy code work goes
through Octopus. This skill wraps `/octo:develop` and adds the project's own
checks before and after it.

Octopus lives at `~/.claude-octopus/plugin` (a stable symlink to the installed
version). Call it as `$OCTO` below.

## Workflow

1. **Scope the task.** Restate in one or two sentences what will be built and
   which files it touches. If the request could mean two different things, ask
   before starting.
2. **Gather context.** Read `AGENTS.md` and one or two existing skills under
   `skills/` that are similar, so the new work matches their structure and tone.
   For a wide codebase search, use the `search` skill instead of reading file by
   file.
3. **Check Octopus is available.**
   ```bash
   OCTO="$HOME/.claude-octopus/plugin"
   test -x "$OCTO/scripts/orchestrate.sh" && echo "octo:ok" || echo "octo:missing"
   ```
   If it reports `octo:missing`, stop and tell the user to install or repair the
   plugin (`/octo:setup`). Don't quietly fall back to building it by hand.
4. **Write the prompt with `prompt-master`.** Invoke the `prompt-master` skill (target: Claude Code / Codex agents, Template M) to turn the task into a short prompt: objective, `plan:PLAN.md` pointer, scope (files to touch and not touch), "done when" checks, stop conditions. Put the details in `PLAN.md`, not in the prompt.
5. **Run the develop workflow.** Read `$OCTO/commands/develop.md` and follow it
   exactly. It runs `orchestrate.sh develop` through Bash with its quality gates.
   Pass only the short prompt from step 4. The project constraints live in
   `PLAN.md`, which the prompt points to. Make sure it covers:
   - the target path (e.g. `skills/<name>/`)
   - the SKILL.md frontmatter rules (`name` matches the folder; `description`
     says what and when)
   - scripts: Python 3 or POSIX shell, standard library only, non-interactive,
     no network calls, no secrets, no absolute paths
   - keep `SKILL.md` under ~500 lines and move long material into `references/`
   Don't invoke `/octo:develop` with the Skill tool. It's a user-only command,
   so read the file and follow it as the command says.
6. **Verify.** When Octopus finishes, check its output against the project's
   "Definition of done" in `AGENTS.md`:
   - frontmatter parses and `name` matches the folder
   - every script that was added or changed runs once without errors
   - `README.md` skill index updated if a skill was added, renamed or removed
7. **Hand off to QA.** For anything more than a small change, finish by running
   the `qa-review` skill on the changed files.

## Report back

Finish with a short summary:
- what was built, with the files listed as `path:line` links
- which providers Octopus used (copy its agent summary table if it printed one)
- what you ran to verify it, and the result
- anything left undone or any provider that failed
