from __future__ import annotations

import argparse

from ..core.client import ArxivClient
from ..core.io import parse_key_values, read_json_file, write_json
from ..core.registry import EndpointRegistry


def add_api_parser(subparsers: argparse._SubParsersAction) -> None:
    api = subparsers.add_parser("api", help="Inspect and call endpoints from the bundled api_inventory")
    api_sub = api.add_subparsers(dest="api_command", required=True)

    stats = api_sub.add_parser("stats", help="Show registry statistics")
    stats.add_argument("--output", help="Write JSON result to file")

    list_parser = api_sub.add_parser("list", help="List registered endpoints")
    list_parser.add_argument("--prefix", help="Filter endpoint path prefix")
    list_parser.add_argument("--output", help="Write JSON result to file")

    show_parser = api_sub.add_parser("show", help="Show one endpoint definition")
    show_parser.add_argument("path")
    show_parser.add_argument("--output", help="Write JSON result to file")

    params_parser = api_sub.add_parser("params", help="Show query/form parameter hints for one endpoint")
    params_parser.add_argument("path")
    params_parser.add_argument("--output", help="Write JSON result to file")

    call_parser = api_sub.add_parser("call", help="Execute one inventory endpoint call")
    call_parser.add_argument("method", choices=["GET", "POST"])
    call_parser.add_argument("path")
    call_parser.add_argument("--param", action="append", help="Query parameter KEY=VALUE")
    call_parser.add_argument("--data", action="append", help="Form field KEY=VALUE")
    call_parser.add_argument("--input", help="JSON file containing params or data")
    call_parser.add_argument("--output", help="Write JSON result to file")


def load_registry(args: argparse.Namespace) -> EndpointRegistry:
    return EndpointRegistry.load(getattr(args, "registry", None))


def handle_api(args: argparse.Namespace) -> int:
    registry = load_registry(args)
    if args.api_command == "stats":
        write_json(registry.stats(), args.output)
        return 0
    if args.api_command == "list":
        write_json(
            [
                {
                    "path": endpoint.path,
                    "methods": list(endpoint.methods),
                    "description": endpoint.description,
                }
                for endpoint in registry.list(args.prefix)
            ],
            args.output,
        )
        return 0
    if args.api_command == "show":
        write_json(registry.get(args.path).raw, args.output)
        return 0
    if args.api_command == "params":
        endpoint = registry.get(args.path)
        write_json(
            {
                "path": endpoint.path,
                "methods": list(endpoint.methods),
                "params": endpoint.params,
                "request_body": endpoint.request_body,
                "source": list(endpoint.source),
            },
            args.output,
        )
        return 0
    if args.api_command == "call":
        endpoint = registry.get(args.path)
        input_payload = read_json_file(args.input)
        params = {}
        params.update(input_payload.get("params") or {})
        params.update(parse_key_values(args.param))
        data = None
        if args.method.upper() == "POST":
            data = {}
            data.update(input_payload.get("data") or {})
            data.update(parse_key_values(args.data))
        client = ArxivClient.from_args(args)
        prepared = client.prepare(endpoint, args.method, params=params, data=data)
        write_json(client.call(prepared, parse_atom=True), args.output)
        return 0
    raise AssertionError(args.api_command)
