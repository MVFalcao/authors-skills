# Rules: grammar-review

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
- Don't comment on plot, pacing or characters. That's beta-reader's job.
- Review at most one chapter per pass. Split chapters longer than ~5,000 words into parts.
