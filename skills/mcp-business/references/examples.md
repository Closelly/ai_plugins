# MCP Business — ejemplos pregunta → tool

| Pregunta | Tool | Argumentos | Notas |
|----------|------|------------|-------|
| ¿Cuántos estudiantes tengo? | `get_reports_summary` | `{}` | `students_count` vs `total_enrollments` |
| ¿Cuántos cursos tengo? | `list_courses` / `get_reports_summary` | `{}` | ids en `list_courses` |
| Datos de mi empresa | `get_business` | `{}` | `id`, `name`, `cif` |
| ¿Qué cursos tengo? | `list_courses` | `{}` | descubrir `course_id` |
| Listar mis estudiantes | `search_students` | `{ "page": 1 }` | sin email/rut salvo PII |
| Busca a Patricia | `search_students` | `{ "query": "Patricia" }` | requiere PII para ver nombre/email |
| Usuarios inactivos | `search_students` | `{ "active": false }` | |
| No han comenzado el curso 15 | `search_students` | `{ "course_id": 15, "progress_status": "not_started" }` | |
| Menos de 20 % de avance | `search_students` | `{ "max_progress": 20 }` | |
| Estudiantes del grupo 12 con resumen | `search_students` | `{ "group_id": 12, "include_summary": true }` | agrega perfil, grupos y sesiones |
| Sin usuarios de prueba activos esta semana | `search_students` | `{ "is_test": false, "last_activity_from": "2026-08-05" }` | |
| Usuarios de la empresa CCU | `search_students` | `{ "custom_field": "Empresa", "custom_field_value": "CCU" }` | |
| Mis grupos | `list_groups` | `{}` | categorías no de sistema + conteo |
| Perfil completo de María (id 42) | `get_student` | `{ "student_id": 42 }` | grupos + sesiones; PII con scope |
| ¿Cómo va María (id 42)? | `get_student_progress` | `{ "student_id": 42 }` | |
| Qué hizo María en la app | `get_student_activity` | `{ "student_id": 42, "event_types": ["session", "conversation"] }` | timeline, metadatos sin texto |
| % de completitud general | `get_progress` | `{}` | `unit=enrollments` |
| Resumen del curso 15 | `get_course_progress_summary` | `{ "course_id": 15 }` | buckets + estancados |
| Detalle del curso 15 | `get_course_detail` | `{ "course_id": 15 }` | tras `list_courses` |
| Engagement por empresa esta semana | `get_reports_summary` | `{ "group_by": "company", "company_field": "Empresa", "from_date": "2026-08-05" }` | bloque `engagement` con señales |
| Señales de intención por estudiante | `get_reports_summary` | `{ "group_by": "student", "exclude_test_users": true }` | el LLM arma el score |
| Exportar avance del curso 15 | `export_course_progress` | `{ "course_id": 15 }` | descargar `.json` vía `download_url` (caduca 60 min); dataset completo sin filtros |
| Export sin detalle de actividades | `export_course_progress` | `{ "course_id": 15, "include_activity_detail": false }` | JSON más liviano |
| Export con conversaciones LENA | `export_course_progress` | `{ "course_id": 15, "include_lena_conversations": true, "include_message_text": true }` | texto requiere `mcp.clients.interactions.read` |
| Export con email/RUT | `export_course_progress` | `{ "course_id": 15, "include_pii": true }` | requiere scope PII |
| Exportar todo el avance | `export_business_progress` | `{}` | descargar `.json` con todas las matrículas; enlace 60 min |
| Export sin usuarios de prueba | `export_business_progress` | `{ "exclude_test_users": true }` | omite `is_test` |

## Analytics expandidas (envelope analítico)

| Pregunta | Tool | Argumentos | Notas |
|----------|------|------------|-------|
| Detalle de actividades de María (id 42) | `get_student_activity_progress` | `{ "student_id": 42 }` | intentos, score y puntos por actividad |
| ¿Cómo le fue en el role play de la actividad 210? | `get_conversational_assessment` | `{ "student_id": 42, "activity_id": 210 }` | feedback/reporte requieren `interactions.read` |
| Conversaciones LENA por WhatsApp | `search_lena_conversations` | `{ "channel": "whatsapp" }` | metadata, sin transcripción |
| Ver la conversación 555 completa | `get_lena_conversation` | `{ "conversation_id": 555, "content_mode": "full" }` | `full` requiere `interactions.read` |
| Métricas de LENA este mes | `get_lena_metrics` | `{ "from_date": "2026-08-01" }` | usuarios, turnos, sentimiento, outcome |
| ¿Qué encuestas tengo? | `list_surveys` | `{}` | participación por encuesta |
| Resultados de la encuesta 30 | `get_survey_summary` | `{ "survey_id": 30 }` | preguntas + `response_rate` (sin respuestas abiertas) |
| Mis desafíos activos | `list_challenges` | `{ "status": "active" }` | conteos de participación |
| Detalle del desafío 8 | `get_challenge_summary` | `{ "challenge_id": 8 }` | participantes; PII con scope |
| ¿Qué campañas tengo? | `list_campaigns` | `{}` | misiones, equipos, participantes |
| Resumen de la campaña 4 | `get_campaign_summary` | `{ "campaign_id": 4 }` | equipos y misiones |
| Ranking de la campaña 4 con individuales | `get_campaign_ranking` | `{ "campaign_id": 4, "include_individual": true }` | equipos + `individual[]` |
| Puntos y medallas de María | `get_student_gamification` | `{ "student_id": 42 }` | `total_points`, `level`, `medals[]` |
| ¿Qué noticias tengo? | `list_news` | `{}` | vistas, lectores únicos, favoritos |
| Engagement de la noticia 12 | `get_news_engagement` | `{ "article_id": 12 }` | por usuario; PII con scope |
| Resumen de notificaciones enviadas | `get_communications_summary` | `{ "from_date": "2026-08-01" }` | envío/entrega/apertura; `data_quality: partial` |
| Notificaciones de María | `search_communications` | `{ "student_id": 42 }` | metadata, sin contenido |
| KPIs de uso (DAU/WAU/MAU) | `get_engagement_summary` | `{ "from_date": "2026-07-14" }` | stickiness y duración; `data_quality: partial` |

## Encadenamientos útiles

1. `list_courses` / `list_groups` → `get_course_progress_summary` / `get_course_detail` / `export_course_progress`.
2. `search_students` (con `include_summary`) → `get_student` / `get_student_progress` / `get_student_activity` con el `id` encontrado.
3. `get_reports_summary` para panorama; con `group_by`/fechas para el bloque `engagement`; si hace falta detalle por persona o curso, tools de análisis.
4. `get_engagement_summary` / `get_lena_metrics` para panorama analítico → `search_lena_conversations` → `get_lena_conversation` (`content_mode=full` con `interactions.read`) para bajar al detalle.
5. `list_surveys` / `list_challenges` / `list_campaigns` / `list_news` → tool `get_*_summary` o `get_*_engagement` con el `id` encontrado.
6. Curso o estudiante de otro business → `Course not found` / `Student not found` (correcto; no insistir con IDs externos).
