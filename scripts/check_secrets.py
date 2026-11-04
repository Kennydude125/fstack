"""Run the required, redacted Gitleaks checks before publication."""
from pathlib import Path
import argparse
import os
import shutil
import subprocess


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--staged", action="store_true")
    parser.add_argument("--history", action="store_true")
    args = parser.parse_args()
    binary = os.environ.get("GITLEAKS_BIN") or shutil.which("gitleaks")
    if not binary:
        parser.error("Install official Gitleaks v8.30.1 or set GITLEAKS_BIN to its executable.")
    root = Path(__file__).resolve().parents[1]
    modes = []
    if args.staged:
        modes.append(["git", "--pre-commit", "--staged"])
    if args.history:
        modes.append(["git", "--log-opts=--all"])
    if not modes:
        modes.append(["dir"])
    for mode in modes:
        result = subprocess.run([binary, *mode, "--redact=100", "--no-banner", str(root)], cwd=root)
        if result.returncode:
            return result.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
