# Rules: inicio

> **Editable rules.** The skill reads this file first, and it overrides the defaults in SKILL.md.
> These are starting assumptions: add, change or delete rules freely. One rule per bullet.
> Remove a whole section if you do not want it.

## Start of every request
- Read `projeto-livro.md` and `memoria-da-historia.md` (if they exist) before anything else.
- Only open full chapters when the task needs them or they changed since the memory was updated.

## Manuscript files
- Read only the file the writer names. Never guess which file is "capítulo 1" and never scan chapters on your own. If no file is named, ask for it (you may list the file names in `manuscrito/` as neutral options, without opening them, but don't suggest or ask to confirm one).
- Supported formats: `.docx`, `.odt`, `.txt`. Read them with `scripts/extract_text.py`. For `.doc`, `.pdf`, `.pages`, `.rtf` or `.md`, ask the writer to save the chapter as `.docx`.
- Never modify the manuscript file.

## Routing
- Send the work to the right skill. **Never do the leaf skill's job itself.**
- Ambiguous request: ask **one** short question with the options (revisão, opinião, pesquisa). Never more than one question before acting.
- Combined requests run in this order: pesquisa → revisao → leitor-beta → design-editorial.
- "Melhora / reescreve o capítulo": don't rewrite. Offer revisão or opinião instead.

## Files
- Ask before creating files or folders in the book folder **the first time**. When `revisao/`, `pesquisa/` or `design/` already exists, the helpers save there without asking.
- Never modify the manuscript files.
- After each skill run, update `memoria-da-historia.md` (summaries only, never long passages).

## Replies
- Always reply in PT-BR.
- Final summary: at most 10 lines, with links to every report created.
