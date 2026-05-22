# arxiv-cli

`arxiv-cli` is an agent-first command line toolkit for querying the public arXiv metadata API.

It is structured as a standalone sibling project to `wqb_cli`, while keeping a similar package layout: command groups under `commands/`, core HTTP and parsing helpers under `core/`, bundled docs under `resources/docs/`, workflow notes under `workflow/`, and subprocess smoke tests under `tests/`.

- API reference: [arXiv API Access](https://info.arxiv.org/help/api/index.html)
- Basics: [arXiv API Basics](https://info.arxiv.org/help/api/basics.html)
- Manual: [arXiv API User's Manual](https://info.arxiv.org/help/api/user-manual.html)
- Terms: [Terms of Use for arXiv APIs](https://info.arxiv.org/help/api/tou.html)

## Design

- Structured JSON output by default, so coding agents can chain results safely.
- Local config and request-rate spacing, matching arXiv's public API guidance.
- Bundled docs that can be inspected through `arxiv docs ...` without opening a browser.
- Minimal but explicit workflow notes under `workflow/` for repeatable paper search and fetch tasks.

## Project Layout

```text
arxiv_cli/
  __main__.py
  __init__.py
  cli.py
  commands/
  core/
  resources/docs/
  workflow/
  local/
  tests/
  pyproject.toml
  README.md
  MANIFEST.in
  CHANGELOG.md
```

## Requirements

- Python 3.11 or newer
- Network access to `https://export.arxiv.org/api/query`

## Installation

From the parent source directory:

```powershell
cd arxiv_cli
python -m pip install -e .
```

Or run directly from the source checkout parent:

```powershell
python -m arxiv_cli --help
```

## Commands

### Config

```powershell
arxiv config init
arxiv config show
arxiv config set contact you@example.com
```

### Docs

```powershell
arxiv docs list
arxiv docs show search/query
```

### Search

```powershell
arxiv search query --all "graph neural network" --category cs.LG --max-results 5
arxiv search raw "au:\"Yann LeCun\" AND cat:cs.LG" --sort-by submittedDate
```

### Fetch by arXiv id

```powershell
arxiv paper get 1706.03762 2401.10401
```

## Local Config

`arxiv config init` writes `local/config.json` by default. The default config contains:

- `base_url`: `https://export.arxiv.org/api/query`
- `tool`: `arxiv-cli`
- `contact`: empty by default, intended to hold an email or project contact
- `delay_seconds`: `3.0`
- `timeout_seconds`: `30.0`

## Notes

- This project is independent and not affiliated with arXiv.
- Commands call the live public API. There is no fake or dry-run mode.
- arXiv returns Atom XML; `arxiv-cli` normalizes the feed into JSON for downstream use.
