# Rules: revisao

> **Editable rules.** The skill reads this file first, and it overrides the defaults in SKILL.md.
> These are starting assumptions: add, change or delete rules freely. One rule per bullet.
> Remove a whole section if you do not want it.

## Norm
- Follow the norma-padrão of Brazilian Portuguese and the Acordo Ortográfico (2009). Use the VOLP (Academia Brasileira de Letras) as the spelling reference.
- European Portuguese forms in narration ("facto", "estou a fazer") are **atenção**, not **erro**.

## What to flag
- Narration: full check (spelling, crase, concordância, regência, colocação pronominal, pontuação, tempos verbais, repetição).
- Dialogue: flag only clear typos and punctuation of the dialogue itself (travessão). Informal speech, slang and dialect are **possível escolha de estilo**.
- Colloquial forms in narration ("pra", "tá", "a gente"): **atenção**, never **erro**.
- Repetition: flag the same content word 3+ times within ~3 sentences.
- Don't flag choices the author has already approved (listed in `memoria-da-historia.md` → "decisões do autor").

## Severity
- **erro**: breaks the norma-padrão with no stylistic reason.
- **atenção**: correct but awkward, ambiguous, informal in narration, or repetitive.
- **possível escolha de estilo**: deviates from the norm but may be intentional (voice, dialect, rhythm).

## Limits
- Suggest the **smallest** change that fixes the problem. Never rewrite a sentence for style.
- Don't comment on plot, pacing or characters. That's leitor-beta's job.
- Review at most one chapter per pass. Split chapters longer than ~5,000 words into parts.

## Manuscript files
- Read only the file the writer names, or text they paste. If neither is given, ask for the file name. Never guess which file a chapter is.
- Supported formats: `.docx`, `.odt`, `.txt`, read with the `inicio` skill's `scripts/extract_text.py`. For other formats, ask the writer to save the chapter as `.docx`.

## Saving
- If `revisao/` already exists in the book folder, save the result there without asking, and give the file path in the reply.
- If `revisao/` doesn't exist, ask once before creating it. If the writer says no, return the result in the chat.
- Never overwrite an earlier result: if the file name is taken, add `-2`, `-3`, and so on.
