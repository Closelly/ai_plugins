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

## MCP Business (bundle Codex / ChatGPT)

Al instalar el plugin, ChatGPT/Codex deben cargar el MCP Business porque:

1. Root `plugin.json` declara **`extensions.com.openai.mcpServers": "./.mcp.json"`** (obligatorio: si solo existe `interface` en `extensions.com.openai`, ese objeto **reemplaza** todo el overlay `.codex-plugin/plugin.json` y se pierde el MCP).
2. `.codex-plugin/plugin.json` también declara `"mcpServers": "./.mcp.json"` (fallback si no hay overlay inline).
3. `.mcp.json` usa el shape de plugins oficiales OpenAI: `"type": "http"`, `url`, `oauth_resource` + OAuth DCR.

Flujo:

1. Instala o **reinstala** `closelly-ai-plugins` (tras 1.10.0).
2. Con `policy.authentication: ON_INSTALL`, el host debe pedir OAuth del connector `closelly-business`.
3. Usa `/closelly` o `/LENA`.

Requisitos: `business.mcp_enabled = true`. El tenant sale del token.

### Icono del plugin

`interface.logo` / `composerIcon` apuntan a PNG cuadrados coloridos en `assets/` (`logo.png` 512×512, `icon.png` 256×256). Un `logo.png` blanco o no cuadrado deja el avatar del marketplace en blanco.

### `.app.json` (opcional, directory App)

Los plugins del directorio público de OpenAI suelen mapear un `asdk_app_…` / `connector_…` en `.app.json`. Eso solo aplica si ya registraste el MCP una vez en ChatGPT (Plugins → Add custom MCP) y obtuviste el ID técnico. **No** es necesario para que el bundle `mcpServers` conecte el MCP en un marketplace de repo; sí puede hacer aparecer una fila “App” aparte en el directory oficial.
