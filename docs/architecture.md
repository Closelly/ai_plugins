# Arquitectura portable

Este repositorio es la fuente única del plugin `closelly-ai-plugins`. El mismo árbol se instala en ChatGPT/Codex, Claude Code y GitHub Copilot CLI. Solo hay markdown y JSON.

## Identidad

| Campo | Valor |
| --- | --- |
| Identificador | `closelly-ai-plugins` |
| Versión | `1.2.0` |
| MCP Business | `https://auth.closelly.com/mcp/business` (OAuth, skill `mcp-business`) |

Alinea `name`, `version` y `description` en `plugin.json`, `.codex-plugin/plugin.json`, `.claude-plugin/plugin.json` y el marketplace Claude.

## Layout

```
.
├── plugin.json
├── .codex-plugin/plugin.json
├── .claude-plugin/plugin.json
├── .claude-plugin/marketplace.json
├── .agents/plugins/marketplace.json
├── skills/
│   ├── diagnose-plugin/SKILL.md
│   └── mcp-business/
└── config/mcp.business.json
```

## MCP

El connector está en `config/mcp.business.json`. No hay `mcp.json`, `.mcp.json` ni `.app.json`.
