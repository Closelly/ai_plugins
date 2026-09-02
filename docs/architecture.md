# Arquitectura portable

Este repositorio es la fuente única del plugin `closelly-ai-plugins`. El mismo árbol se instala en ChatGPT/Codex, Claude Code y GitHub Copilot CLI sin duplicar skills.

## Identidad

| Campo | Valor |
| --- | --- |
| Identificador | `closelly-ai-plugins` |
| Versión | SemVer en `plugin.json` (ahora `1.1.0`) |
| Descripción | Sincronizada en todos los manifiestos de plugin |
| MCP Business | `https://auth.closelly.com/mcp/business` (OAuth, skill `mcp-business`) |

Cualquier cambio de nombre, versión o descripción debe actualizarse en:

- `plugin.json`
- `.codex-plugin/plugin.json`
- `.claude-plugin/plugin.json`
- entradas de plugin en `.claude-plugin/marketplace.json`
- `metadata.plugin_*` de cada `skills/<nombre>/SKILL.md`

`python3 scripts/validate.py` falla si esos campos se desalinean.

## Layout

```
.
├── plugin.json                      # Agent Plugins 1.0 / Copilot CLI
├── .codex-plugin/plugin.json        # ChatGPT / Codex
├── .claude-plugin/plugin.json       # Claude Code
├── .claude-plugin/marketplace.json  # Catálogo Claude / Copilot
├── .agents/plugins/marketplace.json # Catálogo ChatGPT / Codex
├── skills/                          # Único directorio físico de skills
│   ├── diagnose-plugin/
│   └── mcp-business/
└── config/mcp.business.json         # Connector MCP Business (OAuth, no auto-activo)
```

Los hosts descubren skills desde `skills/`. No hay copias por plataforma ni enlaces simbólicos.

## MCP remoto

El connector MCP Business está documentado en `config/mcp.business.json` y `docs/mcp-remote.md`. No existe `mcp.json`, `.mcp.json` ni `.app.json` en la raíz, y `extensions.com.closelly.mcp.remote.enabled` es `false`.
