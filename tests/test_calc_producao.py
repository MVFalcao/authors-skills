import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "skills" / "design-editorial" / "scripts" / "calc_producao.py"
MANUSCRIPT = ROOT / "tests" / "fixtures" / "livro-exemplo" / "manuscrito"


def run(*args):
    result = subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        text=True,
    )
    values = {}
    for line in result.stdout.splitlines():
        key, _, value = line.partition(": ")
        values[key] = value
    return result, values


class ManchaTest(unittest.TestCase):
    def test_default_margins_for_14x21(self):
        result, values = run("mancha", "--formato", "14x21")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(values["mancha_mm"], "105,0 x 170,0")
        self.assertEqual(values["linhas_por_pagina"], "32")
        self.assertEqual(values["caracteres_por_linha"], "58")
        self.assertNotIn("aviso", result.stdout)

    def test_decimal_comma_format(self):
        result, values = run("mancha", "--formato", "15,5x23")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(values["mancha_mm"], "120,0 x 190,0")

    def test_long_line_warning(self):
        result, _ = run("mancha", "--formato", "21x28", "--corpo", "10", "--entrelinha", "13")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("aviso: linha longa", result.stdout)

    def test_landscape_format_rejected(self):
        result, _ = run("mancha", "--formato", "21x14")
        self.assertEqual(result.returncode, 2)
        self.assertIn("largura deve ser menor", result.stderr)

    def test_margins_larger_than_page(self):
        result, _ = run("mancha", "--formato", "14x21", "--margem-interna", "80",
                        "--margem-externa", "70")
        self.assertEqual(result.returncode, 2)
        self.assertIn("margens não cabem", result.stderr)

    def test_leading_smaller_than_body(self):
        result, _ = run("mancha", "--formato", "14x21", "--corpo", "12", "--entrelinha", "10")
        self.assertEqual(result.returncode, 2)


class PaginasTest(unittest.TestCase):
    def test_estimate_rounds_to_signatures(self):
        result, values = run("paginas", "--palavras", "60000", "--formato", "14x21",
                             "--capitulos", "20")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(values["palavras_por_pagina"], "307")
        self.assertEqual(values["paginas_estimadas"], "223")
        self.assertEqual(values["paginas_em_cadernos_de_16"], "224")

    def test_signature_size_option(self):
        result, values = run("paginas", "--palavras", "60000", "--formato", "14x21",
                             "--capitulos", "20", "--caderno", "32")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(values["paginas_em_cadernos_de_32"], "224")

    def test_zero_words_rejected(self):
        result, _ = run("paginas", "--palavras", "0", "--formato", "14x21")
        self.assertEqual(result.returncode, 2)


class LombadaCapaTest(unittest.TestCase):
    def test_spine_includes_cover(self):
        result, values = run("lombada", "--paginas", "272", "--micra", "110",
                             "--capa-micra", "300")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(values["folhas"], "136")
        self.assertEqual(values["lombada_mm"], "15,6")

    def test_odd_page_count_warns(self):
        result, values = run("lombada", "--paginas", "271", "--micra", "100")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(values["folhas"], "136")
        self.assertIn("aviso", result.stdout)

    def test_open_cover_with_flaps(self):
        result, values = run("capa", "--formato", "14x21", "--lombada", "15,6",
                             "--orelha", "80")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(values["capa_aberta_mm"], "461,6 x 216,0")

    def test_open_cover_without_flaps(self):
        result, values = run("capa", "--formato", "14x21", "--lombada", "10")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(values["capa_aberta_mm"], "296,0 x 216,0")
        self.assertNotIn("orelha", values["composicao"])


class PalavrasTest(unittest.TestCase):
    def test_counts_fixture_chapters(self):
        result, values = run("palavras", str(MANUSCRIPT / "capitulo-01.docx"),
                             str(MANUSCRIPT / "capitulo-02.odt"))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(values["total_palavras"], "313")

    def test_counts_hyphenated_word_once(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "cena.txt"
            path.write_text("Guarda-chuva na mão, disse-lhe: não!", encoding="utf-8")
            result, values = run("palavras", str(path))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(values["total_palavras"], "5")

    def test_unsupported_format(self):
        result, _ = run("palavras", "capitulo.pdf")
        self.assertEqual(result.returncode, 2)
        self.assertIn("não suportado", result.stderr)

    def test_manuscript_is_not_modified(self):
        path = MANUSCRIPT / "capitulo-01.docx"
        before = path.read_bytes()
        run("palavras", str(path))
        self.assertEqual(path.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
