# Catálogo de actividades — brief pedagógico ↔ MCP

Fuente de verdad de tipos disponibles: `get_course_authoring_schema` / `tools/list`. Esta tabla es orientativa; si un `content_type` no aparece en el schema, no lo uses.

## Flashcard

- **Propósito:** reforzar conceptos, presentar ideas simples, dar la bienvenida o instrucciones.
- **Formato de diseño:** tarjetas ~20 cm alto × 10 cm ancho; texto breve (móvil); pueden incluir imagen/icono.
- **Límite:** máximo 10 cards por set.
- **`content_type` MCP:** preferir `ContentArticle` o `ContentImage` (no existe tipo `Flashcard`).
- **Entregable pedagógico:** descripción de cada card (texto + imagen/icono sugerido).
- **Payload MCP:** actividad borrador con nombre, duración 1–3 min, descripción/contenido breve; el arte de las cards puede quedar en el chat si no hay upload.

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
- **Payload MCP:** metadatos de la actividad + URL/archivo cuando exista. El storyboard **no** sustituye el video.

## Interactivo (Genially / slideshow)

- **Propósito:** interacción slide a slide, selección, feedback positivo/negativo.
- **Formato de diseño:** 5–15 slides; contenido más denso que flashcard, aún legible en móvil.
- **`content_type` MCP:** `ContentCanvas` (Genially) o `ContentIframe` (interactivo externo).
- **Entregable pedagógico:**
  - Nombre (hasta 40 caracteres)
  - Hasta 3 objetivos
  - Descripción general
  - Número de slides + detalle slide a slide (interacciones y navegación)
  - Duración estimada
- **Payload MCP:** actividad + URL/`genially_file` cuando el schema lo permita.

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
