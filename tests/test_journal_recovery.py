from pathlib import Path
import tempfile
import unittest

from fstack_tools.runtime import journal_append


class JournalRecoveryTests(unittest.TestCase):
    def test_missing_terminal_newline_does_not_corrupt_journal(self):
        base = Path(__file__).resolve().parents[1] / ".fstack" / "tests"
        base.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=base) as folder:
            journal = Path(folder) / "decisions.jsonl"
            event = dict(event_id="one", run_id="run", phase="research", decision="wait",
                         reason="missing evidence", evidence="source.md")
            journal_append(journal, event)
            truncated = journal.read_bytes().rstrip(b"\r\n")
            journal.write_bytes(truncated)
            with self.assertRaisesRegex(ValueError, "incomplete final line"):
                journal_append(journal, {**event, "event_id": "two"})
            self.assertEqual(journal.read_bytes(), truncated)
            self.assertFalse(journal.with_suffix(".jsonl.lock").exists())
