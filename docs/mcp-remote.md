# MCP Business

Este plugin documenta el **MCP Business** de Closelly y, en Claude Code, lo conecta vía `.mcp.json`.

## Coexistencia (no mezclar hosts)

| Archivo | Host | Estado |
| --- | --- |
| `.mcp.json` | Claude Code | Publicado. OAuth al primer uso de tools. |
| `config/mcp.business.json` | Documentación portable | Publicado. Misma URL/OAuth. |
| `skills/mcp-business/agents/openai.yaml` | ChatGPT / Codex UI (Closelly MCP App) | Publicado. |
| `commands/closelly.md`, `commands/LENA.md` | `/closelly`, `/LENA` | Publicado. |
| `.app.json` + `"apps"` en `.codex-plugin/plugin.json` | ChatGPT App | **Pendiente** (`connector_…`). |
| `mcpServers` en `.codex-plugin/plugin.json` | ChatGPT Web | **No.** No es el camino de ChatGPT. |
| Claude.ai / Cowork custom connector | Claude.ai | Siempre **manual** (Settings → URL). |

`extensions.com.closelly.mcp.remote.enabled` permanece `false` para no tratar la config Claude como App de ChatGPT.

## Connector canónico

| Campo | Valor |
| --- | --- |
| Nombre | `closelly-business` |
| URL | `https://auth.closelly.com/mcp/business` |
| Auth | OAuth 2.0 (User email + password) |
| Login | `https://auth.closelly.com/oauth/login` |
| Skill | `skills/mcp-business/` |
| Config portable | `config/mcp.business.json` |
| Claude Code | `.mcp.json` |

El tenant sale del token; no se pasa `business_id` de otro negocio. Requiere `business.mcp_enabled = true`.

La plantilla copiable está también en `config/mcp.remote.example.json`. No copies secretos ni tokens Bearer al repositorio.

## Activar en un host

1. Instala este plugin (skills + config).
2. **Claude Code:** `.mcp.json` ya está; completa OAuth al usar una tool.
3. **ChatGPT:** Custom Connector manual hasta que exista `.app.json`.
4. **Claude.ai / Cowork:** Settings → custom connector → URL Business.
5. Usa `/closelly` o `/LENA`. El playbook de tools está en `skills/mcp-business/SKILL.md`.

Cuando exista el `connector_…` de ChatGPT, el mismo cambio debe añadir `.app.json`, `"apps": "./.app.json"` en `.codex-plugin/plugin.json`, subir SemVer y documentarlo en `CHANGELOG.md`.
