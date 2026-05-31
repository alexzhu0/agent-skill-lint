"""Lint agent skills and prompt packs for missing boundaries."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Dict, List, Sequence


REQUIRED_HEADINGS = ["Purpose", "Use_When", "Do_Not_Use_When", "Verification"]
RISKY_PATTERNS = [r"\balways\b", r"\bnever ask\b", r"\bignore\b.*\binstruction", r"\bdelete\b.*\bwithout\b"]


def lint_text(text: str) -> Dict[str, List[str]]:
    headings = {line.strip("# <>").strip().lower() for line in text.splitlines() if line.startswith("#") or line.startswith("<")}
    issues = []
    warnings = []
    for heading in REQUIRED_HEADINGS:
        if heading.lower() not in headings:
            issues.append(f"missing section: {heading}")
    for pattern in RISKY_PATTERNS:
        if re.search(pattern, text, flags=re.IGNORECASE | re.DOTALL):
            warnings.append(f"risky wording matched: {pattern}")
    if "test" not in text.lower() and "verify" not in text.lower():
        issues.append("missing explicit test or verification guidance")
    return {"issues": issues, "warnings": warnings}


def run(input_path: str, output_format: str = "text") -> str:
    result = lint_text(Path(input_path).read_text(encoding="utf-8"))
    if output_format == "json":
        return json.dumps(result, indent=2, sort_keys=True)
    lines = [f"Issues: {len(result['issues'])}", f"Warnings: {len(result['warnings'])}", ""]
    lines.extend(f"- {item}" for item in result["issues"] + result["warnings"])
    return "\n".join(lines).rstrip()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Lint agent skills and prompt packs for missing boundaries.")
    parser.add_argument("input", help="Markdown skill or prompt pack")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    print(run(args.input, args.format))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
