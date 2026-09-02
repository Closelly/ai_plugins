# Arquitectura portable

Este repositorio es la fuente única de **Closelly MCP App** (`closelly-ai-plugins`). El mismo árbol se instala en ChatGPT/Codex, Claude Code y GitHub Copilot CLI. El paquete es markdown, JSON y YAML. No hay scripts.

## Identidad

| Campo | Valor |
| --- | --- |
| Nombre visible | Closelly MCP App |
| Identificador | `closelly-ai-plugins` |
| Versión | `1.5.0` |
| Comandos | `/closelly`, `/LENA` |
| MCP Business | `https://auth.closelly.com/mcp/business` (OAuth, skill `mcp-business`) |

Alinea `name`, `version` y el display name **Closelly MCP App** en `plugin.json`, `.codex-plugin/plugin.json`, `.claude-plugin/plugin.json` y el marketplace Claude.

## Layout

```
.
├── plugin.json
├── .mcp.json                          # Claude Code (OAuth al primer uso)
├── commands/
│   ├── closelly.md                    # /closelly
│   └── LENA.md                        # /LENA
├── .codex-plugin/plugin.json          # sin mcpServers ni apps
├── .claude-plugin/plugin.json
├── .claude-plugin/marketplace.json
├── .agents/plugins/marketplace.json
├── skills/
│   └── mcp-business/
│       ├── SKILL.md
│       ├── agents/openai.yaml         # UI ChatGPT: Closelly MCP App
│       └── references/
└── config/mcp.business.json           # config portable / documentación
```

## MCP por host

| Host | Cómo se conecta |
| --- | --- |
| Claude Code | `.mcp.json` en la raíz. Invoca `/closelly` o `/LENA`. OAuth al primer uso de tools. |
| ChatGPT / Codex | UI Closelly MCP App; `/closelly` o `/LENA`. App (`.app.json`) **pendiente**. Custom Connector manual hasta entonces. |
| Claude.ai / Cowork | Siempre manual: Settings → custom connector → URL Business. |
| Copilot CLI | MCP HTTP manual; `/closelly` o `/LENA` si el host carga `commands/`. |

No hay `mcpServers` ni `apps` en `.codex-plugin/plugin.json`. `extensions.com.closelly.mcp.remote.enabled` permanece `false` para no tratar `.mcp.json` como App de ChatGPT.
