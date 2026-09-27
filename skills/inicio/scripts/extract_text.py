#!/usr/bin/env python3
"""Print the plain text of a manuscript file (.docx, .odt or .txt).

Usage: extract_text.py <arquivo>

Paragraphs are separated by a blank line. Tabs and manual line breaks are
kept. The file is only read, never changed. Standard library only.

Exit codes: 0 ok, 1 unreadable or invalid file, 2 bad usage or unsupported
format. Error messages are in PT-BR because the writer may see them.
"""

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


def _docx_paragraphs(root):
    paragraphs = []

    def walk(elem, parts):
        for child in elem:
            if child.tag == W + "p":
                inner = []
                walk(child, inner)
                paragraphs.append("".join(inner))
            elif child.tag == W + "t":
                parts.append(child.text or "")
            elif child.tag == W + "tab":
                parts.append("\t")
            elif child.tag in (W + "br", W + "cr"):
                parts.append("\n")
            else:
                walk(child, parts)

    walk(root, [])
    return paragraphs


def _odt_inline(elem, parts):
    if elem.text:
        parts.append(elem.text)
    for child in elem:
        if child.tag == TEXT + "s":
            parts.append(" " * int(child.get(TEXT + "c", "1") or 1))
        elif child.tag == TEXT + "tab":
            parts.append("\t")
        elif child.tag == TEXT + "line-break":
            parts.append("\n")
        elif child.tag == TEXT + "note":
            pass  # footnotes would land mid-sentence; leave them out
        else:
            _odt_inline(child, parts)
        if child.tail:
            parts.append(child.tail)


def _odt_paragraphs(root):
    paragraphs = []
    for elem in root.iter():
        if elem.tag in (TEXT + "p", TEXT + "h"):
            parts = []
            _odt_inline(elem, parts)
            paragraphs.append("".join(parts))
    return paragraphs


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
        paragraphs = _docx_paragraphs(_read_xml_member(path, "word/document.xml"))
    else:
        paragraphs = _odt_paragraphs(_read_xml_member(path, "content.xml"))
    return "\n\n".join(paragraphs) + "\n"


def main(argv):
    if len(argv) != 1:
        print("uso: extract_text.py <arquivo .docx/.odt/.txt>", file=sys.stderr)
        return 2
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
