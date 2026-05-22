from __future__ import annotations

import argparse

from ..core.client import ArxivClient
from ..core.io import write_json


def add_paper_parser(subparsers: argparse._SubParsersAction) -> None:
    paper = subparsers.add_parser("paper", help="Fetch papers by arXiv id")
    paper_sub = paper.add_subparsers(dest="paper_command", required=True)

    get_parser = paper_sub.add_parser("get", help="Fetch one or more arXiv ids")
    get_parser.add_argument("ids", nargs="+", help="One or more arXiv ids")
    get_parser.add_argument("--base-url", help="Override API endpoint")
    get_parser.add_argument("--delay-seconds", type=float, help="Minimum spacing between requests")
    get_parser.add_argument("--timeout-seconds", type=float, help="HTTP timeout")
    get_parser.add_argument("--output", help="Write JSON result to file")


def handle_paper(args: argparse.Namespace) -> int:
    if args.paper_command == "get":
        client = ArxivClient.from_args(args)
        result = client.fetch_by_ids(args.ids)
        write_json(result, args.output)
        return 0
    raise AssertionError(args.paper_command)
