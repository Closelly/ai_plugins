# Closelly AI Plugins

Fuente única, versionada y portable de plugins y skills de Closelly para **ChatGPT/Codex**, **Claude Code** y **GitHub Copilot CLI**.

| Campo | Valor |
| --- | --- |
| Identificador | `closelly-ai-plugins` |
| Versión | `1.1.0` |
| Skills | `skills/` (único directorio físico) |
| MCP Business | Documentado (`config/mcp.business.json`); **no auto-activado** |

## Instalar desde GitHub

No hace falta parches manuales si el host soporta plugins desde un repo git:

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

La skill `mcp-business` da contexto a los agentes sobre el MCP de clientes Closelly:

- URL: `https://auth.closelly.com/mcp/business`
- Auth: OAuth de User (email + password)
- Config: `config/mcp.business.json`
- Playbook: `skills/mcp-business/SKILL.md`

El plugin **no** crea `mcp.json` / `.mcp.json` / `.app.json`. Cada host añade el connector y el usuario completa OAuth.

## Actualizar y desinstalar

Cada guía de plataforma documenta update y uninstall. En resumen, vuelve a sincronizar el marketplace o instala la etiqueta SemVer `vX.Y.Z`. Para ZIP, descarga el artefacto del host y verifica `SHA256SUMS`.

## Diagnóstico

La skill `diagnose-plugin` informa el mismo nombre y la misma versión en los tres hosts:

```
plugin.name=closelly-ai-plugins
plugin.version=1.1.0
```

```bash
python3 skills/diagnose-plugin/scripts/diagnose.py
```

## Validar y empaquetar

```bash
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
python3 scripts/package_release.py --output dist --check
```

Un push de etiqueta `v1.1.0` publica los ZIP por servicio y sus checksums SHA-256.

## Arquitectura y mantenimiento

- [Arquitectura portable](docs/architecture.md)
- [MCP Business](docs/mcp-remote.md)
- [Solución de problemas](docs/troubleshooting.md)
- [Seguridad](SECURITY.md)
- [Changelog](CHANGELOG.md)

Al añadir una skill, colócala solo en `skills/<nombre>/SKILL.md`, alinea identidad y versión, y ejecuta el validador. No dupliques el directorio `skills/` por host y no auto-actives MCP con `mcp.json`.
