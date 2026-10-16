# Claude Code

## Instalar desde GitHub

```bash
claude plugin marketplace add Closelly/ai_plugins
claude plugin install closelly-ai-plugins@closelly-ai-plugins
```

En una sesión interactiva:

```
/plugin marketplace add Closelly/ai_plugins
/plugin install closelly-ai-plugins@closelly-ai-plugins
```

Prueba local:

```bash
claude --plugin-dir .
```

## Actualizar

```bash
claude plugin marketplace update closelly-ai-plugins
claude plugin update closelly-ai-plugins@closelly-ai-plugins
```

Un bump de `version` en `.claude-plugin/plugin.json` es lo que dispara la actualización para usuarios que instalaron desde el marketplace.

## Desinstalar

```bash
claude plugin uninstall closelly-ai-plugins@closelly-ai-plugins
claude plugin marketplace remove closelly-ai-plugins
```

## ZIP de release

El workflow de release (desde plugin.json, sin tag manual) publica: `closelly-ai-plugins-<version>.zip`.

## MCP Business

Claude Code lee **`.mcp.json`** en la raíz del plugin (`.claude-plugin/plugin.json` y el marketplace declaran `mcpServers: ./.mcp.json`). ChatGPT/Codex usan el portable `mcp.json` (`streamable-http`); no confundir ambos archivos:

- URL: `https://auth.closelly.com/mcp/business`
- Auth: OAuth de User (email + password), no InternalCredential

Tras instalar el plugin, el primer uso de una tool MCP dispara el flujo OAuth. Requiere `business.mcp_enabled = true`. El tenant sale del token.

La UI del plugin es **Closelly MCP App**. Comandos: **`/closelly`** y **`/LENA`** (`commands/`). El playbook de tools sigue en `skills/mcp-business/SKILL.md`.

## Claude.ai / Cowork

En Claude.ai y Cowork el custom connector es **siempre manual**: Settings → añadir connector → URL `https://auth.closelly.com/mcp/business`. Los archivos del repo no preconfiguran esa UI.
