from __future__ import annotations

import argparse

from ..core.client import ArxivClient
from ..core.output import emit_payload


def add_query_parser(subparsers: argparse._SubParsersAction) -> None:
    query = subparsers.add_parser("query", help="1:1 resource command for the /api/query endpoint")
    query_sub = query.add_subparsers(dest="query_command", required=True)

    run_parser = query_sub.add_parser("run", help="Call the /api/query endpoint with endpoint-native arguments")
    run_parser.add_argument("--method", choices=["GET", "POST"], default="GET")
    run_parser.add_argument("--search-query", help="Raw arXiv search_query string")
    run_parser.add_argument("--id", dest="ids", action="append", help="Repeatable arXiv id value")
    run_parser.add_argument("--start", type=int, default=0, help="Result offset")
    run_parser.add_argument("--max-results", type=int, default=10, help="Number of results to request")
    run_parser.add_argument(
        "--sort-by",
        choices=["relevance", "lastUpdatedDate", "submittedDate"],
        help="Sort key",
    )
    run_parser.add_argument(
        "--sort-order",
        choices=["ascending", "descending"],
        help="Sort order",
    )
    run_parser.add_argument("--base-url", help="Override API endpoint")
    run_parser.add_argument("--delay-seconds", type=float, help="Minimum spacing between requests")
    run_parser.add_argument("--timeout-seconds", type=float, help="HTTP timeout")
    run_parser.add_argument("--dry-run", action="store_true", help="Show the prepared request without executing it")
    run_parser.add_argument("--format", choices=["json", "text"], default="json", help="Render output as json or text")
    run_parser.add_argument("--output", help="Write result to file")


def handle_query(args: argparse.Namespace) -> int:
    if args.query_command == "run":
        if not args.search_query and not args.ids:
            raise ValueError("Provide --search-query or at least one --id.")
        client = ArxivClient.from_args(args)
        result = client.run_query(
            search_query=args.search_query,
            id_list=args.ids,
            start=args.start,
            max_results=args.max_results,
            sort_by=args.sort_by,
            sort_order=args.sort_order,
            dry_run=args.dry_run,
            method=args.method,
        )
        emit_payload(result, output=args.output, fmt=args.format)
        return 0
    raise AssertionError(args.query_command)
