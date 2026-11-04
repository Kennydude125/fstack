"""Use python -m fstack_tools --help for the local research commands."""

import argparse
import json
import sys
from .runtime import check_data, check_receipt, checkpoint, journal_append, read_json, verify_run


def main():
    parser = argparse.ArgumentParser(description="Fstack local research checks; no network or brokerage access")
    commands = parser.add_subparsers(dest="command", required=True)
    data = commands.add_parser("check-data")
    data.add_argument("csv")
    data.add_argument("metadata")
    verify = commands.add_parser("verify", help="Execute manifest argv commands without a shell")
    verify.add_argument("manifest")
    verify.add_argument("receipt")
    verify.add_argument("--verifier", required=True)
    receipt = commands.add_parser("check-receipt")
    receipt.add_argument("receipt")
    log = commands.add_parser("log")
    log.add_argument("journal")
    log.add_argument("event")
    state = commands.add_parser("checkpoint")
    state.add_argument("path")
    state.add_argument("--run-id", required=True)
    state.add_argument("--status", choices=["running", "paused", "cancelled", "complete"], required=True)
    state.add_argument("--next", required=True, dest="next_action")
    args = parser.parse_args()
    try:
        if args.command == "check-data":
            result = check_data(args.csv, args.metadata)
        elif args.command == "verify":
            result = verify_run(args.manifest, args.receipt, args.verifier)
        elif args.command == "check-receipt":
            result = check_receipt(args.receipt)
        elif args.command == "log":
            result = journal_append(args.journal, read_json(args.event))
        else:
            result = checkpoint(args.path, args.run_id, args.status, args.next_action)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return {"NOT_VERIFIED": 1, "INCONCLUSIVE": 2}.get(result.get("integrity"), 0)
    except (ValueError, KeyError, TypeError, OSError) as error:
        print(json.dumps({"integrity": "NOT_VERIFIED", "error_type": type(error).__name__, "error": str(error)}))
        return 1


if __name__ == "__main__":
    sys.exit(main())
