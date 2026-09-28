# Evals: design-editorial

Run in a copy of `tests/fixtures/livro-exemplo/` with the skills installed and
an empty `design/` folder.

## 1. Projeto gráfico
**Prompt:** `monta o projeto gráfico do livro impresso: romance de 60 mil palavras em 20 capítulos`
**Expected:**
- Creates `design/projeto-grafico.md` with format, margins, mancha, typography table, hierarchy, pre/post-text pages and a page estimate.
- Reads `projeto-livro.md` (literary fiction, adult readers) and justifies the format and font from it.
- Numbers come from `scripts/calc_producao.py` (`mancha`, `paginas`) with the inputs shown; defaults listed under `Premissas`.
- Suggests at least one free (OFL) text font; commercial fonts marked `⚠️ verificar licença`.
- Does not open any chapter file.

## 2. Pages and spine
**Prompt:** `quantas páginas e qual a lombada se o livro tem 60 mil palavras, em 14x21 e pólen 80?`
**Expected:** a `cálculo` answer in chat (no file): page estimate from `paginas`, spine from `lombada`. The paper thickness is not given, so a typical value is used and marked `⚠️ verificar com a gráfica`, with a note that the cover waits for the shop's spine.

## 3. Print production
**Prompt:** `vou imprimir 300 exemplares, o que peço para a gráfica?`
**Expected:** `design/producao-grafica.md` with the technical spec table, files for the print shop, the quote checklist and the proof checklist. No prices, delivery times or named shops invented. Mentions digital vs offset for a 300-copy run as something to quote both ways.

## 4. Ebook
**Prompt:** `como deve ser a diagramação do ebook?`
**Expected:** `design/diagramacao-ebook.md`: EPUB 3 reflowable (the book is prose), structure, styles in em, lang pt-BR, alt text, EPUBCheck. Store-specific limits marked `⚠️ verificar`.

## 5. Word count from named files
**Prompt:** `conta as palavras de manuscrito/capitulo-01.docx e manuscrito/capitulo-02.odt e estima as páginas do livro com 20 capítulos desse tamanho`
**Expected:** runs `calc_producao.py palavras` on exactly those two files, uses the total (and the writer's scaling) for `paginas`, and does not quote or summarise the chapters.

## 6. Missing essential input
**Prompt:** `qual papel eu uso?`
**Expected:** asks one short question (for example printed vs ebook, or images/colour) or states the assumptions from `rules.md` under `Premissas`. Never more than one question.

## 7. Not this skill
**Prompt:** `o primeiro capítulo prende o leitor?` → leitor-beta.
**Prompt:** `revisa a pontuação do capitulo-01.docx` → revisao.
**Prompt:** `desenha a capa do livro` → says it doesn't create cover art; may offer the cover's technical spec (open size, bleed, spine).

## H1. Help with no arguments
**Prompt:** `/livro:design-editorial` (nothing else)
**Expected:** help mode in PT-BR from `references/ajuda.md`: what it does, the four modes, 3–4 example requests, the `⚠️ verificar com a gráfica` convention, and that specs go to `design/`. Reads no chapter and creates no file.
