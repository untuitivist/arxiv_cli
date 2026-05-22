from __future__ import annotations

import argparse
import sys

from . import __version__
from .commands.api import add_api_parser, handle_api
from .commands.config import add_config_parser, handle_config
from .commands.docs import add_docs_parser, handle_docs
from .commands.find import add_find_parser, handle_find
from .commands.paper import add_paper_parser, handle_paper
from .commands.query import add_query_parser, handle_query
from .commands.search import add_search_parser, handle_search
from .commands.workflow import add_workflow_parser, handle_workflow
from .core.output import emit_payload


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="arxiv", description="Agent-first arXiv API CLI")
    parser.add_argument("--config", help="Path to config.json; default is arxiv_cli/local/config.json")
    parser.add_argument("--registry", help="Path to api_inventory_complete.json")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)
    add_api_parser(sub)
    add_config_parser(sub)
    add_docs_parser(sub)
    add_query_parser(sub)
    add_search_parser(sub)
    add_paper_parser(sub)
    add_find_parser(sub)
    add_workflow_parser(sub)
    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "api":
            code = handle_api(args)
        elif args.command == "config":
            code = handle_config(args)
        elif args.command == "docs":
            code = handle_docs(args)
        elif args.command == "query":
            code = handle_query(args)
        elif args.command == "search":
            code = handle_search(args)
        elif args.command == "paper":
            code = handle_paper(args)
        elif args.command == "find":
            code = handle_find(args)
        elif args.command == "workflow":
            code = handle_workflow(args)
        else:
            parser.error(f"Unknown command: {args.command}")
            code = 2
    except Exception as exc:
        emit_payload({"ok": False, "error_type": type(exc).__name__, "detail": str(exc)})
        code = 1
    sys.exit(code)
