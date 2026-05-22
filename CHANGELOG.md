# Changelog

## 0.2.0

- Upgrade the project to the layered `api-cli-builder` architecture with explicit resource, shortcut, workflow, safety, output, and config boundaries.
- Add `query run` as a 1:1 `/api/query` resource command.
- Add `find papers` as a shortcut search command for free-text literature discovery.
- Add `workflow list` and `workflow show` for bundled workflow notes.
- Add `--dry-run` request preview and `--format text` output mode across the main command groups.
- Add environment-variable config overrides and bump the CLI package version to `0.2.0`.

## 0.1.0

- Bootstrap standalone `arxiv_cli` project structure under the source tree.
- Add `config`, `docs`, `search`, and `paper` command groups.
- Add bundled command docs, workflow notes, and smoke tests.
