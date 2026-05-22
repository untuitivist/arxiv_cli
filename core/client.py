from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any

import requests

from .config_store import ConfigStore
from .feed import parse_feed
from .paths import DEFAULT_STATE_PATH
from .registry import Endpoint


class ArxivRateLimitError(RuntimeError):
    """Raised when arXiv reports a rate-limit response."""


@dataclass
class ClientSettings:
    base_url: str
    tool: str
    contact: str
    delay_seconds: float
    timeout_seconds: float


@dataclass
class PreparedRequest:
    endpoint: str
    method: str
    url: str
    params: dict[str, Any]
    data: dict[str, Any] | None
    headers: dict[str, str]


class ArxivClient:
    def __init__(self, settings: ClientSettings, state_path=DEFAULT_STATE_PATH) -> None:
        self.settings = settings
        self.state_path = state_path

    @classmethod
    def from_args(cls, args: Any) -> "ArxivClient":
        store = ConfigStore(getattr(args, "config", None) or getattr(args, "config_path", None))
        config = store.load()
        settings = ClientSettings(
            base_url=str(getattr(args, "base_url", None) or config["base_url"]),
            tool=str(config.get("tool") or "arxiv-cli"),
            contact=str(config.get("contact") or ""),
            delay_seconds=float(getattr(args, "delay_seconds", None) or config["delay_seconds"]),
            timeout_seconds=float(getattr(args, "timeout_seconds", None) or config["timeout_seconds"]),
        )
        return cls(settings)

    def prepare(
        self,
        endpoint: Endpoint,
        method: str,
        *,
        params: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
    ) -> PreparedRequest:
        return PreparedRequest(
            endpoint=endpoint.path,
            method=method.upper(),
            url=self.settings.base_url,
            params=params or {},
            data=data,
            headers={"User-Agent": self._build_user_agent()},
        )

    def call(self, prepared: PreparedRequest, *, parse_atom: bool = True) -> dict[str, Any]:
        self._respect_rate_limit()
        started = time.time()
        response = requests.request(
            prepared.method,
            prepared.url,
            params=prepared.params,
            data=prepared.data,
            headers=prepared.headers,
            timeout=self.settings.timeout_seconds,
        )
        self._remember_request()
        body_text = response.text
        if "Rate exceeded" in body_text:
            raise ArxivRateLimitError("arXiv API rate limit exceeded; wait and retry.")
        elapsed_ms = int((time.time() - started) * 1000)
        parsed_atom: dict[str, Any] | None = None
        parse_error: str | None = None
        if parse_atom and "xml" in response.headers.get("content-type", "").lower():
            try:
                parsed_atom = parse_feed(body_text)
            except Exception as exc:  # pragma: no cover - defensive parsing path
                parse_error = f"{type(exc).__name__}: {exc}"
        return {
            "ok": 200 <= response.status_code < 400,
            "endpoint": prepared.endpoint,
            "request": {
                "method": prepared.method,
                "url": response.url,
                "params": prepared.params,
                "data": prepared.data,
                "headers": prepared.headers,
            },
            "response": {
                "status_code": response.status_code,
                "reason": response.reason,
                "elapsed_ms": elapsed_ms,
                "content_type": response.headers.get("content-type", ""),
                "body_text": body_text,
                "parsed_atom": parsed_atom,
                "parse_error": parse_error,
            },
        }

    def search(
        self,
        *,
        terms: dict[str, list[str] | None],
        start: int,
        max_results: int,
        sort_by: str,
        sort_order: str,
    ) -> dict[str, Any]:
        clauses: list[str] = []
        for field, values in terms.items():
            for value in values or []:
                cleaned = " ".join(value.strip().split())
                if cleaned:
                    clauses.append(f'{field}:"{cleaned}"')
        if not clauses:
            raise ValueError("At least one search term is required.")
        return self.search_raw(
            " AND ".join(clauses),
            start=start,
            max_results=max_results,
            sort_by=sort_by,
            sort_order=sort_order,
        )

    def search_raw(
        self,
        search_query: str,
        *,
        start: int,
        max_results: int,
        sort_by: str,
        sort_order: str,
    ) -> dict[str, Any]:
        params = {
            "search_query": search_query,
            "start": start,
            "max_results": max_results,
            "sortBy": sort_by,
            "sortOrder": sort_order,
        }
        return self._query(params)

    def fetch_by_ids(self, ids: list[str]) -> dict[str, Any]:
        params = {"id_list": ",".join(ids), "start": 0, "max_results": len(ids)}
        return self._query(params)

    def _query(self, params: dict[str, Any]) -> dict[str, Any]:
        prepared = PreparedRequest(
            endpoint="/api/query",
            method="GET",
            url=self.settings.base_url,
            params=params,
            data=None,
            headers={"User-Agent": self._build_user_agent()},
        )
        result = self.call(prepared, parse_atom=True)
        if not result["ok"]:
            response = result["response"]
            raise RuntimeError(f"HTTP {response['status_code']} {response['reason']}")
        payload = result["response"]["parsed_atom"] or {}
        payload["ok"] = True
        payload["request"] = result["request"]
        payload["response"] = {
            "status_code": result["response"]["status_code"],
            "reason": result["response"]["reason"],
            "elapsed_ms": result["response"]["elapsed_ms"],
            "content_type": result["response"]["content_type"],
        }
        return payload

    def _build_user_agent(self) -> str:
        contact = self.settings.contact.strip()
        if contact:
            return f"{self.settings.tool}/0.1.0 ({contact})"
        return f"{self.settings.tool}/0.1.0 (contact-not-set)"

    def _respect_rate_limit(self) -> None:
        last_request_at = self._load_last_request_at()
        if last_request_at is None:
            return
        wait_seconds = self.settings.delay_seconds - (time.time() - last_request_at)
        if wait_seconds > 0:
            time.sleep(wait_seconds)

    def _load_last_request_at(self) -> float | None:
        if not self.state_path.exists():
            return None
        try:
            return float(self.state_path.read_text(encoding="utf-8-sig").strip())
        except ValueError:
            return None

    def _remember_request(self) -> None:
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        self.state_path.write_text(f"{time.time():.6f}\n", encoding="utf-8")
