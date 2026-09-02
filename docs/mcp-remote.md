# MCP remoto (preparado, desactivado)

Este plugin deja listo el contrato para un servidor MCP remoto de Closelly, pero **no lo activa**.

No se publican todavía:

- `mcp.json`
- `.mcp.json`
- `.app.json`
- `mcpServers` / `apps` en `.codex-plugin/plugin.json`

La plantilla está en `config/mcp.remote.example.json`. Usa `https://mcp.example.invalid/mcp` y `${CLOSELLY_MCP_TOKEN}` como marcadores. No copies secretos al repositorio.

Para activarlo en una versión futura hay que, en el mismo cambio:

1. Definir el endpoint real y el esquema de autenticación.
2. Copiar la plantilla a `mcp.json` / `.mcp.json` según el host.
3. Poner `extensions.com.closelly.mcp.remote.enabled` en `true`.
4. Subir la versión SemVer y documentar el cambio en `CHANGELOG.md`.
