# Contributing

## Development setup

```powershell
python -m pip install -e .
python -m pytest tests -q
```

If you prefer Conda:

```powershell
conda run -n WQBRAIN python -m pip install -e .
conda run -n WQBRAIN python -m pytest tests -q
```

## Conventions

- Keep command outputs structured and JSON-first.
- Do not commit machine-local files under `local/`.
- Prefer adding bundled docs and inventory updates together when changing command behavior.
- Keep tests green before opening a pull request.

## Pull requests

- Describe the user-facing change.
- Mention whether `resources/api_inventory/` was updated.
- Include the validation commands you ran.
