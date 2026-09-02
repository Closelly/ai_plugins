# MCP Business — referencia de tools

JSON en `content[0].text`. Tenant fijado por la sesión OAuth.

## get_business

- **Scope:** `mcp.clients.students.read`
- **Input:** (ninguno)
- **Success:**

```json
{
  "id": 106,
  "name": "Demo",
  "cif": "76.XXX.XXX-X",
  "formal_name_business": "...",
  "sub_domain": "demo",
  "active": true,
  "created_at": "2024-01-01T00:00:00.000Z"
}
```

- **Errors:** `insufficient_scope`, `forbidden_tenant`, `mcp_disabled`

## list_courses

- **Scope:** `mcp.clients.progress.read`
- **Input:** (ninguno)
- **Success:**

```json
{
  "business_id": 106,
  "total": 5,
  "courses": [
    {
      "id": 123,
      "name": "Nombre del curso",
      "active": true,
      "students_count": 40,
      "completed_count": 12,
      "average_progress": 46.8,
      "metrics": { "total": 40, "not_started": 18, "in_progress": 10, "completed": 12, "completion_percentage": 30.0, "average_progress": 40.0 }
    }
  ]
}
```

## list_groups

- **Scope:** `mcp.clients.students.read`
- **Input:** `page`, `per_page`, opcional `student_id` (solo grupos de ese estudiante)
- **Qué es:** grupos = categorías **no de sistema** del business.
- **Success:**

```json
{
  "business_id": 106,
  "pagination": { "page": 1, "per_page": 50, "total": 8 },
  "groups": [{ "id": 12, "name": "Ventas", "description": "...", "students_count": 40 }]
}
```

## search_students

- **Scope:** `mcp.clients.students.read` (+ `mcp.clients.pii.read` para PII y valores de campos personalizados)
- **Input:** `page`, `per_page`, `query`, `email`, `rut`, `active`, `course_id`, `progress_status`, `min_progress`, `max_progress`, `group_id`, `is_test`, `front_user_type`, `last_activity_from`, `last_activity_to` (ISO8601), `custom_field` + `custom_field_value`, `include_summary`
- **Success sin PII:**

```json
{
  "business_id": 106,
  "pagination": { "page": 1, "per_page": 20, "total": 50 },
  "items": [{ "id": 1, "business_id": 106, "active": true }]
}
```

- **Success con PII:** mismos campos + `name`, `email`, `rut`
- **Con `include_summary: true`:** cada item agrega `front_user_type`, `is_test`, `last_connection`, `count_connections`, `usage_time_seconds`, `device`, `language`, `groups[]`; `custom_fields[]` solo con PII.
- `progress_status`: `completed` | `in_progress` | `not_started`
- `custom_field` acepta nombre o título del campo; filtra por igualdad exacta de `custom_field_value`.

## get_student

- **Scope:** `mcp.clients.students.read` (+ `mcp.clients.pii.read` para contacto y `custom_fields`)
- **Input (required):** `student_id`; opcional `include` (`profile`, `custom_fields`, `groups`, `sessions_summary`, `progress_summary`)
- **Success:**

```json
{
  "business_id": 106,
  "student_id": 42,
  "profile": {
    "id": 42, "business_id": 106, "active": true, "created_at": "...",
    "front_user_type": "front_user", "is_test": false, "language": "es",
    "timezone": "America/Santiago", "device": "android", "last_connection": "...",
    "first_connection_date": "...", "count_connections": 12, "usage_time": 3600.0
  },
  "groups": [{ "id": 12, "name": "Ventas", "description": "..." }],
  "sessions_summary": {
    "sessions_count": 12, "first_connection": "...", "last_connection": "...",
    "usage_time_seconds": 3600.0, "distinct_active_days": 7
  },
  "progress_summary": { "courses": [] }
}
```

- **Con PII:** `profile` agrega `name`, `lastname`, `email`, `rut`, `phone`; se incluye `custom_fields[]` (`name`, `title`, `value`).
- **Errors:** `{ "error": "Student not found" }`

## get_student_activity

- **Scope:** `mcp.clients.progress.read`
- **Input (required):** `student_id`; opcional `from_date`, `to_date` (ISO8601), `event_types`, `page`, `per_page`
- **Qué es:** timeline transversal (metadatos por evento, **sin** texto de conversaciones).
- **event_types:** `session`, `course_viewed`, `activity_initiated`, `activity_completed`, `conversation`
- **Success:**

```json
{
  "business_id": 106,
  "student_id": 42,
  "from_date": null,
  "to_date": null,
  "event_types": ["session"],
  "pagination": { "page": 1, "per_page": 50, "total": 3 },
  "events": [
    {
      "student_id": 42,
      "event_type": "session",
      "timestamp": "2026-08-11T12:00:00Z",
      "entity_type": null,
      "entity_id": 987,
      "metadata": { "duration_seconds": 300.0, "total_requests": 3 }
    }
  ]
}
```

- **Errors:** `{ "error": "Student not found" }`, `invalid_argument` (fecha inválida)

## get_student_progress

- **Scope:** `mcp.clients.progress.read` (+ PII opcional para bloque `student`)
- **Input (required):** `student_id`; opcional `course_id`
- **Success:**

```json
{
  "business_id": 106,
  "student_id": 1,
  "active": true,
  "courses": [
    {
      "course_id": 15,
      "course_name": "...",
      "status": "in_progress",
      "progress_percent": 42.0,
      "assignment_date": "...",
      "initiated_date": "...",
      "completed_date": null,
      "last_activity_at": "...",
      "completed_activities": 3,
      "pending_activities": 2,
      "initiated_activities": 1
    }
  ]
}
```

- **Errors:** `{ "error": "Student not found" }`

## get_progress

- **Scope:** `mcp.clients.progress.read`
- **Input:** opcional `course_id`
- **Success (business):**

```json
{
  "business_id": 106,
  "unit": "enrollments",
  "total_students": 129,
  "total_enrollments": 153,
  "students_with_enrollments": 94,
  "active_students_count": 69,
  "inactive_students_count": 60,
  "as_of": "2026-08-11T12:00:00Z",
  "definitions": {},
  "metrics": {
    "total": 153,
    "not_started": 83,
    "in_progress": 43,
    "completed": 27,
    "completion_percentage": 17.65,
    "average_progress": 31.7
  }
}
```

- **Success (curso):** `business_id`, `course_id`, `unit`, `as_of`, `metrics`
- **Errors:** `{ "error": "Course not found" }`

## get_course_progress_summary

- **Scope:** `mcp.clients.progress.read`
- **Input (required):** `course_id`
- **Success:** `enrolled`, `not_started`, `in_progress`, `completed`, `average_progress`, `completion_percentage`, `stale_in_progress`, `last_activity_at`, `progress_distribution` (rangos 0 / 1-25 / 26-50 / 51-75 / 76-99 / 100), `metrics`
- **Errors:** `Course not found`

## get_course_detail

- **Scope:** `mcp.clients.progress.read`
- **Input (required):** `course_id` (descubrir con `list_courses`)
- **Success:** `export_structure` del curso + `business_id` + `metrics`
- **Errors:** `Course not found`, scopes/tenant

## get_reports_summary

- **Scope:** `mcp.clients.reports.read`
- **Input:** (ninguno para el dashboard). Opcional para el bloque `engagement`: `from_date`, `to_date` (ISO8601), `group_by` (`student` | `company`), `company_field`, `exclude_test_users`, `page`, `per_page`.
- **Success (dashboard):** `courses_count`, `students_count`, `active_students_count`, `inactive_students_count`, `total_enrollments`, `students_with_enrollments`, `students_without_recent_activity`, `progress`, `progress_by_course`, `definitions`, `as_of`
- **Con parámetros de engagement:** se agrega `engagement` con señales crudas por estudiante o empresa dentro de la ventana (`sessions_count`, `distinct_active_days`, `courses_started`, `courses_completed`, `activity_completions`, `assessment_completions`, `role_play_completions`, `lena_users`, `conversations_count`, `active_users`). El backend **no** calcula un lead score; expone señales para que el LLM las combine.
- `group_by: "company"` agrupa por el campo personalizado `company_field` (o dominio de email como fallback) y devuelve `total_companies` + `groups[]`.

```json
{
  "engagement": {
    "group_by": "company",
    "company_field": "Empresa",
    "total_companies": 3,
    "groups": [
      { "company": "CCU", "registered_users": 7, "active_users": 2, "sessions_count": 15,
        "courses_started": 2, "courses_completed": 1, "lena_users": 2, "role_play_completions": 1 }
    ],
    "definitions": {}
  }
}
```

## export_course_progress

- **Scope:** `mcp.clients.export` (+ `mcp.clients.pii.read` si `include_pii: true`)
- **Qué es:** genera un **archivo `.json` descargable** con el avance **completo** del curso (todos los asignados, **sin filtros ni paginación**) para análisis posteriores. La tool **no** incrusta el dataset en el chat.
- **Input (required):** `course_id`
- **Input (opcional):**
  - `format` — solo `json` (archivo `.json`)
  - `include_activity_detail` — `true`|`false` (default `true`; incluye `user_activities`)
  - `include_lena_conversations` — `true`|`false` (default `false`; agrega `lena_conversations` por usuario: chat de curso y de actividades quiz/role play)
  - `include_assessment_answers` — `true`|`false` (default `false`; respuestas crudas; requiere `mcp.clients.interactions.read`)
  - `include_message_text` — `true`|`false` (default `false`; conserva el texto de los mensajes; requiere `mcp.clients.interactions.read`)
  - `exclude_test_users` — `true`|`false` (default `false`; omite usuarios `is_test`)
  - `include_pii` — `true`|`false` (default `false`; email/rut/phone; requiere scope PII)
- **Success (metadatos de descarga):**

```json
{
  "course_id": 1075,
  "business_id": 106,
  "file_name": "clientes-felices-progreso.json",
  "download_url": "https://s3-[REDACTED].amazonaws.com/[REDACTED]/...?X-Amz-...",
  "expires_at": "2026-08-11T22:00:00Z",
  "expires_in_seconds": 3600,
  "format": "json",
  "rows": 128,
  "include_activity_detail": true,
  "include_pii": false
}
```

- **TTL:** el `download_url` caduca a los **60 minutos**. Si expiró, volver a llamar la tool.
- **Uso:** descargar `download_url` y analizar el `.json` (no resumir inventando datos sin descargar).
- **Estructura del archivo `.json`:**

```json
{
  "course_id": 1075,
  "business_id": 106,
  "as_of": "2026-08-11T21:00:00Z",
  "include_activity_detail": true,
  "include_pii": false,
  "export": {
    "course": { "id": 1075, "name": "...", "sections": [{ "id": 1, "activities": [] }] },
    "users": [
      {
        "id": 1,
        "name": "...",
        "lastname": "...",
        "course_status": "completed",
        "progress_percent": 100.0,
        "completed_activities": 10,
        "total_activities": 10,
        "user_activities": [
          { "activity_id": 10, "activity_title": "...", "status": "completed", "grade": 90.0 }
        ]
      }
    ]
  }
}
```

- **Sin `include_pii`:** se conservan id/name/lastname/estado/avance; se omiten `email`, `rut`, `document_number`, `phone`
- **Errors:** `Course not found`, `insufficient_scope` (si `include_pii` sin scope), `export_upload_failed`, `invalid_argument`

## export_business_progress

- **Scope:** `mcp.clients.export` (+ `mcp.clients.pii.read` si `include_pii: true`)
- **Qué es:** genera un **archivo `.json` descargable** con el avance **completo** de matrículas del tenant (**todas** las filas, sin paginación; opcional `course_id`) para análisis posteriores. No incrusta el dataset en el chat.
- **Input:** opcional `course_id`, `format` (`json`), `exclude_test_users` (default `false`), `include_pii` (default `false`)
- **Success (metadatos):** `file_name`, `download_url`, `expires_at`, `expires_in_seconds` (**3600 = 60 min**), `format`, `rows`, `business_id`, `course_id`, `include_pii`
- **TTL:** el `download_url` caduca a los **60 minutos**.
- **Estructura del archivo `.json`:**

```json
{
  "business_id": 106,
  "as_of": "2026-08-11T21:00:00Z",
  "unit": "enrollments",
  "total": 500,
  "include_pii": false,
  "rows": [
    {
      "student_id": 1,
      "course_id": 15,
      "course_name": "...",
      "status": "initiated",
      "progress_percent": 40.0,
      "assignment_date": "...",
      "initiated_date": "...",
      "completed_date": null,
      "last_activity_at": "...",
      "active": true,
      "name": "..."
    }
  ]
}
```

- **Sin `include_pii`:** sin `email` / `rut` / `phone` en cada row (se puede conservar `name`)
- **Errors:** `Course not found`, `insufficient_scope`, `export_upload_failed`, `invalid_argument`

---

# Tools analíticas expandidas

Estas tools envuelven la respuesta en el **envelope analítico** (los datos van en `result`):

```json
{
  "schema_version": 1,
  "business_id": 106,
  "as_of": "2026-08-13T18:00:00Z",
  "from_date": null,
  "to_date": null,
  "grain": "...",
  "unit": "...",
  "definitions": {},
  "data_quality": { "status": "ready", "freshness_at": "2026-08-13T18:00:00Z", "warnings": [] },
  "result": { }
}
```

`data_quality.status` = `partial` cuando hay `warnings`. Los ejemplos siguientes muestran solo el contenido de `result`.

## get_student_activity_progress

- **Scope:** `mcp.clients.activities.read`
- **Input (required):** `student_id`; opcional `course_id`, `from_date`, `to_date` (ISO8601), `page`, `per_page`
- **grain/unit:** `activity_attempt` / `activity_records`
- **`result`:**

```json
{
  "pagination": { "page": 1, "per_page": 50, "total": 12 },
  "activities": [
    {
      "front_users_activity_id": 987,
      "student_id": 42,
      "course_id": 15,
      "section_id": 3,
      "activity_id": 210,
      "activity_title": "...",
      "activity_type": "ContentAssistantQuiz",
      "status": "completed",
      "result_activity": "approved",
      "initiated_at": "...",
      "completed_at": "...",
      "last_interaction_at": "...",
      "attempts": 2,
      "duration_seconds": 300,
      "score_percentage": 90.0,
      "points_possible": 100,
      "points_earned": 90
    }
  ]
}
```

- **Errors:** `{ "error": "Student not found" }`, `insufficient_scope`, `invalid_argument`

## get_conversational_assessment

- **Scope:** `mcp.clients.assessments.read` (+ `mcp.clients.interactions.read` para `question`, `feedback`, `evaluation` completa y `final_report`)
- **Input (required):** `student_id`, `activity_id`
- **Qué es:** resultado de un quiz asistido (`ContentAssistantQuiz`) o role play (`ContentRolePlay`).
- **grain/unit:** `activity_attempt` / `assessment_attempt`
- **`result` (assistant_quiz):** `assessment_type: "assistant_quiz"`, `status`, `score_percentage`, `points_earned`, `approved_with`, `criteria[]` (`question_id`, `question_index`, `score`; `question`/`feedback` solo con `interactions.read`).
- **`result` (role_play):** `assessment_type: "role_play"`, `scenario` (`general_objective`, `user_role`, `lena_role`, `difficulty`, `evaluation_criteria`), `evaluation` (`score` + `breakdown`; detalle completo solo con `interactions.read`).
- **Con `interactions.read`:** además `final_report`.
- **Errors:** `Student not found`, `Activity not found`, `Activity is not a conversational assessment`, `Assessment attempt not found`

## search_lena_conversations

- **Scope:** `mcp.clients.lena.conversations.read`
- **Input:** opcional `student_id`, `course_id`, `activity_id`, `surface`, `channel`, `from_date`, `to_date`, `page`, `per_page`
- **Qué es:** busca conversaciones LENA por filtros. **No** devuelve transcripción.
- **surface:** `dashboard`, `assistant_quiz`, `role_play`, `learning_activity`, `course`, … · **channel:** `app_web` | `whatsapp`
- **grain/unit:** `conversation` / `conversations`
- **`result`:**

```json
{
  "pagination": { "page": 1, "per_page": 50, "total": 3 },
  "conversations": [
    {
      "conversation_id": 555,
      "student_id": 42,
      "surface": "role_play",
      "channel": "app_web",
      "module_type": "Activity",
      "module_id": 210,
      "started_at": "...",
      "ended_at": "...",
      "message_count": 14,
      "student_turns": 7,
      "lena_turns": 7,
      "summary": "...",
      "conversation_type": "...",
      "conversation_depth": "...",
      "sentiment": "positive",
      "outcome": "...",
      "has_audio": false,
      "has_files": false
    }
  ]
}
```

## get_lena_conversation

- **Scope:** `mcp.clients.lena.conversations.read` (+ `mcp.clients.interactions.read` para `content_mode=full`)
- **Input (required):** `conversation_id`; opcional `content_mode` (`none` | `summary` | `full`, default `summary`)
- **grain/unit:** `conversation` / `conversation`
- **`result`:** insights de la conversación (`summary`, `conversation_type`, `conversation_depth`, `sentiment`, `outcome`). Con `content_mode=full` agrega `messages[]` (`role`, `timestamp`, `text`, `intent`, `sentiment`, `score`, …).
- **Errors:** `Conversation not found`; `insufficient_scope` si `content_mode=full` sin `mcp.clients.interactions.read`

## get_lena_metrics

- **Scope:** `mcp.clients.lena.metrics.read`
- **Input:** opcional `from_date`, `to_date`, `course_id`
- **grain/unit:** `conversation` / `conversations`
- **`result`:** `unique_students`, `conversations`, `student_turns`, `lena_turns`, `with_score`, `by_surface`, `by_channel`, `by_sentiment`, `by_outcome`

## list_surveys

- **Scope:** `mcp.clients.surveys.read`
- **Input:** opcional `page`, `per_page`
- **grain/unit:** `survey` / `surveys`
- **`result`:** `pagination`, `surveys[]` (`survey_id`, `course_id`, `title`, `questions_count`, `assigned`, `started`, `completed`, `created_at`)

## get_survey_summary

- **Scope:** `mcp.clients.surveys.read`
- **Input (required):** `survey_id`
- **Qué es:** definición y resumen de participación. **No** expone respuestas abiertas individuales.
- **grain/unit:** `survey` / `survey`
- **`result`:** `survey_id`, `course_id`, `title`, `assigned`, `started`, `completed`, `response_rate`, `questions[]` (`question_id`, `index`, `question`, `question_type`, `options`, `topics`)
- **Errors:** `Survey not found`

## list_challenges

- **Scope:** `mcp.clients.challenges.read`
- **Input:** opcional `status`, `page`, `per_page`
- **grain/unit:** `challenge` / `challenges`
- **`result`:** `pagination`, `challenges[]` (`challenge_id`, `name`, `description`, `status`, `published_at`, `closed_at`, `duration_days`, `assigned`, `participating`, `completed`)

## get_challenge_summary

- **Scope:** `mcp.clients.challenges.read` (+ `mcp.clients.pii.read` para nombre/email/rut de participantes)
- **Input (required):** `challenge_id`; opcional `page`, `per_page`
- **Qué es:** detalle por participante **sin** el contenido de las evidencias.
- **grain/unit:** `challenge_submission` / `participants`
- **`result`:** `challenge_id`, `name`, `status`, `reward`, `states` (conteo por estado), `pagination`, `participants[]` (identidad + `status`, fechas de flujo, `evaluation_comment`, `total_attempts`, `points_earned`, `is_winner`, recompensa)
- **Errors:** `Challenge not found`

## list_campaigns

- **Scope:** `mcp.clients.campaigns.read`
- **Input:** opcional `status`, `page`, `per_page`
- **grain/unit:** `campaign` / `campaigns`
- **`result`:** `pagination`, `campaigns[]` (`campaign_id`, `name`, `status`, `active`, `missions_count`, `teams_count`, `participants_count`, `end_date`)

## get_campaign_summary

- **Scope:** `mcp.clients.campaigns.read`
- **Input (required):** `campaign_id`
- **grain/unit:** `campaign` / `campaign`
- **`result`:** `campaign_id`, `name`, `status`, `participants_count`, `teams[]` (posición, puntos, miembros), `missions[]` (`status`, fechas)
- **Errors:** `Campaign not found`

## get_campaign_ranking

- **Scope:** `mcp.clients.campaigns.read`
- **Input (required):** `campaign_id`; opcional `include_individual` (`true`|`false`, default `false`)
- **grain/unit:** `ranking_position` / `positions`
- **`result`:** `campaign_id`, `teams[]` (`position`, `last_position`, `points_total`, `points_average`); con `include_individual: true` agrega `individual[]` (`student_id`, `position`, `points`)
- **Errors:** `Campaign not found`

## get_student_gamification

- **Scope:** `mcp.clients.gamification.read`
- **Input (required):** `student_id`
- **grain/unit:** `student` / `student_gamification`
- **`result`:** `balance_points`, `extra_points`, `total_points`, `level` (crown), `medals_count`, `medals[]` (`name`, `medal_type`, `classification`, `assignment_date`, `assignment_route`)
- **Errors:** `Student not found`

## list_news

- **Scope:** `mcp.clients.news.read`
- **Input:** opcional `page`, `per_page`
- **grain/unit:** `article` / `articles`
- **`result`:** `pagination`, `news[]` (`article_id`, `title`, `status`, `published_at`, `views`, `unique_viewers`, `favorites`)

## get_news_engagement

- **Scope:** `mcp.clients.news.read` (+ `mcp.clients.pii.read` para identidad de lectores)
- **Input (required):** `article_id`; opcional `page`, `per_page`
- **grain/unit:** `article_view` / `views`
- **`result`:** `article_id`, `pagination`, `views[]` (identidad + `viewed`, `favorite`, `opened_at`)
- **Errors:** `News not found`

## get_communications_summary

- **Scope:** `mcp.clients.communications.read`
- **Input:** opcional `from_date`, `to_date`, `type_notification`
- **grain/unit:** `communication` / `communications`
- **`result`:** `total`, `sent`, `provider_delivered`, `opened`, `unread`, `failed`, `unique_students_reached`, `by_type`
- **Nota:** `data_quality.status = partial` — la semántica de entrega/apertura refleja el tracking de Notification/OneSignal y no está normalizada por canal.

## search_communications

- **Scope:** `mcp.clients.communications.read`
- **Input:** opcional `student_id`, `from_date`, `to_date`, `type_notification`, `page`, `per_page`
- **Qué es:** metadata de comunicaciones. **No** incluye el contenido del mensaje.
- **grain/unit:** `communication` / `communications`
- **`result`:** `pagination`, `communications[]` (`communication_id`, `student_id`, `type`, `channel`, `model_id`, fechas, `sent`, `provider_delivered`, `read`, `opened`, `request_code`)

## get_engagement_summary

- **Scope:** `mcp.clients.analytics.read`
- **Input:** opcional `from_date`, `to_date` (default: últimos 30 días), `exclude_test_users` (default `true`)
- **Qué es:** KPIs derivados de sesiones existentes (`FrontUsersConnection`).
- **grain/unit:** `student` / `unique_students`
- **`result`:** `eligible_users`, `active_users`, `sessions`, `distinct_active_days`, `total_duration_seconds`, `average_session_duration_seconds`, `dau`, `wau`, `mau`, `sessions_per_active_user`, `dau_mau_stickiness`, `wau_mau_stickiness`
- **`definitions`:** describe DAU/WAU/MAU. **`data_quality.status = partial`** — las sesiones no persisten canal/dispositivo/OS histórico, por eso esas distribuciones se omiten.
