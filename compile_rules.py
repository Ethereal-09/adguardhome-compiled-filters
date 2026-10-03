"""Compile all Excel-selected subscriptions with upstream scope preserved."""
import argparse
from pathlib import Path

from compiler.pipeline import run


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--offline", action="store_true", help="Use verified, unexpired cache; do not refresh timestamps")
    parser.add_argument("--github-api", action="store_true", help="Use authenticated gh CLI for exact GitHub file URLs")
    args = parser.parse_args()
    result = run(Path(__file__).resolve().parent, args.offline, args.github_api)
    print(f"Build {result['status']}; errors: {result['errors']}")
    return 0 if result["status"] == "success" and not result.get("degraded_sources") else 1


if __name__ == "__main__":
    raise SystemExit(main())
