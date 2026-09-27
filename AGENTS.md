# AGENTS.md

Rules for any AI agent (Claude Code, Codex, Cursor, and others) working in this repository.

## What this project is

`authors-skills` is a collection of **Claude Agent Skills** for authors and writers.
Each skill is a self-contained folder that Claude loads when a task matches the skill's description.

## Repository layout

```
authors-skills/
├── AGENTS.md              # this file
├── CLAUDE.md              # imports AGENTS.md for Claude Code
├── README.md              # human-facing overview and skill index
├── .claude/skills/        # workflow skills for working ON this repo (not shipped)
│   ├── develop/           # build/change code via /octo:develop
│   ├── qa-review/         # QA via /octo:review + project checklist
│   └── search/            # research via Octopus + Perplexity
└── skills/
    └── <skill-name>/
        ├── SKILL.md       # required: frontmatter + instructions
        ├── references/    # optional: longer docs loaded on demand
        ├── scripts/       # optional: deterministic helpers the skill runs
        ├── assets/        # optional: templates and files used in output
        └── evals/         # optional: test prompts and expected behavior
```

- One skill per folder under `skills/`. Never put two skills in one folder.
- Folder names are `kebab-case` and match the `name` in the frontmatter.

## Writing a skill

### Frontmatter (required)

```yaml
---
name: manuscript-editor          # kebab-case, same as the folder name
description: >-
  What the skill does and when to use it. Name the trigger phrases and
  situations ("edit my chapter", "tighten this prose", a .docx manuscript).
---
```

- `description` is the only thing Claude sees before loading the skill, so it decides whether the skill triggers.
  State **what** the skill does **and when** to use it, with concrete trigger words. Also say when **not** to use it if it could be confused with another skill.
- Keep the description under ~1024 characters.

### SKILL.md body

- Write instructions for Claude, in the imperative ("Read the chapter, then…"), not marketing copy.
- Keep `SKILL.md` short (aim for under ~500 lines). Move long reference material into `references/` and tell Claude when to read each file.
- Explain **why** a rule exists when it isn't obvious. That works better than ALL-CAPS commands.
- Give a clear workflow (numbered steps), the expected output format, and one or two short examples.
- Refer to bundled files with relative paths (`references/style-guide.md`, `scripts/word_count.py`).

### Scripts

- Use scripts for deterministic, repeatable work (counting, formatting, file conversion). Leave judgement and writing to the model.
- Python 3 or POSIX shell. Standard library only unless the dependency is unavoidable; if it is, document it in the SKILL.md.
- Scripts must be non-interactive, print useful errors, and exit non-zero on failure.
- No network calls, hard-coded absolute paths, or secrets.

## Content rules for an authors' toolkit

- Respect the author's voice. Skills that edit prose must preserve style, dialect, and intentional rule-breaking unless asked otherwise, and should show or summarise what changed.
- Never present generated text as the author's own verified facts, quotes, reviews, or citations. Mark anything invented or unverified.
- Don't reproduce copyrighted text beyond short quotes. Sample manuscripts in `assets/` or `evals/` must be original or public domain.
- Keep manuscripts and personal data out of the repo. Use small, made-up samples for tests.

## Working rules for agents

0. **Use Octopus (`octo`) for search and heavy code work.** This is the first rule and it comes before all the others. Hand these tasks to the Claude Octopus plugin instead of doing them by hand:
   - **Search, research and exploring the codebase** → `/octo:discover`
   - **Implementing a skill, scripts, or multi-file changes** → `/octo:develop`
   - **Tests / TDD** → `/octo:tdd`
   - **Debugging failures** → `/octo:debug`
   - **Reviewing changes** → `/octo:review`
   - **Security checks on scripts** → `/octo:security`
   - **Comparing approaches or making design decisions** → `/octo:debate`

   In Claude Code, use the project skills that wrap these commands: **`develop`**, **`qa-review`** and **`search`** (in `.claude/skills/`).
   Small edits (a typo, one line in a `SKILL.md`, a frontmatter tweak) can be done directly. If Octopus isn't installed (for example in a non-Claude agent), say so and use that agent's equivalent tools.
   **Octopus prompt size:** keep the prompt short. Put the details in a committed brief (`PLAN.md`) and point to it with `plan:PLAN.md`.
1. **Write prompts with `prompt-master`.** Use the user-level skill `prompt-master` (`~/.claude/skills/prompt-master`) in two places:
   - **Every Octopus prompt** (develop, review, research, discover): run it through `prompt-master` with the target set to the Octopus workflow's agents (Claude Code / Codex). Use Template M, kept short: objective, pointer to `PLAN.md`, scope (files to touch and files not to touch), "done when" checks and stop conditions. Save the final prompt in `PLAN.md` or the run log so it can be reused.
   - **The user's requests:** for any non-trivial request, rewrite it into a precise task (objective, scope, done when) and **show it to the user before starting**. Start after they confirm or adjust it. Skip this for small, clear requests (a typo, a question, a one-line change).
2. **Use `caveman` for code tasks.** For all coding work in this repo (implementing, debugging, reviewing, running Octopus, tests, git), turn on the user-level skill `caveman` (`~/.claude/skills/caveman`, level **full**) for replies in the chat.
   - **Stays in normal prose** (the skill's own boundary): code, comments, commit messages, docs, `SKILL.md` / `rules.md` / `README.md` content, prompts sent to Octopus or other agents, and memory files.
   - **Never caveman:** anything a writer sees, meaning all skill output and PT-BR text. The writer skills must stay clear, full PT-BR.
   - **Switch back to normal prose** for security warnings, irreversible actions, plans shown for approval, and whenever the user asks a question about the plan or is confused. Turn it off with "stop caveman" / "normal mode".
3. **Read before writing.** Read the relevant `SKILL.md` and neighbouring skills before changing or adding one, and match their structure and tone.
4. **Stay in scope.** Change only what the task asks for. Don't rename, reorganise, or "improve" unrelated skills.
5. **One skill per change.** Keep commits and PRs focused on a single skill where possible.
6. **Test it.** After creating or editing a skill:
   - check that the frontmatter parses and `name` matches the folder;
   - run every script you touched at least once;
   - try the skill on 2–3 realistic prompts (store them in `evals/` if they're useful again) and check that it triggers and gives the expected output.
7. **Update the index.** When you add, rename, or remove a skill, update the table in `README.md`.
8. **Report honestly.** Say what you tested and what you didn't. If something failed, show the output.
9. **Ask when it's unclear.** If a request could mean two different skills or behaviours, ask before building.
10. **Git.** Don't commit or push unless asked. Use short imperative commit messages scoped to the skill, e.g. `manuscript-editor: add dialogue checks`.

## Definition of done

- [ ] `skills/<name>/SKILL.md` exists with valid `name` and `description` frontmatter
- [ ] Description says what the skill does and when to trigger it
- [ ] Long material lives in `references/`, not in `SKILL.md`
- [ ] Scripts run cleanly and have no network calls or secrets
- [ ] Tested on realistic prompts
- [ ] `README.md` index updated
