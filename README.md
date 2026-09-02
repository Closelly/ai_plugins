# Closelly AI Plugins

Fuente única, versionada y portable de plugins y skills de Closelly para **ChatGPT/Codex**, **Claude Code** y **GitHub Copilot CLI**.

| Campo | Valor |
| --- | --- |
| Identificador | `closelly-ai-plugins` |
| Versión | `1.3.0` |
| Skills | `skills/` (markdown) |
| Config | `plugin.json`, `config/*.json` |
| MCP Business | `https://auth.closelly.com/mcp/business` (OAuth; no auto-activado) |

Este paquete solo contiene **markdown** y **JSON**. No incluye scripts ejecutables.

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
- Config: `config/mcp.business.json`
- Playbook: `skills/mcp-business/SKILL.md`

Cada host añade el connector; el usuario completa OAuth. No hay `mcp.json` en este repo.

## Release

Una etiqueta `vX.Y.Z` publica **un** ZIP: `closelly-ai-plugins-X.Y.Z.zip`.

## Arquitectura y mantenimiento

- [Arquitectura](docs/architecture.md)
- [MCP Business](docs/mcp-remote.md)
- [Solución de problemas](docs/troubleshooting.md)
- [Seguridad](SECURITY.md)
- [Changelog](CHANGELOG.md)
