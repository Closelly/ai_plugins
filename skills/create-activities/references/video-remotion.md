# Videos educativos con Remotion

Usa **Remotion** para producir el video. El mismo agente desarrolla el guion, crea o coordina la voz en off con su herramienta de audio y sincroniza los subtítulos. El resultado debe ser un video educativo renderizado y revisado.

## Brief visual y selección de estilo

Recoge la paleta de colores, tipografías, logo y referencias de diseño que el usuario debería entregar. Si ya están en la conversación o en sus documentos, reutilízalos. Si faltan, solicítalos antes de fijar el diseño final; puedes avanzar objetivos, guion y storyboard mientras llegan. Si el usuario autoriza proponer una identidad, presenta esa propuesta como tal.

Busca las opciones actuales en [plugins y plantillas de Remotion](remotion-options.md). Comprueba adopción con métricas públicas y fecha de consulta, y elige el estilo por su utilidad educativa: explicación con gráficos, tutorial, relato ilustrado, audio visualizado o demostración espacial. La opción más popular no sustituye el criterio pedagógico.

Usa los skills oficiales de Remotion si están disponibles en el host. Consulta su documentación vigente para la API y mantén `remotion` y los paquetes `@remotion/*` en versiones compatibles. Selecciona solo los paquetes y recursos que requiera el estilo elegido.

## Formato de producción

Estos son valores recomendados para la entrega, no límites universales del backend:

| Propiedad | Recomendación |
| --- | --- |
| Orientación | Una por video: horizontal 1920×1080 o vertical 1080×1920, según el destino y el usuario. |
| Archivo final | MP4, video H.264, audio AAC y formato de píxel compatible con reproducción móvil, como `yuv420p`. |
| Cadencia | 30 fps como base si el brief o el material no requieren otra. |
| Duración | Para microlearning, partir de 20 segundos a 3 minutos y ajustar al objetivo. |
| Voz | Locución creada por el mismo LLM/agente con la capacidad de síntesis disponible; ver [audio](audio.md). |
| Subtítulos | Visibles y sincronizados en el MP4. Entregar también SRT o VTT si se genera una pista separada. |
| Editables | Proyecto Remotion y assets que se puedan reutilizar, con guion y transcripción final. |

Las medidas 1600×900 y 900×1600 del ZIP interactivo no son una restricción del video. `ContentVideo` admite orientación `landscape` o `portrait`; la herramienta de autoría debe exponer ese campo antes de enviarlo. No inventes un campo de subtítulos si el schema no lo incluye.

## Flujo de creación

1. Define un objetivo de aprendizaje y un guion basado en las fuentes del usuario. Organiza la explicación y los ejemplos en escenas; fija texto en pantalla y apoyos visuales sin duplicar párrafos completos de la narración.
2. Elabora un storyboard con estilo, colores del usuario, duración estimada y texto de locución de cada escena.
3. Genera la voz en off real con el flujo de [audio](audio.md). Si la sesión no puede sintetizar audio, informa esa limitación antes de prometer el video narrado completo.
4. Mide la duración de ese audio y obtén tiempos reales de palabras o segmentos mediante la síntesis, transcripción o alineación disponible. No repartas el guion por igual entre escenas como si fueran tiempos medidos.
5. Implementa la composición en Remotion con el aspecto y fps elegidos. Los frames dependen de la duración real de la voz; carga la narración en la composición y ajusta las animaciones a su ritmo.
6. Añade subtítulos legibles sobre fondos variables, con separación de frases y zonas seguras. Evita cubrir diagramas o acciones importantes. Usa las utilidades oficiales de captions o el template adecuado y revisa nombres, cifras y puntuación contra el audio.
7. Renderiza una muestra de las escenas más densas y corrige legibilidad, sincronización y pronunciación. Después renderiza el MP4 completo y comprueba que contiene el audio, termina correctamente y se reproduce en tamaño móvil.
8. Entrega el MP4, subtítulos y editables disponibles. Si se va a crear la actividad, usa `ContentVideo` mediante el flujo de `create-courses`, con archivo/URL ya alojado en una referencia admitida.

Remotion permite renderizar por Studio o CLI. En un proyecto existente, el comando usa su entry point, composition id y ruta de salida reales; comprueba las opciones actuales de codec antes de ejecutarlo. No des por finalizado el trabajo por haber abierto Studio o generado el código React.

## Herramientas para escenas y subtítulos

- `@remotion/transitions`: transiciones y tiempos entre escenas.
- `@remotion/shapes`, `@remotion/paths` o `@remotion/lottie`: recursos gráficos cuando el estilo los necesita; Lottie admite animaciones compatibles, que hay que revisar en el render.
- `@remotion/captions`: importación, agrupación y exportación de subtítulos. La transcripción requiere una herramienta adicional, por ejemplo Whisper local o una integración ya disponible; este paquete no sintetiza por sí solo la voz.

Los subtítulos quemados en imagen permanecen visibles incluso cuando no se ha confirmado soporte de pistas externas en el reproductor. Una pista SRT/VTT separada se entrega como recurso adicional; no se afirma que quedó cargada en Closelly sin verificarlo.

Fuentes oficiales: [skills](https://www.remotion.dev/docs/ai/skills), [transitions](https://www.remotion.dev/docs/transitions/), [Lottie](https://www.remotion.dev/docs/lottie/), [transcripción de audio](https://www.remotion.dev/docs/captions/transcribing), [exportación de subtítulos](https://www.remotion.dev/docs/captions/exporting), [codificación](https://www.remotion.dev/docs/encoding) y [render](https://www.remotion.dev/docs/render).
