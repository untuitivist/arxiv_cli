from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


def read_json_file(path: str | None) -> dict[str, Any]:
    if not path:
        return {}
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def parse_key_values(items: list[str] | None) -> dict[str, str]:
    parsed: dict[str, str] = {}
    for item in items or []:
        if "=" not in item:
            raise ValueError(f"Expected KEY=VALUE, got: {item}")
        key, value = item.split("=", 1)
        parsed[key] = value
    return parsed


def write_json(payload: Any, output: str | None = None) -> None:
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    write_text(text, output)


def write_text(text: str, output: str | None = None) -> None:
    if output:
        path = Path(output)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text + "\n", encoding="utf-8")
        return
    sys.stdout.buffer.write((text + "\n").encode("utf-8"))
