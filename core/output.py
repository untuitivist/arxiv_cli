from __future__ import annotations

import json
from typing import Any

from .io import write_json, write_text


def emit_payload(payload: Any, *, output: str | None = None, fmt: str = "json") -> None:
    if fmt == "text":
        write_text(render_text(payload), output)
        return
    write_json(payload, output)


def render_text(payload: Any) -> str:
    if isinstance(payload, list):
        if all(isinstance(item, dict) and "path" in item for item in payload):
            return "\n".join(_render_endpoint_row(item) for item in payload)
        return json.dumps(payload, ensure_ascii=False, indent=2)

    if not isinstance(payload, dict):
        return str(payload)

    if payload.get("dry_run") and "request" in payload:
        request = payload["request"]
        lines = [
            "DRY RUN",
            f"{request.get('method', 'GET')} {request.get('url', '')}",
        ]
        if request.get("params"):
            lines.append("params: " + json.dumps(request["params"], ensure_ascii=False))
        if request.get("data"):
            lines.append("data: " + json.dumps(request["data"], ensure_ascii=False))
        return "\n".join(lines)

    if "endpoint_count" in payload and "method_counts" in payload:
        counts = ", ".join(f"{method}={count}" for method, count in payload["method_counts"].items())
        return "\n".join(
            [
                f"base_url: {payload.get('base_url', '')}",
                f"endpoint_count: {payload['endpoint_count']}",
                f"method_counts: {counts}",
            ]
        )

    if "nodes" in payload and isinstance(payload["nodes"], list):
        return "\n".join(item.get("node", "") for item in payload["nodes"])

    if "config" in payload and isinstance(payload["config"], dict):
        lines = [f"path: {payload.get('path', '')}"]
        lines.extend(f"{key}={value}" for key, value in payload["config"].items())
        return "\n".join(lines)

    if "entries" in payload and isinstance(payload["entries"], list):
        lines = [
            f"total_results: {payload.get('total_results', len(payload['entries']))}",
            f"start_index: {payload.get('start_index', 0)}",
            f"items_per_page: {payload.get('items_per_page', len(payload['entries']))}",
        ]
        for entry in payload["entries"]:
            lines.append(_render_entry_row(entry))
        return "\n".join(lines)

    if {"path", "methods", "description"}.issubset(payload.keys()):
        lines = [
            f"path: {payload['path']}",
            f"methods: {', '.join(payload['methods'])}",
            f"description: {payload['description']}",
        ]
        if payload.get("params"):
            lines.append("params:")
            for key, meta in payload["params"].items():
                location = ",".join(meta.get("location", []))
                lines.append(f"  {key} [{location}]")
        return "\n".join(lines)

    if payload.get("ok") and "text" in payload:
        return str(payload["text"]).rstrip()

    return json.dumps(payload, ensure_ascii=False, indent=2)


def _render_endpoint_row(item: dict[str, Any]) -> str:
    methods = ",".join(item.get("methods", []))
    description = item.get("description", "")
    return f"{item.get('path', '')} [{methods}] {description}".rstrip()


def _render_entry_row(entry: dict[str, Any]) -> str:
    arxiv_id = entry.get("arxiv_id") or entry.get("id") or "unknown-id"
    title = " ".join(str(entry.get("title", "")).split())
    primary_category = ""
    if isinstance(entry.get("primary_category"), dict):
        primary_category = entry["primary_category"].get("term", "")
    authors = ", ".join(entry.get("authors", []))
    parts = [arxiv_id, title]
    if primary_category:
        parts.append(primary_category)
    if authors:
        parts.append(authors)
    return " | ".join(parts)
