# Seguridad

## Secretos

Este repositorio no debe contener credenciales, tokens, claves privadas ni archivos `.env`. El pipeline rechaza patrones habituales de secretos.

La plantilla `config/mcp.remote.example.json` solo usa marcadores (`example.invalid`, `${CLOSELLY_MCP_TOKEN}`).

## Empaquetado

- Prohibidos los enlaces simbólicos y las rutas absolutas en manifiestos.
- Los ZIP de release se generan en CI con checksums SHA-256.
- MCP remoto permanece desactivado hasta definir endpoint y autenticación.

## Reportes

Si encuentras un secreto publicado o un ZIP manipulado, avisa al equipo de Closelly y rota las credenciales afectadas. No abras un issue público con el valor del secreto.
