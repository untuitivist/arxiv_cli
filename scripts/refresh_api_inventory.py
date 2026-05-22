from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from textwrap import dedent
from urllib.parse import urlencode

import requests

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from core.feed import parse_feed


DOC_URLS = {
    "docs_access.html": "https://info.arxiv.org/help/api/index.html",
    "docs_basics.html": "https://info.arxiv.org/help/api/basics.html",
    "docs_manual.html": "https://info.arxiv.org/help/api/user-manual.html",
    "docs_terms.html": "https://info.arxiv.org/help/api/tou.html",
}

MANUAL_SECTIONS = {
    "search_query_and_id_list_logic": (
        "The search_query parameter accepts a search expression used to find articles, "
        "while id_list accepts a comma-delimited list of arXiv ids. If only search_query "
        "is present, the API returns matching articles. If only id_list is present, the API "
        "returns the listed articles. If both are present, the API returns only the listed "
        "articles that also match search_query."
    ),
    "start_and_max_results_paging": (
        "start is a 0-based offset of the first returned result. max_results controls how many "
        "results are returned. The manual recommends a 3 second delay between repeated calls, "
        "limits max_results to 30000 overall, and advises retrieving slices of at most 2000 at a time."
    ),
    "sort_order": (
        "sortBy can be relevance, lastUpdatedDate, or submittedDate. sortOrder can be ascending or descending."
    ),
    "response_format": "Everything returned by the API in HTTP response bodies, including errors, is Atom 1.0 XML.",
}

RATE_LIMIT_EXCERPT = (
    "When using the legacy APIs (including OAI-PMH, RSS, and the arXiv API), make no more than one request "
    "every three seconds, and limit requests to a single connection at a time."
)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, payload: object) -> None:
    write_text(path, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def build_inventory(root: Path, sample_query: str, max_results: int) -> None:
    generated_at = datetime.now(timezone.utc).isoformat()
    raw_dir = root / "_raw"
    reports_dir = root / "reports"
    endpoint_dir = root / "endpoints" / "api" / "query"
    get_dir = endpoint_dir / "examples" / "GET"
    post_dir = endpoint_dir / "examples" / "POST"

    for directory in [raw_dir, reports_dir, get_dir, post_dir]:
        directory.mkdir(parents=True, exist_ok=True)

    for filename, url in DOC_URLS.items():
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        write_text(raw_dir / filename, response.text)

    sample_params = {"search_query": sample_query, "start": 0, "max_results": max_results}
    get_response = requests.get("https://export.arxiv.org/api/query", params=sample_params, timeout=30)
    get_response.raise_for_status()
    post_form_response = requests.post("https://export.arxiv.org/api/query", data=sample_params, timeout=30)
    post_form_response.raise_for_status()
    post_query_response = requests.post("https://export.arxiv.org/api/query", params=sample_params, timeout=30)

    sample_name = "sample_query_all_electron.xml" if sample_query == "all:electron" else "sample_query.xml"
    write_text(raw_dir / sample_name, get_response.text)

    get_summary = parse_feed(get_response.text)
    post_form_summary = parse_feed(post_form_response.text)
    post_query_summary = parse_feed(post_query_response.text)

    endpoint = {
        "path": "/api/query",
        "url_template": "https://export.arxiv.org/api/query",
        "methods": ["GET", "POST"],
        "source": [
            "arxiv_api_access",
            "arxiv_api_basics",
            "arxiv_api_user_manual",
            "arxiv_api_terms_of_use",
            "live_probe",
        ],
        "description": "Public arXiv metadata query endpoint returning Atom 1.0 feeds.",
        "safe_probe": True,
        "params": {
            "search_query": {"location": ["query", "form"], "type": "string", "required": False, "description": "Fielded search expression."},
            "id_list": {"location": ["query", "form"], "type": "string", "required": False, "description": "Comma-delimited arXiv ids."},
            "start": {"location": ["query", "form"], "type": "integer", "required": False, "default": 0, "description": "0-based result offset."},
            "max_results": {
                "location": ["query", "form"],
                "type": "integer",
                "required": False,
                "default": 10,
                "recommended_max": 2000,
                "absolute_max": 30000,
                "description": "Number of results to return.",
            },
            "sortBy": {
                "location": ["query", "form"],
                "type": "string",
                "required": False,
                "choices": ["relevance", "lastUpdatedDate", "submittedDate"],
                "description": "Sort field.",
            },
            "sortOrder": {
                "location": ["query", "form"],
                "type": "string",
                "required": False,
                "choices": ["ascending", "descending"],
                "description": "Sort direction.",
            },
        },
        "request_body": {
            "POST": {
                "content_type": "application/x-www-form-urlencoded",
                "fields": ["search_query", "id_list", "start", "max_results", "sortBy", "sortOrder"],
                "notes": [
                    "POST with form-encoded body fields succeeded during live probing.",
                    "POST with only query-string params returned HTTP 400 during live probing.",
                ],
            }
        },
        "notes": [
            "Response bodies, including error payloads, are Atom 1.0 XML.",
            "Rate limit guidance requires one request every three seconds and one connection at a time.",
        ],
        "docs_refs": [{"title": title, "url": url} for title, url in [
            ("API Access", DOC_URLS["docs_access.html"]),
            ("API Basics", DOC_URLS["docs_basics.html"]),
            ("API User Manual", DOC_URLS["docs_manual.html"]),
            ("API Terms of Use", DOC_URLS["docs_terms.html"]),
        ]],
        "manual_sections": MANUAL_SECTIONS,
        "response_format": {
            "content_type": "application/atom+xml",
            "body_format": "Atom 1.0 XML",
            "feed_fields": ["id", "title", "updated", "opensearch:totalResults", "opensearch:startIndex", "opensearch:itemsPerPage", "entry[]"],
            "entry_fields": ["id", "title", "summary", "published", "updated", "author[]", "link[]", "category[]", "arxiv:primary_category"],
        },
        "probe": {
            "get_with_query_params": {
                "status_code": get_response.status_code,
                "content_type": get_response.headers.get("content-type"),
                "url": get_response.url,
                "ok": get_response.ok,
            },
            "post_with_form_body": {
                "status_code": post_form_response.status_code,
                "content_type": post_form_response.headers.get("content-type"),
                "url": post_form_response.url,
                "ok": post_form_response.ok,
            },
            "post_with_query_params_only": {
                "status_code": post_query_response.status_code,
                "content_type": post_query_response.headers.get("content-type"),
                "url": post_query_response.url,
                "ok": post_query_response.ok,
                "note": "Observed HTTP 400; use form-encoded body fields instead.",
            },
        },
    }

    write_json(root / "api_inventory.json", {
        "generated_at": generated_at,
        "base_url": endpoint["url_template"],
        "endpoint_count": 1,
        "endpoints": [{"path": endpoint["path"], "methods": endpoint["methods"], "description": endpoint["description"], "safe_probe": endpoint["safe_probe"]}],
    })
    write_json(root / "api_inventory_complete.json", {"generated_at": generated_at, "endpoints": [endpoint]})
    write_text(root / "api_inventory.md", dedent(
        """
        # arXiv API Inventory

        This inventory captures the current public arXiv metadata query surface used by `arxiv_cli`.

        ## Endpoints

        - `GET /api/query`
        - `POST /api/query`

        ## Notes

        - The endpoint is public and does not require auth.
        - Normal and error bodies are Atom XML.
        - GET is the standard documented form; POST works when fields are form-encoded in the body.
        """
    ).strip() + "\n")
    write_text(root / "API_DOCUMENTATION.md", dedent(
        f"""
        # API Documentation

        - API Access: {DOC_URLS["docs_access.html"]}
        - API Basics: {DOC_URLS["docs_basics.html"]}
        - API User Manual: {DOC_URLS["docs_manual.html"]}
        - API Terms of Use: {DOC_URLS["docs_terms.html"]}

        ## Extracted guidance

        - Query logic: {MANUAL_SECTIONS["search_query_and_id_list_logic"]}
        - Paging: {MANUAL_SECTIONS["start_and_max_results_paging"]}
        - Sorting: {MANUAL_SECTIONS["sort_order"]}
        - Response format: {MANUAL_SECTIONS["response_format"]}
        - Rate limits: {RATE_LIMIT_EXCERPT}
        """
    ).strip() + "\n")
    write_json(endpoint_dir / "endpoint.json", endpoint)
    write_text(endpoint_dir / "endpoint.md", dedent(
        f"""
        # GET|POST /api/query

        ## Summary

        - URL: `https://export.arxiv.org/api/query`
        - Methods: `GET`, `POST`
        - Response format: `application/atom+xml` (Atom 1.0 XML)

        ## Query Logic

        {MANUAL_SECTIONS["search_query_and_id_list_logic"]}

        ## Paging

        {MANUAL_SECTIONS["start_and_max_results_paging"]}

        ## Sorting

        {MANUAL_SECTIONS["sort_order"]}

        ## Rate Limits

        {RATE_LIMIT_EXCERPT}
        """
    ).strip() + "\n")

    for target_dir, method, response_text, summary, input_payload, parameter_command, file_command, extra_note in [
        (
            get_dir,
            "GET",
            get_response.text,
            get_summary,
            {"url": endpoint["url_template"], "method": "GET", "params": sample_params},
            f'curl "{endpoint["url_template"]}?{urlencode(sample_params)}"',
            f'Invoke-WebRequest -Uri "{endpoint["url_template"]}?{urlencode(sample_params)}" -OutFile "resources/api_inventory/endpoints/api/query/examples/GET/file_output.xml"',
            "",
        ),
        (
            post_dir,
            "POST",
            post_form_response.text,
            post_form_summary,
            {"url": endpoint["url_template"], "method": "POST", "data": sample_params},
            'curl -X POST "https://export.arxiv.org/api/query" -d "search_query=all:electron&start=0&max_results=1"',
            'Invoke-WebRequest -Method Post -Uri "https://export.arxiv.org/api/query" -Body @{search_query="all:electron"; start="0"; max_results="1"} -OutFile "resources/api_inventory/endpoints/api/query/examples/POST/file_output.xml"',
            "\nNote: POST with only URL query parameters returned HTTP 400 during live probing.\n",
        ),
    ]:
        write_json(target_dir / "input.json", input_payload)
        write_text(target_dir / "parameter_command.txt", parameter_command + "\n")
        write_text(target_dir / "file_io_command.txt", file_command + "\n")
        write_text(target_dir / "print_result.xml", response_text)
        write_text(target_dir / "file_output.xml", response_text)
        write_json(target_dir / "summary_output.json", summary)
        write_text(
            target_dir / "README.md",
            dedent(
                f"""
                # {method} /api/query

                ## Parameter command

                ```powershell
                {parameter_command}
                ```

                ## File IO command

                ```powershell
                {file_command}
                ```
                {extra_note}
                """
            ).strip()
            + "\n",
        )

    write_json(reports_dir / "endpoint_test_results.json", {
        "generated_at": generated_at,
        "results": [
            {"path": endpoint["path"], "method": "GET", "transport": "query_params", "status_code": get_response.status_code, "ok": get_response.ok},
            {"path": endpoint["path"], "method": "POST", "transport": "form_body", "status_code": post_form_response.status_code, "ok": post_form_response.ok},
            {
                "path": endpoint["path"],
                "method": "POST",
                "transport": "query_params_only",
                "status_code": post_query_response.status_code,
                "ok": post_query_response.ok,
                "note": "Observed HTTP 400; keep POST requests form-encoded.",
            },
        ],
    })
    write_text(reports_dir / "endpoint_test_results.md", dedent(
        f"""
        # Endpoint Test Results

        - Generated at: `{generated_at}`
        - Tested endpoint method cases: `3`

        | Method | Path | Transport | Status | Note |
        |---|---|---|---:|---|
        | `GET` | `/api/query` | `query_params` | `{get_response.status_code}` | standard documented query form |
        | `POST` | `/api/query` | `form_body` | `{post_form_response.status_code}` | supported live POST shape |
        | `POST` | `/api/query` | `query_params_only` | `{post_query_response.status_code}` | returns HTTP 400; avoid this form |
        """
    ).strip() + "\n")
    write_json(reports_dir / "endpoint_cli_examples_summary.json", {
        "generated_at": generated_at,
        "method_cases": 2,
        "failures": 0,
        "cases": [
            {"method": "GET", "path": "/api/query", "example_directory": "api_inventory/endpoints/api/query/examples/GET", "status": "ok"},
            {"method": "POST", "path": "/api/query", "example_directory": "api_inventory/endpoints/api/query/examples/POST", "status": "ok"},
        ],
    })
    write_text(reports_dir / "ENDPOINT_CLI_EXAMPLES.md", dedent(
        """
        # Endpoint CLI Examples

        Each endpoint method example lives under `api_inventory/endpoints/.../examples/<METHOD>/`.

        | Method | Path | Example directory | Status |
        |---|---|---|---|
        | `GET` | `/api/query` | `api_inventory/endpoints/api/query/examples/GET` | `ok` |
        | `POST` | `/api/query` | `api_inventory/endpoints/api/query/examples/POST` | `ok` |
        """
    ).strip() + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Refresh the bundled arXiv api_inventory from the live public API.")
    parser.add_argument(
        "--root",
        default=Path(__file__).resolve().parents[1] / "resources" / "api_inventory",
        type=Path,
        help="Target api_inventory root",
    )
    parser.add_argument("--sample-query", default="all:electron", help="Search query used for live GET/POST examples")
    parser.add_argument("--max-results", type=int, default=1, help="Sample max_results for live examples")
    args = parser.parse_args()
    build_inventory(args.root, args.sample_query, args.max_results)


if __name__ == "__main__":
    main()
