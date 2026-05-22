# local

Local runtime files for `arxiv-cli`.

Expected contents:

- `config.json`: CLI configuration written by `arxiv config init`
- `state/last_request_at.txt`: timestamp cache used to maintain request spacing
- ad hoc query outputs written with `--output`

Keep this directory machine-local.
