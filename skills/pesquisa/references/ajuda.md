# Ajuda — pesquisa

Pesquisa contexto verificável para a escrita: nomes, lugares, épocas,
profissões, detalhes técnicos e livros de referência, separando fontes,
inferências, opções e pontos a confirmar. Fatos sem fonte ou que precisem de
confirmação são marcados com `⚠️ verificar`.

## Opções

Descreva o assunto, o lugar, a época e o uso narrativo. Para nomes, indique se
é pessoa, família, lugar ou instituição. Se a pesquisa precisar de contexto do
manuscrito, informe exatamente um arquivo `.docx`, `.odt` ou `.txt`, ou cole o
trecho; uma pesquisa comum não precisa de manuscrito.

## Exemplos

```text
/livro:pesquisa sugira nomes para uma estação ferroviária fictícia
/livro:pesquisa como era o transporte fluvial no interior do Brasil em 1930?
/livro:pesquisa manuscrito/cena-do-porto.txt confira detalhes náuticos
/livro:pesquisa ajuda
```

Se as skills foram instaladas com `scripts/install.sh` (sem o plugin), use o comando sem o prefixo `livro:`, por exemplo `/pesquisa`.

Também funciona pedir em linguagem natural, como “pesquise nomes para uma
cooperativa de montanha”.

## Onde os resultados ficam

Com autorização, notas ficam em `pesquisa/`, com nomes como
`pesquisa/nomes-<assunto>.md` ou `pesquisa/lugar-<assunto>.md`. Sem autorização
ou acesso a arquivos, o resultado completo é devolvido no chat. O modo de
ajuda não lê manuscrito nem cria arquivos.
