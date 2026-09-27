# Evals: beta-reader

## 1. Opinion using theme and previous book
**Prompt:** `lê o manuscrito/capitulo-02.odt como leitor beta e me diz o que achou`
**Expected:**
- Reads `projeto-livro.md` (theme: memória, perda, mar) and `livros-anteriores/o-farol-conto.txt`.
- Creates `revisao/capitulo-02-leitura-beta.md` with: primeira impressão, pontos fortes, preocupações ranked by impact, perguntas do leitor.
- Quotes specific lines from the chapter (e.g. "Zefa, se eu demorar, não fica na janela.").
- Compares with *O Farol*: a similar motif (someone watching the sea, grief), consistent voice, and whether the new book repeats or grows.

## 2. Persona crítico
**Prompt:** `lê o capitulo-01.docx como um leitor crítico` (persona **crítico**)
**Expected:** a more demanding tone. Points out the rushed pacing and the "barco" repetition as a reading problem. Grammar errors are only mentioned, with a suggestion to run grammar-review.

## 3. Missing context
**Prompt (in a folder without projeto-livro.md):** `o que você acha desse capítulo?` + pasted text
**Expected:** asks for genre, theme and audience (one short question) or states the assumptions it made.

## 4. Previous books from a link
**Prompt:** `compara com meu livro anterior: <link>`
**Expected:** uses WebFetch/WebSearch on the link. If the fetch fails it says so and doesn't invent content from the earlier book.

## 5. Personas side by side
**Prompt:** `lê o capitulo-02.odt e me mostra as três visões: gentil, neutra e crítica`
**Expected:**
- Three sections (gentil / neutro / crítico) that quote the same passages but differ clearly in tone.
- Each persona still lists at least 3 strengths and 3 concerns. The gentil one doesn't hide problems, and the crítico one doesn't insult the author.
- A final list, "onde as três concordam".

## 6. Default persona
**Prompt:** `o que você achou do capitulo-01.docx?` (no persona given)
**Expected:** uses **neutro** and says so in one line ("Leitura no modo neutro — posso fazer gentil ou crítica").

## 7. Harsh on request
**Prompt:** `pode ser bem duro com o capitulo-01.docx, sem filtro`
**Expected:** uses **crítico** and leads with the biggest problems (rushed pacing, the repeated "barco", the abrupt ending). No softening, and nothing personal about the author.

## 8. No file named
**Prompt:** `o que você achou do capítulo 2?` (no file named, no pasted text)
**Expected:** does not guess or open any chapter. Asks one short question for the file name.
