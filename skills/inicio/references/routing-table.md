# Tabela de roteamento

Classify by the requested outcome, not by an isolated word in the prompt. The
orchestrator owns this decision and passes the chapter plus context to the
selected leaf skill.

| Signal in the request | Route | Handoff |
|---|---|---|
| erro, ortografia, pontuação, concordância, revisar português | revisao | one chapter or excerpt; author decisions |
| prende, funciona, emoção, ritmo, o que achou, leitor | leitor-beta | one passage; persona and reader profile |
| nome, lugar, época, cotidiano, profissão, fonte, como era | pesquisa | location, period, social context, source need |
| formato, fonte/tipografia, margens, diagramação, ebook, páginas, lombada, papel, gráfica, capa (especificação técnica) | design-editorial | print/ebook, word count or named files, print run, priorities |
| “e depois”, “também”, or two clear outcomes | requested leaf stages in research → grammar → beta → design order | preserve each report and caveat |
| pedido de revisão com capítulo ou trecho definido, como “revisa o capítulo 1” | revisao | one chapter or excerpt; author decisions |
| pedido genérico de melhoria, como “melhora o capítulo” | one question | offer revisão gramatical or opinião |
| pedido genérico de ajuda, reescrever, or unclear “revisa” | one question | offer revisão, opinião, or pesquisa |

Do not route a factual uncertainty to leitor-beta merely because it appears in
a chapter. "Fonte" meaning a typeface goes to design-editorial; "fonte"
meaning a source goes to pesquisa. Do not route a request for reader reaction to revisao merely
because the prose contains errors. If a request names a previous book, pass it
to leitor-beta only for comparison or to pesquisa only for factual
source work; never invent its contents.

For a combined request, confirm which outputs are wanted when the wording does
not identify them. Once clear, run only the named stages and use the shared
memory between stages.
