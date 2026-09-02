---
name: mcp-business
description: Playbook del MCP Business de Closelly (/mcp/business). Tools single-tenant, scopes OAuth, PII, analytics y exports. Úsalo para dar contexto a ChatGPT/Codex, Claude Code y GitHub Copilot CLI sobre el connector de clientes.
license: MIT
metadata:
  plugin_name: closelly-ai-plugins
  plugin_version: "1.1.0"
  mcp_server: closelly-business
  mcp_url: https://auth.closelly.com/mcp/business
---

# Closelly MCP Business

Playbook para usar el MCP de empresa (cliente). Solo el business de la sesión OAuth. Este repositorio es la fuente portable de la skill; el servidor vive en el backend Closelly.

Conectar el MCP **y** usar esta habilidad. No uses este skill con `/mcp/internal` (ops Closelly).

## Connector

| Campo | Valor |
|-------|--------|
| Nombre | `closelly-business` |
| URL | `https://auth.closelly.com/mcp/business` |
| Transporte | HTTP (JSON-RPC MCP) |
| Auth | OAuth 2.0 (User email + password, no InternalCredential) |
| Login | `https://auth.closelly.com/oauth/login` |
| Resource metadata | `https://auth.closelly.com/.well-known/oauth-protected-resource/mcp/business` |
| Authorization server | `https://auth.closelly.com/.well-known/oauth-authorization-server/mcp/business` |
| Config del plugin | `config/mcp.business.json` |

La config **no se auto-activa** (`mcp.json` / `.mcp.json` / `.app.json` siguen ausentes). Cada host debe añadir el connector OAuth; el usuario completa el consentimiento.

## Distribución

Fuente portable: este plugin (`skills/mcp-business/`). ZIP público del backend:

`https://auth.closelly.com/skills/closelly-skill.zip`

| Host | Cómo usar esta skill |
|------|----------------------|
| **ChatGPT / Codex** | Instala `closelly-ai-plugins`; connector MCP URL `https://auth.closelly.com/mcp/business` |
| **Claude Code** | Instala el plugin; Skills cargan `skills/mcp-business/`; conectar MCP OAuth |
| **GitHub Copilot CLI** | Instala el plugin; usa esta skill como contexto del MCP Business |
| **Cursor** | Descomprimir o `cp -r` a `~/.cursor/skills/`; conectar MCP OAuth |

El ZIP del backend debe contener la carpeta `mcp-business/` con `SKILL.md` (no archivos sueltos en la raíz).

## Conectar MCP

1. Custom Connector → URL exacta `https://auth.closelly.com/mcp/business`.
2. OAuth: `/oauth/login` con **User** (email + password), no InternalCredential.
3. Si el User tiene varios businesses con `mcp_enabled`, elegir uno; si tiene uno, se selecciona solo.
4. Prerrequisito: `business.mcp_enabled = true`.
5. Scopes base: `mcp.clients.students.read`, `mcp.clients.progress.read`, `mcp.clients.reports.read`, `mcp.clients.export`, opcional `mcp.clients.pii.read` (contacto + valores de campos personalizados) y `mcp.clients.interactions.read` (texto de conversaciones / respuestas crudas de evaluaciones).
6. Scopes analíticos por dominio (uno por familia de tools): `mcp.clients.activities.read`, `mcp.clients.assessments.read`, `mcp.clients.lena.conversations.read`, `mcp.clients.lena.metrics.read`, `mcp.clients.surveys.read`, `mcp.clients.challenges.read`, `mcp.clients.campaigns.read`, `mcp.clients.gamification.read`, `mcp.clients.news.read`, `mcp.clients.communications.read`, `mcp.clients.analytics.read`.

## Audiencia

Administradores del cliente: estudiantes, progreso y reportes **solo de su tenant**. Nunca pasar `business_id` de otro negocio; el tenant viene del token.

## Contrato de respuesta

- JSON en `result.content[0].text`.
- Errores tool: `{ "error": "...", "message": "..." }` o `{ "error": "Course not found" }` / `{ "error": "Student not found" }`.
- Errores de acceso: `insufficient_scope`, `forbidden_tenant`, `mcp_disabled`.
- Paginación: `{ "page", "per_page", "total" }`.
- Métricas (`metrics` / `progress`): `total`, `not_started`, `in_progress`, `completed`, `completion_percentage`, `average_progress`.
- **`unit: "enrollments"`**: `metrics.total` son matrículas (pares usuario–curso), no personas únicas. Ver `total_students` / `students_with_enrollments`.

### Envelope analítico (tools de analytics expandidas)

Las 18 tools analíticas (`get_student_activity_progress`, evaluaciones, LENA, encuestas, desafíos, campañas, gamificación, noticias, comunicaciones, engagement) envuelven la respuesta en un contrato versionado. Los datos útiles viven en `result`:

```json
{
  "schema_version": 1,
  "business_id": 106,
  "as_of": "2026-08-13T18:00:00Z",
  "from_date": null,
  "to_date": null,
  "grain": "conversation",
  "unit": "conversations",
  "definitions": {},
  "data_quality": { "status": "ready", "freshness_at": "2026-08-13T18:00:00Z", "warnings": [] },
  "result": { }
}
```

- `grain` describe la unidad de la fila (`activity_attempt`, `conversation`, `survey`, `challenge_submission`, `campaign`, `ranking_position`, `student`, `article_view`, `communication`, …).
- `data_quality.status` es `ready` sin advertencias o `partial` cuando hay `warnings` (p. ej. comunicaciones y engagement declaran límites de semántica de entrega y de canal/dispositivo histórico).
- `definitions` documenta métricas derivadas (p. ej. DAU/WAU/MAU en `get_engagement_summary`).

## Scopes por tool

| Tool | Scope mínimo |
|------|--------------|
| `get_business`, `search_students`, `get_student`, `list_groups` | `mcp.clients.students.read` |
| `list_courses`, `get_progress`, `get_student_progress`, `get_student_activity`, `get_course_detail`, `get_course_progress_summary` | `mcp.clients.progress.read` |
| `get_reports_summary` (incl. bloque `engagement`) | `mcp.clients.reports.read` |
| `export_course_progress`, `export_business_progress` | `mcp.clients.export` |
| `get_student_activity_progress` | `mcp.clients.activities.read` |
| `get_conversational_assessment` | `mcp.clients.assessments.read` |
| `search_lena_conversations`, `get_lena_conversation` | `mcp.clients.lena.conversations.read` |
| `get_lena_metrics` | `mcp.clients.lena.metrics.read` |
| `list_surveys`, `get_survey_summary` | `mcp.clients.surveys.read` |
| `list_challenges`, `get_challenge_summary` | `mcp.clients.challenges.read` |
| `list_campaigns`, `get_campaign_summary`, `get_campaign_ranking` | `mcp.clients.campaigns.read` |
| `get_student_gamification` | `mcp.clients.gamification.read` |
| `list_news`, `get_news_engagement` | `mcp.clients.news.read` |
| `get_communications_summary`, `search_communications` | `mcp.clients.communications.read` |
| `get_engagement_summary` | `mcp.clients.analytics.read` |
| PII (contacto) y valores de campos personalizados en listados / detalle / export / participantes | `mcp.clients.pii.read` (adicional) |
| Texto de conversaciones (`include_message_text`, `get_lena_conversation` con `content_mode=full`), respuestas crudas (`include_assessment_answers`) y feedback/reportes de evaluación (`get_conversational_assessment`) | `mcp.clients.interactions.read` (adicional) |

## Flujo recomendado (3 niveles)

1. **Descubrimiento:** `get_business` → `list_courses` → `list_groups` → `search_students` (usa `include_summary` para traer perfil resumido + grupos + sesiones).
2. **Análisis:** `get_reports_summary` (con `from_date`/`to_date`/`group_by` para el bloque `engagement`) → `get_progress` / `get_course_progress_summary` → `get_student` / `get_student_progress` / `get_student_activity`.
3. **Exportación:** `export_course_progress` / `export_business_progress` → entregar al usuario el `download_url` del archivo `.json` (no incrustar el contenido en la conversación). El enlace **caduca a los 60 minutos**.

Nunca pedir un `course_id` al usuario si puedes obtenerlo con `list_courses`.

## Exportaciones (archivo .json descargable)

Las tools de export **no** devuelven el dataset en el chat. Generan un **archivo `.json`** en S3 con **todos los datos completos** (sin filtros ni paginación) para análisis posteriores. La respuesta MCP solo trae metadatos de descarga.

| Campo de respuesta | Significado |
|--------------------|-------------|
| `file_name` | Nombre del `.json` |
| `download_url` | URL firmada GET para descargar el archivo |
| `expires_at` / `expires_in_seconds` | Caducidad del enlace (**60 min** / `3600`) |
| `format` | Siempre `json` |
| `rows` | Cantidad de filas/usuarios en el archivo |

**Uso obligatorio del LLM/cliente:** llamar la tool → descargar `download_url` → analizar el `.json`. Si el enlace expiró, volver a llamar la tool.

Detalle de estructura: [references/tools-reference.md](references/tools-reference.md).

## Tools (resumen)

| Tool | Uso | Respuesta clave |
|------|-----|-----------------|
| `get_business` | Tenant de la sesión | `id`, `name`, `cif`, `sub_domain`, `active` |
| `list_courses` | Descubrir cursos e ids | `courses[]` con `id`, `students_count`, `average_progress` |
| `list_groups` | Descubrir grupos (categorías no de sistema) | `groups[]` con `id`, `name`, `students_count` |
| `search_students` | Listar / buscar FrontUsers | filtros `query`, `active`, `course_id`, `progress_status`, `group_id`, `is_test`, `front_user_type`, `last_activity_from/to`, `custom_field`; `include_summary`; sin PII por defecto |
| `get_student` | Perfil consolidado de una persona | `profile`, `groups`, `sessions_summary`, `progress_summary`; `custom_fields`/contacto con PII |
| `get_student_progress` | Avance de una persona | `courses[]` con % y fechas |
| `get_student_activity` | Timeline transversal de una persona | `events[]` (sesiones, vistas, actividades, conversaciones), metadatos sin texto |
| `get_progress` | Métricas globales o por curso | `unit`, `total_enrollments`, `metrics` |
| `get_course_progress_summary` | Resumen rico de un curso | buckets, `stale_in_progress` |
| `get_course_detail` | Estructura curso propio | `sections`, `metrics` |
| `get_reports_summary` | Dashboard (+ `engagement` opcional) | usuarios, matrículas, `progress_by_course`, `definitions`, `engagement` |
| `export_course_progress` | Archivo `.json` completo de un curso (descargar; enlace 60 min) | `download_url`, `expires_at`, `rows` |
| `export_business_progress` | Archivo `.json` de matrículas (descargar; enlace 60 min) | `download_url`, `expires_at`, `rows` |

### Tools analíticas expandidas (envelope analítico)

| Tool | Uso | Respuesta clave (`result`) |
|------|-----|-----------------|
| `get_student_activity_progress` | Detalle por actividad de un estudiante | `activities[]` con estado, intentos, score, puntos, fechas |
| `get_conversational_assessment` | Resultado de quiz asistido o role play | `criteria`/`scenario`, `score_percentage`; feedback/reporte con `interactions.read` |
| `search_lena_conversations` | Buscar conversaciones LENA (sin transcripción) | `conversations[]` con turnos, sentimiento, outcome |
| `get_lena_conversation` | Detalle de una conversación LENA | insights; `messages[]` solo con `content_mode=full` + `interactions.read` |
| `get_lena_metrics` | Métricas agregadas de LENA | usuarios únicos, conversaciones, turnos, `by_surface`/`by_channel`/`by_sentiment`/`by_outcome` |
| `list_surveys` | Encuestas del business + participación | `surveys[]` con `assigned`, `started`, `completed` |
| `get_survey_summary` | Definición y participación de una encuesta | `questions[]`, `response_rate` (sin respuestas abiertas individuales) |
| `list_challenges` | Desafíos y participación | `challenges[]` con estados y conteos |
| `get_challenge_summary` | Detalle de un desafío por participante | `participantes[]` (PII opcional), `states`, `reward` |
| `list_campaigns` | Campañas con misiones/equipos | `campaigns[]` con conteos |
| `get_campaign_summary` | Resumen de campaña | `teams[]`, `missions[]`, puntos y posiciones |
| `get_campaign_ranking` | Ranking de equipos (e individual) | `teams[]`; `individual[]` con `include_individual: true` |
| `get_student_gamification` | Puntos, nivel y medallas | `total_points`, `level`, `medals[]` |
| `list_news` | Noticias/artículos + engagement | `news[]` con `views`, `unique_viewers`, `favorites` |
| `get_news_engagement` | Engagement por usuario de una noticia | `views[]` (PII opcional) |
| `get_communications_summary` | Resumen de notificaciones/comunicaciones | totales de envío/entrega/apertura, `by_type` |
| `search_communications` | Metadata de comunicaciones (sin contenido) | `communications[]` con estados de envío |
| `get_engagement_summary` | KPIs de sesiones | activos, sesiones, DAU/WAU/MAU, stickiness, duración |

Detalle: [references/tools-reference.md](references/tools-reference.md).  
Ejemplos: [references/examples.md](references/examples.md).

## vs MCP Internal (ops)

- Business es **single-tenant**; Internal ve toda la plataforma.
- `get_course_detail` existe en ambos, pero Business rechaza cursos de otro business (`Course not found`).
- Export Business: `export_course_progress` / `export_business_progress` → `.json` en S3 + `download_url` (60 min). `export_course_progress` puede incluir chats LENA (`include_lena_conversations`); el texto de los mensajes y las respuestas crudas de evaluaciones requieren `mcp.clients.interactions.read`. Internal: `get_course_full_export` → mismo patrón S3 e incluye chats LENA sin scope extra (es ops).
- Sin `json_config` administrativo.
