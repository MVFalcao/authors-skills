# Evals: book-orchestrator (routing)

| # | Prompt | Expected route |
|---|---|---|
| 1 | `revisa o capítulo 1` | grammar-review |
| 2 | `tem erro de português aqui?` + text | grammar-review |
| 3 | `o que você achou do capítulo 2?` | beta-reader |
| 4 | `esse começo prende o leitor?` | beta-reader |
| 5 | `me ajuda com nome pra uma personagem cigana do século XIX` | writer-research |
| 6 | `como é o clima em Ouro Preto em julho?` | writer-research |
| 7 | `revisa o capítulo 1 e me diz o que achou` | grammar-review → beta-reader (in sequence, one combined summary) |
| 8 | `me ajuda com o capítulo 2` | **ambiguous**: asks ONE short question (revisão, opinião ou pesquisa?) |
| 9 | `melhora o capítulo` | **ambiguous**: asks whether it's revisão gramatical or opinião; does not rewrite |

## First use
**Prompt (folder without projeto-livro.md):** `oi, quero ajuda com meu livro`
**Expected:** explains the three helpers in 3 lines, asks for title, genre, theme and audience and where the previous books are (folder or link), and **asks before** creating `projeto-livro.md`.

## Story memory (`memoria-da-historia.md`)
Use a copy of `tests/fixtures/livro-exemplo/` (it includes `memoria-da-historia.md`).

### M1. Answer from memory
**Prompt:** `resume o que você sabe da história até agora`
**Expected:** answers from `memoria-da-historia.md` alone, without opening the chapters. Keeps the `⚠️ verificar` marks visible.

### M2. Refresh only the changed chapter
**Prompt:** `revisa o capítulo 1`
**Expected:** reads the memory file first and compares the control table with the chapter files. `capitulo-02.md` is 1075 bytes but the table says 940, so only the chapter 2 entry is refreshed (summary, table row). The chapter 1 entry is left as it is.

### M3. Author decisions are respected
**Prompt:** `revisa o capítulo 1`
**Expected:** grammar-review does not report Seu Tonho's line as **erro**, because it is listed under "Decisões do autor". It may leave it out or mention it as an accepted choice.

### M4. First use asks before creating the file
**Prompt (folder without memoria-da-historia.md):** `revisa o capítulo 1`
**Expected:** asks once before creating `memoria-da-historia.md`. If the writer says no, the review still runs.
