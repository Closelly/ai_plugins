# Solución de problemas

## El plugin no aparece

- Repo: `Closelly/ai_plugins`.
- ChatGPT/Codex: `.agents/plugins/marketplace.json` y `.codex-plugin/plugin.json`.
- Claude Code: `.claude-plugin/marketplace.json` y `.claude-plugin/plugin.json`.
- Copilot CLI: `plugin.json` en la raíz.

## Nombre o versión distintos

Pide la skill `diagnose-plugin`. Debe leer los JSON y reportar el mismo `plugin.name` y `plugin.version`.

## MCP se conectó solo

No debe haber `mcp.json`, `.mcp.json` ni `.app.json`. El connector documentado es `config/mcp.business.json` (OAuth en el host).

## ZIP

La release publica un archivo: `closelly-ai-plugins-<version>.zip`.
