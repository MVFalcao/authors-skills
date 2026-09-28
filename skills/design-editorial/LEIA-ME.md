<!-- fonte: 9de31c6bf37f -->
> Tradução para leitura. As instruções que valem estão em `SKILL.md` e `rules.md` (em inglês).

## O que faz

Cuida do design editorial do livro em PT-BR (`/livro:design-editorial`): o projeto gráfico (formato, grid, margens, tipografia e ritmo das páginas), a diagramação de texto e imagens para o impresso e o ebook, e a produção gráfica (papel, acabamento, encadernação, orçamento e prova na gráfica). Entrega especificações, não arquivos de diagramação.

A skill faz três papéis: designer editorial (a estrutura visual da publicação), diagramador (texto e imagens na página, impresso e digital) e produtor gráfico (papel, acabamentos, custos e a gráfica). Ela escreve especificações que um designer, um programa de diagramação ou uma gráfica podem seguir; não gera arquivos de InDesign, Affinity, Word ou EPUB.

## Quando usar e quando não usar

Use quando o escritor pergunta "que formato e fonte uso no meu romance?", "quantas páginas vai dar e qual a lombada?", "como monto o ebook?", "que papel peço para a gráfica?" ou "o que confiro na prova impressa?".

Não use para revisar o texto (isso é a revisao), opinar sobre a história (isso é o leitor-beta) ou pesquisar fatos (isso é a pesquisa). Pedidos para desenhar a capa também vêm aqui: a skill não cria arte nem imagens, só a especificação técnica da capa. Uma pergunta sobre se o primeiro capítulo prende o leitor pertence ao leitor-beta.

## Como funciona

0. Trata o texto completo do comando como o pedido, tira espaços em branco e entra em modo de ajuda para entrada vazia ou para qualquer pergunta (sem diferenciar maiúsculas/pontuação) sobre o que a skill faz ou como usá-la (por exemplo "ajuda", "o que o design editorial faz?" ou "como funciona?"). Nesse caso lê `references/ajuda.md` e, quando existir, `projeto-livro.md` só para leitura, para adaptar o texto, sem ler memória nem capítulo, sem inspecionar resultados e sem criar arquivos. Fora do modo de ajuda, preserva o pedido completo.
1. Lê `rules.md`; ele substitui os padrões descritos aqui. Depois lê as referências que o pedido precisa:
   - `references/formatos-e-margens.md` para formato, grid e margens;
   - `references/tipografia-e-grid.md` para fontes, corpo, entrelinha, hierarquia e ritmo das páginas;
   - `references/papel-e-acabamento.md` para papel, impressão, encadernação, acabamentos, orçamento e prova;
   - `references/diagramacao-digital.md` para EPUB e PDF digital.
2. Lê `projeto-livro.md` e `memoria-da-historia.md` quando existirem, para título, gênero, público, tom e as decisões do autor (um formato ou uma fonte já escolhidos são decisões a manter). Não cria nem atualiza a memória compartilhada; devolve as adições propostas para a skill `inicio`.
3. Classifica o pedido em um ou mais modos:
   - **projeto gráfico**: formato, grid, margens, tipografia, hierarquia, ritmo, páginas pré e pós-textuais;
   - **diagramação**: organização de texto e imagens para o impresso ou o ebook;
   - **produção gráfica**: papel, método de impressão, cores, encadernação, acabamentos, arquivos para impressão, pedido de orçamento, checklist da prova;
   - **cálculo**: um número só (palavras, páginas, lombada, capa aberta).
   Para vários modos, responde na ordem projeto gráfico → diagramação → produção gráfica, um documento por modo. Escreve só os modos que o escritor pediu; oferece os outros em uma linha no final, em vez de escrevê-los. Um pedido para desenhar, ilustrar ou fazer um esboço da capa (ou de qualquer outra imagem) está fora do escopo: nunca cria imagem, SVG, HTML ou outro arquivo visual, nem como rascunho. Diz isso em uma linha e oferece a especificação técnica da capa (tamanho aberto, lombada, sangria, o que entregar ao ilustrador).
4. Reúne os dados que o modo precisa: impresso, ebook ou os dois; formato; número de palavras; número de capítulos; imagens ou cor; tiragem; o que pesa mais (custo, durabilidade, acabamento especial). Se um dado ausente mudar a resposta de forma relevante, faz uma pergunta curta. Se não, usa os padrões de `rules.md` e lista esses padrões em "Premissas".
5. Contagem de palavras. Usa o número que o escritor der. Se não houver, conta só os arquivos que o escritor nomear explicitamente (ou todos os arquivos de `manuscrito/` quando o escritor pedir explicitamente o livro inteiro) com `scripts/calc_producao.py palavras <arquivo> ...`, que usa o extrator compartilhado. Contar palavras é o único uso dos arquivos do manuscrito aqui: não lê, não resume e não cita o conteúdo dos capítulos, e nunca os modifica. Sem contagem, pula a estimativa de páginas e diz o que falta.
6. Calcula todos os números com `scripts/calc_producao.py` (`mancha`, `paginas`, `lombada`, `capa`), nunca de cabeça, e mostra ao lado de cada resultado os dados usados. Passa para `paginas` os mesmos números de páginas pré e pós-textuais listados no documento (`--pre-textuais`, `--pos-textuais`). Os caminhos são relativos à pasta desta própria skill. Se o script não puder rodar, dá a fórmula e marca o resultado com `⚠️ verificar`.
7. Escreve a especificação com o modelo correspondente abaixo. Explica cada escolha em uma linha (por que este formato, esta fonte, este papel). Marca tudo o que depende de um fornecedor ou de uma licença com `⚠️ verificar com a gráfica` ou `⚠️ verificar licença`. Nunca inventa preços, estoque de papel de uma gráfica específica nem os termos de licença de uma fonte.
8. Salva o documento em `design/` seguindo as regras de salvamento de `rules.md`; uma resposta de `cálculo` com um número só fica no chat, a menos que o escritor peça para salvar. Se o ambiente não puder gravar arquivos, devolve o documento completo no chat. Termina com as perguntas em aberto e as atualizações de memória propostas.

## Formato do resultado

- Projeto gráfico (`design/projeto-grafico.md`): premissas; formato e mancha; tabela de tipografia; hierarquia e ritmo; páginas pré e pós-textuais; estimativa de páginas; perguntas em aberto; atualização proposta para a memória.
- Diagramação (`design/diagramacao-impresso.md` ou `design/diagramacao-ebook.md`): estilos de parágrafo e caractere; regras de texto (hifenização, viúvas e órfãs, alinhamento, recuo, diálogos, quebras de cena); imagens; checklist de diagramação; perguntas em aberto.
- Produção gráfica (`design/producao-grafica.md`): tabela de especificação técnica (miolo, capa, encadernação, lombada, capa aberta); arquivos para a gráfica; pedido de orçamento; checklist da prova; riscos e decisões.

Um exemplo de pedido é "quero imprimir 300 exemplares do meu romance de 70 mil palavras em 14x21, o que peço para a gráfica?": roda `paginas`, depois `lombada` com a espessura que o escritor der (ou um valor típico marcado) e escreve `design/producao-grafica.md`.

## Regras

> Estas são as regras de `rules.md`, que a skill lê primeiro e que substituem os padrões acima.

### Padrões quando o escritor não indica preferência
- Ficção adulta impressa: formato **14x21 cm**, corpo **11/15 pt** em uma serifada de livro, margens interna 20, externa 15, superior 18, inferior 22 mm.
- Não ficção com notas, tabelas ou imagens: considera **16x23 cm** e diz por quê.
- Papel: miolo em **pólen 80 g/m²** para leitura longa, **offset 90 g/m²** quando há imagens em traço, **couché** só para fotos coloridas. Capa em **cartão 250–300 g/m²** com **laminação fosca**.
- Encadernação: **brochura** (lombada quadrada) com cola PUR; cadernos de 16 páginas.
- Ebook: **EPUB 3 refluível**. Layout fixo só para livros em que a posição das imagens é o conteúdo (livros ilustrados infantis, quadrinhos).
- Lista todos os padrões usados em "Premissas", para o escritor poder mudar.

### Tipografia
- Linhas de texto com cerca de 55–70 caracteres; nunca fora de 45–75.
- Entrelinha de 120–140% do corpo.
- Prefere fontes com suporte completo ao PT-BR (ã, õ, ç, acentos, travessão) e licença que permita impresso e ebook. Sugere pelo menos uma opção gratuita (SIL Open Font License) ao lado de qualquer fonte comercial.
- No máximo duas famílias: uma para o texto, uma para títulos.
- Ficção: recuo de 1 em na primeira linha, sem espaço entre parágrafos, sem recuo depois de título ou quebra de cena.
- Os diálogos seguem a convenção do manuscrito (travessão no PT-BR). Nunca muda isso na especificação.

### Diagramação
- Sem viúvas nem órfãs: pelo menos 2 linhas de um parágrafo no topo ou no pé da página.
- Quebras de cena recebem um ornamento ou asterismo, não só uma linha em branco (a linha em branco some numa virada de página).
- Capítulos abrem em página nova, com um rebaixo de cerca de um terço da página. Abrir sempre na página ímpar é escolha do escritor: acrescenta páginas em branco.
- Sem cabeço nas aberturas de capítulo nem nas páginas em branco.

### Produção
- Nunca inventa preços, prazos ou o estoque de papel de uma gráfica. Dá o checklist para pedir orçamento.
- A espessura do papel (micra) e a lombada vêm da gráfica. Sem esse número, usa um valor típico, marca com `⚠️ verificar com a gráfica` e avisa que a capa precisa esperar a lombada da gráfica.
- Arquivos para impressão: PDF/X-1a ou PDF/X-4, fontes incorporadas, imagens a 300 dpi no tamanho final, sangria de 3 mm, marcas de corte. Pede as especificações da própria gráfica.
- Sempre recomenda uma prova física antes da tiragem completa.

### Limites
- Só especificações: não produz arquivos de diagramação, arte de capa nem ilustrações. Nunca cria imagem, SVG ou esboço em HTML, mesmo quando pedem uma capa; oferece a especificação técnica da capa.
- Escreve só os documentos dos modos que o escritor pediu; oferece os outros modos em uma linha.
- Não edita nem reescreve o manuscrito. Não comenta a história; isso é o leitor-beta.
- Os arquivos do manuscrito só são abertos para contar palavras, nunca para ler o conteúdo.

### Salvamento
- Para saber se `design/` existe, lista a própria pasta do livro (por exemplo com `ls`). Uma busca por arquivos não enxerga uma pasta vazia. Se listar não for permitido, roda `python3 -c "import os; print(os.path.isdir('design'))"`. Se não conseguir verificar de jeito nenhum, diz que não conseguiu verificar; nunca diz que a pasta não existe.
- Se `design/` já existe na pasta do livro, salva o resultado lá sem perguntar e informa o caminho do arquivo na resposta.
- Se `design/` não existe, pergunta uma vez antes de criar a pasta. Se o escritor disser que não, devolve o resultado no chat.
- Nomes de arquivo: `design/projeto-grafico.md`, `design/diagramacao-impresso.md`, `design/diagramacao-ebook.md`, `design/producao-grafica.md`.
- Nunca sobrescreve um resultado anterior: se o nome do arquivo já estiver em uso, acrescenta `-2`, `-3` e assim por diante.

## Onde ficam os arquivos

- `rules.md`, `references/ajuda.md` e as outras referências em `references/`: regras, texto de ajuda e guias desta skill.
- `scripts/calc_producao.py`: cálculos de mancha, páginas, lombada, capa aberta e contagem de palavras.
- `projeto-livro.md` e `memoria-da-historia.md`: lidos na pasta do livro, quando existirem.
- `../inicio/scripts/extract_text.py`: usado pelo script para contar palavras de um arquivo nomeado (caminho relativo à pasta desta skill).
- `design/projeto-grafico.md`, `design/diagramacao-impresso.md`, `design/diagramacao-ebook.md`, `design/producao-grafica.md`: ficam na pasta `design/`.
