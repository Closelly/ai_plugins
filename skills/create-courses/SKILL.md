---
name: create-courses
description: Autoría de cursos vía MCP Business (crear, editar, publicar y despublicar con OTP). Usar con /closelly o /LENA cuando el usuario pida crear o gestionar cursos.
license: MIT
metadata:
  plugin_name: closelly-ai-plugins
  plugin_version: "1.11.0"
  plugin_display_name: Closelly MCP App
  mcp_server: closelly-business
  mcp_url: https://auth.closelly.com/mcp/business
  invoke: "/closelly or /LENA"
---

# Crear y gestionar cursos (MCP Business)

Skill de autoría para Closelly MCP App. Requiere connector `/mcp/business` y permisos de escritura habilitados en la empresa y el User.

## Importante

- Descubre capacidades reales con `get_course_authoring_capabilities` antes de invocar tools de escritura.
- No inventes nombres de tools: usa solo las que el servidor lista y autoriza.
- Tenant y User vienen del OAuth; nunca pidas ni aceptes otro `business_id` o destinatario OTP.
- Crear/editar **no publica**. Publicar es explícito.
- Despublicar exige OTP humano por correo; no leas el código desde Gmail ni lo inventes.
- No elimines cursos ni matricules usuarios en esta fase.
- El prompt canónico del diseñador instruccional está **pendiente de entrega por Luis**. Hasta entonces, guía al usuario con preguntas claras de objetivos, audiencia, módulos y tipos de actividad, y guarda borradores solo con autorización explícita.

## Flujo operativo

1. `get_course_authoring_capabilities` → revisar `write_enabled` y `actions`.
2. Si no hay escritura/permisos: explicar el bloqueo y conservar solo consultas (`list_courses`, `get_course_detail`).
3. Diseñar propuesta con el usuario (objetivos, audiencia, módulos, actividades).
4. `create_course` (idempotency_key) → secciones → actividades borrador.
5. Revisar con `get_course_detail` / `validate_course_for_publication`.
6. Publicar con `publish_course_activity` / `publish_course` solo si el usuario lo pide y tiene permiso.
7. Despublicar: `request_course_unpublish_code` → el humano entrega el OTP → `unpublish_course`.

## Tools de autoría

Ver `references/authoring-contract.md` y el playbook `skills/mcp-business/`.

Scopes de escritura (no base): `mcp.clients.courses.create|update|activities.write|publish|unpublish`.
