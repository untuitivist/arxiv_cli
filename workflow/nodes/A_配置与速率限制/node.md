# A 配置与速率限制

## Goal

Ensure the CLI has a valid local config and respects arXiv public API pacing.

## Inputs

- Optional custom config path
- Optional contact identity for the User-Agent

## Commands

```powershell
arxiv config init
arxiv config show
arxiv config set contact you@example.com
```

## Success Criteria

- `config.json` exists
- `delay_seconds` is set sanely
- contact information is available if needed for identification
