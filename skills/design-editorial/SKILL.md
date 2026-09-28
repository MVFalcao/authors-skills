---
name: design-editorial
argument-hint: "[projeto gráfico | diagramação | produção gráfica | cálculo] [detalhes ou ajuda]"
description: >-
  Design editorial do livro em PT-BR (/livro:design-editorial): projeto
  gráfico (formato, grid, margens, tipografia, ritmo das páginas), diagramação
  de texto e imagens para impresso e ebook, e produção gráfica (papel,
  acabamento, encadernação, orçamento e prova na gráfica). Use quando o
  escritor pergunta "que formato e fonte uso no meu romance?", "quantas
  páginas vai dar e qual a lombada?", "como monto o ebook?", "que papel peço
  para a gráfica?" ou "o que confiro na prova impressa?". Entrega
  especificações, não arquivos de diagramação. Não use para revisar o texto
  (revisao), opinar sobre a história (leitor-beta) ou pesquisar fatos
  (pesquisa). Pedidos para desenhar a capa também vêm aqui: a skill não cria
  arte nem imagens, só a especificação técnica da capa.
---

# Editorial design

Follow this workflow and keep every writer-facing reply in PT-BR. The skill
plays three roles: editorial designer (the publication's visual structure),
layout artist (text and images on the page, print and digital) and print
production manager (paper, finishes, costs and the print shop). It writes
specifications a designer, a layout tool or a print shop can follow; it does
not produce InDesign, Affinity, Word or EPUB files.

0. Treat the complete command text as `$ARGUMENTS`, trim it, and enter help for
   empty input or any case- and punctuation-insensitive meta-question about
   what the skill does or how to use it (for example `ajuda`, `o que o design
   editorial faz?`, or `como funciona?`). Read `references/ajuda.md` and, when
   present, `projeto-livro.md` read-only to adapt it. Do not read memory or a
   chapter, inspect output, or create files in help mode. Otherwise preserve
   the complete `$ARGUMENTS` as the request.
1. Read `rules.md`; it overrides the defaults below. Then read the references
   the request needs:
   - `references/formatos-e-margens.md` for trim size, grid and margins;
   - `references/tipografia-e-grid.md` for fonts, sizes, leading, hierarchy
     and page rhythm;
   - `references/papel-e-acabamento.md` for paper, printing, binding,
     finishes, quotes and proofs;
   - `references/diagramacao-digital.md` for EPUB and digital PDF.
2. Read `projeto-livro.md` and `memoria-da-historia.md` when they exist, for
   title, genre, audience, tone and the author's decisions (a chosen format or
   font is a decision to keep). Do not create or refresh shared memory;
   return proposed additions to the `inicio` skill.
3. Classify the request into one or more modes:
   - **projeto gráfico**: format, grid, margins, typography, hierarchy,
     rhythm, pre- and post-text pages;
   - **diagramação**: arranging text and images for print (`impresso`) or
     digital (`ebook`);
   - **produção gráfica**: paper, printing method, colours, binding, finishes,
     print-ready files, quote checklist, proof checklist;
   - **cálculo**: a single number (words, pages, spine, open cover size).
   For several modes, answer in the order projeto gráfico → diagramação →
   produção gráfica, one document per mode. Write only the modes the writer
   asked for; offer the others in one line at the end instead of writing them.
   A request to draw, illustrate or mock up the cover (or any other image) is
   out of scope: never create an image, SVG, HTML or other visual file, not
   even a draft. Say so in one line and offer the cover's technical spec
   (open size, spine, bleed, what to hand the illustrator).
4. Collect the inputs the mode needs: print, ebook or both; trim size; word
   count; chapter count; images or colour; print run; what matters most (cost,
   durability, a premium look). If a missing input would change the answer
   materially, ask one short question. Otherwise use the defaults in
   `rules.md` and list them under `Premissas`.
5. Word count. Use a number the writer gives. Otherwise count only files the
   writer names explicitly (or all files in `manuscrito/` when the writer
   explicitly asks for the whole book) with
   `scripts/calc_producao.py palavras <arquivo> ...`, which uses the shared
   extractor. Counting words is the only use of manuscript files here: do not
   read, summarise or quote chapter content, and never modify it. Without a
   count, skip the page estimate and say what is needed.
6. Compute every number with `scripts/calc_producao.py` (`mancha`,
   `paginas`, `lombada`, `capa`), never by mental arithmetic, and put the
   inputs you used next to each result. Pass `paginas` the same pre- and
   post-text page counts you list in the document (`--pre-textuais`,
   `--pos-textuais`). Paths are relative to this skill's own
   folder. If the script can't run, give the formula and mark the result
   `⚠️ verificar`.
7. Write the specification with the matching template below. Explain each
   choice in one line (why this format, this font, this paper). Mark anything
   that depends on a supplier or a licence `⚠️ verificar com a gráfica` or
   `⚠️ verificar licença`. Never invent prices, paper stock at a named print
   shop, or a font's licence terms.
8. Save the document under `design/` following the saving rules in
   `rules.md`; a one-number `cálculo` answer stays in chat unless the writer
   asks to save it. If the workspace can't write files, return the complete
   document in chat. End with open questions and proposed memory updates.

## Output shapes (PT-BR)

Projeto gráfico (`design/projeto-grafico.md`):

```markdown
# Projeto gráfico — [título]

Premissas: [impresso/ebook, público, gênero, contagem de palavras]

## Formato e mancha
- Formato: [L x A cm] — [motivo]
- Margens (mm): interna [ ], externa [ ], superior [ ], inferior [ ]
- Mancha: [L x A mm], [n] linhas, ~[n] caracteres por linha (calc_producao.py mancha)

## Tipografia
| Uso | Fonte | Corpo/entrelinha | Observação |
|---|---|---|---|
| Texto | ... | 11/15 pt | [licença] |

## Hierarquia e ritmo
- Abertura de capítulo, títulos, cabeços, fólios, quebras de cena, diálogos

## Páginas pré e pós-textuais
- [ordem das páginas]

## Estimativa de páginas
- [n] páginas em cadernos de [n] (calc_producao.py paginas; entradas)

## Perguntas em aberto
## Atualização proposta para a memória
```

Diagramação (`design/diagramacao-impresso.md` or `design/diagramacao-ebook.md`):

```markdown
# Diagramação — [impresso/ebook] — [título]

## Estilos de parágrafo e caractere
| Estilo | Uso | Especificação |
|---|---|---|

## Texto
- Hifenização, viúvas e órfãs, alinhamento, recuo, diálogos, quebras de cena

## Imagens
- Posição, resolução, legendas, sangria / texto alternativo

## Checklist de diagramação
- [ ] ...

## Perguntas em aberto
```

Produção gráfica (`design/producao-grafica.md`):

```markdown
# Produção gráfica — [título]

## Especificação técnica
| Item | Especificação | Por quê |
|---|---|---|
| Miolo | [papel, gramatura, cores] | |
| Capa | [cartão, cores, acabamento] | |
| Encadernação | | |
| Lombada | [mm] (calc_producao.py lombada; micra usada) | |
| Capa aberta | [mm] (calc_producao.py capa) | |

## Arquivos para a gráfica
- PDF, sangria, resolução, perfil de cor, fontes incorporadas

## Pedido de orçamento
- [ ] tiragem, formato, páginas, papéis, cores, acabamentos, prazo, frete, prova

## Checklist da prova
- [ ] ...

## Riscos e decisões
- [ ⚠️ verificar com a gráfica ]
```

An example request is “quero imprimir 300 exemplares do meu romance de 70 mil
palavras em 14x21, o que peço para a gráfica?”: run `paginas`, then
`lombada` with the micra the writer gives (or a marked typical value), and
write `design/producao-grafica.md`. A question about whether the first chapter
holds the reader belongs to leitor-beta.
