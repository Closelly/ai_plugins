# Seguridad

Este repositorio no debe contener credenciales, tokens, claves privadas ni archivos `.env`.

El paquete de plugin es markdown, JSON y YAML: no incluye scripts ejecutables. `.mcp.json` y `config/mcp.business.json` solo publican URLs OAuth públicas; no se empaquetan tokens. `.app.json` no existe hasta tener un `connector_…` real.

Si encuentras un secreto publicado, avisa al equipo de Closelly y rota las credenciales. No abras un issue público con el valor del secreto.
