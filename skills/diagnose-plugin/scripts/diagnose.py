#!/usr/bin/env python3
"""Report plugin name and version equivalently across hosts."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

PLUGIN_NAME = "closelly-ai-plugins"
PLUGIN_VERSION = "1.0.0"

MANIFEST_RELATIVE_PATHS = (
    "plugin.json",
    ".codex-plugin/plugin.json",
    ".claude-plugin/plugin.json",
)

HOST_ENV = (
    ("CLAUDE_PLUGIN_ROOT", "claude-code"),
    ("COPILOT_HOME", "github-copilot-cli"),
    ("COPILOT_PLUGIN_DATA", "github-copilot-cli"),
    ("CODEX_HOME", "chatgpt-codex"),
    ("PLUGIN_ROOT", "chatgpt-codex"),
)


def _load_json(path: Path) -> dict[str, Any] | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return data if isinstance(data, dict) else None


def find_plugin_root(start: Path | None = None) -> Path:
    env_keys = ("CLAUDE_PLUGIN_ROOT", "PLUGIN_ROOT")
    for key in env_keys:
        value = os.environ.get(key)
        if value:
            candidate = Path(value).expanduser().resolve()
            if (candidate / "plugin.json").is_file() or (
                candidate / ".codex-plugin" / "plugin.json"
            ).is_file() or (candidate / ".claude-plugin" / "plugin.json").is_file():
                return candidate

    here = (start or Path(__file__).resolve()).parent
    for current in [here, *here.parents]:
        if (current / "plugin.json").is_file() or (
            current / ".codex-plugin" / "plugin.json"
        ).is_file() or (current / ".claude-plugin" / "plugin.json").is_file():
            return current
    raise FileNotFoundError("No se encontró la raíz del plugin Closelly.")


def detect_host() -> str:
    for env_name, host in HOST_ENV:
        if os.environ.get(env_name):
            return host
    return "unknown"


def collect_identities(root: Path) -> list[tuple[str, str, str, str]]:
    found: list[tuple[str, str, str, str]] = []
    for relative in MANIFEST_RELATIVE_PATHS:
        path = root / relative
        payload = _load_json(path)
        if not payload:
            continue
        name = str(payload.get("name") or "").strip()
        version = str(payload.get("version") or "").strip()
        description = str(payload.get("description") or "").strip()
        if name or version:
            found.append((relative, name, version, description))
    return found


def mcp_remote_enabled(root: Path) -> bool:
    payload = _load_json(root / "plugin.json") or {}
    extensions = payload.get("extensions")
    if not isinstance(extensions, dict):
        return False
    remote = (
        extensions.get("com.closelly.mcp", {}).get("remote")
        if isinstance(extensions.get("com.closelly.mcp"), dict)
        else {}
    )
    if isinstance(remote, dict) and remote.get("enabled") is True:
        return True
    for relative in ("mcp.json", ".mcp.json", ".app.json"):
        if (root / relative).is_file():
            return True
    return False


def build_report(root: Path) -> str:
    identities = collect_identities(root)
    names = {item[1] for item in identities if item[1]}
    versions = {item[2] for item in identities if item[2]}
    descriptions = {item[3] for item in identities if item[3]}

    name = next(iter(names), PLUGIN_NAME)
    version = next(iter(versions), PLUGIN_VERSION)
    description = next(iter(descriptions), "")
    consistent = len(names) <= 1 and len(versions) <= 1 and len(descriptions) <= 1
    if names and PLUGIN_NAME not in names:
        consistent = False
    if versions and PLUGIN_VERSION not in versions:
        consistent = False

    lines = [
        f"plugin.name={name}",
        f"plugin.version={version}",
        f"plugin.description={description}",
        f"host={detect_host()}",
        f"identity.consistent={'true' if consistent else 'false'}",
        f"mcp.remote.enabled={'true' if mcp_remote_enabled(root) else 'false'}",
    ]
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    del argv
    try:
        root = find_plugin_root()
    except FileNotFoundError as exc:
        sys.stderr.write(f"{exc}\n")
        return 1
    sys.stdout.write(build_report(root))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
