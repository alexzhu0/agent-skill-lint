"""Lint agent skills and prompt packs for missing boundaries."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Sequence


REQUIRED_HEADINGS = ["Purpose", "Use_When", "Do_Not_Use_When", "Verification"]
RISKY_PATTERNS = [
    ("ASL201", r"\balways\b", "Replace absolute wording with scoped conditions."),
    ("ASL202", r"\bnever ask\b", "Name the exact safe auto-run boundary instead of banning questions."),
    ("ASL203", r"\bignore\b.*\binstruction", "Clarify precedence instead of telling agents to ignore instructions."),
    ("ASL204", r"\bdelete\b.*\bwithout\b", "Require an explicit destructive-action approval rule."),
]


def finding(rule_id: str, severity: str, message: str, suggestion: str) -> Dict[str, str]:
    return {
        "rule_id": rule_id,
        "severity": severity,
        "message": message,
        "suggestion": suggestion,
    }


def lint_text(text: str) -> Dict[str, Any]:
    headings = {line.strip("# <>").strip().lower() for line in text.splitlines() if line.startswith("#") or line.startswith("<")}
    issues = []
    warnings = []
    findings = []
    for heading in REQUIRED_HEADINGS:
        if heading.lower() not in headings:
            message = f"missing section: {heading}"
            issues.append(message)
            findings.append(
                finding("ASL101", "error", message, f"Add a `{heading}` section with concrete boundaries.")
            )
    for rule_id, pattern, suggestion in RISKY_PATTERNS:
        if re.search(pattern, text, flags=re.IGNORECASE | re.DOTALL):
            message = f"risky wording matched: {pattern}"
            warnings.append(message)
            findings.append(finding(rule_id, "warning", message, suggestion))
    if "test" not in text.lower() and "verify" not in text.lower():
        message = "missing explicit test or verification guidance"
        issues.append(message)
        findings.append(
            finding("ASL102", "error", message, "Add a command or checklist that proves the skill works.")
        )
    return {"issues": issues, "warnings": warnings, "findings": findings}


def run(input_path: str, output_format: str = "text") -> str:
    result = lint_text(Path(input_path).read_text(encoding="utf-8"))
    if output_format == "json":
        return json.dumps(result, indent=2, sort_keys=True)
    lines = [f"Issues: {len(result['issues'])}", f"Warnings: {len(result['warnings'])}", ""]
    for item in result["findings"]:
        lines.append(
            f"- [{item['severity']}] {item['rule_id']}: {item['message']} "
            f"Fix: {item['suggestion']}"
        )
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
