#!/usr/bin/env python3
"""Install a project-scoped Fstack payload and discoverable skill shims."""
from __future__ import annotations

import argparse
import fnmatch
import os
from pathlib import Path
import sys

from check_package import frontmatter

PAYLOAD_DIRS = {"skills", "agents", "adapters", "references", "templates", "fstack_tools", "scripts", "schemas", "examples", "docs", ".codex-plugin"}
PAYLOAD_FILES = {"upstream-lock.json", "plugin.json", "LICENSE", "NOTICE", "README.md", "pyproject.toml", "fstack.config.example.json", ".gitignore", ".env.example"}
EXCLUDED_PARTS = {"__pycache__", ".fstack", ".git", ".venv", "node_modules", "runs", "logs", "private", "data", "holdings", "trades", "credentials", "secrets", ".ssh", ".aws", ".azure", ".kube"}
PRIVATE_NAMES = (".env", ".env.*", "*.pem", "*.key", "*.p12", "*.pfx",
                 "credentials*.json", "credentials*.yaml", "credentials*.yml",
                 "secrets*.json", "secrets*.yaml", "secrets*.yml", "*.secrets.*", "*.local.json",
                 ".netrc", ".npmrc", ".pypirc", "portfolio*.csv", "holdings*.csv", "transactions*.csv")


def payload_files(source: Path) -> list[Path]:
    files = []
    candidates = [source / name for name in PAYLOAD_FILES if (source / name).is_file()]
    for name in sorted(PAYLOAD_DIRS):
        directory = source / name
        if directory.is_symlink():
            raise ValueError(f"Payload contains a symlink: {name}")
        if not directory.is_dir():
            continue
        for current, folders, names in os.walk(directory, followlinks=False):
            for folder in folders:
                if (Path(current) / folder).is_symlink():
                    raise ValueError(f"Payload contains a symlink: {Path(current) / folder}")
            folders[:] = sorted(folder for folder in folders if folder not in EXCLUDED_PARTS)
            candidates.extend(Path(current) / filename for filename in sorted(names))
    for path in sorted(candidates):
        relative = path.relative_to(source)
        if relative.parts[0] not in PAYLOAD_DIRS and relative.as_posix() not in PAYLOAD_FILES:
            continue
        if any(part in EXCLUDED_PARTS for part in relative.parts) or path.suffix in {".pyc", ".pyo", ".log"}:
            continue
        if path.name != ".env.example" and any(fnmatch.fnmatch(path.name, pattern) for pattern in PRIVATE_NAMES):
            continue
        if path.is_symlink():
            raise ValueError(f"Payload contains a symlink: {relative}")
        files.append(path)
    return files


def installation_plan(source: Path, project: Path) -> dict[Path, bytes]:
    source, project = source.resolve(), project.resolve()
    if not source.is_dir():
        raise ValueError("Source package does not exist")
    payload = (project / ".agents" / "fstack").resolve()
    discovery = (project / ".agents" / "skills").resolve()
    if not payload.is_relative_to(project) or not discovery.is_relative_to(project):
        raise ValueError("Installation target leaves project through a symlink")
    if payload.is_relative_to(source) or source.is_relative_to(payload):
        raise ValueError("Source and installation payload overlap")
    planned = {payload / path.relative_to(source): path.read_bytes() for path in payload_files(source)}
    skills = sorted((source / "skills").glob("*/SKILL.md"))
    if not skills:
        raise ValueError("No skills in source package")
    for path in skills:
        fields = frontmatter(path)
        name = fields["name"]
        if name != path.parent.name or (name != "fstack" and not name.startswith("fstack-")):
            raise ValueError(f"Invalid Fstack skill identity: {name}")
        original = path.read_text(encoding="utf-8")
        header = original.split("---", 2)[1]
        text = (
            f"---{header}---\n\n# {name}\n\n"
            f"Read and follow [the canonical {name} skill](../../fstack/skills/{name}/SKILL.md). "
            "Resolve its references relative to that canonical file, not this discovery shim. "
            "The package root is `../../fstack/` relative to this folder. "
            "Run package commands from that root, or use its absolute path.\n"
        )
        planned[discovery / name / "SKILL.md"] = text.encode("utf-8")
        metadata = path.parent / "agents" / "openai.yaml"
        if metadata.is_file():
            planned[discovery / name / "agents" / "openai.yaml"] = metadata.read_bytes()
    for target, content in planned.items():
        if not target.resolve().is_relative_to(project):
            raise ValueError(f"Target leaves project: {target}")
        if target.exists() and (not target.is_file() or target.read_bytes() != content):
            raise ValueError(f"Existing file differs; installation writes nothing: {target}")
        for ancestor in target.parents:
            if ancestor == project:
                break
            if ancestor.exists() and not ancestor.is_dir():
                raise ValueError(f"A parent path is not a directory: {ancestor}")
    return planned


def install(source: Path, project: Path, *, apply: bool = False) -> tuple[int, int]:
    planned = installation_plan(source, project)
    pending = {path: content for path, content in planned.items() if not path.exists()}
    if apply:
        for path, content in pending.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("xb") as handle:
                handle.write(content)
    return len(planned), len(pending)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path)
    parser.add_argument("--source", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--apply", action="store_true", help="Write files after all collision checks pass")
    args = parser.parse_args()
    try:
        total, pending = install(args.source, args.project, apply=args.apply)
    except (ValueError, OSError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    print(f"{'Installed' if args.apply else 'Dry run'}: {total} files, {pending} new, {total-pending} identical.")
    if not args.apply:
        print("No files written. Add --apply to install.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
