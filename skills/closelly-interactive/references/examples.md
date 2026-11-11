# Ejemplos incluidos y procedencia

- [IA tradicional y generativa](../assets/examples/ia-tradicional-vs-generativa/index.html): horizontal, 1600×900, tres pantallas y audio iniciado por el alumno.
- [Pregunta mínima](../assets/examples/example-two/index.html): vertical, 900×1600, respuesta, feedback y finalización.

Abre el `index.html` de cada carpeta en el navegador. Para crear el ZIP de un ejemplo, comprime el contenido de esa carpeta con `index.html` en la raíz; no empaquetes el skill ni el plugin como actividad.

Cada paquete elige una orientación; redimensionar o girar la pantalla solo cambia su escala y centrado. Prueba ambos en miniatura y en pantalla completa, con texto ampliado. Los ejemplos funcionan sin un runtime inventado: la vista local omite el registro cuando Closelly no está presente.

## Fuente de la copia

Archivos copiados byte a byte desde `docs/interactive_packages/` de [Closelly/backend, commit 64456814a2d4717ca418638909b2d5641abdccac](https://github.com/Closelly/backend/tree/64456814a2d4717ca418638909b2d5641abdccac/docs/interactive_packages), incluidos en el [PR #1034](https://github.com/Closelly/backend/pull/1034), que seguía abierto al preparar esta copia. El skill conserva ese contrato y solo adapta las rutas a los recursos incluidos en el plugin.

Cuando cambie el contrato, revisar el skill de clientes y copiar los dos paquetes completos desde una revisión concreta del backend. Conservar las rutas relativas del HTML, CSS, JavaScript y audio; probar el ajuste y la integridad del ZIP antes de actualizar la referencia de origen.
