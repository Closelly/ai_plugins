# ChatGPT / Codex

## Instalar desde GitHub

```bash
codex plugin marketplace add Closelly/ai_plugins
```

En ChatGPT desktop (Work mode / Codex), el catálogo del repo vive en `.agents/plugins/marketplace.json`. Tras añadir el marketplace, instala `closelly-ai-plugins` desde el directorio de plugins y reinicia la app.

La UI muestra **Closelly MCP App** (`agents/openai.yaml`). Invoca con **`/closelly`** o **`/LENA`**.

Instalación local para desarrollo:

1. Clona este repositorio.
2. Confirma que `.agents/plugins/marketplace.json` apunta a `"path": "./"`.
3. Añade el marketplace local:

```bash
codex plugin marketplace add ./
```

## Actualizar

```bash
codex plugin marketplace upgrade closelly-ai-plugins
```

Si instalaste desde git, vuelve a sincronizar el ref (por ejemplo `main` o una etiqueta `vX.Y.Z`) y reinicia ChatGPT/Codex.

## Desinstalar

```bash
codex plugin marketplace remove closelly-ai-plugins
```

Quita también el plugin de `~/.codex/config.toml` si quedó habilitado.

## ZIP de release

La release publica un archivo: `closelly-ai-plugins-<version>.zip`.

## MCP Business

La skill y el marketplace están listos. La **ChatGPT App** (`.app.json` con `connector_…` y `"apps"` en `.codex-plugin/plugin.json`) queda **pendiente** hasta registrar el App en ChatGPT.

Hasta entonces:

1. Añade un Custom Connector con URL `https://auth.closelly.com/mcp/business`.
2. Completa OAuth como User (email + password).
3. Usa `/closelly` o `/LENA` (playbook `skills/mcp-business/SKILL.md`; no `/mcp/internal`).

No uses `.mcp.json` ni `mcpServers` en `.codex-plugin/plugin.json` como integración de ChatGPT Web: ese archivo es para Claude Code.
