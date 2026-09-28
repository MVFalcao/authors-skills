# Ajuda — revisão

Revisa prosa em português brasileiro, capítulo ou trecho por vez, procurando
crase, ortografia, gramática, regência, pontuação, concordância e repetições sem
apagar escolhas intencionais de voz.

## Opções

Informe um único arquivo `.docx`, `.odt` ou `.txt`, ou cole o trecho. Você pode
pedir uma categoria específica, como concordância ou pontuação. A revisão não
avalia ritmo nem recepção de leitor. Cada achado recebe uma das gravidades:
`erro`, `atenção` ou `possível escolha de estilo`.

## Exemplos

```text
/livro:revisao manuscrito/cena-ponte.docx
/livro:revisao manuscrito/dialogo.txt verifique pontuação e travessões
/livro:revisao manuscrito/capitulo-7.odt confira concordância verbal
/livro:revisao ajuda
```

Se as skills foram instaladas com `scripts/install.sh` (sem o plugin), use o comando sem o prefixo `livro:`, por exemplo `/revisao`.

Também funciona dizer, por exemplo, “confira a crase deste trecho”, sem usar o
comando. A revisão nunca reescreve o texto sem que isso seja pedido.

## Onde os resultados ficam

O relatório fica em `revisao/<capitulo>-gramatica.md` (se a pasta ainda não existir, eu pergunto antes de criá-la). Uma
versão corrigida só é criada se você pedir, em um arquivo separado.
O modo de ajuda não lê manuscrito nem cria arquivos.
