---
name: diagnose-plugin
description: Informa el nombre y la versión del plugin Closelly leyendo los manifiestos JSON. Úsalo para identificar la instalación en ChatGPT/Codex, Claude Code y GitHub Copilot CLI.
license: MIT
metadata:
  plugin_name: closelly-ai-plugins
  plugin_version: "1.2.0"
---

# Diagnóstico del plugin Closelly

Lee los manifiestos JSON y reporta **el mismo nombre y la misma versión**. No ejecutes comandos ni scripts.

## Manifiestos

En la raíz del plugin (o `${CLAUDE_PLUGIN_ROOT}` / `${PLUGIN_ROOT}`):

- `plugin.json`
- `.codex-plugin/plugin.json`
- `.claude-plugin/plugin.json`

Extrae `name`, `version` y `description` de cada archivo que exista.

## Informe

Responde en texto plano, una clave por línea:

```
plugin.name=closelly-ai-plugins
plugin.version=1.2.0
plugin.description=<description del manifiesto>
host=<chatgpt-codex|claude-code|github-copilot-cli|unknown>
identity.consistent=<true si name/version/description coinciden>
mcp.remote.enabled=false
```

`host` puede cambiar según el cliente; nombre y versión no. Si un manifiesto difiere, `identity.consistent=false`. No inventes valores.

`mcp.remote.enabled` es `false` salvo que existan `mcp.json`, `.mcp.json` o `.app.json`. El connector Business se documenta en `config/mcp.business.json` y se conecta con OAuth, no con este skill.
