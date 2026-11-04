"""Small, local research validators and append-only records. No network or broker I/O."""

from __future__ import annotations

import csv
import hashlib
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from datetime import date, datetime, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

MARKETS = {"US": ("USD", "America/New_York", {"XNYS", "XNAS"}),
           "HK": ("HKD", "Asia/Hong_Kong", {"XHKG"})}
THESIS = {"unknown", "supported", "contradicted", "mixed"}
PERFORMANCE = {"none", "development", "untouched_evaluation", "prospective_simulation"}


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def digest(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def stamp(value):
    result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if result.tzinfo is None or result.utcoffset() is None:
        raise ValueError("timestamp requires UTC offset")
    return result


def now():
    return datetime.now(timezone.utc).isoformat()


def inside(root, value):
    path = (root / value).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError("artifact path leaves research root")
    return path


def atomic_json(path, value, *, exclusive=False):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
    if exclusive:
        with path.open("x", encoding="utf-8") as stream:
            stream.write(text)
            stream.flush()
            os.fsync(stream.fileno())
        return
    handle, temporary = tempfile.mkstemp(prefix=".fstack-", dir=path.parent)
    try:
        with os.fdopen(handle, "w", encoding="utf-8") as stream:
            stream.write(text)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def outcome(issues, *, scope):
    integrity = "VERIFIED"
    if issues:
        integrity = "NOT_VERIFIED" if any(i["severity"] == "error" for i in issues) else "INCONCLUSIVE"
    return {"integrity": integrity, "issues": issues, "scope": scope}


def check_data(csv_path, metadata_path):
    """Validate raw daily bars against a supplied, explicitly bounded session calendar."""
    issues = []

    def issue(code, detail, severity="error"):
        issues.append({"code": code, "detail": detail, "severity": severity})

    try:
        meta = read_json(metadata_path)
        if not isinstance(meta, dict):
            raise ValueError("Metadata must be a JSON object")
        required = {"schema_version", "market", "venue", "symbol", "currency", "timezone",
                    "as_of", "price_basis", "price_unit", "corporate_actions", "cost_bps", "sessions"}
        if not required.issubset(meta):
            issue("missing_metadata", ", ".join(sorted(required - meta.keys())), "unknown")
            return outcome(issues, scope="daily-bar input contract; source authenticity not checked")
        if meta["schema_version"] != 1:
            issue("schema_version", "Only schema_version 1 is supported", "unknown")
        if meta["market"] not in MARKETS:
            issue("market", "Only declared US/HK equity fixtures are supported", "unknown")
            return outcome(issues, scope="daily-bar input contract")
        currency, timezone_name, venues = MARKETS[meta["market"]]
        if meta["currency"] != currency or meta["timezone"] != timezone_name or meta["venue"] not in venues:
            issue("market_identity", "Market, venue, currency and timezone disagree")
        if not isinstance(meta["symbol"], str) or not meta["symbol"].strip():
            issue("symbol", "A nonempty instrument identifier is required")
        if meta["price_basis"] != "raw":
            issue("price_basis", "Only raw prices with explicit actions are supported", "unknown")
        if meta["price_unit"] != "currency_per_share":
            issue("price_unit", "Only currency_per_share prices are supported", "unknown")
        if meta["corporate_actions"] != "explicit_split_and_cash_dividend":
            issue("corporate_actions", "Declare explicit_split_and_cash_dividend", "unknown")
        if isinstance(meta["cost_bps"], bool) or not isinstance(meta["cost_bps"], (int, float)) or not math.isfinite(meta["cost_bps"]) or meta["cost_bps"] < 0:
            issue("costs", "cost_bps must be a finite nonnegative number")
        zone = ZoneInfo(timezone_name)
        cutoff = stamp(meta["as_of"])
        sessions = {}
        previous = None
        for item in meta["sessions"]:
            local_date = date.fromisoformat(item["date"])
            opened, closed = stamp(item["open_at"]), stamp(item["close_at"])
            if previous is not None and local_date <= previous:
                issue("calendar_order", "Calendar dates must be unique and increasing")
            previous = local_date
            if opened >= closed or opened.astimezone(zone).date() != local_date or closed.astimezone(zone).date() != local_date:
                issue("calendar_session", f"Invalid session {local_date}")
            for value in (opened, closed):
                if value.utcoffset() != value.astimezone(zone).utcoffset():
                    issue("calendar_timezone", f"Offset disagrees with timezone on {local_date}")
            sessions[item["date"]] = (opened, closed)
        if not sessions:
            issue("empty_calendar", "No declared sessions")
        with Path(csv_path).open(newline="", encoding="utf-8-sig") as stream:
            reader = csv.DictReader(stream)
            columns = {"session", "symbol", "currency", "open", "close", "split_ratio", "dividend", "available_at"}
            if not columns.issubset(reader.fieldnames or []):
                issue("missing_columns", ", ".join(sorted(columns - set(reader.fieldnames or []))), "unknown")
                return outcome(issues, scope="daily-bar input contract")
            rows = list(reader)
        if not rows:
            issue("empty_data", "No price observations")
        previous = None
        for number, row in enumerate(rows, 2):
            prefix = f"CSV row {number}"
            session_date = date.fromisoformat(row["session"])
            if previous is not None and session_date <= previous:
                issue("observation_order", f"{prefix}: duplicate or unsorted session")
            previous = session_date
            if row["session"] not in sessions:
                issue("unknown_session", f"{prefix}: not in declared calendar")
                continue
            if row["symbol"] != meta["symbol"] or row["currency"] != meta["currency"]:
                issue("instrument_identity", f"{prefix}: symbol/currency mismatch")
            values = [float(row[key]) for key in ("open", "close", "split_ratio", "dividend")]
            if not all(math.isfinite(v) for v in values) or min(values[:3]) <= 0 or values[3] < 0:
                issue("numeric_domain", f"{prefix}: invalid price, action or dividend")
            available = stamp(row["available_at"])
            if available < sessions[row["session"]][1]:
                issue("premature_bar", f"{prefix}: daily close known before session closes")
            if available > cutoff:
                issue("future_information", f"{prefix}: available after as_of")
            signal, execution = row.get("signal_at", ""), row.get("execute_at", "")
            if bool(signal) != bool(execution):
                issue("execution_pair", f"{prefix}: signal_at and execute_at must both be present")
            elif signal:
                signaled, executed = stamp(signal), stamp(execution)
                later = [v[0] for v in sessions.values() if v[0] > signaled]
                if signaled < available or not later or executed != min(later):
                    issue("execution_timing", f"{prefix}: requires first declared session open after information availability")
        if {r["session"] for r in rows} != set(sessions):
            issue("calendar_coverage", "Each declared session must have exactly one bar")
    except ZoneInfoNotFoundError:
        issue("timezone_database", "Install/provide an IANA timezone database; no timezone validation occurred", "unknown")
    except (ValueError, TypeError, KeyError, OSError, csv.Error) as error:
        issue("invalid_input", f"{type(error).__name__}: {error}")
    return outcome(issues, scope="raw daily bars, supplied calendar, declared actions and timestamps; source authenticity and calendar completeness outside the declared range are not checked")


def _manifest(path, verifier):
    manifest = read_json(path)
    root = Path(path).resolve().parent
    required = {"schema_version", "run_id", "author", "as_of", "inputs", "outputs", "checks", "thesis_support", "performance_evidence"}
    if not isinstance(manifest, dict) or not required.issubset(manifest):
        raise ValueError("Manifest is missing required fields")
    if manifest["schema_version"] != 1 or not manifest["run_id"] or not manifest["author"]:
        raise ValueError("Invalid manifest identity/version")
    if not verifier or verifier == manifest["author"]:
        raise ValueError("Verifier must be identified and distinct from author; identity is operator-attested")
    stamp(manifest["as_of"])
    if manifest["thesis_support"] not in THESIS or manifest["performance_evidence"] not in PERFORMANCE:
        raise ValueError("Invalid thesis/performance classification")
    for key in ("inputs", "outputs", "checks"):
        if not isinstance(manifest[key], list) or not manifest[key]:
            raise ValueError(f"{key} must be a nonempty list")
    inputs = [inside(root, p) for p in manifest["inputs"]]
    outputs = [inside(root, p) for p in manifest["outputs"]]
    if len(set(inputs + outputs)) != len(inputs + outputs):
        raise ValueError("Inputs/outputs must be unique and disjoint")
    if Path(path).resolve() in outputs:
        raise ValueError("Manifest cannot be an output")
    for input_path in inputs:
        if not input_path.is_file() or not input_path.stat().st_size:
            raise ValueError("All input files must exist and be nonempty")
    for check in manifest["checks"]:
        if not isinstance(check, dict) or not check.get("name") or not isinstance(check.get("argv"), list) or not check["argv"] or not all(isinstance(a, str) and a for a in check["argv"]):
            raise ValueError("Each check needs name and nonempty argv strings")
        if not check.get("expected_outputs") or not set(check["expected_outputs"]).issubset(manifest["outputs"]):
            raise ValueError("Each check must declare its expected outputs")
        if not 0 < check.get("timeout_seconds", 60) <= 300:
            raise ValueError("Check timeout must be between 0 and 300 seconds")
        if check["argv"][0] != "{python}" or len(check["argv"]) < 2:
            raise ValueError("Version 1 checks run explicit {python} scripts or inline -c code only")
        if check["argv"][1] not in {"-c", "-m"}:
            script = inside(root, check["argv"][1])
            if script not in inputs:
                raise ValueError("Check script must be a fingerprinted input")
        elif check["argv"][1] == "-m":
            raise ValueError("Module checks need an explicit script entrypoint in version 1")
        code_inputs = check.get("code_inputs", [])
        if not isinstance(code_inputs, list) or not set(code_inputs).issubset(manifest["inputs"]):
            raise ValueError("code_inputs must be a subset of fingerprinted inputs")
        if check["argv"][1] != "-c" and check["argv"][1] not in code_inputs:
            raise ValueError("Script entrypoint must be declared in code_inputs")
        for argument in check["argv"][1:]:
            if argument.endswith((".py", ".js", ".mjs", ".sh", ".ps1")):
                script = inside(root, argument)
                if script not in inputs:
                    raise ValueError("Every script argument must be a fingerprinted input")
    expected = [p for check in manifest["checks"] for p in check["expected_outputs"]]
    if len(set(expected)) != len(expected) or set(expected) != set(manifest["outputs"]):
        raise ValueError("Exactly one check must own each output")
    for dataset in manifest.get("datasets", []):
        if not {dataset["csv"], dataset["metadata"]}.issubset(manifest["inputs"]):
            raise ValueError("Dataset CSV and metadata must be fingerprinted inputs")
        if stamp(read_json(inside(root, dataset["metadata"]))["as_of"]) != stamp(manifest["as_of"]):
            raise ValueError("Dataset and run as_of must agree")
    if manifest["performance_evidence"] != "none":
        protocol = manifest.get("evaluation", {})
        if not {"development_end", "evaluation_start", "evaluation_end", "frozen_at", "attempt_log"}.issubset(protocol):
            raise ValueError("Performance evidence needs a dated evaluation protocol and attempt log")
        if protocol["attempt_log"] not in manifest["inputs"]:
            raise ValueError("Attempt log must be a fingerprinted input")
        if not stamp(protocol["development_end"]) < stamp(protocol["evaluation_start"]) <= stamp(protocol["evaluation_end"]) <= stamp(manifest["as_of"]):
            raise ValueError("Evaluation dates overlap or exceed cutoff")
        attempts = read_json(inside(root, protocol["attempt_log"]))
        if not isinstance(attempts, list) or not attempts:
            raise ValueError("Attempt log must be a nonempty JSON array")
        if manifest["performance_evidence"] == "untouched_evaluation" and any(a.get("evaluation_used_for_tuning") is not False for a in attempts):
            raise ValueError("Evaluation used/unknown for tuning cannot be called untouched")
        if stamp(protocol["frozen_at"]) > stamp(protocol["evaluation_start"]) and manifest["performance_evidence"] == "prospective_simulation":
            raise ValueError("Prospective protocol was not frozen before evaluation started")
    return manifest, root, inputs, outputs


def verify_run(manifest_path, receipt_path, verifier):
    """Execute explicitly requested local argv commands. Never invokes a shell."""
    manifest_path, receipt_path = Path(manifest_path).resolve(), Path(receipt_path).resolve()
    if receipt_path.exists():
        raise FileExistsError("Receipts are immutable; choose a new receipt path")
    manifest, root, inputs, outputs = _manifest(manifest_path, verifier)
    if receipt_path in inputs + outputs or receipt_path == manifest_path:
        raise ValueError("Receipt must be separate from all artifacts")
    if any(p.exists() for p in outputs):
        raise ValueError("Outputs must be fresh; existing artifacts cannot prove a new execution")
    fingerprints = {p.relative_to(root).as_posix(): digest(p) for p in inputs}
    manifest_hash = digest(manifest_path)
    dataset_results = [check_data(inside(root, d["csv"]), inside(root, d["metadata"])) for d in manifest.get("datasets", [])]
    checks = []
    checked_outputs = {}
    status = "VERIFIED"
    if any(r["integrity"] != "VERIFIED" for r in dataset_results):
        status = "NOT_VERIFIED" if any(r["integrity"] == "NOT_VERIFIED" for r in dataset_results) else "INCONCLUSIVE"
    if status == "VERIFIED":
        for check in manifest["checks"]:
            argv = [sys.executable if arg == "{python}" else arg for arg in check["argv"]]
            for output in check["expected_outputs"]:
                inside(root, output).parent.mkdir(parents=True, exist_ok=True)
            record = {"name": check["name"]}
            try:
                process = subprocess.run(argv, cwd=root, stdin=subprocess.DEVNULL, capture_output=True, timeout=check.get("timeout_seconds", 60), shell=False)
                record.update(returncode=process.returncode,
                              stdout_sha256=hashlib.sha256(process.stdout).hexdigest(),
                              stderr_sha256=hashlib.sha256(process.stderr).hexdigest())
                produced = all(inside(root, p).is_file() and inside(root, p).stat().st_size for p in check["expected_outputs"])
                record["status"] = "VERIFIED" if process.returncode == 0 and produced else "NOT_VERIFIED"
                if record["status"] == "VERIFIED":
                    checked_outputs.update({p: digest(inside(root, p)) for p in check["expected_outputs"]})
            except (subprocess.TimeoutExpired, OSError) as error:
                record.update(status="INCONCLUSIVE", reason=type(error).__name__)
            checks.append(record)
            if record["status"] != "VERIFIED":
                status = record["status"]
                break
    artifacts = {p.relative_to(root).as_posix(): digest(p) for p in outputs if p.is_file()}
    if any(artifacts.get(p) != value for p, value in checked_outputs.items()):
        status = "NOT_VERIFIED"
        checks.append({"name": "output_immutability", "status": "NOT_VERIFIED"})
    if digest(manifest_path) != manifest_hash or any(not (root / name).is_file() or digest(root / name) != value for name, value in fingerprints.items()):
        status = "NOT_VERIFIED"
        checks.append({"name": "input_immutability", "status": "NOT_VERIFIED"})
    receipt = {"schema_version": 1, "run_id": manifest["run_id"], "created_at": now(),
               "root": str(root), "manifest": manifest_path.name, "manifest_sha256": manifest_hash,
               "author": manifest["author"], "verifier": verifier, "identity_assurance": "operator_attested",
               "integrity": status, "thesis_support": manifest["thesis_support"],
               "performance_evidence": manifest["performance_evidence"], "inputs": fingerprints,
               "outputs": artifacts, "checks": checks, "dataset_checks": dataset_results,
               "python_version": sys.version, "tool_sha256": digest(Path(__file__)),
               "scope": "Declared local checks only. Does not authenticate sources, verifier identity, economic truth or future returns."}
    atomic_json(receipt_path, receipt, exclusive=True)
    return receipt


def check_receipt(receipt_path):
    receipt = read_json(receipt_path)
    root = Path(receipt["root"]).resolve()
    issues = []
    manifest_path = inside(root, receipt["manifest"])
    manifest, _, inputs, outputs = _manifest(manifest_path, receipt.get("verifier"))
    if receipt.get("schema_version") != 1 or receipt.get("author") != manifest["author"] or receipt.get("run_id") != manifest["run_id"]:
        issues.append({"code": "receipt_identity", "detail": "Receipt identity/schema disagrees with manifest", "severity": "error"})
    if receipt.get("integrity") not in {"VERIFIED", "NOT_VERIFIED", "INCONCLUSIVE"}:
        issues.append({"code": "receipt_integrity", "detail": "Unknown integrity state", "severity": "error"})
    if any(receipt.get(field) != manifest[field] for field in ("thesis_support", "performance_evidence")):
        issues.append({"code": "assessment_mismatch", "detail": "Receipt assessments disagree with manifest", "severity": "error"})
    if set(receipt.get("inputs", {})) != {p.relative_to(root).as_posix() for p in inputs}:
        issues.append({"code": "input_coverage", "detail": "Receipt omits or adds inputs", "severity": "error"})
    if receipt.get("integrity") == "VERIFIED":
        declared = manifest["checks"]
        actual = receipt.get("checks", [])
        if len(actual) != len(declared) or any(record.get("name") != expected["name"] or record.get("status") != "VERIFIED" or record.get("returncode") != 0 for record, expected in zip(actual, declared)):
            issues.append({"code": "check_coverage", "detail": "Successful receipt needs every declared successful command", "severity": "error"})
        if set(receipt.get("outputs", {})) != {p.relative_to(root).as_posix() for p in outputs}:
            issues.append({"code": "output_coverage", "detail": "Successful receipt needs every declared output", "severity": "error"})
        datasets = receipt.get("dataset_checks", [])
        if len(datasets) != len(manifest.get("datasets", [])) or any(d.get("integrity") != "VERIFIED" for d in datasets):
            issues.append({"code": "dataset_coverage", "detail": "Successful receipt needs every dataset check", "severity": "error"})
    if receipt.get("tool_sha256") != digest(Path(__file__)):
        issues.append({"code": "stale_tool", "detail": "Verifier implementation changed", "severity": "error"})
    items = {receipt["manifest"]: receipt["manifest_sha256"], **receipt.get("inputs", {}), **receipt.get("outputs", {})}
    for name, expected in items.items():
        path = inside(root, name)
        if not path.is_file() or digest(path) != expected:
            issues.append({"code": "stale_artifact", "detail": name, "severity": "error"})
    result = outcome(issues, scope="Receipt artifact identity; receipt authenticity is not cryptographically attested")
    result["recorded_integrity"] = receipt["integrity"]
    if result["integrity"] == "VERIFIED" and receipt["integrity"] != "VERIFIED":
        result["integrity"] = receipt["integrity"]
    return result


def journal_append(path, event):
    path = Path(path)
    required = {"event_id", "run_id", "phase", "decision", "reason", "evidence"}
    if not isinstance(event, dict) or not required.issubset(event) or not all(isinstance(event[k], str) and event[k].strip() for k in required):
        raise ValueError("Event requires nonempty event_id, run_id, phase, decision, reason, evidence strings")
    if "recorded_at" in event:
        raise ValueError("recorded_at is assigned by the journal")
    path.parent.mkdir(parents=True, exist_ok=True)
    lock = path.with_suffix(path.suffix + ".lock")
    descriptor = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    try:
        os.close(descriptor)
        if path.exists():
            raw = path.read_bytes()
            if raw and not raw.endswith(b"\n"):
                raise ValueError("Journal has an incomplete final line; preserve it for explicit recovery")
            for line in path.read_text(encoding="utf-8").splitlines():
                old = json.loads(line)
                if (old["run_id"], old["event_id"]) == (event["run_id"], event["event_id"]):
                    if {k: v for k, v in old.items() if k != "recorded_at"} != event:
                        raise ValueError("Event ID already exists with different content")
                    return {"status": "ALREADY_RECORDED", "event_id": event["event_id"]}
        record = {**event, "recorded_at": now()}
        with path.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(record, ensure_ascii=False, allow_nan=False) + "\n")
            stream.flush()
            os.fsync(stream.fileno())
        return {"status": "RECORDED", "event_id": event["event_id"]}
    finally:
        lock.unlink()


def checkpoint(path, run_id, status, next_action):
    transitions = {"running": {"running", "paused", "cancelled", "complete"},
                   "paused": {"paused", "running", "cancelled"},
                   "cancelled": {"cancelled"}, "complete": {"complete"}}
    if status not in transitions or not run_id or not next_action:
        raise ValueError("Checkpoint needs run_id, valid status and next action")
    path = Path(path)
    sequence = 1
    if path.exists():
        previous = read_json(path)
        if previous["run_id"] != run_id or status not in transitions[previous["status"]]:
            raise ValueError("Invalid checkpoint transition or different run ID")
        sequence = previous["sequence"] + 1
    result = {"schema_version": 1, "run_id": run_id, "status": status, "sequence": sequence,
              "next_action": next_action, "updated_at": now(),
              "scope": "Records coordinator state; does not terminate worker processes or certify completion."}
    atomic_json(path, result)
    return result
