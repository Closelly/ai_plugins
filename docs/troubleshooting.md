# Solución de problemas

## El plugin no aparece

- Repo: `Closelly/ai_plugins`.
- ChatGPT/Codex: `.agents/plugins/marketplace.json`, `.codex-plugin/plugin.json`, `commands/` y `skills/mcp-business/agents/openai.yaml` (nombre Closelly MCP App).
- Claude Code: `.claude-plugin/marketplace.json`, `.claude-plugin/plugin.json`, `commands/` (`/closelly`, `/LENA`) y `.mcp.json`.
- Copilot CLI: `plugin.json` en la raíz.

## Icono del marketplace en blanco

Causa típica: `assets/logo.png` era un PNG blanco / no cuadrado y `interface.logo` apuntaba a ese archivo (el skill sí se veía porque usa `icon_small`).

Desde **1.10.0**:

1. `assets/logo.png` debe ser el logo colorido cuadrado (512×512).
2. `composerIcon` → `./assets/icon.png` (256×256).
3. Reinstala/actualiza el marketplace y reinicia ChatGPT/Codex.

## MCP en Claude Code no pide OAuth

Debe existir `.mcp.json` en la raíz con `mcpServers.closelly-business.url` = `https://auth.closelly.com/mcp/business`. Reinstala el plugin y usa una tool; el consentimiento OAuth ocurre al primer uso.

## ChatGPT no conecta el MCP (solo carga Skills)

Causas típicas:

1. **Pre-1.9.0:** faltaba entrypoint MCP.
2. **1.9.0:** existía `mcp.json`, pero `extensions.com.openai` en root `plugin.json` solo tenía `interface` y **reemplaza** el overlay `.codex-plugin` (se perdía `"mcpServers"`).

Desde **1.10.0**:

1. Root `plugin.json` debe incluir `"extensions": { "com.openai": { "mcpServers": "./.mcp.json", "interface": { ... } } }`.
2. `.mcp.json` con `"type": "http"` + `oauth_resource` + OAuth DCR (mismo patrón Notion/Cloudflare).
3. Reinstala/actualiza (`codex plugin marketplace upgrade closelly-ai-plugins`) y reinicia.
4. Autoriza `closelly-business` cuando el host lo pida.

`.app.json` con `asdk_app_…` sigue siendo opcional (directory App mapping pre-registrado).

## Claude.ai / Cowork no ve el connector

Esperado. En esos productos el custom connector es siempre manual (Settings → URL).

## No aparecen `/closelly` ni `/LENA`

Reinstala o actualiza el plugin. Los comandos viven en `commands/closelly.md` y `commands/LENA.md`.

## ZIP

El workflow de release (desde plugin.json, sin tag manual) publica: `closelly-ai-plugins-<version>.zip`.
