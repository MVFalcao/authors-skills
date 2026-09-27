# Rules: book-orchestrator

> **Editable rules.** The skill reads this file first, and it overrides the defaults in SKILL.md.
> These are starting assumptions: add, change or delete rules freely. One rule per bullet.
> Remove a whole section if you do not want it.

## Start of every request
- Read `projeto-livro.md` and `memoria-da-historia.md` (if they exist) before anything else.
- Only open full chapters when the task needs them or they changed since the memory was updated.

## Routing
- Send the work to the right skill. **Never do the leaf skill's job itself.**
- Ambiguous request: ask **one** short question with the options (revisão, opinião, pesquisa). Never more than one question before acting.
- Combined requests run in this order: writer-research → grammar-review → beta-reader.
- "Melhora / reescreve o capítulo": don't rewrite. Offer revisão or opinião instead.

## Files
- Ask before creating files or folders in the book folder **the first time**. After that, write to `revisao/` and `pesquisa/` without asking again.
- Never modify the manuscript files.
- After each skill run, update `memoria-da-historia.md` (summaries only, never long passages).

## Replies
- Always reply in PT-BR.
- Final summary: at most 10 lines, with links to every report created.
