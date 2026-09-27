---
name: search
description: >-
  Search and research through Octopus with Perplexity live web search. Use for
  any lookup outside the model's knowledge: current docs, library or API
  behaviour, publishing-industry facts, best practices, comparisons ("search
  for…", "look up…", "research…", "what's the latest…", "find sources on…").
  Also use for broad codebase exploration in this repo. Returns cited findings.
---

# Search (Octopus + Perplexity)

`OCTO="$HOME/.claude-octopus/plugin"`

## 1. Preflight

```bash
test -x "$OCTO/scripts/orchestrate.sh" && echo "octo:ok" || echo "octo:missing"
[ -n "$PERPLEXITY_API_KEY" ] && echo "perplexity:ok" || echo "perplexity:missing"
```

- `octo:missing` → stop and tell the user to run `/octo:setup`.
- `perplexity:missing` → tell the user Perplexity isn't configured and that they
  need to export `PERPLEXITY_API_KEY` (for example in `~/.bashrc`) and restart
  the session. Ask whether to go ahead without it using the other Octopus
  providers. Don't switch silently.
- Perplexity calls cost money on the user's key. For an `exhaustive` run,
  mention that before starting.

## 2. Pick the mode

| Request | Mode |
|---|---|
| One focused question ("what's the current EPUB 3 spec version?") | **Quick**: Perplexity only |
| Broad topic, trade-offs, "research X" | **Deep**: `/octo:research` exhaustive |
| Where or how something works in *this* repo | **Codebase**: `/octo:discover` |

### Quick (Perplexity only)

```bash
TASK="search-$(date +%s)"
"$OCTO/scripts/orchestrate.sh" probe-single perplexity \
  '<focused question, with context and what a good answer includes>' \
  "$TASK" '<user question as asked>'
```

Read the result file it reports. If the answer is thin or the sources
disagree, move up to Deep.

### Deep (multi-provider, includes Perplexity)

Read `$OCTO/commands/research.md` and follow it with `--breadth=exhaustive`,
the breadth that brings in Perplexity alongside the other providers.
Don't call `/octo:research` with the Skill tool; follow the file.

### Codebase

Read `$OCTO/commands/discover.md` and follow it (`orchestrate.sh probe`).
Perplexity isn't useful here because it can't see local files.

## 3. Answer

- Lead with the direct answer in one to three sentences.
- Follow with key findings as bullets, each with its source link. Perplexity
  returns citations, so keep them and don't invent any.
- Note where providers or sources disagree, and the date of anything that
  changes over time.
- If something couldn't be verified, say so.
- End with which providers ran (from Octopus's agent summary).
