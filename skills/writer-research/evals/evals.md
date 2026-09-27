# Evals: writer-research

## 1. Names for a place and era
**Prompt:** `preciso de nomes para moradores de uma vila de pescadores no litoral da Bahia nos anos 1950`
**Expected:** creates `pesquisa/nomes-*.md` with several options (first names + nicknames), each with origin/meaning and why it fits the era and region. No anachronistic names.

## 2. Real place
**Prompt:** `pesquisa como era Itapuã, em Salvador, nos anos 1950: clima, cotidiano, cheiros, sons`
**Expected:** a `pesquisa/lugar-*.md` note with sections (geografia, clima, cotidiano, detalhes sensoriais, história) and a **Fontes** list with links. Uncertain facts are marked `⚠️ verificar`.

## 3. No web access
**Prompt:** same as 2, with WebSearch/WebFetch unavailable
**Expected:** says there is no web access, gives knowledge-based notes, and marks everything `⚠️ verificar`. No fake links.

## 4. Invented name
**Prompt:** `cria um nome para uma cidade fictícia no sertão`
**Expected:** 5+ options with the technique used (tupi roots, saint's name, geographic feature…). Checks and notes whether a real town already has that name.

## H1. Help with no arguments
**Prompt:** `/livro:pesquisa` (nothing else)
**Expected:** help mode in PT-BR from `references/ajuda.md`: one line on what it does, the kinds of research (nomes, lugares, épocas, profissões, livros de referência), 3–4 example requests, the `⚠️ verificar` convention, and that notes go to `pesquisa/`. Reads no chapter and creates no file.

## H2. Help in plain language
**Prompt:** `o que dá pra pesquisar com você?`
**Expected:** the same help, short. Does not start a task.
