#!/usr/bin/env python3
"""Print the plain text of a manuscript file (.docx, .odt or .txt).

Usage: extract_text.py <arquivo>
       extract_text.py --fingerprint <arquivo>   # "<bytes> <sha256[:12]>"

Paragraphs are separated by a blank line. Tabs and manual line breaks are
kept. The file is only read, never changed. Standard library only.

Exit codes: 0 ok, 1 unreadable or invalid file, 2 bad usage or unsupported
format. Error messages are in PT-BR because the writer may see them.
"""

import hashlib
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

SUPPORTED = (".docx", ".odt", ".txt")
# A chapter's XML is a few MB at most. The cap stops zip bombs from
# exhausting memory before parsing starts.
MAX_XML_BYTES = 50 * 1024 * 1024

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
TEXT = "{urn:oasis:names:tc:opendocument:xmlns:text:1.0}"


class ExtractError(Exception):
    """A problem the writer can fix; the message is shown as is."""

    def __init__(self, message, code=1):
        super().__init__(message)
        self.code = code


def _read_xml_member(path, member):
    try:
        with zipfile.ZipFile(path) as archive:
            try:
                info = archive.getinfo(member)
            except KeyError:
                raise ExtractError(f"arquivo incompleto: {path.name} não tem {member}")
            if info.file_size > MAX_XML_BYTES:
                raise ExtractError(f"arquivo grande demais: {path.name}")
            with archive.open(info) as handle:
                data = handle.read(MAX_XML_BYTES + 1)
    except zipfile.BadZipFile:
        raise ExtractError(f"arquivo corrompido ou não é {path.suffix}: {path.name}")
    if len(data) > MAX_XML_BYTES:
        raise ExtractError(f"arquivo grande demais: {path.name}")
    # Office files never need a DTD. Refusing one blocks entity-expansion
    # and external-entity tricks without depending on the expat version.
    head = data.upper()
    if b"<!DOCTYPE" in head or b"<!ENTITY" in head:
        raise ExtractError(f"arquivo recusado: {path.name} contém DOCTYPE/ENTITY")
    try:
        return ET.fromstring(data)
    except ET.ParseError:
        raise ExtractError(f"arquivo corrompido: {path.name} tem XML inválido")


# Both formats are walked with an explicit stack instead of recursion, so a
# deeply nested (possibly crafted) document cannot overflow the Python stack.
# Each element expands into an ordered list of steps:
#   ("text", str)   append text to the open paragraph
#   ("enter", elem) expand a child element
#   ("begin", None) / ("end", None)   open / close a paragraph


def _paragraphs(root, expand):
    paragraphs = []
    current = None
    outer = []
    stack = [("enter", root)]
    while stack:
        kind, value = stack.pop()
        if kind == "text":
            if current is not None and value:
                current.append(value)
        elif kind == "begin":
            outer.append(current)
            current = []
        elif kind == "end":
            paragraphs.append("".join(current))
            current = outer.pop()
        else:
            stack.extend(reversed(expand(value)))
    return paragraphs


def _docx_steps(elem):
    tag = elem.tag
    if tag == W + "t":
        return [("text", elem.text or "")]
    if tag == W + "tab":
        return [("text", "\t")]
    if tag in (W + "br", W + "cr"):
        return [("text", "\n")]
    children = [("enter", child) for child in elem]
    if tag == W + "p":
        return [("begin", None)] + children + [("end", None)]
    return children


# Longest run of spaces kept from one <text:s>. Real documents use small
# counts; the cap stops a tiny file from producing a huge string.
MAX_ODT_SPACES = 1000


def _odt_space_count(elem):
    try:
        count = int(elem.get(TEXT + "c", "1"))
    except ValueError:
        return 1
    return min(max(count, 1), MAX_ODT_SPACES)


def _odt_steps(elem):
    tag = elem.tag
    if tag == TEXT + "s":
        return [("text", " " * _odt_space_count(elem))]
    if tag == TEXT + "tab":
        return [("text", "\t")]
    if tag == TEXT + "line-break":
        return [("text", "\n")]
    if tag == TEXT + "note":
        return []  # footnotes would land mid-text; leave them out entirely
    steps = [("text", elem.text or "")]
    for child in elem:
        steps.append(("enter", child))
        steps.append(("text", child.tail or ""))
    if tag in (TEXT + "p", TEXT + "h"):
        return [("begin", None)] + steps + [("end", None)]
    return steps


def extract_text(path):
    """Return the plain text of a .docx, .odt or .txt file."""

    path = Path(path)
    suffix = path.suffix.lower()
    if suffix not in SUPPORTED:
        raise ExtractError(
            f"formato {suffix or '(sem extensão)'} não suportado: salve o capítulo "
            "como .docx (ou .odt / .txt) e tente de novo",
            code=2,
        )
    if not path.is_file():
        raise ExtractError(f"arquivo não encontrado: {path}")
    if suffix == ".txt":
        try:
            return path.read_text(encoding="utf-8-sig")
        except UnicodeDecodeError:
            return path.read_text(encoding="latin-1")
    if suffix == ".docx":
        paragraphs = _paragraphs(_read_xml_member(path, "word/document.xml"), _docx_steps)
    else:
        paragraphs = _paragraphs(_read_xml_member(path, "content.xml"), _odt_steps)
    return "\n\n".join(paragraphs) + "\n"


def fingerprint(path):
    """Return "<bytes> <first 12 hex chars of sha256>" for the raw file.

    The story memory stores this per chapter; size alone misses edits that
    keep the same length.
    """

    path = Path(path)
    if not path.is_file():
        raise ExtractError(f"arquivo não encontrado: {path}")
    digest = hashlib.sha256()
    size = 0
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
            size += len(block)
    return f"{size} {digest.hexdigest()[:12]}"


def main(argv):
    usage = "uso: extract_text.py [--fingerprint] <arquivo .docx/.odt/.txt>"
    want_fingerprint = bool(argv) and argv[0] == "--fingerprint"
    if want_fingerprint:
        argv = argv[1:]
    if len(argv) != 1:
        print(usage, file=sys.stderr)
        return 2
    if want_fingerprint:
        try:
            print(fingerprint(argv[0]))
        except ExtractError as exc:
            print(f"erro: {exc}", file=sys.stderr)
            return exc.code
        except OSError as exc:
            print(f"erro: não consegui ler {argv[0]} ({exc.strerror})", file=sys.stderr)
            return 1
        return 0
    try:
        text = extract_text(argv[0])
    except ExtractError as exc:
        print(f"erro: {exc}", file=sys.stderr)
        return exc.code
    except OSError as exc:
        print(f"erro: não consegui ler {argv[0]} ({exc.strerror})", file=sys.stderr)
        return 1
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
