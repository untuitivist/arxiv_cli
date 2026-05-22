from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .paths import DEFAULT_CONFIG_PATH


DEFAULT_CONFIG: dict[str, Any] = {
    "base_url": "https://export.arxiv.org/api/query",
    "tool": "arxiv-cli",
    "contact": "",
    "delay_seconds": 3.0,
    "timeout_seconds": 30.0,
}


class ConfigStore:
    def __init__(self, path: str | None = None) -> None:
        self.path = Path(path) if path else DEFAULT_CONFIG_PATH

    def init(self, force: bool = False) -> bool:
        if self.path.exists() and not force:
            return False
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(DEFAULT_CONFIG, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return True

    def load(self) -> dict[str, Any]:
        if not self.path.exists():
            return dict(DEFAULT_CONFIG)
        data = json.loads(self.path.read_text(encoding="utf-8-sig"))
        merged = dict(DEFAULT_CONFIG)
        merged.update(data)
        return merged

    def save(self, config: dict[str, Any]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def get(self, key: str) -> Any:
        return self.load().get(key)

    def set(self, key: str, raw_value: str) -> Any:
        config = self.load()
        value: Any = raw_value
        lower = raw_value.lower()
        if lower in {"true", "false"}:
            value = lower == "true"
        else:
            try:
                value = int(raw_value)
            except ValueError:
                try:
                    value = float(raw_value)
                except ValueError:
                    value = raw_value
        config[key] = value
        self.save(config)
        return value
