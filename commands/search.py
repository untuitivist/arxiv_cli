from __future__ import annotations

import argparse

from ..core.client import ArxivClient
from ..core.io import write_json


def add_search_parser(subparsers: argparse._SubParsersAction) -> None:
    search = subparsers.add_parser("search", help="Search the arXiv API")
    search_sub = search.add_subparsers(dest="search_command", required=True)

    query_parser = search_sub.add_parser("query", help="Build a search query from common fields")
    query_parser.add_argument("--all", dest="all_terms", action="append", help="Repeatable all-field query")
    query_parser.add_argument("--title", action="append", help="Repeatable title query")
    query_parser.add_argument("--author", action="append", help="Repeatable author query")
    query_parser.add_argument("--abstract", dest="abstract_terms", action="append", help="Repeatable abstract query")
    query_parser.add_argument("--category", action="append", help="Repeatable category filter")
    query_parser.add_argument("--comment", action="append", help="Repeatable comment query")
    query_parser.add_argument("--journal-ref", action="append", help="Repeatable journal-ref query")
    query_parser.add_argument("--report-num", action="append", help="Repeatable report-number query")
    _add_common_search_options(query_parser)

    raw_parser = search_sub.add_parser("raw", help="Send a raw arXiv search_query string")
    raw_parser.add_argument("search_query", help="Raw arXiv search_query string")
    _add_common_search_options(raw_parser)


def _add_common_search_options(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--start", type=int, default=0, help="Result offset")
    parser.add_argument("--max-results", type=int, default=10, help="Number of results to request")
    parser.add_argument(
        "--sort-by",
        choices=["relevance", "lastUpdatedDate", "submittedDate"],
        default="relevance",
        help="Sort key",
    )
    parser.add_argument(
        "--sort-order",
        choices=["ascending", "descending"],
        default="descending",
        help="Sort order",
    )
    parser.add_argument("--base-url", help="Override API endpoint")
    parser.add_argument("--delay-seconds", type=float, help="Minimum spacing between requests")
    parser.add_argument("--timeout-seconds", type=float, help="HTTP timeout")
    parser.add_argument("--output", help="Write JSON result to file")


def handle_search(args: argparse.Namespace) -> int:
    client = ArxivClient.from_args(args)
    if args.search_command == "query":
        result = client.search(
            terms={
                "all": args.all_terms,
                "ti": args.title,
                "au": args.author,
                "abs": args.abstract_terms,
                "cat": args.category,
                "co": args.comment,
                "jr": args.journal_ref,
                "rn": args.report_num,
            },
            start=args.start,
            max_results=args.max_results,
            sort_by=args.sort_by,
            sort_order=args.sort_order,
        )
        write_json(result, args.output)
        return 0
    if args.search_command == "raw":
        result = client.search_raw(
            args.search_query,
            start=args.start,
            max_results=args.max_results,
            sort_by=args.sort_by,
            sort_order=args.sort_order,
        )
        write_json(result, args.output)
        return 0
    raise AssertionError(args.search_command)
