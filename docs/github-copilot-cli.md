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

El artefacto `closelly-ai-plugins-github-copilot-cli-<version>.zip` contiene `plugin.json` y `skills/`. Instálalo desde una ruta local:

```bash
copilot plugin install ./closelly-ai-plugins-github-copilot-cli-<version>
```

tras descomprimir y verificar el checksum SHA-256.

## Diagnóstico

Invoca la skill `diagnose-plugin`. El nombre y la versión deben coincidir con ChatGPT/Codex y Claude Code.
