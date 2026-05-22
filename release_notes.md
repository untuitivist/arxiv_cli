# Release v0.2.0

## What's New

- Agent-native layered architecture with 9 abstraction levels
- API inventory inspection and raw endpoint execution
- Structured JSON output with full request/response context
- English/Chinese bilingual documentation
- Workflow nodes for agent guidance
- `--dry-run` support for safe previews
- Local configuration with environment variable overrides
- Shortcut search commands for quick discovery

## Installation

```bash
pip install arxiv-cli
```

## Quick Start

```bash
arxiv --help
arxiv api stats
arxiv find papers "graph neural network" --max-results 5 --format text
```

## Release Checklist

- [x] Update `pyproject.toml` version to 0.2.0
- [x] Run editable install
- [x] Run tests
- [x] Run `python -m build`
- [x] Commit changes
- [x] Create tag v0.2.0
- [x] Push branch and tag
- [x] Publish GitHub Release

## Full Documentation

See [README.md](https://github.com/untuitivist/arxiv_cli/blob/v0.2.0/README.md) for complete documentation in English, or [README_CN.md](https://github.com/untuitivist/arxiv_cli/blob/v0.2.0/README_CN.md) for Chinese.
