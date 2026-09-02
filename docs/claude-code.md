# Claude Code

## Instalar desde GitHub

```bash
claude plugin marketplace add Closelly/ai_plugins
claude plugin install closelly-ai-plugins@closelly-ai-plugins
```

En una sesión interactiva:

```
/plugin marketplace add Closelly/ai_plugins
/plugin install closelly-ai-plugins@closelly-ai-plugins
```

Prueba local:

```bash
claude --plugin-dir .
claude plugin validate . --strict
```

## Actualizar

```bash
claude plugin marketplace update closelly-ai-plugins
claude plugin update closelly-ai-plugins@closelly-ai-plugins
```

Un bump de `version` en `.claude-plugin/plugin.json` es lo que dispara la actualización para usuarios que instalaron desde el marketplace.

## Desinstalar

```bash
claude plugin uninstall closelly-ai-plugins@closelly-ai-plugins
claude plugin marketplace remove closelly-ai-plugins
```

## ZIP de release

El artefacto `closelly-ai-plugins-claude-code-<version>.zip` se puede cargar con:

```bash
claude --plugin-dir closelly-ai-plugins-claude-code-<version>.zip
```

o `--plugin-url` apuntando a la URL de GitHub Releases. Valida el SHA-256 de `SHA256SUMS`.

## Diagnóstico

```
/closelly-ai-plugins:diagnose-plugin
```

El informe debe mostrar el mismo `plugin.name` y `plugin.version` que en Codex y Copilot CLI.

## MCP Business

Añade el connector `https://auth.closelly.com/mcp/business` (OAuth de User). La skill `mcp-business` describe tools, scopes y el flujo single-tenant.
