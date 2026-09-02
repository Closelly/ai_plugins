# Arquitectura portable

Este repositorio es la fuente única del plugin `closelly-ai-plugins`. El mismo árbol se instala en ChatGPT/Codex, Claude Code y GitHub Copilot CLI. El paquete es markdown, JSON y YAML (UI ChatGPT). No hay scripts.

## Identidad

| Campo | Valor |
| --- | --- |
| Identificador | `closelly-ai-plugins` |
| Versión | `1.4.0` |
| MCP Business | `https://auth.closelly.com/mcp/business` (OAuth, skill `mcp-business`) |

Alinea `name`, `version` y `description` en `plugin.json`, `.codex-plugin/plugin.json`, `.claude-plugin/plugin.json` y el marketplace Claude.

## Layout

```
.
├── plugin.json
├── .mcp.json                          # Claude Code (OAuth al primer uso)
├── .codex-plugin/plugin.json          # sin mcpServers ni apps
├── .claude-plugin/plugin.json
├── .claude-plugin/marketplace.json
├── .agents/plugins/marketplace.json
├── skills/
│   └── mcp-business/
│       ├── SKILL.md
│       ├── agents/openai.yaml         # UI ChatGPT/Codex
│       └── references/
└── config/mcp.business.json           # config portable / documentación
```

## MCP por host

| Host | Cómo se conecta |
| --- | --- |
| Claude Code | `.mcp.json` en la raíz. El usuario completa OAuth al primer uso de tools. |
| ChatGPT / Codex | Skill + marketplace ahora. App (`.app.json` + `"apps"` en `.codex-plugin/plugin.json`) **pendiente** hasta tener `connector_…`. Hasta entonces, Custom Connector manual. |
| Claude.ai / Cowork | Siempre manual: Settings → custom connector → URL Business. El repo no puede preconfigurarlo. |
| Copilot CLI | MCP HTTP manual con la misma URL. |

No hay `mcpServers` ni `apps` en `.codex-plugin/plugin.json`. `extensions.com.closelly.mcp.remote.enabled` permanece `false` para no tratar `.mcp.json` como App de ChatGPT.
