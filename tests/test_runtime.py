import csv
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

from fstack_tools.runtime import check_data, check_receipt, checkpoint, journal_append, verify_run

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "daily_research"


class RuntimeTests(unittest.TestCase):
    def setUp(self):
        temporary_root = ROOT / ".fstack" / "tests"
        temporary_root.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=temporary_root)
        assert Path(self.temporary.name).resolve().is_relative_to(temporary_root.resolve())
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        for path in EXAMPLE.iterdir():
            if path.is_file():
                shutil.copy2(path, self.root / path.name)

    def metadata(self, market="us", **changes):
        path = self.root / f"{market}.metadata.json"
        value = json.loads(path.read_text(encoding="utf-8"))
        value.update(changes)
        path.write_text(json.dumps(value), encoding="utf-8")
        return path

    def manifest(self, **changes):
        path = self.root / "manifest.json"
        value = json.loads(path.read_text(encoding="utf-8"))
        value.update(changes)
        path.write_text(json.dumps(value), encoding="utf-8")
        return path

    def rows(self, mutate, market="us"):
        path = self.root / f"{market}.csv"
        with path.open(newline="", encoding="utf-8") as stream:
            reader = csv.DictReader(stream)
            fields, rows = reader.fieldnames, list(reader)
        mutate(rows)
        with path.open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=list(dict.fromkeys(fields + [k for row in rows for k in row])))
            writer.writeheader()
            writer.writerows(rows)
        return path

    def check(self, market="us"):
        return check_data(self.root / f"{market}.csv", self.root / f"{market}.metadata.json")

    def test_us_hk_and_independent_reproduction(self):
        for market in ("us", "hk"):
            self.assertEqual("VERIFIED", self.check(market)["integrity"])
        receipt = self.root / "receipt.json"
        actual = verify_run(self.root / "manifest.json", receipt, "reviewer")
        self.assertEqual("VERIFIED", actual["integrity"])
        self.assertEqual("unknown", actual["thesis_support"])
        self.assertEqual("VERIFIED", check_receipt(receipt)["integrity"])
        us = json.loads((self.root / ".fstack/us-results.json").read_text())
        hk = json.loads((self.root / ".fstack/hk-results.json").read_text())
        self.assertAlmostEqual(10969.422734128615, float(us["final_equity"]), places=8)
        self.assertEqual(us["final_equity"], hk["final_equity"])
        self.assertEqual("2025-03-04T09:30:00-05:00", us["orders"][0]["execute_at"])
        other = self.root / "again"
        other.mkdir()
        for path in EXAMPLE.iterdir():
            if path.is_file():
                shutil.copy2(path, other / path.name)
        second = verify_run(other / "manifest.json", other / "receipt.json", "other-reviewer")
        self.assertEqual(actual["outputs"], second["outputs"])

    def test_cutoff_and_publication_time(self):
        self.metadata(as_of="2025-03-06T00:00:00Z")
        self.assertIn("future_information", {i["code"] for i in self.check()["issues"]})
        self.metadata(as_of="2025-03-10T00:00:00Z")
        self.rows(lambda rows: rows[0].update(available_at="2025-03-03T09:00:00-05:00"))
        self.assertIn("premature_bar", {i["code"] for i in self.check()["issues"]})

    def test_same_close_execution_rejected(self):
        self.rows(lambda rows: rows[0].update(signal_at="2025-03-03T16:30:00-05:00", execute_at="2025-03-03T16:30:00-05:00"))
        self.assertIn("execution_timing", {i["code"] for i in self.check()["issues"]})

    def test_currency_timezone_and_units(self):
        self.metadata(currency="HKD")
        self.assertEqual("NOT_VERIFIED", self.check()["integrity"])
        self.metadata(currency="USD", timezone="UTC")
        self.assertEqual("NOT_VERIFIED", self.check()["integrity"])
        self.metadata(timezone="America/New_York")
        self.rows(lambda rows: rows[0].update(open="NaN"))
        self.assertEqual("NOT_VERIFIED", self.check()["integrity"])

    def test_missing_cost_and_adjustment_unknown(self):
        path = self.metadata()
        value = json.loads(path.read_text())
        del value["cost_bps"]
        path.write_text(json.dumps(value))
        self.assertEqual("INCONCLUSIVE", self.check()["integrity"])
        self.metadata(cost_bps=10, price_basis="total_return_adjusted")
        self.assertEqual("INCONCLUSIVE", self.check()["integrity"])
        self.metadata(price_basis="raw", price_unit="thousands")
        self.assertEqual("INCONCLUSIVE", self.check()["integrity"])

    def test_empty_duplicate_unsorted_and_actions(self):
        self.rows(lambda rows: rows.clear())
        self.assertEqual("NOT_VERIFIED", self.check()["integrity"])
        shutil.copy2(EXAMPLE / "us.csv", self.root / "us.csv")
        self.rows(lambda rows: rows.reverse())
        self.assertIn("observation_order", {i["code"] for i in self.check()["issues"]})
        shutil.copy2(EXAMPLE / "us.csv", self.root / "us.csv")
        self.rows(lambda rows: rows[0].update(split_ratio="0"))
        self.assertIn("numeric_domain", {i["code"] for i in self.check()["issues"]})

    def test_dst_offset_mismatch(self):
        path = self.metadata()
        value = json.loads(path.read_text())
        value["sessions"][0]["open_at"] = "2025-03-03T09:30:00-04:00"
        path.write_text(json.dumps(value))
        self.assertIn("calendar_timezone", {i["code"] for i in self.check()["issues"]})

    def test_author_cannot_verify_and_outputs_must_be_fresh(self):
        with self.assertRaises(ValueError):
            verify_run(self.root / "manifest.json", self.root / "receipt.json", "example-author")
        output = self.root / ".fstack/us-results.json"
        output.parent.mkdir()
        output.write_text("old data")
        with self.assertRaisesRegex(ValueError, "fresh"):
            verify_run(self.root / "manifest.json", self.root / "receipt.json", "reviewer")

    def test_wrong_calculation_fails_before_receipt_pass(self):
        script = self.root / "backtest.py"
        script.write_text(script.read_text().replace('shares *= D(row["split_ratio"])', 'shares *= D("1")'))
        receipt = verify_run(self.root / "manifest.json", self.root / "receipt.json", "reviewer")
        self.assertEqual("NOT_VERIFIED", receipt["integrity"])
        self.assertNotEqual(0, receipt["checks"][0]["returncode"])

    def test_stale_dataset_code_config_output_and_tool(self):
        receipt_path = self.root / "receipt.json"
        verify_run(self.root / "manifest.json", receipt_path, "reviewer")
        for relative in ("us.csv", "backtest.py", "manifest.json", ".fstack/us-results.json"):
            path = self.root / relative
            original = path.read_bytes()
            path.write_bytes(original + b" ")
            self.assertEqual("NOT_VERIFIED", check_receipt(receipt_path)["integrity"])
            path.write_bytes(original)
        receipt = json.loads(receipt_path.read_text())
        receipt["tool_sha256"] = "changed"
        receipt_path.write_text(json.dumps(receipt))
        self.assertIn("stale_tool", {i["code"] for i in check_receipt(receipt_path)["issues"]})

    def test_receipt_cannot_be_overwritten(self):
        receipt_path = self.root / "receipt.json"
        verify_run(self.root / "manifest.json", receipt_path, "reviewer")
        with self.assertRaises(FileExistsError):
            verify_run(self.root / "manifest.json", receipt_path, "reviewer")

    def test_stripped_receipt_cannot_claim_success(self):
        receipt_path = self.root / "receipt.json"
        verify_run(self.root / "manifest.json", receipt_path, "reviewer")
        original = receipt_path.read_text()
        for field in ("checks", "inputs", "outputs", "dataset_checks"):
            value = json.loads(original)
            value[field] = [] if field in {"checks", "dataset_checks"} else {}
            receipt_path.write_text(json.dumps(value))
            self.assertEqual("NOT_VERIFIED", check_receipt(receipt_path)["integrity"])

    def test_empty_output_and_timeout_are_not_passes(self):
        self.manifest(checks=[{"name": "empty", "argv": ["{python}", "-c", "from pathlib import Path; Path('.fstack/us-results.json').touch(); Path('.fstack/hk-results.json').touch()"], "expected_outputs": [".fstack/us-results.json", ".fstack/hk-results.json"]}])
        self.assertEqual("NOT_VERIFIED", verify_run(self.root / "manifest.json", self.root / "receipt.json", "reviewer")["integrity"])
        for output in (self.root / ".fstack").iterdir():
            output.unlink()
        self.manifest(checks=[{"name": "timeout", "argv": ["{python}", "-c", "import time; time.sleep(1)"], "timeout_seconds": 0.01, "expected_outputs": [".fstack/us-results.json", ".fstack/hk-results.json"]}])
        self.assertEqual("INCONCLUSIVE", verify_run(self.root / "manifest.json", self.root / "other.json", "reviewer")["integrity"])

    def test_tuned_evaluation_cannot_claim_untouched(self):
        self.manifest(performance_evidence="untouched_evaluation")
        (self.root / "attempts.json").write_text('[{"evaluation_used_for_tuning": true}]')
        with self.assertRaisesRegex(ValueError, "untouched"):
            verify_run(self.root / "manifest.json", self.root / "receipt.json", "reviewer")

    def test_script_and_external_paths_must_be_fingerprinted(self):
        value = json.loads((self.root / "manifest.json").read_text())
        self.manifest(inputs=[p for p in value["inputs"] if p != "backtest.py"])
        with self.assertRaisesRegex(ValueError, "script"):
            verify_run(self.root / "manifest.json", self.root / "receipt.json", "reviewer")
        self.manifest(inputs=["../outside.txt"])
        with self.assertRaisesRegex(ValueError, "leaves"):
            verify_run(self.root / "manifest.json", self.root / "receipt.json", "reviewer")

    def test_journal_retry_conflict_lock_and_partial_record(self):
        event = {"event_id": "1", "run_id": "case", "phase": "research", "decision": "unknown", "reason": "consensus unavailable", "evidence": "searched declared sources"}
        path = self.root / "journal.jsonl"
        self.assertEqual("RECORDED", journal_append(path, event)["status"])
        first = path.read_bytes()
        self.assertEqual("ALREADY_RECORDED", journal_append(path, event)["status"])
        self.assertEqual(first, path.read_bytes())
        with self.assertRaises(ValueError):
            journal_append(path, {**event, "decision": "changed"})
        lock = path.with_suffix(".jsonl.lock")
        lock.touch()
        with self.assertRaises(FileExistsError):
            journal_append(path, event)
        lock.unlink()
        with path.open("a") as stream:
            stream.write('{"partial":')
        with self.assertRaises(ValueError):
            journal_append(path, {**event, "event_id": "2"})

    def test_checkpoint_pause_resume_cancel_is_terminal(self):
        path = self.root / "checkpoint.json"
        checkpoint(path, "case", "running", "read source")
        checkpoint(path, "case", "paused", "wait for publication")
        self.assertEqual(3, checkpoint(path, "case", "running", "continue")["sequence"])
        checkpoint(path, "case", "cancelled", "stop")
        with self.assertRaises(ValueError):
            checkpoint(path, "case", "running", "continue")
        self.assertEqual("cancelled", json.loads(path.read_text())["status"])


if __name__ == "__main__":
    unittest.main()
