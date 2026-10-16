# Solución de problemas

## El plugin no aparece

- Repo: `Closelly/ai_plugins`.
- ChatGPT/Codex: `.agents/plugins/marketplace.json`, `.codex-plugin/plugin.json`, `commands/` y `skills/mcp-business/agents/openai.yaml` (nombre Closelly MCP App).
- Claude Code: `.claude-plugin/marketplace.json`, `.claude-plugin/plugin.json`, `commands/` (`/closelly`, `/LENA`) y `.mcp.json`.
- Copilot CLI: `plugin.json` en la raíz.

## MCP en Claude Code no pide OAuth

Debe existir `.mcp.json` en la raíz con `mcpServers.closelly-business.url` = `https://auth.closelly.com/mcp/business`. Reinstala el plugin y usa una tool; el consentimiento OAuth ocurre al primer uso.

## ChatGPT no conecta el MCP solo (solo carga Skills)

Causa típica (pre-1.9.0): faltaba el entrypoint portable **`mcp.json`** en la raíz; el host cargaba Skills pero ignoraba `.mcp.json` (shape Claude).

Desde **1.9.0**:

1. Debe existir `mcp.json` en la raíz (`type: streamable-http` + OAuth DCR).
2. `.codex-plugin/plugin.json` debe tener `"mcpServers": "./mcp.json"`.
3. Reinstala/actualiza el marketplace (`codex plugin marketplace upgrade closelly-ai-plugins`) y reinicia ChatGPT/Codex.
4. Conecta / autoriza el connector `closelly-business` cuando el host lo pida.

`.app.json` sigue siendo opcional (directory App mapping).

## Claude.ai / Cowork no ve el connector

Esperado. En esos productos el custom connector es siempre manual (Settings → URL).

## No aparecen `/closelly` ni `/LENA`

Reinstala o actualiza el plugin a `1.5.0`. Los comandos viven en `commands/closelly.md` y `commands/LENA.md`.

## ZIP

El workflow de release (desde plugin.json, sin tag manual) publica: `closelly-ai-plugins-<version>.zip`.
