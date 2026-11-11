# Catálogo de actividades — brief pedagógico ↔ MCP

Fuente de verdad de tipos disponibles: `get_course_authoring_schema` / `tools/list`. Esta tabla es orientativa; si un `content_type` no aparece en el schema, no lo uses.

## Tarjetas de contenido / flashcards

- **Propósito:** reforzar conceptos, presentar ideas simples, dar la bienvenida o instrucciones.
- **Formato de diseño:** consulta [formatos de tarjetas](../../create-activities/references/activity-formats.md). El editor acepta PNG/SVG y muestra 600×400 como referencia; no es un límite de píxeles validado. Usa texto breve y comprueba el preview móvil. La antigua medida de 20×10 cm no es un requisito del editor.
- **Recomendación pedagógica:** hasta 10 tarjetas por set; no es un límite confirmado del backend.
- **`content_type`:** `ContentCanvas` corresponde a tarjetas de contenido en el backoffice actual; no existe un tipo `Flashcard`. El schema MCP debe exponer los campos necesarios para persistir la secuencia. `ContentArticle` y `ContentImage` son otros formatos y se eligen expresamente, no como equivalentes automáticos.
- **Entregable pedagógico:** descripción de cada card (texto + imagen/icono sugerido).
- **Payload MCP:** campos del schema vivo y referencias alojadas que permita. Si faltan upload o children, entrega los archivos finales mediante `create-activities` y señala la carga pendiente; no declares que la secuencia quedó guardada.

## Video

- **Propósito:** contexto, historia, contenido complejo, captar atención.
- **Duración:** 20 segundos a 3 minutos.
- **`content_type` MCP:** `ContentVideo`.
- **Entregable pedagógico:**
  - Nombre (hasta 40 caracteres)
  - Hasta 3 objetivos de aprendizaje
  - Descripción general (qué ocurre en pantalla)
  - Número de escenas + storyboard escena a escena
  - Duración estimada
- **Payload MCP:** metadatos + referencia alojada cuando exista. El storyboard **no** sustituye el video. Para producirlo, seguir [video con Remotion](../../create-activities/references/video-remotion.md), con diseño del usuario, voz en off y subtítulos.

## Interactivo (Genially / slideshow)

- **Propósito:** interacción slide a slide, selección, feedback positivo/negativo.
- **Formato de diseño:** 5–15 slides; contenido más denso que flashcard, aún legible en móvil.
- **`content_type`:** el wizard actual mapea Genially a `ContentPresentation`. El interactivo externo y el ZIP Interactivo Closelly usan `ContentIframe` con `sub_type=external` o `closelly_interactive`, respectivamente. Confirmar los campos disponibles en el schema MCP.
- **Entregable pedagógico:**
  - Nombre (hasta 40 caracteres)
  - Hasta 3 objetivos
  - Descripción general
  - Número de slides + detalle slide a slide (interacciones y navegación)
  - Duración estimada
- **Payload MCP:** actividad + referencia o URL admitida por el schema. Para el ZIP, seguir [closelly-interactive](../../closelly-interactive/SKILL.md); no inventar un campo `genially_file` o una herramienta de upload.

## Evaluación estándar

- **Propósito:** comprobar comprensión.
- **Patrón sugerido:** 2–3 preguntas al final de cada sección; 8–12 al final del curso.
- **Tipos de ítem:** opción única, múltiple, Likert, abiertas; con imagen/icono si hace falta.
- **`content_type` MCP:** `ContentTest` (preguntas como children según schema).
- **Entregable pedagógico:** lista de preguntas y respuestas (cuando apliquen).
- **Payload MCP:** solo la estructura que acepte el schema de evaluación.

## Evaluación con LENA (recomendada)

LENA es el agente conversacional de voz de Closelly: diálogo, feedback inmediato, puntaje y resumen final.

- **`content_type` MCP:** `ContentAssistantQuiz` (quiz conversacional). Valora `ContentRolePlay` si el schema y el caso lo ameritan.
- **Entregable pedagógico:** guion de evaluación (temas/preguntas, criterios de feedback, qué reforzar).
- **Payload MCP:** configuración AI que permita el schema; no inventes campos.

## Otros tipos (si el schema los lista)

| Label orientativo | `content_type` |
|-------------------|----------------|
| Audio | `ContentAudio` |
| Documento / presentación | `ContentDocument` / `ContentPresentation` |
| Encuesta / brecha | `ContentSurvey` |
| Tarea / evidencias | `ContentHomework`, `ContentTextEvidence`, `ContentImageEvidence`, `ContentAudioEvidence`, `ContentVideoEvidence` |
| Juego | `ContentGame` |
| Blended / compliance | `ContentBlended` / `ContentCompliance` |
| DJ SENCE | `ContentDj` (solo cursos SENCE; restricciones de edición) |
