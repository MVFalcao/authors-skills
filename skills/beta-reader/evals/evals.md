# Evals: beta-reader

## 1. Opinion using theme and previous book
**Prompt:** `lê o capítulo 2 como leitor beta e me diz o que achou`
**Expected:**
- Reads `projeto-livro.md` (theme: memória, perda, mar) and `livros-anteriores/o-farol-conto.md`.
- Creates `revisao/capitulo-02-leitura-beta.md` with: primeira impressão, pontos fortes, preocupações ranked by impact, perguntas do leitor.
- Quotes specific lines from the chapter (e.g. "Zefa, se eu demorar, não fica na janela.").
- Compares with *O Farol*: a similar motif (someone watching the sea, grief), consistent voice, and whether the new book repeats or grows.

## 2. Persona
**Prompt:** `lê o capítulo 1 como um leitor crítico`
**Expected:** a more demanding tone. Points out the rushed pacing and the "barco" repetition as a reading problem. Grammar errors are only mentioned, with a suggestion to run grammar-review.

## 3. Missing context
**Prompt (in a folder without projeto-livro.md):** `o que você acha desse capítulo?` + pasted text
**Expected:** asks for genre, theme and audience (one short question) or states the assumptions it made.

## 4. Previous books from a link
**Prompt:** `compara com meu livro anterior: <link>`
**Expected:** uses WebFetch/WebSearch on the link. If the fetch fails it says so and doesn't invent content from the earlier book.
