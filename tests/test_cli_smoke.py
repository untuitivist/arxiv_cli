from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def run_arxiv(*args: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    package_parent = str(REPO_ROOT.parent)
    env["PYTHONPATH"] = package_parent + os.pathsep + env.get("PYTHONPATH", "")
    env["PYTHONIOENCODING"] = "utf-8"
    return subprocess.run(
        [sys.executable, "-m", "arxiv_cli", *args],
        cwd=REPO_ROOT.parent,
        env=env,
        text=True,
        encoding="utf-8",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=30,
        check=False,
    )


class CliSmokeTests(unittest.TestCase):
    def test_top_level_help_smoke(self) -> None:
        result = run_arxiv("--help")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("api", result.stdout)
        self.assertIn("search", result.stdout)
        self.assertIn("paper", result.stdout)

    def test_config_init_get_set_with_temp_config(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            config_path = Path(tmp) / "config.json"
            init = run_arxiv("config", "--config", str(config_path), "init")
            self.assertEqual(init.returncode, 0, init.stderr)
            self.assertIs(json.loads(init.stdout)["ok"], True)

            set_result = run_arxiv("config", "--config", str(config_path), "set", "contact", "you@example.com")
            self.assertEqual(set_result.returncode, 0, set_result.stderr)
            self.assertEqual(json.loads(set_result.stdout)["value"], "you@example.com")

            get_result = run_arxiv("config", "--config", str(config_path), "get", "contact")
            self.assertEqual(get_result.returncode, 0, get_result.stderr)
            self.assertEqual(json.loads(get_result.stdout)["value"], "you@example.com")

    def test_docs_list_smoke(self) -> None:
        result = run_arxiv("docs", "list")
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        nodes = {item["node"] for item in payload["nodes"]}
        self.assertIn("", nodes)
        self.assertIn("api", nodes)
        self.assertIn("search/query", nodes)
        self.assertIn("paper/get", nodes)

    def test_docs_show_accepts_node_name(self) -> None:
        result = run_arxiv("docs", "show", "search/query")
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertIs(payload["ok"], True)
        self.assertIn("search_query", payload["text"])

    def test_search_help_exposes_sort_and_paging(self) -> None:
        result = run_arxiv("search", "query", "--help")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("--max-results", result.stdout)
        self.assertIn("--sort-by", result.stdout)
        self.assertIn("--category", result.stdout)

    def test_api_stats_smoke(self) -> None:
        result = run_arxiv("api", "stats")
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["endpoint_count"], 1)
        self.assertIn("GET", payload["method_counts"])

    def test_api_show_smoke(self) -> None:
        result = run_arxiv("api", "show", "/api/query")
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["path"], "/api/query")
        self.assertIn("POST", payload["methods"])

    def test_paper_help_smoke(self) -> None:
        result = run_arxiv("paper", "get", "--help")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("One or more arXiv ids", result.stdout)


if __name__ == "__main__":
    unittest.main()
