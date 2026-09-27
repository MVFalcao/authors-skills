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
    EXPECTED = {"grammar-review", "beta-reader", "writer-research", "book-orchestrator"}

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


if __name__ == "__main__":
    unittest.main()
