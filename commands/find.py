from __future__ import annotations

import argparse

from ..core.client import ArxivClient
from ..core.output import emit_payload


def add_find_parser(subparsers: argparse._SubParsersAction) -> None:
    find = subparsers.add_parser("find", help="Shortcut commands for common literature search workflows")
    find_sub = find.add_subparsers(dest="find_command", required=True)

    papers = find_sub.add_parser("papers", help="Find papers from free-text intent plus optional filters")
    papers.add_argument("terms", nargs="+", help="Free-text search terms")
    papers.add_argument("--category", action="append", help="Repeatable category filter")
    papers.add_argument("--author", action="append", help="Repeatable author filter")
    papers.add_argument("--title", action="append", help="Repeatable title filter")
    papers.add_argument("--abstract", dest="abstract_terms", action="append", help="Repeatable abstract filter")
    papers.add_argument("--start", type=int, default=0, help="Result offset")
    papers.add_argument("--max-results", type=int, default=10, help="Number of results to request")
    papers.add_argument(
        "--sort-by",
        choices=["relevance", "lastUpdatedDate", "submittedDate"],
        default="relevance",
        help="Sort key",
    )
    papers.add_argument(
        "--sort-order",
        choices=["ascending", "descending"],
        default="descending",
        help="Sort order",
    )
    papers.add_argument("--base-url", help="Override API endpoint")
    papers.add_argument("--delay-seconds", type=float, help="Minimum spacing between requests")
    papers.add_argument("--timeout-seconds", type=float, help="HTTP timeout")
    papers.add_argument("--dry-run", action="store_true", help="Show the prepared request without executing it")
    papers.add_argument("--format", choices=["json", "text"], default="json", help="Render output as json or text")
    papers.add_argument("--output", help="Write result to file")


def handle_find(args: argparse.Namespace) -> int:
    if args.find_command == "papers":
        client = ArxivClient.from_args(args)
        result = client.search(
            terms={
                "all": [" ".join(args.terms)],
                "cat": args.category,
                "au": args.author,
                "ti": args.title,
                "abs": args.abstract_terms,
            },
            start=args.start,
            max_results=args.max_results,
            sort_by=args.sort_by,
            sort_order=args.sort_order,
            dry_run=args.dry_run,
        )
        emit_payload(result, output=args.output, fmt=args.format)
        return 0
    raise AssertionError(args.find_command)
