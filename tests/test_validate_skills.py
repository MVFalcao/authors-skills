import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from validate_skills import validate_skill, validate_all  # noqa: E402

FIXTURES = ROOT / "tests" / "fixtures"


class ValidateSkillTest(unittest.TestCase):
    def test_good_skill_has_no_errors(self):
        self.assertEqual(validate_skill(FIXTURES / "skills-good" / "good-skill"), [])

    def test_missing_frontmatter(self):
        errors = validate_skill(FIXTURES / "skills-bad" / "no-frontmatter")
        self.assertTrue(any("frontmatter" in e for e in errors), errors)

    def test_name_must_match_folder(self):
        errors = validate_skill(FIXTURES / "skills-bad" / "wrong-name")
        self.assertTrue(any("name" in e for e in errors), errors)

    def test_missing_reference_file(self):
        errors = validate_skill(FIXTURES / "skills-bad" / "missing-ref")
        self.assertTrue(any("references/ghost.md" in e for e in errors), errors)

    def test_missing_rules_file(self):
        errors = validate_skill(FIXTURES / "skills-bad" / "missing-rules")
        self.assertTrue(any("rules.md" in e for e in errors), errors)

    def test_name_must_be_kebab_case(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp) / "Not_Kebab"
            d.mkdir()
            (d / "SKILL.md").write_text(
                "---\nname: Not_Kebab\ndescription: x\n---\n\nBody.\n", encoding="utf-8"
            )
            errors = validate_skill(d)
        self.assertTrue(any("kebab" in e for e in errors), errors)

    def test_inconsistent_block_indentation_is_rejected(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp) / "bad-indent"
            d.mkdir()
            (d / "SKILL.md").write_text(
                "---\nname: bad-indent\ndescription: >-\n    first line\n  second line\n---\n\nBody.\n",
                encoding="utf-8",
            )
            errors = validate_skill(d)
        self.assertTrue(any("indentation" in e for e in errors), errors)

    def test_leia_me_stamp_must_match_sources(self):
        import tempfile
        from validate_skills import leia_me_stamp
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp) / "stamped"
            d.mkdir()
            (d / "SKILL.md").write_text(
                "---\nname: stamped\ndescription: x\n---\n\nRead `rules.md`.\n", encoding="utf-8"
            )
            (d / "rules.md").write_text("# Rules\n", encoding="utf-8")
            stamp = leia_me_stamp(d)
            self.assertRegex(stamp, r"^[0-9a-f]{12}$")
            (d / "LEIA-ME.md").write_text(f"<!-- fonte: {stamp} -->\n# Leia-me\n", encoding="utf-8")
            self.assertEqual(validate_skill(d), [])
            (d / "rules.md").write_text("# Rules changed\n", encoding="utf-8")
            errors = validate_skill(d)
        self.assertTrue(any("LEIA-ME.md" in e for e in errors), errors)

    def test_leia_me_without_stamp_is_rejected(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp) / "nostamp"
            d.mkdir()
            (d / "SKILL.md").write_text("---\nname: nostamp\ndescription: x\n---\n\nBody.\n", encoding="utf-8")
            (d / "LEIA-ME.md").write_text("# Leia-me\n", encoding="utf-8")
            errors = validate_skill(d)
        self.assertTrue(any("LEIA-ME.md" in e for e in errors), errors)

    def test_description_too_long(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp) / "long-desc"
            d.mkdir()
            (d / "SKILL.md").write_text(
                "---\nname: long-desc\ndescription: " + "x" * 1100 + "\n---\n\nBody.\n",
                encoding="utf-8",
            )
            errors = validate_skill(d)
        self.assertTrue(any("description" in e for e in errors), errors)

    def test_validate_all_reports_each_skill(self):
        results = validate_all(FIXTURES / "skills-bad")
        self.assertEqual(
            set(results), {"no-frontmatter", "wrong-name", "missing-ref", "missing-rules"}
        )
        self.assertTrue(all(results.values()))


class RepoSkillsTest(unittest.TestCase):
    EXPECTED = {"revisao", "leitor-beta", "pesquisa", "inicio"}

    def test_all_writer_skills_exist_and_are_valid(self):
        results = validate_all(ROOT / "skills")
        self.assertTrue(self.EXPECTED.issubset(results), f"missing: {self.EXPECTED - set(results)}")
        for name, errors in results.items():
            self.assertEqual(errors, [], f"{name}: {errors}")

    def test_each_skill_has_evals(self):
        for name in self.EXPECTED:
            self.assertTrue((ROOT / "skills" / name / "evals" / "evals.md").is_file(), name)

    def test_each_skill_has_editable_rules(self):
        for name in self.EXPECTED:
            skill_dir = ROOT / "skills" / name
            self.assertTrue((skill_dir / "rules.md").is_file(), name)
            body = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("rules.md", body, f"{name}: SKILL.md must tell the agent to read rules.md")


class PluginPackagingTest(unittest.TestCase):
    SKILLS = ("inicio", "revisao", "leitor-beta", "pesquisa")

    def test_plugin_manifest(self):
        import json
        manifest = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest.get("name"), "livro")

    def test_marketplace_points_to_repo_root(self):
        import json
        market = json.loads(
            (ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8")
        )
        self.assertTrue(market.get("name"))
        self.assertTrue(market.get("owner", {}).get("name"))
        plugins = {p.get("name"): p for p in market.get("plugins", [])}
        self.assertIn("livro", plugins)
        self.assertIn(plugins["livro"].get("source"), ("./", "."))

    def test_each_skill_has_help_and_argument_hint(self):
        for name in self.SKILLS:
            skill_dir = ROOT / "skills" / name
            self.assertTrue((skill_dir / "references" / "ajuda.md").is_file(), name)
            text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
            frontmatter = text.split("---", 2)[1]
            self.assertIn("argument-hint:", frontmatter, name)
            self.assertIn("references/ajuda.md", text, name)

    def test_each_skill_has_portuguese_reading_copy(self):
        for name in self.SKILLS:
            path = ROOT / "skills" / name / "LEIA-ME.md"
            self.assertTrue(path.is_file(), name)
            text = path.read_text(encoding="utf-8")
            self.assertIn("SKILL.md", text, name)
            self.assertGreater(len(text.splitlines()), 20, name)


if __name__ == "__main__":
    unittest.main()
