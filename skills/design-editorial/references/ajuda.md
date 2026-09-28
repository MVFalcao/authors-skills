# Ajuda — design editorial

Planeja a parte visual e de produção do livro: o projeto gráfico (formato,
grid, margens, tipografia e ritmo das páginas), a diagramação de texto e
imagens para o livro impresso e o ebook, e a produção gráfica (papel,
acabamentos, encadernação, arquivos, orçamento e prova na gráfica). Entrego
especificações para você, um diagramador ou a gráfica seguirem; não crio os
arquivos de diagramação nem a arte da capa.

## Opções

- **projeto gráfico**: formato, margens, mancha, fontes, hierarquia e páginas
  pré e pós-textuais.
- **diagramação**: estilos e regras para o impresso ou para o ebook (EPUB).
- **produção gráfica**: papel, cores, acabamento, encadernação, lombada,
  arquivos para a gráfica, pedido de orçamento e checklist da prova.
- **cálculo**: palavras, número de páginas, lombada ou tamanho da capa aberta.

Diga se o livro será impresso, digital ou os dois, e o que pesa mais: custo,
durabilidade ou acabamento. Para estimar páginas, informe o número de palavras
ou os arquivos do manuscrito que devo contar.

## Exemplos

```text
/livro:design-editorial projeto gráfico para um romance de 70 mil palavras em 14x21
/livro:design-editorial quantas páginas e qual a lombada em pólen 80?
/livro:design-editorial produção gráfica para 300 exemplares
/livro:design-editorial diagramação do ebook
```

Se as skills foram instaladas com `scripts/install.sh` (sem o plugin), use o comando sem o prefixo `livro:`, por exemplo `/design-editorial`.

Também funciona pedir em linguagem natural, como “que fonte e formato uso no
meu livro?”.

Preços, papéis disponíveis e a lombada final dependem da gráfica: marco esses
pontos com `⚠️ verificar com a gráfica` e nunca invento valores.

## Onde os resultados ficam

As especificações ficam em `design/` (se a pasta ainda não existir, eu pergunto
antes de criá-la): `design/projeto-grafico.md`,
`design/diagramacao-impresso.md`, `design/diagramacao-ebook.md` ou
`design/producao-grafica.md`. Um cálculo rápido fica no chat. O modo de ajuda
não lê manuscrito nem cria arquivos.
