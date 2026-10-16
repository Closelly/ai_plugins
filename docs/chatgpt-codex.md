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

El workflow de release (desde plugin.json, sin tag manual) publica: `closelly-ai-plugins-<version>.zip`.

## MCP Business (bundle portable)

Al instalar el plugin, ChatGPT/Codex cargan el MCP Business porque el paquete portable incluye **`mcp.json`** en la raíz (Agent Plugins) y `.codex-plugin/plugin.json` declara:

```json
"mcpServers": "./mcp.json"
```

Ese archivo apunta a `https://auth.closelly.com/mcp/business` con transporte **`streamable-http`** y OAuth **DCR** (`extensions.com.openai.auth.client.mode: dcr`).

Flujo:

1. Instala `closelly-ai-plugins` (o reinstálalo tras actualizar el marketplace).
2. Conecta / autoriza el connector `closelly-business` cuando el host lo pida (OAuth User email + password). Si solo ves Skills y no el connector, confirma que existe `mcp.json` en la raíz del plugin.
3. Usa `/closelly` o `/LENA` (playbook `skills/mcp-business/SKILL.md`; no `/mcp/internal`).

Requisitos: `business.mcp_enabled = true`. El tenant sale del token.

### `.app.json` (opcional)

Un mapping `connector_…` / `asdk_app_…` en `.app.json` sigue siendo opcional para el directory App de ChatGPT. **No** es necesario para que el MCP funcione vía el bundle `mcpServers`.
