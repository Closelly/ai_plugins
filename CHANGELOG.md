# Changelog

El versionado sigue [Semantic Versioning](https://semver.org/).

## 1.10.0 - 2026-10-26

### Fixed

- ChatGPT marketplace: el avatar quedaba en blanco porque `assets/logo.png` era un PNG blanco no cuadrado. Ahora `logo.png` / `icon.png` / `icon-small.png` / `logo-dark.png` son el mark colorido cuadrado.
- ChatGPT/Codex: el MCP no se cableaba al instalar porque `extensions.com.openai` en root `plugin.json` solo tenía `interface` y **reemplaza** el overlay `.codex-plugin` (se perdía `mcpServers`). Ahora declara `"mcpServers": "./.mcp.json"` dentro de `extensions.com.openai`.
- Alinea `.mcp.json` / `mcp.json` al shape de plugins oficiales OpenAI (`type: http` + `oauth_resource` + OAuth DCR).

### Changed

- Versión 1.10.0 en manifests y marketplaces.
- Docs `chatgpt-codex.md` y `troubleshooting.md` con la regla del overlay OpenAI y el requisito de logo cuadrado colorido.

## 1.9.0 - 2026-10-16

### Fixed

- ChatGPT/Codex marketplace: el install solo cargaba skills porque faltaba el entrypoint portable `mcp.json` (Agent Plugins). Ahora el MCP Business se declara en `mcp.json` con `type: streamable-http` y OAuth DCR.
- Claude Code: `.claude-plugin/plugin.json` y el marketplace declaran explícitamente `mcpServers: ./.mcp.json` y `skills`.

### Changed

- `.codex-plugin/plugin.json` apunta `mcpServers` a `./mcp.json`.
- `config/mcp.business.json` alineado al shape portable (`streamable-http` + `extensions.com.openai.auth`).
- `plugin.json` incluye `extensions.com.openai.interface` para hosts portables.

## 1.8.0 - 2026-10-15

### Added

- Icono Closelly: `assets/logo.png`, `assets/icon.png`, `assets/logo-dark.png`, `assets/icon-small.png`.
- Claude: campo `icon` en `.claude-plugin/plugin.json`.
- ChatGPT/Codex: `logo`, `logoDark`, `composerIcon`, `brandColor` en `.codex-plugin/plugin.json` y skill `openai.yaml`.
- Release automático desde `plugin.json` al push a `main` (sin crear tag manual): verifica que no exista el release y publica el ZIP.
- Check de PR `pr-version`: falla si la versión en `plugin.json` no cambió respecto a `main`.
- Documentación del flujo en `docs/release.md`.

## 1.7.0 - 2026-10-15

### Added

- ChatGPT/Codex: `"mcpServers": "./.mcp.json"` en `.codex-plugin/plugin.json` para conectar el MCP Business al instalar el plugin (opción bundle portable).
- Auth OpenAI en `.mcp.json`: `extensions.com.openai.auth` with `client.mode: dcr` (el AS de Closelly expone `registration_endpoint`).
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
