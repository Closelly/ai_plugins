# Release y versionado

Fuente de verdad de la versión: **`plugin.json`** → campo `version` (SemVer).

No hace falta crear ni pushear un tag a mano para publicar. El workflow de release lee `plugin.json`, comprueba que el GitHub Release aún no exista y, si corresponde, publica el ZIP.

## Regla de PRs (obligatoria)

**Cada PR debe incrementar la versión** del plugin respecto a la rama base (`main`).

1. Sube `version` en `plugin.json` (p. ej. `1.7.0` → `1.8.0`).
2. Alinea la misma versión en:
   - `.codex-plugin/plugin.json`
   - `.claude-plugin/plugin.json`
   - `.claude-plugin/marketplace.json` (`metadata.version` y `plugins[].version`)
3. Documenta el cambio en `CHANGELOG.md`.
4. Actualiza la tabla de versión en `README.md` si aplica.

El workflow **PR version** (`.github/workflows/pr-version.yml`) falla el check si:

- `plugin.json` mantiene la misma versión que `main`, o
- la versión del PR no es mayor (SemVer `major.minor.patch`), o
- los manifests listados arriba no están sincronizados.

## Pipeline de release (sin tag manual)

Workflow: `.github/workflows/release.yml`

| Trigger | Comportamiento |
| --- | --- |
| `push` a `main` | Lee `plugin.json`, decide si publicar |
| `workflow_dispatch` | Igual, útil para reintentos |

Pasos:

1. Lee `version` de `plugin.json` (debe ser SemVer).
2. Comprueba si ya existe el GitHub Release `v{version}` (`gh release view`).
3. Si **existe**: no hace nada (idempotente).
4. Si **no existe**:
   - Genera `closelly-ai-plugins-{version}.zip`
   - Publica el GitHub Release con `softprops/action-gh-release` usando `tag_name: v{version}` y `target_commitish` del commit mergeado

El action puede materializar el tag `v{version}` como parte del release. Eso es un efecto del publish; el desarrollador **no** necesita ejecutar `git tag` ni `git push --tags`.

## Flujo recomendado

```text
PR → bump version en plugin.json (+ manifests) → merge a main
                                                  ↓
                                         release.yml
                                                  ↓
                              ¿Existe release vX.Y.Z?
                               /                \
                             sí                  no
                            skip         ZIP + GitHub Release
```

## Artefacto

Cada release publica un único archivo:

`closelly-ai-plugins-X.Y.Z.zip`

## Notas

- Releases históricos creados solo con tags `v*.*.*` siguen siendo válidos; el nuevo flujo los respeta (si el release ya está, no lo regenera).
- Para forzar un reintento tras un fallo intermitente, usa **Actions → Release → Run workflow** (`workflow_dispatch`) en el commit de `main` que ya tenga la versión deseada en `plugin.json`.
