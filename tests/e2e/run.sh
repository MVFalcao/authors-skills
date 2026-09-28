#!/bin/sh
# End-to-end check of the writer skills with headless Claude Code.
#
# Copies the sample book (tests/fixtures/livro-exemplo) into a temp folder,
# installs the skills there with scripts/install.sh, then runs each eval
# prompt in its own fresh copy. Needs the `claude` CLI, logged in.
#
# Usage: sh tests/e2e/run.sh [output-dir]
# Prints one line per case: exit code and the files saved in revisao/ and
# pesquisa/. Full replies are in <output-dir>/out-<case>.md.
set -eu

REPO=$(cd "$(dirname "$0")/../.." && pwd)
OUT=${1:-$(mktemp -d "${TMPDIR:-/tmp}/authors-e2e.XXXXXX")}
mkdir -p "$OUT"

command -v claude >/dev/null 2>&1 || { echo "e2e: claude CLI not found" >&2; exit 1; }

BOOK="$OUT/livro"
rm -rf "$BOOK"
cp -r "$REPO/tests/fixtures/livro-exemplo" "$BOOK"
# An initialised book: the report folders exist but are still empty.
mkdir -p "$BOOK/revisao" "$BOOK/pesquisa"
sh "$REPO/scripts/install.sh" --force "$BOOK" >/dev/null

run_case() {
    name=$1
    prompt=$2
    dir="$OUT/case-$name"
    rm -rf "$dir"
    cp -r "$BOOK" "$dir"
    status=0
    (cd "$dir" && timeout 900 claude -p "$prompt" \
        --allowedTools "Read" "Write" "Edit" "Glob" "Grep" "Skill" \
        "WebSearch" "WebFetch" "Bash(python3:*)" "Bash(ls:*)" \
        >"$OUT/out-$name.md" 2>"$OUT/err-$name.txt") || status=$?
    saved=$(cd "$dir" && find revisao pesquisa -type f 2>/dev/null | tr '\n' ' ')
    # Cases that must save a file vs cases that must not create any.
    case "$name" in
        revisao|leitor|pesquisa) want=file ;;
        *) want=none ;;
    esac
    verdict=PASS
    [ "$status" -eq 0 ] || verdict=FAIL
    if [ "$want" = file ] && [ -z "$saved" ]; then verdict=FAIL; fi
    if [ "$want" = none ] && [ -n "$saved" ]; then verdict=FAIL; fi
    echo "$verdict $name exit=$status saved: ${saved:-none}" | tee "$OUT/verdict-$name.txt"
}

run_case revisao "revisa a gramática de manuscrito/capitulo-01.docx" &
run_case leitor "lê o manuscrito/capitulo-02.odt como leitor beta e me diz o que achou" &
run_case pesquisa "preciso de nomes para moradores de uma vila de pescadores no litoral da Bahia nos anos 1950" &
run_case ambiguo "me ajuda com o capitulo-02.odt" &
run_case ajuda "/leitor-beta" &
run_case semarquivo "revisa o capítulo 1" &
wait
echo "e2e: outputs in $OUT"
# Only file effects are checked here; read out-<case>.md against the evals
# for the content (errors found, one question asked, and so on).
if grep -q '^FAIL' "$OUT"/verdict-*.txt; then
    echo "e2e: FAILED" >&2
    exit 1
fi
echo "e2e: file checks passed"
