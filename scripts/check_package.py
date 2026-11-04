#!/usr/bin/env python3
"""Check the actual skill package, local references, and pinned adaptation map."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote

PINNED_COMMIT = "c742dd61706fbacc1b95f1a20b7b988cf096ce6c"
TREATMENTS = {"preserve", "adapt", "development-only", "omit"}


def inside(root: Path, relative: str) -> Path:
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError(f"Path leaves package: {relative}")
    return path


def frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)", text, re.S)
    if not match:
        raise ValueError(f"{path}: missing YAML frontmatter")
    fields = {}
    for line in match.group(1).splitlines():
        item = re.match(r"^([a-z][a-z_-]*):\s*(.*)$", line)
        if item:
            fields[item[1]] = item[2].strip().strip("\"'")
    for key in ("name", "description"):
        if not fields.get(key):
            raise ValueError(f"{path}: missing {key}")
    name = fields["name"]
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 64:
        raise ValueError(f"{path}: invalid skill name")
    return fields


def prose(text: str) -> str:
    return re.sub(r"(?ms)^\s*(`{3,}|~{3,}).*?^\s*\1\s*$", "", text)


def check_links(root: Path) -> list[str]:
    errors = []
    for path in sorted(root.rglob("*.md")):
        if any(part in {".git", ".agents", ".fstack", ".venv", "node_modules"} for part in path.relative_to(root).parts):
            continue
        text = prose(path.read_text(encoding="utf-8"))
        for match in re.finditer(r"\]\((<[^>]+>|[^\s)]+)(?:\s+\"[^\"]*\")?\)", text):
            target = match[1].strip("<>")
            if target.startswith("#") or re.match(r"^[a-z][a-z0-9+.-]*:", target, re.I):
                continue
            target = unquote(target.split("#", 1)[0].split("?", 1)[0])
            if not target:
                continue
            try:
                resolved = inside(root, str(path.parent.relative_to(root) / target))
                if not resolved.exists():
                    errors.append(f"{path.relative_to(root)}: missing link target {target}")
            except ValueError as exc:
                errors.append(f"{path.relative_to(root)}: {exc}")
    return errors


def normalize_source(value: str) -> str:
    return value.removeprefix("pstack/")


def check_mapping(root: Path, lock: dict, registry: dict) -> list[str]:
    errors = []
    if not isinstance(lock, dict) or not isinstance(registry, dict):
        return ["Provenance metadata must be JSON objects"]
    upstream = registry.get("upstream", {})
    if not isinstance(upstream, dict):
        return ["Adaptation upstream metadata must be an object"]
    if upstream.get("commit") != lock.get("commit"):
        errors.append("Adaptation registry commit differs from upstream lock")
    for group in ("skills", "principles", "playbooks"):
        expected = {normalize_source(item if isinstance(item, str) else item["path"]) for item in lock.get(group, [])}
        rows = registry.get(group, [])
        if not isinstance(rows, list):
            errors.append(f"{group}: dispositions must be a list")
            continue
        found = []
        for row in rows:
            if not isinstance(row, dict) or not isinstance(row.get("source"), str):
                errors.append(f"{group}: disposition needs a source string")
                continue
            source = normalize_source(row["source"])
            found.append(source)
            treatment = row.get("treatment")
            if treatment not in TREATMENTS:
                errors.append(f"{group}/{source}: invalid treatment")
            if not isinstance(row.get("reason"), str) or not row["reason"].strip():
                errors.append(f"{group}/{source}: missing disposition reason")
            target = row.get("target")
            if treatment != "omit":
                if not isinstance(target, str) or not target:
                    errors.append(f"{group}/{source}: missing target")
                    continue
                try:
                    if not inside(root, target).exists():
                        errors.append(f"{group}/{source}: missing target {target}")
                except ValueError as exc:
                    errors.append(str(exc))
        if len(found) != len(set(found)):
            errors.append(f"{group}: duplicate upstream source")
        for missing in sorted(expected - set(found)):
            errors.append(f"{group}: missing upstream disposition {missing}")
        for extra in sorted(set(found) - expected):
            errors.append(f"{group}: unknown upstream source {extra}")
    return errors


def check_package(root: Path) -> list[str]:
    root = root.resolve()
    errors = []
    skill_paths = sorted((root / "skills").glob("*/SKILL.md"))
    if not skill_paths:
        errors.append("No active skills found")
    for path in skill_paths:
        try:
            metadata = frontmatter(path)
            if metadata["name"] != path.parent.name:
                errors.append(f"{path.relative_to(root)}: name differs from folder")
            if metadata["name"] != "fstack" and not metadata["name"].startswith("fstack-"):
                errors.append(f"{path.relative_to(root)}: missing fstack namespace")
            if "disable-model-invocation" in metadata:
                errors.append(f"{path.relative_to(root)}: unsupported Cursor invocation field")
            for line in path.read_text(encoding="utf-8").splitlines():
                if re.search(r"\b(?:never|do not|unsupported|original|upstream|historical|mapping|maps)\b", line, re.I):
                    continue
                if re.search(r"~[/\\]\.cursor[/\\]|\b(?:Task|AskQuestion)\s*\(|subagent_type\s*:\s*[\"'](?:poteto-agent|generalPurpose)", line):
                    errors.append(f"{path.relative_to(root)}: unadapted Cursor instruction: {line[:100]}")
        except (ValueError, OSError) as exc:
            errors.append(str(exc))
    errors.extend(check_links(root))
    try:
        lock = json.loads((root / "upstream-lock.json").read_text(encoding="utf-8"))
        registry = json.loads((root / "docs/upstream-map.json").read_text(encoding="utf-8"))
        if not isinstance(lock, dict):
            raise ValueError("Upstream lock must be a JSON object")
        if lock.get("commit") != PINNED_COMMIT:
            errors.append("Unexpected upstream commit")
        for group, count in (("skills", 58), ("principles", 24), ("playbooks", 23)):
            if len(lock.get(group, [])) != count:
                errors.append(f"Upstream lock must enumerate {count} {group}")
        if len(lock.get("pstack_files", [])) != 573:
            errors.append("Upstream lock must enumerate all 573 pstack files")
        errors.extend(check_mapping(root, lock, registry))
    except (OSError, ValueError, TypeError, KeyError) as exc:
        errors.append(f"Invalid provenance metadata: {exc}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    errors = check_package(args.root)
    for error in errors:
        print(f"FAIL {error}")
    if errors:
        print(f"{len(errors)} package issues")
        return 1
    print("PASS: skills, local references, namespace, and upstream dispositions")
    return 0


if __name__ == "__main__":
    sys.exit(main())
