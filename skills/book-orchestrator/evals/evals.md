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
