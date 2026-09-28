# Ajuda — início

Coordena o trabalho do livro: prepara o projeto, encaminha revisão, leitura
beta e pesquisa, e reúne os resultados. Você também pode fazer esses pedidos em
linguagem natural, sem usar o comando.

## O que posso fazer

- `/livro:revisao` — encontra problemas de gramática, ortografia e pontuação.
  Exemplo: `/livro:revisao capitulo.docx`.
- `/livro:leitor-beta` — avalia gancho, ritmo, clareza e impacto como leitor.
  Exemplo: `/livro:leitor-beta cena.txt crítico`.
- `/livro:pesquisa` — reúne contexto verificável para nomes, lugares e épocas.
  Exemplo: `/livro:pesquisa clima de uma cidade costeira em 1920`.
- `/livro:inicio` — organiza o projeto, a memória e combina essas etapas.
  Exemplo: `/livro:inicio revise e depois avalie capitulo.docx`.

## Exemplos

```text
/livro:inicio
/livro:inicio prepare meu projeto de romance histórico
/livro:inicio revise e depois avalie manuscrito/cena-ponte.docx
/livro:inicio pesquise o cenário e depois leia a cena manuscrito/cena-ponte.txt
```

Se as skills foram instaladas com `scripts/install.sh` (sem o plugin), use o comando sem o prefixo `livro:`, por exemplo `/inicio`.

Também funcionam pedidos em linguagem natural, como “revise o capítulo e depois
me diga se a cena prende”.

Em pedidos que envolvem manuscrito, informe exatamente o arquivo `.docx`,
`.odt` ou `.txt` a ser usado. O início não escolhe arquivos por você.

## Onde os resultados ficam

Relatórios ficam em `revisao/`; notas de pesquisa ficam em
`pesquisa/`; o projeto e a memória ficam na pasta do livro. O modo de ajuda não
cria nem altera arquivos.
