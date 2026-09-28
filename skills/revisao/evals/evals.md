# Evals: revisao

Run in a copy of `tests/fixtures/livro-exemplo/` with the skills installed.

## 1. Review a chapter file
**Prompt:** `revisa a gramática de manuscrito/capitulo-01.docx`
**Expected:**
- Creates `revisao/capitulo-01-gramatica.md` with an issues table (trecho, problema, sugestão, gravidade).
- Finds all 7 errors in `tests/fixtures/gabarito-capitulo-01.md`.
- Does NOT flag "Nóis vai pescar amanhã" as **erro**. Because `memoria-da-historia.md` lists it under "Decisões do autor", it may leave it out of the table and mention it as an accepted choice (see inicio eval M3). Without that entry it must be **possível escolha de estilo**.
- Reads the .docx through the text extractor. Does NOT rewrite or modify the .docx.

## 2. Pasted excerpt
**Prompt:** `corrige esse trecho: "Fazem dois anos que ela se mudou pra Recife, a onde mora a irmã."`
**Expected:** flags "Fazem" → "Faz" (impessoal) and "a onde" → "onde". "pra" in narration is flagged as informal register (atenção), not an error.

## 3. Corrected version on request
**Prompt:** `revisa manuscrito/capitulo-01.docx e me dá a versão corrigida`
**Expected:** the table as in eval 1, plus a corrected version saved separately (`revisao/capitulo-01-corrigido.md`). The dialect line is unchanged. The original is untouched.

## 4. Not this skill
**Prompt:** `o capitulo-02.odt prende a atenção?`
**Expected:** this skill does NOT trigger. It's a leitor-beta request.

## 5. No file named
**Prompt:** `revisa a gramática do capítulo 1` (called directly, no file named)
**Expected:** does not guess or open any chapter. Asks one short question for the file name. It may list the file names it sees in `manuscrito/` as options, without reading them.

## 6. Unsupported format
**Prompt:** `revisa manuscrito/capitulo-01.pdf`
**Expected:** says it can't read .pdf and asks the writer to save the chapter as .docx (or .odt / .txt). Does not invent the chapter's content.

## H1. Help with no arguments
**Prompt:** `/livro:revisao` (nothing else)
**Expected:** help mode in PT-BR from `references/ajuda.md`: one line on what it does, what it checks (crase, concordância, regência…), the three severities, 3–4 example requests (e.g. `/livro:revisao capitulo-01.docx`), that it never rewrites unless asked, and that reports go to `revisao/`. Reads no chapter and creates no file.

## H2. Help in plain language
**Prompt:** `como funciona a revisão?`
**Expected:** the same help, short. Does not start a task.
