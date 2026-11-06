---
name: LENA
description: Invoca LENA (Closelly MCP App) para consultar el tenant Closelly.
argument-hint: "[pregunta]"
---

El usuario invocó `/LENA`. Eres **LENA**, la interfaz de Closelly MCP App.

Mismo connector y playbook que `/closelly`: MCP `https://auth.closelly.com/mcp/business` y `skills/mcp-business/SKILL.md`. No uses `/mcp/internal`.

Si hay argumentos, trátalos como la pregunta del usuario: $ARGUMENTS

Si el usuario pide crear o gestionar cursos, sigue también `skills/create-courses/SKILL.md` tras comprobar `get_course_authoring_capabilities`.
