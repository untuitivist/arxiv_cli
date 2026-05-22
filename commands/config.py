from __future__ import annotations

import argparse

from ..core.config_store import ConfigStore
from ..core.io import write_json


def add_config_parser(subparsers: argparse._SubParsersAction) -> None:
    config = subparsers.add_parser("config", help="Manage local arXiv CLI config")
    config.add_argument("--config", dest="config_path", help="Path to config.json")
    config_sub = config.add_subparsers(dest="config_command", required=True)

    init_parser = config_sub.add_parser("init", help="Create a default config file")
    init_parser.add_argument("--force", action="store_true", help="Overwrite an existing config file")

    config_sub.add_parser("show", help="Show the full config")

    get_parser = config_sub.add_parser("get", help="Get one config value")
    get_parser.add_argument("key")

    set_parser = config_sub.add_parser("set", help="Set one config value")
    set_parser.add_argument("key")
    set_parser.add_argument("value")


def handle_config(args: argparse.Namespace) -> int:
    store = ConfigStore(args.config_path)
    if args.config_command == "init":
        created = store.init(force=args.force)
        write_json({"ok": True, "path": str(store.path), "created": created, "config": store.load()})
        return 0
    if args.config_command == "show":
        write_json({"ok": True, "path": str(store.path), "config": store.load()})
        return 0
    if args.config_command == "get":
        write_json({"ok": True, "path": str(store.path), "key": args.key, "value": store.get(args.key)})
        return 0
    if args.config_command == "set":
        value = store.set(args.key, args.value)
        write_json({"ok": True, "path": str(store.path), "key": args.key, "value": value})
        return 0
    raise AssertionError(args.config_command)
