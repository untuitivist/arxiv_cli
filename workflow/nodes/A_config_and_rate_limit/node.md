# A_config_and_rate_limit

Goal: initialize local config and confirm safe request spacing before live calls.

Checklist:

- run `arxiv config init` if `local/config.json` does not exist
- set `contact` to an email or project contact string
- confirm `delay_seconds` stays at or above `3.0` for repeated calls
- use `--dry-run` first when validating a new command sequence
