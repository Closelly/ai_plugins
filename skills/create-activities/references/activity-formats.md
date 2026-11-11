# Formatos por actividad y tarjetas

Referencia comprobada el **11 de noviembre de 2026** contra el schema de autoría del backend y el editor del backoffice. El schema de la sesión decide los tipos y campos disponibles. Las recomendaciones de exportación no añaden restricciones al validador del producto.

## Tipos y entregables

| Actividad | `content_type` | Qué producir o configurar |
| --- | --- | --- |
| Tarjetas de contenido | `ContentCanvas` | Secuencia ordenada de imágenes PNG o SVG. En el editor se guardan como `canvas_cards` con `index` y `body_url`; el schema MCP puede exponer otra estructura o no permitir children. |
| Video | `ContentVideo` | Video terminado, recomendado MP4/H.264 con audio AAC y subtítulos visibles. El modelo admite orientación `landscape` o `portrait`, valida URL HTTP(S) y puede cargar un archivo a Vimeo. Ver [video](video-remotion.md). |
| Audio / podcast | `ContentAudio` | MP3 real y su transcripción. El modelo valida URL HTTP(S) terminada en `.mp3`, y el flujo de children comprueba esa extensión. Ver [audio](audio.md). |
| Imagen / carrusel de imágenes | `ContentImage` | Imágenes finales y orden de lectura. El modelo usa una colección `url_images`, no un campo universal `url`; confirmar cómo lo expone el schema. Dimensiones según el uso y preview, sin un tamaño universal confirmado. |
| Documento | `ContentDocument` | PDF final como opción de entrega compatible con el editor PDF; conservar el editable si se solicita. El modelo valida una URL HTTP(S), sin imponer una medida de página universal. |
| Presentación / Genially | `ContentPresentation` | URL de presentación que el reproductor pueda abrir. El wizard actual mapea Genially a este tipo y el modelo acepta orientación. Un PPTX local no es automáticamente una URL embebible. |
| Interactivo alojado en Closelly | `ContentIframe`, `sub_type=closelly_interactive` | ZIP del [skill de interactivos](../../closelly-interactive/SKILL.md): una orientación fija por paquete, horizontal 1600×900 o vertical 900×1600. |
| Iframe externo | `ContentIframe`, `sub_type=external` | URL embebible del proveedor; no usar el contrato ZIP como si fuera un iframe externo. |
| Artículo | `ContentArticle` | Texto o HTML y bloques de artículo según el editor/schema; no es el mismo tipo que tarjetas PNG/SVG. |
| Evaluación | `ContentTest` | Preguntas, alternativas, respuesta correcta y feedback cuando corresponda; children y tipos de pregunta solo según schema. |
| Encuesta / brecha | `ContentSurvey` | Preguntas y escalas; diferenciar encuesta y brecha mediante los valores de `assessment_type` que devuelva el schema. |
| Quiz conversacional LENA | `ContentAssistantQuiz` | Instrucciones, temas, criterios y configuración AI admitida; no necesita un archivo multimedia ficticio. |
| Role play | `ContentRolePlay` | Escenario, roles, objetivo y criterios de evaluación; adjuntos solo cuando el schema los permita. |
| Tarea | `ContentHomework` | Consigna, entregable esperado y rúbrica; comprobar los archivos o evidencias admitidos en ese flujo. |
| Blended | `ContentBlended` | Instrucciones y condición de aprobación manual/presencial, según configuración disponible. |
| Compliance | `ContentCompliance` | Contenido y condición de cumplimiento que permita el schema; no hay un formato multimedia universal. |
| Juego | `ContentGame` | Recurso o configuración de juego según la herramienta disponible; no asumir que acepta el ZIP de Interactivo Closelly. |
| Declaración SENCE | `ContentDj` | Configuración propia de la plataforma para cursos SENCE; respetar las restricciones que exponga el flujo de autoría. |
| Respuesta o evidencia de texto | `ContentTextEvidence` | Consigna y criterios para la respuesta del alumno; no inventar un tipo `ContentText`. |
| Evidencia de imagen | `ContentImageEvidence` | Consigna y criterios; el alumno entrega el archivo con las extensiones admitidas por su formulario. |
| Evidencia de audio | `ContentAudioEvidence` | Consigna, duración sugerida y criterios; comprobar formatos del formulario, sin heredar automáticamente la restricción MP3 de `ContentAudio`. |
| Evidencia de video | `ContentVideoEvidence` | Consigna, duración sugerida, orientación y criterios; comprobar formatos del flujo de evidencia. |

`Flashcard`, `PDF`, `Genially` y `Tarjetas` son etiquetas de interfaz o de diseño, no necesariamente valores de `content_type`. El mapeo del wizard actual distingue tarjetas (`ContentCanvas`), presentación Genially (`ContentPresentation`) e interactivo (`ContentIframe`).

## Tarjetas de contenido: medidas y archivos

**Comprobado en el editor:** acepta `.png` y `.svg` y muestra **600×400** como referencia de imagen. La subida directa no comprueba dimensiones de píxeles. El mismo componente conserva un modal de recorte 4:3, así que no hay evidencia para declarar una proporción única obligatoria en todas las rutas.

**Recomendación de producción:** si el usuario no aporta una plantilla, partir de 600×400 px (3:2), o 1200×800 px para mayor resolución conservando la proporción. Mantener el mismo formato en toda la secuencia y comprobar el preview móvil del editor concreto antes de finalizar. Si hay una plantilla del cliente o un recorte activo diferente, trabajar con ese formato y validarlo en esa vista.

- Una idea principal por tarjeta; imágenes y texto legibles sin ampliar. Numerar los archivos para conservar el orden, por ejemplo `tarjeta-01.png`.
- Exportar PNG para una tarjeta compuesta, o SVG autocontenido con tipografía resuelta y recursos incluidos.
- La referencia pedagógica de hasta diez tarjetas por set es una recomendación de carga cognitiva, no un límite de archivos confirmado en el backend.
- No convertir centímetros a píxeles sin elegir resolución; el antiguo consejo de 20×10 cm describía un diseño pedagógico y no el contrato del editor de tarjetas.
- No confundir estas imágenes con una portada de curso, un banner o las pantallas HTML de un interactivo: cada recurso tiene un destino diferente.

## Archivos frente a payload MCP

El backend de autoría documenta `file_uploads.mode=reference`: se usan referencias o URLs ya cargadas. Los nombres de campos de los modelos/editor ayudan a entender el contenido, pero no autorizan a enviar `canvas_cards`, `url_images` o cualquier otro campo si el schema de la herramienta no lo ofrece. No se deben enviar los binarios por el chat ni cambiar la extensión de un archivo para simular una conversión.

## Fuentes de producto

- [Schema de tipos y referencias de archivo, backend](https://github.com/Closelly/backend/blob/4fe159f491ed76a82e137c24fbffaf2f2d021b00/lib/closelly/mcp/course_authoring/schema.rb).
- [Tarjetas: selección PNG/SVG y subida directa](https://github.com/Closelly/backoffice_frontend/blob/6be31af78b08114e22a2de26d28b7df1acb8d6f2/src/app/pages/courses/pages/courses-cards/courses-cards.component.ts), [referencia 600×400 y modal de recorte](https://github.com/Closelly/backoffice_frontend/blob/6be31af78b08114e22a2de26d28b7df1acb8d6f2/src/app/pages/courses/pages/courses-cards/courses-cards.component.html).
- [Mapeo de tipos del wizard](https://github.com/Closelly/backoffice_frontend/blob/6be31af78b08114e22a2de26d28b7df1acb8d6f2/src/app/pages/courses/pages/course-wizard/constants/course-activity-backend.constants.ts).
- [Modelos del backend](https://github.com/Closelly/backend/tree/4fe159f491ed76a82e137c24fbffaf2f2d021b00/app/models): `content_audio.rb`, `content_video.rb`, `content_canvas.rb`, `content_image.rb`, `content_document.rb`, `content_presentation.rb` y `content_article.rb`.
