[Português](#ajudantes-de-escrita-para-o-seu-livro) · [English](#writing-helpers-for-your-book)

# Ajudantes de escrita para o seu livro

## 1. O que é

Este projeto reúne quatro ajudantes para escrever um livro em português: início,
revisão, leitor-beta e pesquisa. Eles leem o contexto da pasta do livro e o
arquivo que você indicar, quando necessário. Nunca alteram o arquivo do
manuscrito. Os relatórios e as notas só são salvos quando você autoriza.

## 2. Instalação

### Claude Code (recomendado)

Adicione o marketplace e instale o plugin:

```text
/plugin marketplace add MVFalcao/authors-skills
/plugin install livro@authors-skills
```

### Outras ferramentas

Na pasta deste repositório, instale em uma pasta de livro:

```sh
sh scripts/install.sh --target <alvo> <pasta-do-livro>
```

Para instalar no diretório global da ferramenta:

```sh
sh scripts/install.sh --target <alvo> --global
```

Os alvos são `claude`, `agents`, `codex`, `cursor`, `gemini`, `opencode`,
`copilot` e `all`. `all` instala para `claude` e `agents`. `copilot` funciona
somente em uma pasta de projeto, não com `--global`.

Se já houver uma cópia instalada, ela é guardada em uma pasta irmã chamada
`skills-backup/`. Use `--force` para substituir a cópia existente sem fazer
esse backup.

## 3. Comandos

| Comando | O que faz | Exemplo |
|---|---|---|
| `/livro:inicio` | Organiza o projeto, encaminha pedidos e reúne resultados. | `/livro:inicio prepare o projeto do meu romance e revise manuscrito/capitulo-um.docx` |
| `/livro:revisao` | Procura problemas de português, ortografia, gramática e pontuação. | `/livro:revisao manuscrito/capitulo-dois.txt confira a concordância` |
| `/livro:leitor-beta` | Avalia gancho, ritmo, personagens, diálogos, clareza e impacto como leitor. | `/livro:leitor-beta manuscrito/cena-da-estacao.odt crítico leitor casual` |
| `/livro:pesquisa` | Pesquisa nomes, lugares, épocas, profissões, detalhes técnicos e livros de referência. | `/livro:pesquisa sugira nomes para uma biblioteca fictícia de bairro` |

Quando você chama um comando sem tarefa, ele mostra a ajuda correspondente.
Também funcionam pedidos em linguagem natural, como “confira a pontuação da
cena” ou “me diga onde minha atenção caiu”.

Use `/livro:inicio` quando quiser combinar etapas; um pedido de uma coisa só
vai para o ajudante correspondente. A revisão cuida do português, o leitor-beta
da experiência de leitura e a pesquisa do contexto verificável.

## 4. Formatos do manuscrito

Informe exatamente um arquivo `.docx`, `.odt` ou `.txt`, ou cole o trecho no
pedido. Quando a ferramenta consegue executar o extrator compartilhado, os
ajudantes leem esses três formatos. Se essa capacidade não estiver disponível,
eles leem diretamente um `.txt`; para `.docx` ou `.odt`, peça um `.txt` ou
cole o texto. O ajudante lê somente o arquivo que você nomear; ele não escolhe
um capítulo nem vasculha a pasta `manuscrito/`. Se você não nomear um arquivo,
ele pergunta qual é.

Arquivos `.doc`, `.pdf`, `.pages`, `.rtf` e `.md` não são aceitos para leitura.
Salve o capítulo como `.docx`, `.odt` ou `.txt` antes de pedir a análise.

O manuscrito nunca é modificado. A revisão gera um relatório separado; uma
versão corrigida só é criada se você pedir e autorizar.

## 5. Pasta do livro

Na primeira utilização, o comando `/livro:inicio` explica o projeto e pede
permissão antes de criar a estrutura. Os outros ajudantes encaminham essa
primeira configuração para `/livro:inicio`:

```text
<livro>/
├── projeto-livro.md
├── memoria-da-historia.md
├── manuscrito/
├── revisao/
└── pesquisa/
```

`projeto-livro.md` guarda o contexto do projeto. `memoria-da-historia.md`
mantém resumos, personagens, lugares, linha do tempo, fios em aberto e
decisões do autor. Os capítulos ficam em `manuscrito/`, os relatórios em
`revisao/` e as notas de pesquisa em `pesquisa/`.

O ajudante lê a memória antes de abrir um capítulo quando ela existe. Ele lê o
capítulo inteiro somente quando a tarefa precisa dele e nunca altera esse
arquivo.

## 6. Personalizar

Cada ajudante tem um `rules.md`. Você pode editar esse arquivo livremente: ele é
lido primeiro e substitui as regras padrão do ajudante.

Cada ajudante também tem `references/ajuda.md`, que contém a explicação exibida
no modo de ajuda, suas opções, exemplos e o local dos resultados. O modo de
ajuda não lê capítulos nem cria arquivos.

## 7. Compatibilidade

| Ferramenta | `--target` | Comando | Arquivos | Web | Orquestrador |
|---|---|---|---|---|---|
| Claude Code | `claude` | `/livro:<nome>` pelo plugin; `/<nome>` pelo instalador | `.txt`; `.docx`/`.odt` dependem do extrator ⚠️ verificar | Pesquisa usa a capacidade web disponível | `/livro:inicio` |
| Agents | `agents` | `/<nome>` ⚠️ verificar | `.txt`; `.docx`/`.odt` dependem do extrator ⚠️ verificar | Depende da capacidade disponível | `inicio` |
| Codex | `codex` | `$<nome>` ou `/skills` ⚠️ verificar | `.txt`; `.docx`/`.odt` dependem do extrator ⚠️ verificar | Depende da capacidade disponível | `inicio` |
| Cursor | `cursor` | Não especificado ⚠️ verificar | `.txt`; `.docx`/`.odt` dependem do extrator ⚠️ verificar | Depende da capacidade disponível | `inicio` |
| Gemini | `gemini` | Não especificado ⚠️ verificar | `.txt`; `.docx`/`.odt` dependem do extrator ⚠️ verificar | Depende da capacidade disponível | `inicio` |
| OpenCode | `opencode` | Não especificado ⚠️ verificar | `.txt`; `.docx`/`.odt` dependem do extrator ⚠️ verificar | Depende da capacidade disponível | `inicio` |
| Copilot | `copilot` (somente projeto) | Não especificado ⚠️ verificar | `.txt`; `.docx`/`.odt` dependem do extrator ⚠️ verificar | Depende da capacidade disponível | `inicio` |

O instalador coloca as skills no diretório correspondente: `.claude/skills`,
`.agents/skills`, `.codex/skills`, `.cursor/skills`, `.gemini/skills`,
`.opencode/skills` ou `.github/skills`. Na instalação global, usa os diretórios
globais correspondentes; para OpenCode, usa `~/.config/opencode/skills`.

No Codex (CLI 0.158.0), foi verificado que as quatro skills são encontradas
com `--target codex`, `--target agents` e `--target codex --global`. As tarefas
em si ainda não foram testadas no Codex.

## 8. Para quem mantém o repositório

As regras de contribuição e o layout estão em `AGENTS.md`. O validador é
`python3 scripts/validate_skills.py`; ele verifica as quatro skills. Os testes
ficam em `tests/`: rode `python3 -m unittest discover tests` e, para o teste de
ponta a ponta com o Claude Code, `sh tests/e2e/run.sh`.

---

# Writing helpers for your book

## 1. What it is

This project bundles four helpers for writing a book in Portuguese: inicio,
revisao (grammar review), leitor-beta (beta reader) and pesquisa (research).
They read the context in the book folder and, when needed, the file you name.
They never change the manuscript file. Reports and notes are only saved with
your permission.

The helpers talk to the writer in Brazilian Portuguese, so the commands and
example requests below stay in Portuguese.

## 2. Installation

### Claude Code (recommended)

Add the marketplace and install the plugin:

```text
/plugin marketplace add MVFalcao/authors-skills
/plugin install livro@authors-skills
```

### Other tools

From this repository's folder, install into a book folder:

```sh
sh scripts/install.sh --target <target> <book-folder>
```

To install into the tool's global directory:

```sh
sh scripts/install.sh --target <target> --global
```

The targets are `claude`, `agents`, `codex`, `cursor`, `gemini`, `opencode`,
`copilot` and `all`. `all` installs for `claude` and `agents`. `copilot` only
works in a project folder, not with `--global`.

If a copy is already installed, it is kept in a sibling folder called
`skills-backup/`. Use `--force` to replace the existing copy without that
backup.

## 3. Commands

| Command | What it does | Example |
|---|---|---|
| `/livro:inicio` | Sets up the project, routes requests and gathers the results. | `/livro:inicio prepare o projeto do meu romance e revise manuscrito/capitulo-um.docx` |
| `/livro:revisao` | Looks for Portuguese spelling, grammar and punctuation problems. | `/livro:revisao manuscrito/capitulo-dois.txt confira a concordância` |
| `/livro:leitor-beta` | Reacts as a reader: hook, pacing, characters, dialogue, clarity and impact. | `/livro:leitor-beta manuscrito/cena-da-estacao.odt crítico leitor casual` |
| `/livro:pesquisa` | Researches names, places, eras, professions, technical details and reference books. | `/livro:pesquisa sugira nomes para uma biblioteca fictícia de bairro` |

A command with no task shows its help. Plain requests work too, such as
“confira a pontuação da cena” or “me diga onde minha atenção caiu”.

Use `/livro:inicio` when you want to combine steps; a request for one thing
goes straight to the matching helper. Revisao handles the Portuguese,
leitor-beta the reading experience, and pesquisa the verifiable context.

## 4. Manuscript formats

Name exactly one `.docx`, `.odt` or `.txt` file, or paste the passage into the
request. When the tool can run the shared extractor, the helpers read all three
formats. Without that capability they read a `.txt` directly; for `.docx` or
`.odt`, ask for a `.txt` or paste the text. The helper reads only the file you
name; it doesn't pick a chapter or search the `manuscrito/` folder. If you don't
name a file, it asks which one.

`.doc`, `.pdf`, `.pages`, `.rtf` and `.md` files can't be read. Save the
chapter as `.docx`, `.odt` or `.txt` before asking for the analysis.

The manuscript is never modified. Revisao writes a separate report; a
corrected version is only created if you ask for it and allow it.

## 5. Book folder

On first use, `/livro:inicio` explains the project and asks for permission
before creating the structure. The other helpers send that first setup to
`/livro:inicio`:

```text
<book>/
├── projeto-livro.md
├── memoria-da-historia.md
├── manuscrito/
├── revisao/
└── pesquisa/
```

`projeto-livro.md` holds the project context. `memoria-da-historia.md` keeps
summaries, characters, places, the timeline, open threads and the author's
decisions. Chapters go in `manuscrito/`, reports in `revisao/` and research
notes in `pesquisa/`.

When the memory file exists, the helper reads it before opening a chapter. It
reads a whole chapter only when the task needs it and never changes that file.

## 6. Customizing

Each helper has a `rules.md`. You can edit it freely: it is read first and
overrides the helper's default rules.

Each helper also has `references/ajuda.md`, which holds the explanation shown
in help mode, its options, examples and where results are saved. Help mode
reads no chapter and creates no files.

## 7. Compatibility

| Tool | `--target` | Command | Files | Web | Orchestrator |
|---|---|---|---|---|---|
| Claude Code | `claude` | `/livro:<name>` from the plugin; `/<name>` from the installer | `.txt`; `.docx`/`.odt` depend on the extractor ⚠️ to verify | Pesquisa uses the available web capability | `/livro:inicio` |
| Agents | `agents` | `/<name>` ⚠️ to verify | `.txt`; `.docx`/`.odt` depend on the extractor ⚠️ to verify | Depends on the available capability | `inicio` |
| Codex | `codex` | `$<name>` or `/skills` ⚠️ to verify | `.txt`; `.docx`/`.odt` depend on the extractor ⚠️ to verify | Depends on the available capability | `inicio` |
| Cursor | `cursor` | Not specified ⚠️ to verify | `.txt`; `.docx`/`.odt` depend on the extractor ⚠️ to verify | Depends on the available capability | `inicio` |
| Gemini | `gemini` | Not specified ⚠️ to verify | `.txt`; `.docx`/`.odt` depend on the extractor ⚠️ to verify | Depends on the available capability | `inicio` |
| OpenCode | `opencode` | Not specified ⚠️ to verify | `.txt`; `.docx`/`.odt` depend on the extractor ⚠️ to verify | Depends on the available capability | `inicio` |
| Copilot | `copilot` (project only) | Not specified ⚠️ to verify | `.txt`; `.docx`/`.odt` depend on the extractor ⚠️ to verify | Depends on the available capability | `inicio` |

The installer puts the skills in the matching directory: `.claude/skills`,
`.agents/skills`, `.codex/skills`, `.cursor/skills`, `.gemini/skills`,
`.opencode/skills` or `.github/skills`. A global install uses the matching
global directories; for OpenCode it uses `~/.config/opencode/skills`.

In Codex (CLI 0.158.0), all four skills were confirmed to be discovered with
`--target codex`, `--target agents` and `--target codex --global`. The tasks
themselves have not been tested in Codex yet.

## 8. For maintainers

Contribution rules and the layout are in `AGENTS.md`. The validator is
`python3 scripts/validate_skills.py`; it checks all four skills. Tests live in
`tests/`: run `python3 -m unittest discover tests` and, for the end-to-end test
with Claude Code, `sh tests/e2e/run.sh`.
