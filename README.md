# Closelly AI Plugins

Fuente única, versionada y portable de plugins y skills de Closelly para **ChatGPT/Codex**, **Claude Code** y **GitHub Copilot CLI**.

| Campo | Valor |
| --- | --- |
| Identificador | `closelly-ai-plugins` |
| Versión | `1.4.0` |
| Skills | `skills/` (markdown + YAML de UI ChatGPT) |
| Config | `plugin.json`, `config/*.json`, `.mcp.json` (Claude Code) |
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

Guías: [ChatGPT/Codex](docs/chatgpt-codex.md), [Claude Code](docs/claude-code.md), [Copilot CLI](docs/github-copilot-cli.md).

## MCP Business

La skill `mcp-business` da contexto sobre el MCP de clientes:

- URL: `https://auth.closelly.com/mcp/business`
- Auth: OAuth de User (email + password)
- Config portable: `config/mcp.business.json`
- Claude Code: `.mcp.json` en la raíz (OAuth al primer uso de tools)
- ChatGPT UI: `skills/mcp-business/agents/openai.yaml`
- ChatGPT App (`.app.json`): **pendiente** hasta tener `connector_…`
- Playbook: `skills/mcp-business/SKILL.md`

Claude.ai / Cowork: Settings → custom connector con la misma URL (siempre manual).

## Release

Una etiqueta `vX.Y.Z` publica **un** ZIP: `closelly-ai-plugins-X.Y.Z.zip`.

## Arquitectura y mantenimiento

- [Arquitectura](docs/architecture.md)
- [MCP Business](docs/mcp-remote.md)
- [Solución de problemas](docs/troubleshooting.md)
- [Seguridad](SECURITY.md)
- [Changelog](CHANGELOG.md)
