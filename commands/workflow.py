from __future__ import annotations

import argparse
import re

from ..core.output import emit_payload
from ..core.paths import WORKFLOW_NODES_ROOT, WORKFLOW_ROOT


NODE_NAME_PATTERN = re.compile(r"^[A-Z]_[A-Za-z0-9_]+$")


def add_workflow_parser(subparsers: argparse._SubParsersAction) -> None:
    workflow = subparsers.add_parser("workflow", help="Inspect bundled workflow notes")
    workflow_sub = workflow.add_subparsers(dest="workflow_command", required=True)

    list_parser = workflow_sub.add_parser("list", help="List workflow nodes")
    list_parser.add_argument("--format", choices=["json", "text"], default="json", help="Render output as json or text")
    list_parser.add_argument("--output", help="Write result to file")

    show_parser = workflow_sub.add_parser("show", help="Show a workflow node or the graph")
    show_parser.add_argument("node", help="Node name such as A_config_and_rate_limit, or graph")
    show_parser.add_argument("--format", choices=["json", "text"], default="json", help="Render output as json or text")
    show_parser.add_argument("--output", help="Write result to file")


def handle_workflow(args: argparse.Namespace) -> int:
    if args.workflow_command == "list":
        nodes = []
        for node_doc in sorted(WORKFLOW_NODES_ROOT.glob("*/node.md")):
            node = node_doc.parent.name
            if not NODE_NAME_PATTERN.match(node):
                continue
            nodes.append({"node": node, "path": str(node_doc)})
        emit_payload({"ok": True, "workflow_root": str(WORKFLOW_ROOT), "nodes": nodes}, output=args.output, fmt=args.format)
        return 0
    if args.workflow_command == "show":
        if args.node == "graph":
            target = WORKFLOW_ROOT / "workflow_graph.md"
        else:
            target = WORKFLOW_NODES_ROOT / args.node / "node.md"
        if not target.exists():
            emit_payload({"ok": False, "reason": "workflow_doc_not_found", "node": args.node}, output=args.output, fmt=args.format)
            return 1
        emit_payload({"ok": True, "path": str(target), "text": target.read_text(encoding="utf-8-sig")}, output=args.output, fmt=args.format)
        return 0
    raise AssertionError(args.workflow_command)
