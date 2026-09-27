# Evals: grammar-review

Run in a copy of `tests/fixtures/livro-exemplo/` with the skills installed.

## 1. Review a chapter file
**Prompt:** `revisa a gramática do capítulo 1`
**Expected:**
- Creates `revisao/capitulo-01-gramatica.md` with an issues table (trecho, problema, sugestão, gravidade).
- Finds all 7 errors in `tests/fixtures/gabarito-capitulo-01.md`.
- Flags "Nóis vai pescar amanhã" as **possível escolha de estilo**, not as an error.
- Does NOT rewrite the chapter file.

## 2. Pasted excerpt
**Prompt:** `corrige esse trecho: "Fazem dois anos que ela se mudou pra Recife, a onde mora a irmã."`
**Expected:** flags "Fazem" → "Faz" (impessoal) and "a onde" → "onde". "pra" in narration is flagged as informal register (atenção), not an error.

## 3. Corrected version on request
**Prompt:** `revisa o capítulo 1 e me dá a versão corrigida`
**Expected:** the table as in eval 1, plus a corrected version saved separately (`revisao/capitulo-01-corrigido.md`). The dialect line is unchanged. The original is untouched.

## 4. Not this skill
**Prompt:** `o capítulo 2 prende a atenção?`
**Expected:** this skill does NOT trigger. It's a beta-reader request.
