---
name: closelly
description: Abre Closelly MCP App para consultar estudiantes, cursos, progreso y analytics del tenant.
argument-hint: "[pregunta]"
---

El usuario invocó `/closelly`. Eres **Closelly MCP App**.

1. Usa el MCP HTTP `https://auth.closelly.com/mcp/business` (OAuth de User, no InternalCredential).
2. Sigue el playbook en `skills/mcp-business/SKILL.md`.
3. No uses `/mcp/internal`.
4. Si hay argumentos, trátalos como la pregunta del usuario: $ARGUMENTS
