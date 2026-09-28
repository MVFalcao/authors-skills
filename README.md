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
/plugin marketplace add <dono>/authors-skills
/plugin install livro@authors-skills
```

Substitua `<dono>` pelo proprietário do repositório no GitHub quando ele for
publicado.

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
helpers leem esses três formatos. Se essa capacidade não estiver disponível,
eles leem diretamente um `.txt`; para `.docx` ou `.odt`, peça um `.txt` ou
cole o texto. O ajudante lê somente o arquivo que você nomear; ele não escolhe
um capítulo nem vasculha a pasta `manuscrito/`.

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

## 8. Para quem mantém o repositório

As regras de contribuição e o layout estão em `AGENTS.md`. O validador é
`python3 scripts/validate_skills.py`; ele verifica as quatro skills. Os testes
ficam em `tests/` e não são rastreados no git.
