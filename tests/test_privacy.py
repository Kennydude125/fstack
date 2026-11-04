from pathlib import Path
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[1]


class PrivacyTests(unittest.TestCase):
    def ignored(self, path):
        result = subprocess.run(["git", "check-ignore", "--no-index", "--quiet", path], cwd=ROOT)
        self.assertIn(result.returncode, (0, 1))
        return result.returncode == 0

    def test_private_files_are_ignored(self):
        for path in (".env", ".env.production", "sub/.env", "secrets.yaml", "credentials.json",
                     "key.pem", "certificate.pfx", ".aws/credentials", "data/import.csv",
                     ".fstack/run/receipt.json", "runs/output.json", "logs/agent.log",
                     "holdings.csv", "portfolio-2026.csv", "settings.local.json"):
            with self.subTest(path=path):
                self.assertTrue(self.ignored(path))

    def test_public_examples_and_code_are_visible(self):
        for path in (".env.example", "examples/daily_research/us.csv", "fstack_tools/runtime.py",
                     ".github/workflows/ci.yml", "skills/fstack/SKILL.md"):
            with self.subTest(path=path):
                self.assertFalse(self.ignored(path))
