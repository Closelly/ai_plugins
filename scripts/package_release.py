#!/usr/bin/env python3
"""Build per-host plugin ZIP archives and SHA-256 checksums."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

FIXED_TIME = (2026, 1, 1, 0, 0, 0)
PLUGIN_NAME = "closelly-ai-plugins"

HOSTS = {
    "chatgpt-codex": (
        ".codex-plugin/plugin.json",
        "plugin.json",
        "skills",
        "LICENSE",
        "config/mcp.business.json",
        "config/mcp.remote.example.json",
        "docs/mcp-remote.md",
        "docs/chatgpt-codex.md",
    ),
    "claude-code": (
        ".claude-plugin/plugin.json",
        "skills",
        "LICENSE",
        "config/mcp.business.json",
        "config/mcp.remote.example.json",
        "docs/mcp-remote.md",
        "docs/claude-code.md",
    ),
    "github-copilot-cli": (
        "plugin.json",
        "skills",
        "LICENSE",
        "config/mcp.business.json",
        "config/mcp.remote.example.json",
        "docs/mcp-remote.md",
        "docs/github-copilot-cli.md",
    ),
}


def load_version(root: Path) -> str:
    payload = json.loads((root / "plugin.json").read_text(encoding="utf-8"))
    return str(payload["version"])


def iter_path_files(root: Path, relative: str) -> list[Path]:
    target = root / relative
    if target.is_file():
        return [target]
    if target.is_dir():
        files = [
            path
            for path in target.rglob("*")
            if path.is_file()
            and "__pycache__" not in path.parts
            and path.suffix != ".pyc"
        ]
        return sorted(files, key=lambda item: item.relative_to(root).as_posix())
    raise FileNotFoundError(relative)


def add_file(zf: zipfile.ZipFile, root: Path, path: Path) -> None:
    if path.is_symlink():
        raise ValueError(f"No se empaquetan enlaces simbólicos: {path}")
    arcname = path.relative_to(root).as_posix()
    data = path.read_bytes()
    info = zipfile.ZipInfo(arcname, date_time=FIXED_TIME)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o644 << 16
    zf.writestr(info, data)


def build_zip(root: Path, host: str, members: tuple[str, ...]) -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as zf:
        for relative in members:
            for path in iter_path_files(root, relative):
                add_file(zf, root, path)
    return buffer.getvalue()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def package(root: Path, output: Path, expected_version: str | None = None) -> list[Path]:
    version = load_version(root)
    if expected_version and expected_version.lstrip("v") != version:
        raise ValueError(f"La etiqueta {expected_version} no coincide con plugin.json version {version}")
    output.mkdir(parents=True, exist_ok=True)
    created: list[Path] = []
    checksum_lines: list[str] = []
    for host, members in HOSTS.items():
        payload = build_zip(root, host, members)
        filename = f"{PLUGIN_NAME}-{host}-{version}.zip"
        target = output / filename
        target.write_bytes(payload)
        created.append(target)
        checksum_lines.append(f"{sha256_bytes(payload)}  {filename}")
    sums = output / "SHA256SUMS"
    body = "\n".join(checksum_lines) + "\n"
    sums.write_text(body, encoding="utf-8")
    created.append(sums)
    (output / "SHA256SUMS.sha256").write_text(
        f"{sha256_bytes(body.encode('utf-8'))}  SHA256SUMS\n",
        encoding="utf-8",
    )
    created.append(output / "SHA256SUMS.sha256")
    stamp = output / "build-info.txt"
    stamp.write_text(
        f"plugin={PLUGIN_NAME}\nversion={version}\nbuilt_at={datetime.now(timezone.utc).isoformat()}\n",
        encoding="utf-8",
    )
    created.append(stamp)
    return created


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Empaqueta ZIP por host con checksums SHA-256")
    parser.add_argument("--root", type=Path, default=None)
    parser.add_argument("--output", type=Path, default=Path("dist"))
    parser.add_argument("--version-from-tag", default=None)
    parser.add_argument("--check", action="store_true", help="Construye en un directorio temporal y verifica miembros")
    args = parser.parse_args(argv)
    root = (args.root or Path(__file__).resolve().parents[1]).resolve()
    try:
        created = package(root, args.output.resolve(), args.version_from_tag)
    except Exception as exc:  # noqa: BLE001 - CLI boundary
        sys.stderr.write(f"{exc}\n")
        return 1
    if args.check:
        for path in created:
            if path.suffix != ".zip":
                continue
            with zipfile.ZipFile(path) as zf:
                names = zf.namelist()
                if "skills/diagnose-plugin/SKILL.md" not in names:
                    sys.stderr.write(f"{path.name} no incluye skills/diagnose-plugin/SKILL.md\n")
                    return 1
                if any(name in names for name in ("mcp.json", ".mcp.json", ".app.json")):
                    sys.stderr.write(f"{path.name} incluye MCP activo\n")
                    return 1
    for path in created:
        sys.stdout.write(f"{path}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
