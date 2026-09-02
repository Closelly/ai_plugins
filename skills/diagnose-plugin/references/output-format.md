# Formato de informe de diagnóstico

Imprime el informe en texto plano, una clave por línea, sin markdown alrededor del bloque:

```
plugin.name=<kebab-case>
plugin.version=<semver>
plugin.description=<texto>
host=<chatgpt-codex|claude-code|github-copilot-cli|unknown>
identity.consistent=<true|false>
mcp.remote.enabled=false
```

Reglas:

- `plugin.name` y `plugin.version` salen de los manifiestos, no del nombre de carpeta de instalación.
- El valor de `host` puede cambiar según el cliente; **nombre y versión no**.
- Si hay más de un host detectable, usa el más específico y no alteres nombre ni versión.
- `mcp.remote.enabled` permanece `false` hasta que Closelly defina endpoint y autenticación y active el soporte de forma explícita.
