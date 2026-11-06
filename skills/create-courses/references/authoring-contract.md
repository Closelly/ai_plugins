# Contrato de autoría MCP Business

## Prerrequisitos

- `business.mcp_enabled` y `business.mcp_write_enabled`
- Permisos personales en `businesses_users.mcp_permissions` (grupo cursos)
- Scopes OAuth de escritura correspondientes

## Tools

| Tool | Permiso |
|------|---------|
| `get_course_authoring_capabilities` | contexto de sesión |
| `create_course` | courses.create |
| `update_course` | courses.update |
| `create_course_section` / `update_course_section` | courses.update |
| `create_course_activity` / `update_course_activity` / `add_activity_to_course` / `reorder_course_content` | update + activities.manage |
| `validate_course_for_publication` | contexto autoría |
| `publish_course` / `publish_course_activity` | courses.publish |
| `request_course_unpublish_code` / `unpublish_course` | courses.unpublish |

## OTP despublicación

- Destinatario: email del User OAuth (enmascarado en respuesta)
- Nunca devolver el código en la tool
- TTL 15 minutos; intentos y reenvíos limitados
- Sin `confirmed: true` ni bypass

## Errores

`mcp_write_disabled`, `permission_denied`, `insufficient_scope`, `validation_error`, `conflict`, `otp_invalid`, `otp_delivery_failed`
