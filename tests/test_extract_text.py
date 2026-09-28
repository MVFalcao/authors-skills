import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "skills" / "inicio" / "scripts" / "extract_text.py"
sys.path.insert(0, str(SCRIPT.parent))

from extract_text import extract_text  # noqa: E402

MANUSCRIPT = ROOT / "tests" / "fixtures" / "livro-exemplo" / "manuscrito"

W_NS = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'
ODF_NS = (
    'xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" '
    'xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"'
)


def make_docx(path, body_xml, prolog=""):
    document = (
        f'<?xml version="1.0" encoding="UTF-8"?>{prolog}'
        f"<w:document {W_NS}><w:body>{body_xml}</w:body></w:document>"
    )
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("[Content_Types].xml", "<Types/>")
        archive.writestr("word/document.xml", document)


def make_odt(path, text_xml):
    content = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        f"<office:document-content {ODF_NS}><office:body><office:text>"
        f"{text_xml}</office:text></office:body></office:document-content>"
    )
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("mimetype", "application/vnd.oasis.opendocument.text")
        archive.writestr("content.xml", content)


def run_cli(*args):
    return subprocess.run(
        [sys.executable, str(SCRIPT), *map(str, args)],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


class FixtureManuscriptTest(unittest.TestCase):
    def test_docx_chapter(self):
        text = extract_text(MANUSCRIPT / "capitulo-01.docx")
        self.assertTrue(text.startswith("Capítulo 1 — A volta"), text[:40])
        # The fixture splits this word across two runs; they must be joined.
        self.assertIn("Concerteza Dona Zefa", text)
        self.assertIn("Ela foi a praia ainda no escuro", text)
        self.assertIn("— Nóis vai pescar amanhã, se Deus quiser —", text)
        self.assertNotIn("<", text)

    def test_paragraphs_are_separated_by_blank_lines(self):
        text = extract_text(MANUSCRIPT / "capitulo-01.docx")
        paragraphs = text.strip().split("\n\n")
        self.assertEqual(len(paragraphs), 6, paragraphs)

    def test_odt_chapter(self):
        text = extract_text(MANUSCRIPT / "capitulo-02.odt")
        self.assertTrue(text.startswith("Capítulo 2 — A janela"), text[:40])
        self.assertIn('"Zefa, se eu demorar, não fica na janela."', text)
        self.assertEqual(len(text.strip().split("\n\n")), 10)


class FormatDetailsTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_docx_tabs_and_line_breaks(self):
        path = self.tmp / "t.docx"
        make_docx(
            path,
            "<w:p><w:r><w:t>um</w:t><w:tab/><w:t>dois</w:t><w:br/>"
            "<w:t>três</w:t></w:r></w:p>",
        )
        self.assertEqual(extract_text(path).strip(), "um\tdois\ntrês")

    def test_odt_spaces_tabs_spans_and_line_breaks(self):
        path = self.tmp / "t.odt"
        make_odt(
            path,
            '<text:p>a<text:s text:c="3"/>b<text:tab/>c<text:line-break/>'
            "<text:span>d</text:span>e</text:p>",
        )
        self.assertEqual(extract_text(path).strip(), "a   b\tc\nde")

    def test_odt_space_count_is_validated_and_capped(self):
        for count, expected in (("abc", 1), ("-5", 1), ("", 1), ("3", 3), ("200000000", 1000)):
            path = self.tmp / "s.odt"
            make_odt(path, f'<text:p>a<text:s text:c="{count}"/>b</text:p>')
            text = extract_text(path).strip()
            self.assertEqual(text, "a" + " " * expected + "b", count)

    def test_odt_footnotes_are_left_out(self):
        path = self.tmp / "n.odt"
        make_odt(
            path,
            "<text:p>Corpo<text:note><text:note-citation>1</text:note-citation>"
            "<text:note-body><text:p>NOTA</text:p></text:note-body></text:note> fim.</text:p>",
        )
        self.assertEqual(extract_text(path), "Corpo fim.\n")

    def test_deeply_nested_docx_does_not_crash(self):
        path = self.tmp / "deep.docx"
        make_docx(path, "<w:sdt>" * 5000 + "<w:p><w:r><w:t>x</w:t></w:r></w:p>" + "</w:sdt>" * 5000)
        self.assertEqual(extract_text(path).strip(), "x")

    def test_docx_table_cells_keep_order(self):
        path = self.tmp / "tbl.docx"
        make_docx(
            path,
            "<w:p><w:r><w:t>antes</w:t></w:r></w:p><w:tbl><w:tr><w:tc>"
            "<w:p><w:r><w:t>celula</w:t></w:r></w:p></w:tc></w:tr></w:tbl>"
            "<w:p><w:r><w:t>depois</w:t></w:r></w:p>",
        )
        self.assertEqual(extract_text(path), "antes\n\ncelula\n\ndepois\n")

    def test_odt_tracked_deletions_are_left_out(self):
        path = self.tmp / "tc.odt"
        make_odt(
            path,
            '<text:tracked-changes><text:changed-region text:id="c1"><text:deletion>'
            "<text:p>APAGADO</text:p></text:deletion></text:changed-region></text:tracked-changes>"
            "<text:p>Texto final.</text:p>",
        )
        self.assertEqual(extract_text(path), "Texto final.\n")

    def test_total_output_is_capped(self):
        import extract_text as module
        path = self.tmp / "many.odt"
        make_odt(path, "<text:p>" + '<text:s text:c="1000"/>' * 50 + "</text:p>")
        old = module.MAX_TEXT_CHARS
        module.MAX_TEXT_CHARS = 10_000
        try:
            with self.assertRaises(module.ExtractError):
                extract_text(path)
        finally:
            module.MAX_TEXT_CHARS = old

    def test_txt_passes_through(self):
        path = self.tmp / "t.txt"
        path.write_text("Olá, ação.\n\nSegundo parágrafo.\n", encoding="utf-8")
        self.assertEqual(extract_text(path), "Olá, ação.\n\nSegundo parágrafo.\n")


class CliErrorTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_cli_prints_text(self):
        result = run_cli(MANUSCRIPT / "capitulo-01.docx")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Concerteza", result.stdout)

    def test_unsupported_formats_suggest_docx(self):
        for suffix in (".doc", ".pdf", ".pages", ".md", ".rtf"):
            path = self.tmp / f"cap{suffix}"
            path.write_bytes(b"x")
            result = run_cli(path)
            self.assertNotEqual(result.returncode, 0, suffix)
            self.assertIn(".docx", result.stderr, suffix)
            self.assertNotIn("Traceback", result.stderr, suffix)

    def test_missing_file(self):
        result = run_cli(self.tmp / "nope.docx")
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("Traceback", result.stderr)

    def test_corrupt_docx(self):
        path = self.tmp / "bad.docx"
        path.write_bytes(b"not a zip file")
        result = run_cli(path)
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("Traceback", result.stderr)

    def test_docx_without_document_part(self):
        path = self.tmp / "empty.docx"
        with zipfile.ZipFile(path, "w") as archive:
            archive.writestr("[Content_Types].xml", "<Types/>")
        result = run_cli(path)
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("Traceback", result.stderr)

    def test_rejects_doctype_entities(self):
        path = self.tmp / "entity.docx"
        make_docx(
            path,
            "<w:p><w:r><w:t>&x;</w:t></w:r></w:p>",
            prolog='<!DOCTYPE w:document [<!ENTITY x "boom">]>',
        )
        result = run_cli(path)
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("boom", result.stdout)
        self.assertNotIn("Traceback", result.stderr)

    def test_fingerprint_changes_when_content_changes(self):
        path = self.tmp / "f.txt"
        path.write_text("abc", encoding="utf-8")
        first = run_cli("--fingerprint", path)
        self.assertEqual(first.returncode, 0, first.stderr)
        size, digest = first.stdout.split()
        self.assertEqual(size, "3")
        self.assertRegex(digest, r"^[0-9a-f]{12}$")
        path.write_text("abd", encoding="utf-8")  # same size, new content
        second = run_cli("--fingerprint", path)
        self.assertEqual(second.stdout.split()[0], "3")
        self.assertNotEqual(second.stdout.split()[1], digest)

    def test_fingerprint_of_sample_chapters_matches_memory_fixture(self):
        memory = (MANUSCRIPT.parent / "memoria-da-historia.md").read_text(encoding="utf-8")
        result = run_cli("--fingerprint", MANUSCRIPT / "capitulo-01.docx")
        size, digest = result.stdout.split()
        self.assertIn(f"| {size} | {digest} |", memory)

    def test_no_arguments(self):
        result = run_cli()
        self.assertNotEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
