# GitHub Copilot CLI

## Instalar desde GitHub

Instalación directa del repo (manifiesto `plugin.json` en la raíz):

```bash
copilot plugin install Closelly/ai_plugins
```

O registrando el marketplace del repositorio (Claude marketplace compatible):

```bash
copilot plugin marketplace add Closelly/ai_plugins
copilot plugin install closelly-ai-plugins@closelly-ai-plugins
```

## Actualizar

```bash
copilot plugin update closelly-ai-plugins
```

Para refrescar el catálogo:

```bash
copilot plugin marketplace update closelly-ai-plugins
```

## Desinstalar

```bash
copilot plugin uninstall closelly-ai-plugins
copilot plugin marketplace remove closelly-ai-plugins
```

## ZIP de release

La release publica un archivo: `closelly-ai-plugins-<version>.zip`.

## MCP Business

Añade el MCP HTTP `https://auth.closelly.com/mcp/business` con OAuth de User. La skill `mcp-business` es el contexto de tools y scopes del tenant. `.mcp.json` es para Claude Code; Copilot CLI no lo auto-activa.
