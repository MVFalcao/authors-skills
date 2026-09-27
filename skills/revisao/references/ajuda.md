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
/livro:revisao /rascunhos/cena-ponte.docx
/livro:revisao /rascunhos/dialogo.txt verifique pontuação e travessões
/livro:revisao /rascunhos/capitulo-7.odt confira concordância verbal
/livro:revisao ajuda
```

Também funciona dizer, por exemplo, “confira a crase deste trecho”, sem usar o
comando. A revisão nunca reescreve o texto sem que isso seja pedido.

## Onde os resultados ficam

Com autorização, o relatório fica em `revisao/<capitulo>-gramatica.md`. Uma
versão corrigida só é criada se for pedida e autorizada, em um arquivo separado.
O modo de ajuda não lê manuscrito nem cria arquivos.
