# Changelog

El versionado sigue [Semantic Versioning](https://semver.org/).

## 1.3.0 - 2026-09-02

### Removed

- Skill `diagnose-plugin` (no forma parte del estándar de plugins y no aporta contexto de MCP Business).

## 1.2.0 - 2026-09-02

### Changed

- El paquete queda solo con markdown y JSON (sin scripts, tests ni workflow de validación).
- El release de GitHub Actions genera un único `closelly-ai-plugins-<version>.zip`.

## 1.1.0 - 2026-09-02

### Added

- Skill `mcp-business` portada del playbook de backend (tools, scopes OAuth, PII, analytics y exports).
- Config documentada del connector MCP Business en `config/mcp.business.json` (`https://auth.closelly.com/mcp/business`, OAuth).
- Referencias `tools-reference.md` y `examples.md` como único directorio físico `skills/mcp-business/`.

### Changed

- `extensions.com.closelly.mcp` documenta el endpoint y la skill de Business; `remote.enabled` sigue en `false` (sin auto-activar `mcp.json`).

## 1.0.0 - 2026-09-02

### Added

- Identidad portable `closelly-ai-plugins` sincronizada en `plugin.json`, `.codex-plugin/plugin.json` y `.claude-plugin/plugin.json`.
- Catálogos `.agents/plugins/marketplace.json` y `.claude-plugin/marketplace.json`.
- Releases SemVer.
- Plantilla de MCP remoto desactivada.
