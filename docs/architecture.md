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
├── .codex-plugin/plugin.json          # mcpServers -> ./.mcp.json
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
| ChatGPT / Codex | UI Closelly MCP App; `/closelly` o `/LENA`. MCP vía `mcpServers` → `.mcp.json` (OAuth DCR). `.app.json` opcional. |
| Claude.ai / Cowork | Siempre manual: Settings → custom connector → URL Business. |
| Copilot CLI | MCP HTTP manual; `/closelly` o `/LENA` si el host carga `commands/`. |

`.codex-plugin/plugin.json` declara `mcpServers: "./.mcp.json"`. `extensions.com.closelly.mcp.remote.enabled` es `true` (bundle ChatGPT/Codex). `.app.json` sigue opcional.
