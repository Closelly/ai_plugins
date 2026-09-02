# Solución de problemas

## El plugin no aparece

- Repo: `Closelly/ai_plugins`.
- ChatGPT/Codex: `.agents/plugins/marketplace.json`, `.codex-plugin/plugin.json` y `skills/mcp-business/agents/openai.yaml`.
- Claude Code: `.claude-plugin/marketplace.json`, `.claude-plugin/plugin.json` y `.mcp.json`.
- Copilot CLI: `plugin.json` en la raíz.

## MCP en Claude Code no pide OAuth

Debe existir `.mcp.json` en la raíz con `mcpServers.closelly-business.url` = `https://auth.closelly.com/mcp/business`. Reinstala el plugin y usa una tool; el consentimiento OAuth ocurre al primer uso.

## ChatGPT no conecta el MCP solo

Esperado. `.app.json` está pendiente (hace falta `connector_…`). Añade un Custom Connector manual. No uses `.mcp.json` como integración de ChatGPT Web.

## Claude.ai / Cowork no ve el connector

Esperado. En esos productos el custom connector es siempre manual (Settings → URL).

## ZIP

La release publica un archivo: `closelly-ai-plugins-<version>.zip`.
