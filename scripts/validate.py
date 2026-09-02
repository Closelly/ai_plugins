#!/usr/bin/env python3
"""Validate Closelly portable plugin manifests, skills, and packaging constraints."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Iterable

PLUGIN_NAME = "closelly-ai-plugins"
PLUGIN_VERSION_RE = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+([.-][0-9A-Za-z.-]+)?$")
KEBAB_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SKILL_NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
IDENTITY_MANIFESTS = (
    "plugin.json",
    ".codex-plugin/plugin.json",
    ".claude-plugin/plugin.json",
)
REQUIRED_FILES = IDENTITY_MANIFESTS + (
    ".claude-plugin/marketplace.json",
    ".agents/plugins/marketplace.json",
    "skills/diagnose-plugin/SKILL.md",
    "skills/diagnose-plugin/scripts/diagnose.py",
    "config/mcp.remote.example.json",
    "LICENSE",
)
FORBIDDEN_ACTIVE_MCP = ("mcp.json", ".mcp.json", ".app.json")
SKIP_SCAN_DIRS = {".git", "dist", "__pycache__", ".venv", "node_modules"}
TEXT_SUFFIXES = {
    ".json",
    ".md",
    ".py",
    ".yml",
    ".yaml",
    ".toml",
    ".txt",
    ".example",
    ".sh",
    ".csv",
}
_BEGIN = "-----BEGIN "
_PRIV = "PRIVATE KEY-----"
SECRET_PATTERNS = (
    ("aws-access-key", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("github-pat", re.compile(r"ghp_[A-Za-z0-9]{20,}")),
    ("github-fine-grained-pat", re.compile(r"github_pat_[A-Za-z0-9_]{20,}")),
    ("slack-token", re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}")),
    ("private-key", re.compile(_BEGIN + r"(?:RSA |OPENSSH |EC |DSA )?" + _PRIV)),
    ("pem-private", re.compile(_BEGIN + _PRIV)),
)
PLACEHOLDER_HINTS = (
    "example.invalid",
    "replace_me",
    "changeme",
    "your_",
    "${",
    "pending",
)
ABSOLUTE_PATH_RE = re.compile(r"(^|[\s\"'])(/?(?:Users|home|opt|var|etc)/[^\s\"']+|file:///[\s\"']+|[A-Za-z]:\\[^\s\"']+)")


class ValidationError(Exception):
    pass


def repo_root_from(start: Path | None = None) -> Path:
    here = (start or Path(__file__).resolve()).parent
    for current in [here, *here.parents]:
        if (current / "plugin.json").is_file() and (current / "skills").is_dir():
            return current
    raise ValidationError("No se encontró la raíz del repositorio de plugins.")


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValidationError(f"{path}: JSON inválido ({exc})") from exc
    except OSError as exc:
        raise ValidationError(f"{path}: no se pudo leer ({exc})") from exc


def parse_frontmatter(text: str) -> dict[str, str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        raise ValidationError("SKILL.md no tiene frontmatter YAML delimitado por ---")
    data: dict[str, str] = {}
    current_key: str | None = None
    for raw_line in match.group(1).splitlines():
        line = raw_line.rstrip()
        if not line or line.strip().startswith("#"):
            continue
        if line.startswith("  ") and current_key == "metadata":
            nested = line.strip()
            if ":" in nested:
                nested_key, nested_value = nested.split(":", 1)
                data[f"metadata.{nested_key.strip()}"] = nested_value.strip().strip('"').strip("'")
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        current_key = key.strip()
        data[current_key] = value.strip().strip('"').strip("'")
    return data


def iter_files(root: Path) -> Iterable[Path]:
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [name for name in dirnames if name not in SKIP_SCAN_DIRS]
        for filename in filenames:
            yield Path(dirpath) / filename


def check_required_files(root: Path, errors: list[str]) -> None:
    for relative in REQUIRED_FILES:
        if not (root / relative).is_file():
            errors.append(f"Falta el archivo requerido {relative}")


def check_identity_sync(root: Path, errors: list[str]) -> dict[str, str]:
    canonical = load_json(root / "plugin.json")
    if not isinstance(canonical, dict):
        errors.append("plugin.json debe ser un objeto JSON")
        return {}

    name = str(canonical.get("name") or "")
    version = str(canonical.get("version") or "")
    description = str(canonical.get("description") or "")
    if name != PLUGIN_NAME:
        errors.append(f"plugin.json name debe ser {PLUGIN_NAME}, recibido {name!r}")
    if not PLUGIN_VERSION_RE.match(version):
        errors.append(f"plugin.json version no es SemVer: {version!r}")
    if not description:
        errors.append("plugin.json description está vacío")
    schema = str(canonical.get("$schema") or "")
    if schema != "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json":
        errors.append("plugin.json debe declarar el schema Agent Plugins 1.0.0")
    extra = set(canonical) - {
        "$schema",
        "name",
        "version",
        "description",
        "author",
        "homepage",
        "repository",
        "license",
        "keywords",
        "extensions",
    }
    if extra:
        errors.append(f"plugin.json tiene campos no portables: {sorted(extra)}")

    for relative in IDENTITY_MANIFESTS:
        payload = load_json(root / relative)
        if not isinstance(payload, dict):
            errors.append(f"{relative} debe ser un objeto JSON")
            continue
        for field, expected in (("name", name), ("version", version), ("description", description)):
            actual = str(payload.get(field) or "")
            if actual != expected:
                errors.append(f"{relative} {field}={actual!r} no coincide con plugin.json ({expected!r})")

    claude_market = load_json(root / ".claude-plugin/marketplace.json")
    if isinstance(claude_market, dict):
        if str(claude_market.get("name") or "") != name:
            errors.append(".claude-plugin/marketplace.json name no coincide con el identificador del plugin")
        plugins = claude_market.get("plugins")
        if not isinstance(plugins, list) or not plugins:
            errors.append(".claude-plugin/marketplace.json debe listar al menos un plugin")
        else:
            entry = plugins[0]
            if not isinstance(entry, dict):
                errors.append("Entrada de marketplace Claude inválida")
            else:
                if str(entry.get("name") or "") != name:
                    errors.append("Marketplace Claude: name de plugin no sincronizado")
                if str(entry.get("version") or "") != version:
                    errors.append("Marketplace Claude: version de plugin no sincronizada")
                if str(entry.get("description") or "") != description:
                    errors.append("Marketplace Claude: description de plugin no sincronizada")
                if str(entry.get("source") or "") != "./":
                    errors.append("Marketplace Claude debe apuntar a ./ para no duplicar skills/")
                if str(entry.get("skills") or "") not in {"./skills/", "./skills"}:
                    errors.append("Marketplace Claude debe cargar skills desde ./skills/")

    agents_market = load_json(root / ".agents/plugins/marketplace.json")
    if isinstance(agents_market, dict):
        if str(agents_market.get("name") or "") != name:
            errors.append(".agents/plugins/marketplace.json name no coincide con el identificador del plugin")
        plugins = agents_market.get("plugins")
        if not isinstance(plugins, list) or not plugins:
            errors.append(".agents/plugins/marketplace.json debe listar al menos un plugin")
        else:
            entry = plugins[0]
            source = entry.get("source") if isinstance(entry, dict) else None
            if not isinstance(entry, dict) or str(entry.get("name") or "") != name:
                errors.append("Marketplace Codex: name de plugin no sincronizado")
            elif not isinstance(source, dict) or source.get("source") != "local" or source.get("path") != "./":
                errors.append("Marketplace Codex debe usar source.local path ./")
            policy = entry.get("policy") if isinstance(entry, dict) else None
            if not isinstance(policy, dict) or "installation" not in policy or "authentication" not in policy:
                errors.append("Marketplace Codex requiere policy.installation y policy.authentication")
            if not isinstance(entry, dict) or not entry.get("category"):
                errors.append("Marketplace Codex requiere category")

    return {"name": name, "version": version, "description": description}
