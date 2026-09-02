# Solución de problemas

## El plugin no aparece tras añadirlo desde GitHub

- Confirma que usas el repo `Closelly/ai_plugins` y no un fork desactualizado.
- ChatGPT/Codex lee `.agents/plugins/marketplace.json` y `.codex-plugin/plugin.json`.
- Claude Code lee `.claude-plugin/marketplace.json` y `.claude-plugin/plugin.json`.
- Copilot CLI lee `plugin.json` en la raíz. También acepta el marketplace en `.claude-plugin/`.

## Nombre o versión distintos entre hosts

Ejecuta la skill `diagnose-plugin`. Si `identity.consistent=false`, un manifiesto está desfasado. Alinea `name`, `version` y `description` y vuelve a validar:

```bash
python3 scripts/validate.py
```

## Skills duplicadas o que no cargan

Debe existir un único directorio físico `skills/`. No crees `skills/` dentro de `.codex-plugin/` ni `.claude-plugin/`, ni uses enlaces simbólicos.

## MCP se intentó conectar solo

El plugin no debe incluir `mcp.json`, `.mcp.json` ni `.app.json`. Si aparecen, elimínalos. El connector documentado vive en `config/mcp.business.json` y se conecta con OAuth en el host.

## El ZIP no instala

Descarga también `SHA256SUMS` de la misma release:

```bash
sha256sum -c SHA256SUMS
```

Usa el ZIP del host correcto (`chatgpt-codex`, `claude-code` o `github-copilot-cli`).

## Validación local

```bash
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
git diff --check
```
