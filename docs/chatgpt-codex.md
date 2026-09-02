# ChatGPT / Codex

## Instalar desde GitHub

```bash
codex plugin marketplace add Closelly/ai_plugins
```

En ChatGPT desktop (Work mode / Codex), el catálogo del repo vive en `.agents/plugins/marketplace.json`. Tras añadir el marketplace, instala `closelly-ai-plugins` desde el directorio de plugins y reinicia la app.

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

El artefacto `closelly-ai-plugins-chatgpt-codex-<version>.zip` incluye `.codex-plugin/plugin.json`, `plugin.json` y `skills/`. Verifica el SHA-256 publicado en `SHA256SUMS` antes de usarlo.

## Diagnóstico

Pide al agente que use la skill `diagnose-plugin`. Debe informar:

```
plugin.name=closelly-ai-plugins
plugin.version=<semver del manifiesto>
```
