from __future__ import annotations

import argparse

from ..core.config_store import ConfigStore
from ..core.output import emit_payload


def add_config_parser(subparsers: argparse._SubParsersAction) -> None:
    config = subparsers.add_parser("config", help="Manage local arXiv CLI config")
    config.add_argument("--config", dest="config_path", help="Path to config.json")
    config_sub = config.add_subparsers(dest="config_command", required=True)

    init_parser = config_sub.add_parser("init", help="Create a default config file")
    init_parser.add_argument("--force", action="store_true", help="Overwrite an existing config file")
    init_parser.add_argument("--format", choices=["json", "text"], default="json")

    show_parser = config_sub.add_parser("show", help="Show the full config")
    show_parser.add_argument("--format", choices=["json", "text"], default="json")

    get_parser = config_sub.add_parser("get", help="Get one config value")
    get_parser.add_argument("key")
    get_parser.add_argument("--format", choices=["json", "text"], default="json")

    set_parser = config_sub.add_parser("set", help="Set one config value")
    set_parser.add_argument("key")
    set_parser.add_argument("value")
    set_parser.add_argument("--format", choices=["json", "text"], default="json")


def handle_config(args: argparse.Namespace) -> int:
    store = ConfigStore(args.config_path)
    if args.config_command == "init":
        created = store.init(force=args.force)
        emit_payload(
            {"ok": True, "path": str(store.path), "created": created, "config": store.load()},
            fmt=args.format,
        )
        return 0
    if args.config_command == "show":
        emit_payload({"ok": True, "path": str(store.path), "config": store.load()}, fmt=args.format)
        return 0
    if args.config_command == "get":
        emit_payload(
            {"ok": True, "path": str(store.path), "key": args.key, "value": store.get(args.key)},
            fmt=args.format,
        )
        return 0
    if args.config_command == "set":
        value = store.set(args.key, args.value)
        emit_payload(
            {"ok": True, "path": str(store.path), "key": args.key, "value": value},
            fmt=args.format,
        )
        return 0
    raise AssertionError(args.config_command)
