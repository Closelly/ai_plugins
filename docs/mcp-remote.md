# MCP Business

Este plugin documenta y conecta el **MCP Business** de Closelly.

## Coexistencia por host

| Archivo | Host | Estado |
| --- | --- |
| `.mcp.json` | Claude Code | Publicado. OAuth al primer uso de tools. |
| `.mcp.json` vía `mcpServers` en `.codex-plugin/plugin.json` | ChatGPT / Codex | Publicado. OAuth DCR al conectar. |
| `config/mcp.business.json` | Documentación portable | Publicado. Misma URL/OAuth (+ auth OpenAI). |
| `skills/mcp-business/agents/openai.yaml` | ChatGPT / Codex UI | Publicado. Incluye `dependencies.tools`. |
| `commands/closelly.md`, `commands/LENA.md` | `/closelly`, `/LENA` | Publicado. |
| `.app.json` + `"apps"` | ChatGPT App directory mapping | **Opcional** (`connector_…`). |
| Claude.ai / Cowork custom connector | Claude.ai | Siempre **manual** (Settings → URL). |

`extensions.com.closelly.mcp.remote.enabled` es `true` (bundle ChatGPT/Codex activo).

## Connector canónico

| Campo | Valor |
| --- | --- |
| Nombre | `closelly-business` |
| URL | `https://auth.closelly.com/mcp/business` |
| Auth | OAuth 2.0 (User email + password) |
| Login | `https://auth.closelly.com/oauth/login` |
| ChatGPT/Codex client registration | DCR (`registration_endpoint` del AS) |
| Skill | `skills/mcp-business/` |
| Config | `.mcp.json` / `config/mcp.business.json` |

El tenant sale del token; no se pasa `business_id` de otro negocio. Requiere `business.mcp_enabled = true`.

La plantilla copiable está también en `config/mcp.remote.example.json`. No copies secretos ni tokens Bearer al repositorio.

## Activar en un host

1. Instala este plugin (skills + MCP bundle).
2. **Claude Code:** `.mcp.json` en la raíz; completa OAuth al usar una tool.
3. **ChatGPT / Codex:** el plugin declara `mcpServers`; completa OAuth DCR al conectar `closelly-business`.
4. **Claude.ai / Cowork:** Settings → custom connector → URL Business (manual).
5. Usa `/closelly` o `/LENA`. Playbook: `skills/mcp-business/SKILL.md`.

Cuando exista un `connector_…` de ChatGPT Directory, se puede añadir `.app.json` + `"apps"` como mapping adicional sin quitar el bundle `mcpServers`.
