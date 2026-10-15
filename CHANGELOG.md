# Changelog

El versionado sigue [Semantic Versioning](https://semver.org/).
## 1.7.0 - 2026-10-15

### Added

- ChatGPT/Codex: `"mcpServers": "./.mcp.json"` en `.codex-plugin/plugin.json` para conectar el MCP Business al instalar el plugin (opción bundle portable).
- Auth OpenAI en `.mcp.json`: `extensions.com.openai.auth` con `client.mode: dcr` (el AS de Closelly expone `registration_endpoint`).
- `dependencies.tools` del MCP en `skills/mcp-business/agents/openai.yaml`.

### Changed

- `extensions.com.closelly.mcp.remote.enabled` pasa a `true` con status `chatgpt-codex-mcp-servers-bundled`.
- Docs de coexistencia: ChatGPT/Codex ya no exigen Custom Connector manual ni `.app.json` para usar el MCP; `.app.json` queda opcional.

## 1.6.0 - 2026-10-14

### Added

- Tools SENCE en el skill Business: `list_sence_implementations`, `get_sence_implementation`, `get_sence_implementation_syncs`, `get_sence_implementation_declarations` (scope `mcp.clients.progress.read`).
- Vista 360 de `get_student` (`include: ["360"]` / secciones challenges, rooms, sence, devices, login_url).
- Ejemplos SENCE y export structure alineados con el playbook del backend.

### Changed

- Inventario documentado: **35 tools** (antes 31).
- Comparación vs MCP Internal: exports unificados (`export_course_progress` / `export_business_progress`); se elimina la referencia obsoleta a `get_course_full_export`.
- Skill resincronizada desde `.agents/skills/mcp-business/` del backend Closelly (rutas `references/` del plugin).

## 1.5.0 - 2026-09-02

### Changed

- Nombre visible del plugin: **Closelly MCP App** (deja de usarse "Closelly Business" / "Closelly AI Plugins" en la UI).
- Comandos de invocación: **`/closelly`** y **`/LENA`** (`commands/closelly.md`, `commands/LENA.md`).

## 1.4.0 - 2026-09-02

### Added

- `.mcp.json` en la raíz para Claude Code (mismo connector OAuth que `config/mcp.business.json`). OAuth de User al primer uso de tools.
- `skills/mcp-business/agents/openai.yaml` con metadatos de UI para ChatGPT/Codex.

### Changed

- Documentación de coexistencia: ChatGPT App (`.app.json`) queda pendiente; Claude.ai/Cowork sigue siendo connector custom manual; Claude Code usa `.mcp.json`.
- `extensions.com.closelly.mcp.remote.enabled` permanece `false` (no hay `mcpServers` ni apps en `.codex-plugin/plugin.json`).

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
