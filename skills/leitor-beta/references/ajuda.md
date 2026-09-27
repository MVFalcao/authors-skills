# Ajuda — leitor beta

Oferece a reação de um leitor ao capítulo ou trecho: gancho, ritmo,
personagens, diálogos, clareza, impacto emocional, pontos fortes e dúvidas.

## Opções

Informe um único arquivo `.docx`, `.odt` ou `.txt`, ou cole o texto. Escolha a
persona `gentil`, `neutro` (padrão), `crítico` ou `todas`; também pode indicar
um perfil, como fã do gênero ou leitor casual.

## Exemplos

```text
/livro:leitor-beta /rascunhos/cena-do-mercado.docx gentil
/livro:leitor-beta /rascunhos/capitulo-3.txt neutro leitor casual
/livro:leitor-beta /rascunhos/prologo.odt crítico fã do gênero
/livro:leitor-beta ajuda
```

Também funciona pedir em linguagem natural, como “leia esta cena como leitora
casual e diga onde minha atenção cai”.

## Onde os resultados ficam

Com autorização, o relatório fica em `revisao/<capitulo>-leitura-beta.md`. O
manuscrito não é alterado. O modo de ajuda não lê manuscrito nem cria arquivos.
