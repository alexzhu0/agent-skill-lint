# Agent Skill Lint

Lint agent skills and prompt packs for missing boundaries and risky wording.

## Why

Agent skills often ship without clear scope, safety boundaries, or tests.

This repository is intentionally small: it should be useful in one command, easy to inspect, and simple to fork.

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

```bash
PYTHONPATH=src python3 -m agent_skill_lint examples/skill.md
```

## API

The first release is CLI-first. Public Python APIs can be added after real usage proves the right shape.

## FAQ

**Does this call external AI APIs?**

No. The generated starter uses the Python standard library only.

**Is this production-ready?**

Treat `v0.1.0` as a focused utility release. Pin versions and review output before adding it to CI.

## Contributing

Issues and pull requests are welcome when they include a concrete use case or failing example.

## License

MIT
