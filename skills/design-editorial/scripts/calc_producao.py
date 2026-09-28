#!/usr/bin/env python3
"""Deterministic numbers for a book's layout and print specs.

Usage:
  calc_producao.py palavras <arquivo> [<arquivo> ...]
  calc_producao.py mancha  --formato 14x21 [margins] [--corpo 11 --entrelinha 15]
  calc_producao.py paginas --palavras 60000 --formato 14x21 [margins] [...]
  calc_producao.py lombada --paginas 240 --micra 110 [--capa-micra 300]
  calc_producao.py capa    --formato 14x21 --lombada 14 [--orelha 80] [--sangria 3]

Formats are width x height in cm ("14x21", "15,5x23"). Margins, spine, flaps
and bleed are in mm; body size and leading in points; paper thickness in
micrometres (micra). Every result is an estimate for planning: the final page
count comes from the actual layout and the spine from the print shop's proof.

Output is "chave: valor" lines in PT-BR. Standard library only. The shared
extractor (../../inicio/scripts/extract_text.py) is used for word counts.

Exit codes: 0 ok, 1 unreadable manuscript file, 2 bad usage.
"""

import argparse
import math
import re
import sys
from pathlib import Path

PT_PER_MM = 72 / 25.4
# Average glyph width of a book serif at 1 pt body, in points. Typical text
# faces set about 2.0-2.3 characters per em; 0.47 sits in that range.
DEFAULT_CHAR_WIDTH = 0.47
# Average characters per word in Portuguese prose, counting the space and
# punctuation after the word.
DEFAULT_CHARS_PER_WORD = 6.0
# A chapter opening wastes part of a page: the sunken first page (~1/3) and
# the half-empty last page on average.
CHAPTER_OVERHEAD_PAGES = 0.85
WORD_RE = re.compile(r"\w+(?:[-'’]\w+)*")

EXTRACTOR_DIR = Path(__file__).resolve().parent.parent.parent / "inicio" / "scripts"


def number(text):
    """Parse a positive number that may use a decimal comma."""
    try:
        value = float(str(text).replace(",", "."))
    except ValueError:
        raise argparse.ArgumentTypeError(f"número inválido: {text}")
    if not math.isfinite(value) or value <= 0:
        raise argparse.ArgumentTypeError(f"o número deve ser positivo: {text}")
    return value


def non_negative(text):
    try:
        value = float(str(text).replace(",", "."))
    except ValueError:
        raise argparse.ArgumentTypeError(f"número inválido: {text}")
    if not math.isfinite(value) or value < 0:
        raise argparse.ArgumentTypeError(f"o número não pode ser negativo: {text}")
    return value


def positive_int(text):
    try:
        value = int(text)
    except ValueError:
        raise argparse.ArgumentTypeError(f"inteiro inválido: {text}")
    if value <= 0:
        raise argparse.ArgumentTypeError(f"o inteiro deve ser positivo: {text}")
    return value


def non_negative_int(text):
    try:
        value = int(text)
    except ValueError:
        raise argparse.ArgumentTypeError(f"inteiro inválido: {text}")
    if value < 0:
        raise argparse.ArgumentTypeError(f"o inteiro não pode ser negativo: {text}")
    return value


def book_format(text):
    """Parse "LxA" in cm into (width_mm, height_mm)."""
    parts = re.split(r"\s*[xX×]\s*", str(text).strip())
    if len(parts) != 2:
        raise argparse.ArgumentTypeError(
            f"formato inválido: {text} (use largura x altura em cm, ex.: 14x21)"
        )
    width, height = (number(part) * 10 for part in parts)
    if width >= height:
        raise argparse.ArgumentTypeError(
            f"formato inválido: {text} (a largura deve ser menor que a altura)"
        )
    return width, height


def fmt(value, decimals=1):
    text = f"{value:.{decimals}f}"
    return text.replace(".", ",")


def text_block(args):
    """Return the text block and line figures for the layout arguments."""
    width, height = args.formato
    block_w = width - args.margem_interna - args.margem_externa
    block_h = height - args.margem_superior - args.margem_inferior
    if block_w <= 0 or block_h <= 0:
        raise ValueError("as margens não cabem no formato")
    if args.entrelinha < args.corpo:
        raise ValueError("a entrelinha deve ser maior ou igual ao corpo")
    lines = math.floor(block_h * PT_PER_MM / args.entrelinha)
    chars = block_w * PT_PER_MM / (args.corpo * args.largura_media)
    if lines < 1:
        raise ValueError("a mancha não comporta nenhuma linha")
    return block_w, block_h, lines, chars


def cmd_palavras(args):
    sys.path.insert(0, str(EXTRACTOR_DIR))
    try:
        from extract_text import ExtractError, extract_text
    except ImportError:
        print(
            "erro: extrator não encontrado em ../inicio/scripts/extract_text.py; "
            "informe a contagem de palavras",
            file=sys.stderr,
        )
        return 1
    total = 0
    for name in args.arquivos:
        try:
            text = extract_text(Path(name))
        except ExtractError as exc:
            print(f"erro: {exc}", file=sys.stderr)
            return exc.code
        count = len(WORD_RE.findall(text))
        total += count
        print(f"{name}: {count}")
    print(f"total_palavras: {total}")
    return 0


def cmd_mancha(args):
    block_w, block_h, lines, chars = text_block(args)
    print(f"mancha_mm: {fmt(block_w)} x {fmt(block_h)}")
    print(f"linhas_por_pagina: {lines}")
    print(f"caracteres_por_linha: {round(chars)}")
    if chars < 45:
        print("aviso: linha curta (menos de 45 caracteres); muitas hifenizações")
    elif chars > 75:
        print("aviso: linha longa (mais de 75 caracteres); leitura cansativa")
    return 0


def cmd_paginas(args):
    _, _, lines, chars = text_block(args)
    words_per_page = lines * chars / args.caracteres_por_palavra
    text_pages = args.palavras / words_per_page
    openings = args.capitulos * CHAPTER_OVERHEAD_PAGES
    raw = math.ceil(text_pages + openings) + args.pre_textuais + args.pos_textuais
    rounded = math.ceil(raw / args.caderno) * args.caderno
    print(f"palavras_por_pagina: {round(words_per_page)}")
    print(f"paginas_de_texto: {fmt(text_pages)}")
    print(f"paginas_estimadas: {raw}")
    print(f"paginas_em_cadernos_de_{args.caderno}: {rounded}")
    print("observacao: estimativa; a contagem final sai da diagramação")
    return 0


def cmd_lombada(args):
    if args.paginas % 2:
        print("aviso: número ímpar de páginas; contando a última folha inteira")
    sheets = math.ceil(args.paginas / 2)
    spine = sheets * args.micra / 1000 + 2 * args.capa_micra / 1000
    print(f"folhas: {sheets}")
    print(f"lombada_mm: {fmt(spine)}")
    print("observacao: confirme a lombada com a gráfica antes de fechar a capa")
    return 0


def cmd_capa(args):
    width, height = args.formato
    open_w = 2 * width + args.lombada + 2 * args.orelha + 2 * args.sangria
    open_h = height + 2 * args.sangria
    print(f"capa_aberta_mm: {fmt(open_w)} x {fmt(open_h)}")
    print(
        "composicao: "
        + (f"orelha {fmt(args.orelha)} + " if args.orelha else "")
        + f"quarta capa {fmt(width)} + lombada {fmt(args.lombada)} + "
        + f"primeira capa {fmt(width)}"
        + (f" + orelha {fmt(args.orelha)}" if args.orelha else "")
        + f" + sangria {fmt(args.sangria)} em cada borda"
    )
    return 0


def add_layout_arguments(parser):
    parser.add_argument("--formato", type=book_format, required=True,
                        help="largura x altura em cm, ex.: 14x21")
    parser.add_argument("--margem-interna", type=number, default=20)
    parser.add_argument("--margem-externa", type=number, default=15)
    parser.add_argument("--margem-superior", type=number, default=18)
    parser.add_argument("--margem-inferior", type=number, default=22)
    parser.add_argument("--corpo", type=number, default=11, help="pontos")
    parser.add_argument("--entrelinha", type=number, default=15, help="pontos")
    parser.add_argument("--largura-media", type=number, default=DEFAULT_CHAR_WIDTH,
                        help="largura média do caractere, em ems")


def build_parser():
    parser = argparse.ArgumentParser(
        prog="calc_producao.py",
        description="Cálculos de projeto gráfico e produção de um livro.",
    )
    sub = parser.add_subparsers(dest="comando", required=True)

    palavras = sub.add_parser("palavras", help="conta palavras de .docx/.odt/.txt")
    palavras.add_argument("arquivos", nargs="+")
    palavras.set_defaults(func=cmd_palavras)

    mancha = sub.add_parser("mancha", help="mancha, linhas e caracteres por linha")
    add_layout_arguments(mancha)
    mancha.set_defaults(func=cmd_mancha)

    paginas = sub.add_parser("paginas", help="estima o número de páginas do miolo")
    paginas.add_argument("--palavras", type=positive_int, required=True)
    add_layout_arguments(paginas)
    paginas.add_argument("--capitulos", type=non_negative_int, default=0)
    paginas.add_argument("--pre-textuais", type=non_negative_int, default=8)
    paginas.add_argument("--pos-textuais", type=non_negative_int, default=2)
    paginas.add_argument("--caderno", type=positive_int, default=16,
                         help="páginas por caderno (8, 16 ou 32)")
    paginas.add_argument("--caracteres-por-palavra", type=number,
                         default=DEFAULT_CHARS_PER_WORD)
    paginas.set_defaults(func=cmd_paginas)

    lombada = sub.add_parser("lombada", help="largura da lombada")
    lombada.add_argument("--paginas", type=positive_int, required=True)
    lombada.add_argument("--micra", type=number, required=True,
                         help="espessura de uma folha do miolo, em micrômetros")
    lombada.add_argument("--capa-micra", type=non_negative, default=0,
                         help="espessura do cartão da capa, em micrômetros")
    lombada.set_defaults(func=cmd_lombada)

    capa = sub.add_parser("capa", help="tamanho da capa aberta")
    capa.add_argument("--formato", type=book_format, required=True)
    capa.add_argument("--lombada", type=non_negative, required=True, help="mm")
    capa.add_argument("--orelha", type=non_negative, default=0, help="mm")
    capa.add_argument("--sangria", type=non_negative, default=3, help="mm")
    capa.set_defaults(func=cmd_capa)
    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except ValueError as exc:
        print(f"erro: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
