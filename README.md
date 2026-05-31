# Agent Skill Lint

Lint agent skills and prompt packs for missing boundaries and risky wording.

## Why

Agent skills often ship without clear scope, verification, or destructive-action boundaries.

This is a baseline HighStar AI developer tool: dependency-light, local-first, and built around one quick command.

## Install

```bash
git clone https://github.com/alexzhu0/agent-skill-lint.git
cd agent-skill-lint
PYTHONPATH=src python3 -m unittest discover -s tests
```

## Quickstart

```bash
PYTHONPATH=src python3 -m agent_skill_lint examples/skill.md
```

## Examples

Human-readable output:

```bash
PYTHONPATH=src python3 -m agent_skill_lint examples/skill.md
```

Machine-readable output:

```bash
PYTHONPATH=src python3 -m agent_skill_lint examples/skill.md --format json
```

## CLI Reference

- `PYTHONPATH=src python3 -m agent_skill_lint --help`
- Main demo: `PYTHONPATH=src python3 -m agent_skill_lint examples/skill.md`
- CI gate: `PYTHONPATH=src python3 -m unittest discover -s tests`

## Features

- Required section checks
- Risky wording detection
- Rule IDs and severity
- Fix suggestions
- Text and JSON output

## API

The public Python surface is intentionally small:

```python
from agent_skill_lint.cli import lint_text
```

Use the CLI first. Import the Python functions when you want to embed the same behavior in a larger tool.

## Why Star This

It gives skill authors a lightweight quality gate before sharing prompts or agent packages.

## Roadmap

See [ROADMAP.md](ROADMAP.md).

## FAQ

**Does this call external AI APIs?**

No. The current release uses the Python standard library only.

**Is this production-ready?**

Treat this as a focused utility. Run it in CI or local review first, then adapt thresholds and examples to your workflow.

**Can I contribute examples?**

Yes. The most useful issue or pull request includes a real input file, expected output, and the workflow where it helps.

## Contributing

Issues and pull requests are welcome when they include a concrete use case or failing example.

Run tests before opening a pull request:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests
```

## License

MIT
