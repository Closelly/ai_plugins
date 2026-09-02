---
name: diagnose-plugin
description: Informa el nombre y la versión del plugin Closelly de forma equivalente en ChatGPT/Codex, Claude Code y GitHub Copilot CLI. Úsalo para diagnosticar la instalación, comprobar identidad sincronizada y verificar que MCP remoto sigue desactivado.
license: MIT
metadata:
  plugin_name: closelly-ai-plugins
  plugin_version: "1.0.0"
---

# Diagnóstico del plugin Closelly

Informa **el mismo nombre y la misma versión** en ChatGPT/Codex, Claude Code y GitHub Copilot CLI. No improvises metadatos: léelos de los manifiestos empaquetados.

## Cuándo usarla

- El usuario pide diagnosticar, verificar o identificar este plugin.
- Hay que confirmar que la instalación cargó `closelly-ai-plugins`.
- Hay que comparar la identidad entre hosts.

## Procedimiento

1. Localiza la raíz del plugin. Prueba en este orden:
   - `${CLAUDE_PLUGIN_ROOT}`
   - `${PLUGIN_ROOT}`
   - el directorio padre de `skills/` (dos niveles por encima de este `SKILL.md`)
2. Ejecuta el script portable, si el entorno permite comandos:

   ```bash
   python3 "${PLUGIN_ROOT}/skills/diagnose-plugin/scripts/diagnose.py"
   ```

   Si `PLUGIN_ROOT` no está definido, usa `CLAUDE_PLUGIN_ROOT` o la raíz detectada.
3. Si no puedes ejecutar el script, lee estos JSON en la raíz detectada (el primero que exista para cada host) y extrae `name` y `version`:
   - `plugin.json`
   - `.codex-plugin/plugin.json`
   - `.claude-plugin/plugin.json`
4. Responde **exactamente** con el bloque de informe descrito en [references/output-format.md](references/output-format.md). Los campos `plugin.name` y `plugin.version` deben coincidir en los tres hosts.
5. Si algún manifiesto difiere, marca `identity.consistent=false` y lista las diferencias. No “corrijas” el informe inventando un valor.
6. No actives MCP remoto. El diagnóstico debe reportar `mcp.remote.enabled=false` mientras el endpoint y la autenticación no estén definidos.

## Identidad canónica

- `plugin.name`: `closelly-ai-plugins`
- `plugin.version`: `1.0.0`

Esos valores deben coincidir con `plugin.json` en la raíz y con los manifiestos de cada host.
