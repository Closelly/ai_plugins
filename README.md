# Closelly MCP App

Fuente única, versionada y portable de **Closelly MCP App** para **ChatGPT/Codex**, **Claude Code** y **GitHub Copilot CLI**.

| Campo | Valor |
| --- | --- |
| Nombre visible | Closelly MCP App |
| Identificador | `closelly-ai-plugins` |
| Versión | `1.9.0` |
| Comandos | `/closelly`, `/LENA` |
| Skills | `skills/` (markdown + YAML de UI ChatGPT) |
| Config | `plugin.json`, `mcp.json` (ChatGPT/Codex), `.mcp.json` (Claude Code), `config/*.json` |
| MCP Business | `https://auth.closelly.com/mcp/business` (OAuth) |

Este paquete contiene **markdown**, **JSON** y **YAML**. No incluye scripts ejecutables.

## Instalar desde GitHub

```bash
# ChatGPT / Codex
codex plugin marketplace add Closelly/ai_plugins

# Claude Code
claude plugin marketplace add Closelly/ai_plugins
claude plugin install closelly-ai-plugins@closelly-ai-plugins

# GitHub Copilot CLI
copilot plugin install Closelly/ai_plugins
```

Tras instalar, usa **`/closelly`** o **`/LENA`**.

Guías: [ChatGPT/Codex](docs/chatgpt-codex.md), [Claude Code](docs/claude-code.md), [Copilot CLI](docs/github-copilot-cli.md).

## MCP Business

Closelly MCP App da contexto sobre el MCP de clientes:

- URL: `https://auth.closelly.com/mcp/business`
- Auth: OAuth de User (email + password)
- Comandos: `/closelly`, `/LENA` (`commands/`)
- Config portable: `config/mcp.business.json`
- Claude Code: `.mcp.json` en la raíz (OAuth al primer uso de tools)
- ChatGPT UI: `skills/mcp-business/agents/openai.yaml` (nombre Closelly MCP App)
- ChatGPT/Codex MCP: `mcpServers` → `mcp.json` portable (`streamable-http` + OAuth DCR)
- ChatGPT App (`.app.json` / `connector_…`): opcional, no requerido para el bundle
- Playbook: `skills/mcp-business/SKILL.md`

Claude.ai / Cowork: Settings → custom connector con la misma URL (siempre manual).

## Release

El versionado vive en `plugin.json`. Al mergear a `main`, el workflow crea el GitHub Release (ZIP) **si esa versión aún no existe**. No hace falta crear un tag a mano. Detalle: [docs/release.md](docs/release.md).

**Cada PR debe subir la versión** en `plugin.json` (y manifests alineados). El check `pr-version` lo valida.

## Arquitectura y mantenimiento

- [Arquitectura](docs/architecture.md)
- [Release](docs/release.md)
- [MCP Business](docs/mcp-remote.md)
- [Solución de problemas](docs/troubleshooting.md)
- [Seguridad](SECURITY.md)
- [Changelog](CHANGELOG.md)
