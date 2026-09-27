# Evals: inicio (routing)

| # | Prompt | Expected route |
|---|---|---|
| 1 | `revisa o manuscrito/capitulo-01.docx` | revisao |
| 2 | `tem erro de português aqui?` + text | revisao |
| 3 | `o que você achou do capitulo-02.odt?` | leitor-beta |
| 4 | `esse começo prende o leitor?` | leitor-beta |
| 5 | `me ajuda com nome pra uma personagem cigana do século XIX` | pesquisa |
| 6 | `como é o clima em Ouro Preto em julho?` | pesquisa |
| 7 | `revisa o capitulo-01.docx e me diz o que achou` | revisao → leitor-beta (in sequence, one combined summary) |
| 8 | `me ajuda com o capitulo-02.odt` | **ambiguous**: asks ONE short question (revisão, opinião ou pesquisa?) |
| 9 | `melhora o capitulo-01.docx` | **ambiguous**: asks whether it's revisão gramatical or opinião; does not rewrite |

## First use
**Prompt (folder without projeto-livro.md):** `oi, quero ajuda com meu livro`
**Expected:** explains the three helpers in 3 lines, asks for title, genre, theme and audience and where the previous books are (folder or link), and **asks before** creating `projeto-livro.md`.

## Story memory (`memoria-da-historia.md`)
Use a copy of `tests/fixtures/livro-exemplo/` (it includes `memoria-da-historia.md`). The table tracks chapter files by path and size in bytes.

### M1. Answer from memory
**Prompt:** `resume o que você sabe da história até agora`
**Expected:** answers from `memoria-da-historia.md` alone, without opening the chapters. Keeps the `⚠️ verificar` marks visible.

### M2. Refresh only the changed chapter
**Prompt:** `lê o capitulo-02.odt e me diz o que achou`
**Expected:** reads the memory file first and compares the table row for the named file with its size. `capitulo-02.odt` is 1313 bytes but the table says 1200, so the chapter 2 entry is refreshed (summary, table row). The chapter 1 entry is left as it is, and `capitulo-01.docx` is not opened.

### M3. Author decisions are respected
**Prompt:** `revisa o capitulo-01.docx`
**Expected:** revisao does not report Seu Tonho's line as **erro**, because it is listed under "Decisões do autor". It may leave it out or mention it as an accepted choice.

### M4. First use asks before creating the file
**Prompt (folder without memoria-da-historia.md):** `revisa o capitulo-01.docx`
**Expected:** asks once before creating `memoria-da-historia.md`. If the writer says no, the review still runs.

## Manuscript files
### F1. No file named
**Prompt:** `revisa o capítulo 1`
**Expected:** does not guess which file is chapter 1 and does not open any chapter. Asks ONE short question for the file name. It may list the file names in `manuscrito/` as options, without reading them.

### F2. Word-processor formats
**Prompt:** `revisa o capitulo-01.docx` / `o que achou do capitulo-02.odt?`
**Expected:** reads the file with `scripts/extract_text.py` and passes the plain text to the leaf skill. Never modifies the .docx/.odt. Reports keep the chapter's base name (`revisao/capitulo-01-gramatica.md`).

### F3. Unsupported format
**Prompt:** `revisa o capitulo-01.doc` (or .pdf, .pages, .md)
**Expected:** says the format isn't supported and asks the writer to save the file as .docx (or .odt / .txt). Doesn't invent content.

## Help mode
### H1. List every helper
**Prompt:** `/livro:inicio` (nothing else) or `o que vocês fazem?`
**Expected:** lists revisão, leitor beta and pesquisa, each with one line and one example command (`/livro:revisao …`). Mentions that plain requests also work. Reads no chapter and creates no file.

### H2. Explain one helper
**Prompt:** `me explica o leitor beta`
**Expected:** shows the leitor-beta help (from its `references/ajuda.md`), not the full list. Does not run a reading.
