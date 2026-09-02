# MCP Business (documentado, no auto-activado)

Este plugin documenta el **MCP Business** de Closelly para que ChatGPT/Codex, Claude Code y GitHub Copilot CLI tengan el mismo contexto de tools, scopes y OAuth.

No se publican archivos de auto-conexión:

- `mcp.json`
- `.mcp.json`
- `.app.json`
- `mcpServers` / `apps` en `.codex-plugin/plugin.json`

## Connector canónico

| Campo | Valor |
| --- | --- |
| Nombre | `closelly-business` |
| URL | `https://auth.closelly.com/mcp/business` |
| Auth | OAuth 2.0 (User email + password) |
| Login | `https://auth.closelly.com/oauth/login` |
| Skill | `skills/mcp-business/` |
| Config | `config/mcp.business.json` |

`extensions.com.closelly.mcp.remote.enabled` permanece `false`. El usuario añade el connector en su host y completa OAuth. El tenant sale del token; no se pasa `business_id` de otro negocio. Requiere `business.mcp_enabled = true`.

La plantilla copiable está también en `config/mcp.remote.example.json`. No copies secretos ni tokens Bearer al repositorio.

## Activar en un host

1. Instala este plugin (skills + config).
2. Añade un Custom Connector / MCP con URL `https://auth.closelly.com/mcp/business`.
3. Completa OAuth como User del cliente.
4. Usa la skill `mcp-business` como playbook (qué tool llamar, scopes, PII, exports).

Para auto-activar en una versión futura hay que, en el mismo cambio, copiar la config a `mcp.json` / `.mcp.json` según el host, poner `remote.enabled` en `true`, subir SemVer y documentarlo en `CHANGELOG.md`.
