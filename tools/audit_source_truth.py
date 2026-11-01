from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "content" / "source-truth.json"


def git_head(path: Path) -> str:
    result = subprocess.run(
        ["git", "-C", str(path), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def main() -> int:
    parser = argparse.ArgumentParser(description="Detect implementation drift after the public-site audit.")
    parser.add_argument(
        "--source-root",
        type=Path,
        default=ROOT.parent,
        help="Directory containing the authoritative ContextWeaver repositories.",
    )
    args = parser.parse_args()

    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    missing: list[str] = []
    drifted: list[tuple[str, str, str]] = []
    checked = 0

    for repository, audited_head in ledger["sources"].items():
        path = args.source_root / repository
        if not (path / ".git").exists():
            missing.append(repository)
            continue
        checked += 1
        current_head = git_head(path)
        if current_head != audited_head:
            drifted.append((repository, audited_head, current_head))

    print(f"Checked {checked} authoritative repositories.")
    if missing:
        print("Skipped unavailable repositories: " + ", ".join(missing))
    for repository, audited_head, current_head in drifted:
        print(f"DRIFT {repository}: audited {audited_head[:12]}, current {current_head[:12]}")
    if drifted:
        print("Review the implementation changes, update public claims, then refresh content/source-truth.json.")
        return 1
    print("Source-truth revisions match the audited public-site baseline.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
