from pathlib import Path
import sys
import tempfile
import unittest

PACKAGE = Path(__file__).resolve().parents[1]
SCRIPTS = PACKAGE / "scripts"
sys.path.insert(0, str(SCRIPTS))
from check_package import check_links, check_mapping, frontmatter
from install import install


class PackageTests(unittest.TestCase):
    def setUp(self):
        temporary_base = PACKAGE / ".fstack" / "tests"
        if not temporary_base.resolve().is_relative_to(PACKAGE):
            raise ValueError("Test temporary directory leaves package")
        temporary_base.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix="package-", dir=temporary_base)
        self.root = Path(self.temp.name)
        self.source = self.root / "source"
        self.skill = self.source / "skills/fstack/SKILL.md"
        self.skill.parent.mkdir(parents=True)
        self.skill.write_text('---\nname: fstack\ndescription: "Research with evidence."\n---\n# Fstack\n', encoding="utf-8")

    def tearDown(self):
        self.temp.cleanup()

    def test_missing_and_escaping_links_fail(self):
        self.skill.write_text(self.skill.read_text() + "[missing](absent.md)\n[escape](../../../outside.md)\n", encoding="utf-8")
        errors = check_links(self.source)
        self.assertEqual(len(errors), 2)
        self.assertTrue(any("leaves package" in error for error in errors))

    def test_valid_link_and_code_example(self):
        self.skill.write_text(self.skill.read_text() + "[self](SKILL.md#fstack)\n```md\n[example](not-a-real-file.md)\n```\n", encoding="utf-8")
        self.assertEqual(check_links(self.source), [])

    def test_disposition_coverage_is_not_only_a_count(self):
        lock = {"commit": "same", "skills": ["skills/a/SKILL.md"]}
        registry = {"upstream": {"commit": "same"}, "skills": [{"source": "skills/wrong/SKILL.md", "treatment": "omit", "reason": "Not supported."}]}
        errors = check_mapping(self.source, lock, registry)
        self.assertTrue(any("missing upstream disposition" in error for error in errors))
        self.assertTrue(any("unknown upstream source" in error for error in errors))

    def test_disposition_target_must_exist(self):
        lock = {"commit": "same", "skills": ["skills/a/SKILL.md"]}
        registry = {"upstream": {"commit": "same"}, "skills": [{"source": "skills/a/SKILL.md", "treatment": "adapt", "reason": "Domain adaptation.", "target": "absent.md"}]}
        self.assertTrue(any("missing target" in error for error in check_mapping(self.source, lock, registry)))

    def test_dry_run_then_idempotent_install_preserves_links(self):
        project = self.root / "project"
        total, pending = install(self.source, project)
        self.assertEqual((total, pending), (2, 2))
        self.assertFalse(project.exists())
        self.assertEqual(install(self.source, project, apply=True), (2, 2))
        self.assertEqual(install(self.source, project, apply=True), (2, 0))
        self.assertEqual(check_links(project / ".agents"), [])
        shim = project / ".agents/skills/fstack/SKILL.md"
        self.assertEqual(frontmatter(shim)["name"], "fstack")
        unrelated = project / ".agents/skills/other/SKILL.md"
        unrelated.parent.mkdir()
        unrelated.write_text("user content", encoding="utf-8")
        install(self.source, project, apply=True)
        self.assertEqual(unrelated.read_text(), "user content")

    def test_collision_blocks_every_write(self):
        project = self.root / "project"
        collision = project / ".agents/skills/fstack/SKILL.md"
        collision.parent.mkdir(parents=True)
        collision.write_text("user content", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "writes nothing"):
            install(self.source, project, apply=True)
        self.assertEqual(collision.read_text(), "user content")
        self.assertFalse((project / ".agents/fstack").exists())

    def test_private_files_are_not_installed(self):
        (self.source / ".env").write_text("PRIVATE", encoding="utf-8")
        private = self.source / "examples/private/holdings.csv"
        private.parent.mkdir(parents=True)
        private.write_text("PRIVATE", encoding="utf-8")
        nested_secret = self.source / "examples/.env.production"
        nested_secret.write_text("PRIVATE", encoding="utf-8")
        private_names = ("credentials.yaml", "secrets.yml", "holdings.csv", "portfolio-2026.csv", "transactions.csv", ".netrc")
        for name in private_names:
            (self.source / "examples" / name).write_text("PRIVATE", encoding="utf-8")
        project = self.root / "project"
        install(self.source, project, apply=True)
        self.assertFalse((project / ".agents/fstack/.env").exists())
        self.assertFalse((project / ".agents/fstack/examples/private").exists())
        self.assertFalse((project / ".agents/fstack/examples/.env.production").exists())
        for name in private_names:
            self.assertFalse((project / ".agents/fstack/examples" / name).exists())

    def test_installing_inside_source_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "overlap"):
            install(self.source, self.source, apply=True)


if __name__ == "__main__":
    unittest.main()
