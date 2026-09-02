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
ABSOLUTE_PATH_RE = re.compile(r"(^|[\s\"'])(/?(?:Users|home|opt|var|etc)/[^\s\"']+|file:///[^^\s\"']+|[A-Za-z]:\\[^\s\"']+)")


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


def check_codex_paths(root: Path, errors: list[str]) -> None:
    payload = load_json(root / ".codex-plugin/plugin.json")
    if not isinstance(payload, dict):
        return
    skills = payload.get("skills")
    if skills != "./skills/":
        errors.append('.codex-plugin/plugin.json skills debe ser "./skills/"')
    for key in ("skills", "mcpServers", "hooks", "apps"):
        value = payload.get(key)
        if isinstance(value, str) and not value.startswith("./"):
            errors.append(f".codex-plugin/plugin.json {key} debe ser una ruta relativa que empiece por ./")


def check_skills(root: Path, identity: dict[str, str], errors: list[str]) -> None:
    skills_root = root / "skills"
    if not skills_root.is_dir():
        errors.append("Falta el directorio físico skills/")
        return

    skill_dirs = [path for path in skills_root.iterdir() if path.is_dir()]
    if not skill_dirs:
        errors.append("skills/ no contiene ninguna skill")

    diagnose = skills_root / "diagnose-plugin"
    if not (diagnose / "SKILL.md").is_file():
        errors.append("Falta skills/diagnose-plugin/SKILL.md")
        return

    text = (diagnose / "SKILL.md").read_text(encoding="utf-8")
    try:
        frontmatter = parse_frontmatter(text)
    except ValidationError as exc:
        errors.append(str(exc))
        return

    name = frontmatter.get("name", "")
    description = frontmatter.get("description", "")
    if name != "diagnose-plugin":
        errors.append(f"Frontmatter name debe coincidir con el directorio diagnose-plugin, recibido {name!r}")
    if not SKILL_NAME_RE.match(name):
        errors.append(f"Frontmatter name inválido: {name!r}")
    if not description or len(description) > 1024:
        errors.append("Frontmatter description ausente o demasiado largo")
    if frontmatter.get("metadata.plugin_name") != identity.get("name"):
        errors.append("metadata.plugin_name de la skill no coincide con el identificador del plugin")
    if frontmatter.get("metadata.plugin_version") != identity.get("version"):
        errors.append("metadata.plugin_version de la skill no coincide con la versión del plugin")

    for skill_dir in skill_dirs:
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.is_file():
            errors.append(f"{skill_dir.relative_to(root)} no contiene SKILL.md")
            continue
        try:
            fm = parse_frontmatter(skill_file.read_text(encoding="utf-8"))
        except ValidationError as exc:
            errors.append(f"{skill_file.relative_to(root)}: {exc}")
            continue
        if fm.get("name") != skill_dir.name:
            errors.append(f"{skill_file.relative_to(root)} name={fm.get('name')!r} no coincide con {skill_dir.name}")

    nested = list(skills_root.glob("*/*/SKILL.md"))
    if nested:
        errors.append("No se permiten skills anidadas más allá de skills/<nombre>/SKILL.md")


def check_single_physical_skills_dir(root: Path, errors: list[str]) -> None:
    extra_skill_roots = []
    for candidate in (
        root / ".codex-plugin" / "skills",
        root / ".claude-plugin" / "skills",
        root / ".agents" / "skills",
        root / "chatgpt" / "skills",
        root / "claude" / "skills",
        root / "copilot" / "skills",
    ):
        if candidate.exists():
            extra_skill_roots.append(str(candidate.relative_to(root)))
    if extra_skill_roots:
        errors.append(f"Skills duplicadas fuera de skills/: {extra_skill_roots}")


def check_symlinks(root: Path, errors: list[str]) -> None:
    for path in iter_files(root):
        if path.is_symlink():
            errors.append(f"Enlace simbólico prohibido: {path.relative_to(root)}")
    for dirpath, dirnames, _filenames in os.walk(root):
        dirnames[:] = [name for name in dirnames if name not in SKIP_SCAN_DIRS]
        for name in dirnames:
            candidate = Path(dirpath) / name
            if candidate.is_symlink():
                errors.append(f"Enlace simbólico prohibido: {candidate.relative_to(root)}")


def check_absolute_paths(root: Path, errors: list[str]) -> None:
    for relative in (
        "plugin.json",
        ".codex-plugin/plugin.json",
        ".claude-plugin/plugin.json",
        ".claude-plugin/marketplace.json",
        ".agents/plugins/marketplace.json",
        "config/mcp.remote.example.json",
    ):
        path = root / relative
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        if ABSOLUTE_PATH_RE.search(text) or "file://" in text:
            errors.append(f"{relative} contiene rutas absolutas")
        payload = load_json(path)
        blob = json.dumps(payload)
        if ".." in blob:
            errors.append(f"{relative} contiene recorridos de ruta '..'")


def check_secrets(root: Path, errors: list[str]) -> None:
    for path in iter_files(root):
        if path.suffix.lower() not in TEXT_SUFFIXES and path.name not in {"LICENSE"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            errors.append(f"Archivo binario inesperado: {path.relative_to(root)}")
            continue
        lowered = text.lower()
        for label, pattern in SECRET_PATTERNS:
            for match in pattern.finditer(text):
                snippet = match.group(0)
                window = lowered[max(0, match.start() - 40) : match.end() + 40]
                if any(hint in window for hint in PLACEHOLDER_HINTS):
                    continue
                errors.append(f"Posible secreto ({label}) en {path.relative_to(root)}: {snippet[:12]}…")


def check_mcp_inactive(root: Path, errors: list[str]) -> None:
    for relative in FORBIDDEN_ACTIVE_MCP:
        if (root / relative).exists():
            errors.append(f"MCP remoto no debe activarse: elimina {relative} hasta definir endpoint y autenticación")
    payload = load_json(root / "plugin.json")
    remote = {}
    if isinstance(payload, dict):
        extensions = payload.get("extensions")
        if isinstance(extensions, dict):
            block = extensions.get("com.closelly.mcp")
            if isinstance(block, dict):
                remote = block.get("remote") if isinstance(block.get("remote"), dict) else {}
    if remote.get("enabled") is True:
        errors.append("extensions.com.closelly.mcp.remote.enabled debe ser false")
    example = root / "config/mcp.remote.example.json"
    if not example.is_file():
        errors.append("Falta config/mcp.remote.example.json para preparar MCP remoto desactivado")
    else:
        data = load_json(example)
        if not isinstance(data, dict) or "mcpServers" not in data:
            errors.append("config/mcp.remote.example.json debe declarar mcpServers de ejemplo")

    codex = load_json(root / ".codex-plugin/plugin.json")
    if isinstance(codex, dict):
        for key in ("mcpServers", "apps"):
            if key in codex:
                errors.append(f".codex-plugin/plugin.json no debe activar {key} todavía")


def check_dependencies(root: Path, errors: list[str]) -> None:
    claude = load_json(root / ".claude-plugin/plugin.json")
    if isinstance(claude, dict) and claude.get("dependencies"):
        errors.append("No declares dependencias de otros plugins hasta que existan paquetes versionados")
    package_json = root / "package.json"
    if package_json.is_file():
        errors.append("No empaquetes package.json de runtime; este plugin es de manifiestos y skills")


def check_compatibility(root: Path, errors: list[str]) -> None:
    if not KEBAB_RE.match(PLUGIN_NAME):
        errors.append("El identificador del plugin debe ser kebab-case")
    diagnose = root / "skills/diagnose-plugin/scripts/diagnose.py"
    if diagnose.is_file() and "plugin.name=" not in diagnose.read_text(encoding="utf-8"):
        errors.append("El script de diagnóstico debe emitir plugin.name=")


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    check_required_files(root, errors)
    identity: dict[str, str] = {}
    try:
        identity = check_identity_sync(root, errors)
        check_codex_paths(root, errors)
        check_skills(root, identity, errors)
        check_single_physical_skills_dir(root, errors)
        check_symlinks(root, errors)
        check_absolute_paths(root, errors)
        check_secrets(root, errors)
        check_mcp_inactive(root, errors)
        check_dependencies(root, errors)
        check_compatibility(root, errors)
    except ValidationError as exc:
        errors.append(str(exc))
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Valida el plugin portable Closelly")
    parser.add_argument("--root", type=Path, default=None)
    args = parser.parse_args(argv)
    root = (args.root or repo_root_from()).resolve()
    errors = validate(root)
    if errors:
        sys.stderr.write("Validación fallida:\n")
        for error in errors:
            sys.stderr.write(f"- {error}\n")
        return 1
    sys.stdout.write(f"OK {root}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
