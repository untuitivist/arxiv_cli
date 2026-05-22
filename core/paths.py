from __future__ import annotations

from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = PACKAGE_ROOT.parent
LOCAL_ROOT = PACKAGE_ROOT / "local"
RESOURCES_ROOT = PACKAGE_ROOT / "resources"
DOCS_ROOT = RESOURCES_ROOT / "docs" / "commands"
API_INVENTORY_ROOT = RESOURCES_ROOT / "api_inventory"
WORKFLOW_ROOT = PACKAGE_ROOT / "workflow"
WORKFLOW_NODES_ROOT = WORKFLOW_ROOT / "nodes"

DEFAULT_CONFIG_PATH = LOCAL_ROOT / "config.json"
DEFAULT_STATE_PATH = LOCAL_ROOT / "state" / "last_request_at.txt"
