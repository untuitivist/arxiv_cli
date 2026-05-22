from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT.parent) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT.parent))

from arxiv_cli.core.client import ArxivClient, ClientSettings


class _FakeResponse:
    def __init__(self, url: str, text: str, *, status_code: int = 200, reason: str = "OK") -> None:
        self.url = url
        self.text = text
        self.status_code = status_code
        self.reason = reason
        self.headers = {"content-type": "application/atom+xml; charset=utf-8"}
        self.ok = 200 <= status_code < 400

    def raise_for_status(self) -> None:
        return None


ATOM_SAMPLE = """<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom"
      xmlns:opensearch="http://a9.com/-/spec/opensearch/1.1/"
      xmlns:arxiv="http://arxiv.org/schemas/atom">
  <title>ArXiv Query: search_query=all:test</title>
  <id>http://arxiv.org/api/sample</id>
  <updated>2026-05-23T00:00:00Z</updated>
  <opensearch:totalResults>1</opensearch:totalResults>
  <opensearch:startIndex>0</opensearch:startIndex>
  <opensearch:itemsPerPage>1</opensearch:itemsPerPage>
  <entry>
    <id>http://arxiv.org/abs/1234.5678v1</id>
    <updated>2026-05-23T00:00:00Z</updated>
    <published>2026-05-22T00:00:00Z</published>
    <title>Test Title</title>
    <summary>Test Summary</summary>
    <author><name>Test Author</name></author>
    <link href="http://arxiv.org/abs/1234.5678v1" rel="alternate" type="text/html" />
    <arxiv:primary_category term="cs.LG" />
    <category term="cs.LG" scheme="http://arxiv.org/schemas/atom" />
  </entry>
</feed>
"""


class ClientTests(unittest.TestCase):
    def test_search_raw_returns_parsed_feed(self) -> None:
        client = ArxivClient(
            ClientSettings(
                base_url="https://export.arxiv.org/api/query",
                tool="arxiv-cli",
                contact="you@example.com",
                delay_seconds=0.0,
                timeout_seconds=5.0,
            ),
            state_path=REPO_ROOT / "local" / "state" / "test_last_request_at.txt",
        )
        with patch("arxiv_cli.core.client.requests.request") as mock_request:
            mock_request.return_value = _FakeResponse(
                "https://export.arxiv.org/api/query?search_query=all%3Atest&start=0&max_results=1",
                ATOM_SAMPLE,
            )
            payload = client.search_raw(
                "all:test",
                start=0,
                max_results=1,
                sort_by="relevance",
                sort_order="descending",
            )
        self.assertIs(payload["ok"], True)
        self.assertEqual(payload["total_results"], 1)
        self.assertEqual(payload["entries"][0]["title"], "Test Title")
        self.assertIn("User-Agent", payload["request"]["headers"])


if __name__ == "__main__":
    unittest.main()
