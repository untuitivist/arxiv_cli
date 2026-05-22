from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any

import requests

from .. import __version__
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

    def prepare_query_request(
        self,
        *,
        method: str = "GET",
        search_query: str | None = None,
        id_list: list[str] | None = None,
        start: int = 0,
        max_results: int = 10,
        sort_by: str | None = None,
        sort_order: str | None = None,
    ) -> PreparedRequest:
        payload = self._build_query_payload(
            search_query=search_query,
            id_list=id_list,
            start=start,
            max_results=max_results,
            sort_by=sort_by,
            sort_order=sort_order,
        )
        return PreparedRequest(
            endpoint="/api/query",
            method=method.upper(),
            url=self.settings.base_url,
            params=payload if method.upper() == "GET" else {},
            data=payload if method.upper() == "POST" else None,
            headers={"User-Agent": self._build_user_agent()},
        )

    def describe_prepared(self, prepared: PreparedRequest) -> dict[str, Any]:
        return {
            "ok": True,
            "dry_run": True,
            "endpoint": prepared.endpoint,
            "request": {
                "method": prepared.method,
                "url": prepared.url,
                "params": prepared.params,
                "data": prepared.data,
                "headers": prepared.headers,
            },
        }

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
        dry_run: bool = False,
    ) -> dict[str, Any]:
        search_query = self.build_search_query(terms)
        return self.search_raw(
            search_query,
            start=start,
            max_results=max_results,
            sort_by=sort_by,
            sort_order=sort_order,
            dry_run=dry_run,
        )

    def search_raw(
        self,
        search_query: str,
        *,
        start: int,
        max_results: int,
        sort_by: str,
        sort_order: str,
        dry_run: bool = False,
        method: str = "GET",
    ) -> dict[str, Any]:
        return self.run_query(
            search_query=search_query,
            start=start,
            max_results=max_results,
            sort_by=sort_by,
            sort_order=sort_order,
            dry_run=dry_run,
            method=method,
        )

    def fetch_by_ids(self, ids: list[str], *, dry_run: bool = False, method: str = "GET") -> dict[str, Any]:
        return self.run_query(id_list=ids, start=0, max_results=len(ids), dry_run=dry_run, method=method)

    def run_query(
        self,
        *,
        search_query: str | None = None,
        id_list: list[str] | None = None,
        start: int = 0,
        max_results: int = 10,
        sort_by: str | None = None,
        sort_order: str | None = None,
        dry_run: bool = False,
        method: str = "GET",
    ) -> dict[str, Any]:
        prepared = self.prepare_query_request(
            method=method,
            search_query=search_query,
            id_list=id_list,
            start=start,
            max_results=max_results,
            sort_by=sort_by,
            sort_order=sort_order,
        )
        if dry_run:
            return self.describe_prepared(prepared)
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

    def build_search_query(self, terms: dict[str, list[str] | None]) -> str:
        clauses: list[str] = []
        for field, values in terms.items():
            for value in values or []:
                cleaned = " ".join(value.strip().split())
                if cleaned:
                    clauses.append(f'{field}:"{cleaned}"')
        if not clauses:
            raise ValueError("At least one search term is required.")
        return " AND ".join(clauses)

    def _build_user_agent(self) -> str:
        contact = self.settings.contact.strip()
        if contact:
            return f"{self.settings.tool}/{__version__} ({contact})"
        return f"{self.settings.tool}/{__version__} (contact-not-set)"

    def _build_query_payload(
        self,
        *,
        search_query: str | None = None,
        id_list: list[str] | None = None,
        start: int = 0,
        max_results: int = 10,
        sort_by: str | None = None,
        sort_order: str | None = None,
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {"start": start, "max_results": max_results}
        if search_query:
            payload["search_query"] = search_query
        if id_list:
            payload["id_list"] = ",".join(id_list)
            payload["max_results"] = max_results or len(id_list)
        if sort_by:
            payload["sortBy"] = sort_by
        if sort_order:
            payload["sortOrder"] = sort_order
        return payload

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
