"""Build the sample manuscript files in livro-exemplo/manuscrito/.

The chapters are kept as .docx and .odt because writers deliver manuscripts in
word-processor formats. This script rebuilds them from the plain-text sources
below with the standard library only, with fixed timestamps so the output is
byte-for-byte reproducible (the story-memory fixture records their sizes).

Run from the repo root:  python3 tests/fixtures/make_manuscripts.py
"""

import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

HERE = Path(__file__).resolve().parent
OUT = HERE / "livro-exemplo" / "manuscrito"
FIXED_TIME = (2026, 9, 20, 12, 0, 0)

CHAPTER_1 = [
    "Capítulo 1 — A volta",
    "Naquela manhã, Marina acordou antes do galo. Ela foi a praia ainda no escuro, com os pés afundando na areia fria, e ficou olhando o horizonte como quem espera uma carta.",
    "Os pescadores voltou cedo. O barco do pai dela vinha atrás, e o barco balançava tanto que ela pensou que o barco ia virar.",
    "— Nóis vai pescar amanhã, se Deus quiser — gritou seu Tonho, descendo da canoa.",
    "Marina sorriu. Queria correr até ele, mais não podia: a mãe tinha pedido que ela voltasse antes do café. Concerteza Dona Zefa já estava na janela, contando os minutos.",
    "Quando começou à chover, ela ainda estava lá. Sempre preferiu mais o mar do que a cidade, e a chuva não mudava isso.",
]

CHAPTER_2 = [
    "Capítulo 2 — A janela",
    "Dona Zefa guardava as cartas do marido numa lata de biscoito, embaixo da cama. Ninguém mexia ali. Nem Marina, que aos vinte e seis anos ainda pedia licença para entrar no quarto da mãe.",
    "Naquela tarde, a lata estava aberta sobre a colcha.",
    "— Quem mexeu nisso? — perguntou Marina, da porta.",
    "A mãe não respondeu. Olhava pela janela o mesmo pedaço de mar que olhava havia trinta anos, desde o dia em que o barco do marido não voltou. Marina conhecia aquele silêncio. Era o silêncio das datas.",
    "Sentou-se na beira da cama e pegou a primeira carta. A letra do pai era inclinada, apressada, como se ele escrevesse com medo de a maré subir antes do ponto final.",
    "\"Zefa, se eu demorar, não fica na janela.\"",
    "Marina dobrou o papel devagar. Lá fora, alguém chamava os meninos para o almoço, e o cheiro de peixe frito subia da casa ao lado. A vida seguia, teimosa, como sempre seguiu naquela rua.",
    "— Ele pediu pra senhora não ficar na janela — disse ela, por fim.",
    "Dona Zefa virou o rosto, e pela primeira vez em muitos anos, sorriu.",
]


def _write_zip(path, members):
    with zipfile.ZipFile(path, "w") as archive:
        for name, data, method in members:
            info = zipfile.ZipInfo(name, FIXED_TIME)
            info.compress_type = method
            archive.writestr(info, data)


def _docx_run(text):
    return f'<w:r><w:t xml:space="preserve">{escape(text)}</w:t></w:r>'


def build_docx(path, paragraphs):
    body = []
    for index, text in enumerate(paragraphs):
        if index == 0:
            style = '<w:pPr><w:pStyle w:val="Heading1"/></w:pPr>'
            runs = _docx_run(text)
        else:
            style = ""
            # Word often splits one word across several runs (spell-check,
            # edits, formatting). Split a word on purpose so the extractor
            # has to join runs without adding spaces.
            if "Concerteza" in text:
                before, after = text.split("Concerteza", 1)
                runs = _docx_run(before + "Concer") + _docx_run("teza" + after)
            else:
                runs = _docx_run(text)
        body.append(f"<w:p>{style}{runs}</w:p>")
    document = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        f'<w:body>{"".join(body)}</w:body></w:document>'
    )
    content_types = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Override PartName="/word/document.xml" '
        'ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
        "</Types>"
    )
    rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" '
        'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" '
        'Target="word/document.xml"/></Relationships>'
    )
    _write_zip(
        path,
        [
            ("[Content_Types].xml", content_types, zipfile.ZIP_DEFLATED),
            ("_rels/.rels", rels, zipfile.ZIP_DEFLATED),
            ("word/document.xml", document, zipfile.ZIP_DEFLATED),
        ],
    )


def build_odt(path, paragraphs):
    body = []
    for index, text in enumerate(paragraphs):
        if index == 0:
            body.append(f'<text:h text:outline-level="1">{escape(text)}</text:h>')
        else:
            body.append(f"<text:p>{escape(text)}</text:p>")
    content = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<office:document-content '
        'xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" '
        'xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" office:version="1.3">'
        f'<office:body><office:text>{"".join(body)}</office:text></office:body>'
        "</office:document-content>"
    )
    manifest = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<manifest:manifest xmlns:manifest="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0" manifest:version="1.3">'
        '<manifest:file-entry manifest:full-path="/" manifest:media-type="application/vnd.oasis.opendocument.text"/>'
        '<manifest:file-entry manifest:full-path="content.xml" manifest:media-type="text/xml"/>'
        "</manifest:manifest>"
    )
    _write_zip(
        path,
        [
            # The ODF spec requires an uncompressed "mimetype" entry first.
            ("mimetype", "application/vnd.oasis.opendocument.text", zipfile.ZIP_STORED),
            ("META-INF/manifest.xml", manifest, zipfile.ZIP_DEFLATED),
            ("content.xml", content, zipfile.ZIP_DEFLATED),
        ],
    )


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    build_docx(OUT / "capitulo-01.docx", CHAPTER_1)
    build_odt(OUT / "capitulo-02.odt", CHAPTER_2)
    for name in ("capitulo-01.docx", "capitulo-02.odt"):
        print(f"{name}: {(OUT / name).stat().st_size} bytes")


if __name__ == "__main__":
    main()
