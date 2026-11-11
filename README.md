# Closelly MCP App

Fuente única, versionada y portable de **Closelly MCP App** para **ChatGPT/Codex**, **Claude Code** y **GitHub Copilot CLI**.

| Campo | Valor |
| --- | --- |
| Nombre visible | Closelly MCP App |
| Identificador | `closelly-ai-plugins` |
| Versión | `1.12.0` |
| Comandos | `/closelly`, `/LENA` |
| Skills | `skills/mcp-business` (consulta), `skills/create-courses` (autoría MCP), `skills/instructional-design` (diseño pedagógico), `skills/closelly-interactive` (ZIP HTML), `skills/create-activities` (recursos y formatos) |
| Config | `plugin.json`, `mcp.json` (ChatGPT/Codex), `.mcp.json` (Claude Code), `config/*.json` |
| MCP Business | `https://auth.closelly.com/mcp/business` (OAuth) |

Este paquete contiene instrucciones Markdown, configuración JSON/YAML y ejemplos estáticos HTML/CSS/JavaScript con audio para crear interactivos.

## Instalar desde GitHub

```bash
# ChatGPT / Codex
codex plugin marketplace add Closelly/ai_plugins

# Claude Code
claude plugin marketplace add Closelly/ai_plugins
claude plugin install closelly-ai-plugins@closelly-ai-plugins

# GitHub Copilot CLI
copilot plugin install Closelly/ai_plugins
```

Tras instalar, usa **`/closelly`** o **`/LENA`**.

Guías: [ChatGPT/Codex](docs/chatgpt-codex.md), [Claude Code](docs/claude-code.md), [Copilot CLI](docs/github-copilot-cli.md).

## MCP Business

Closelly MCP App da contexto sobre el MCP de clientes:

- URL: `https://auth.closelly.com/mcp/business`
- Auth: OAuth de User (email + password)
- Comandos: `/closelly`, `/LENA` (`commands/`)
- Config portable: `config/mcp.business.json`
- Claude Code: `.mcp.json` en la raíz (OAuth al primer uso de tools)
- ChatGPT UI: `skills/mcp-business/agents/openai.yaml` (nombre Closelly MCP App)
- ChatGPT/Codex MCP: `mcpServers` → `mcp.json` portable (`streamable-http` + OAuth DCR)
- ChatGPT App (`.app.json` / `connector_…`): opcional, no requerido para el bundle
- Playbook: `skills/mcp-business/SKILL.md`
- Autoría de cursos: `skills/create-courses/SKILL.md` (ver sección siguiente)
- Diseño instruccional: `skills/instructional-design/SKILL.md`

Claude.ai / Cowork: Settings → custom connector con la misma URL (siempre manual).

## Crear cursos (`create-courses`)

Skill portable para crear, editar, validar, publicar y despublicar cursos vía MCP Business. Invoca con `/closelly` o `/LENA` (p. ej. "crea un curso ...").

- Descubre primero `get_course_authoring_capabilities` y `get_course_authoring_schema`; no inventa tools ni campos.
- **Scopes opcionales** (no están en los base; requieren consentimiento explícito al conectar): `mcp.clients.courses.create`, `mcp.clients.courses.update`, `mcp.clients.courses.activities.write`, `mcp.clients.courses.publish`, `mcp.clients.courses.unpublish`. La conexión OAuth y los scopes base de lectura no cambian.
- Despublicar exige un código OTP que **entrega una persona**; el skill nunca lo busca en Gmail/Docs ni en otra fuente.
- No elimina cursos ni matricula usuarios.
- Para brief, curriculum y entregables pedagógicos usa `skills/instructional-design/` y solo después de confirmación persiste con este skill.

## Diseño instruccional (`instructional-design`)

Diseñador instruccional amable de Closelly: entrevista, plan de micro-curso (45–60 min), secciones y actividades mapeadas a `content_type` reales del schema.

- Entregables pedagógicos (storyboard, slides, banco de preguntas, guion LENA) en el chat; payload MCP solo con campos del schema.
- Dos confirmaciones humanas (brief y plan) antes de escribir.
- Handoff a `create-courses` para `create_course` / secciones / actividades / validar / publicar.

## Interactivos (`closelly-interactive`)

Crea un ZIP HTML para **Interactivo Closelly**, con una única orientación fija: horizontal 1600×900 o vertical 900×1600. Incluye el mismo código y audio de los dos ejemplos del backend, copiados del commit del PR #1034 y disponibles en `skills/closelly-interactive/assets/examples/`. [Procedencia y uso](skills/closelly-interactive/references/examples.md).

## Crear actividades y recursos (`create-activities`)

Guía para producir archivos y preparar actividades, con [formatos por tipo](skills/create-activities/references/activity-formats.md): tarjetas PNG/SVG, video, MP3, documentos, preguntas, evidencias e interactivos. Distingue requisitos del producto de recomendaciones de diseño.

Los videos educativos se producen con **Remotion**, usando paleta/diseño del usuario, voz en off generada por el mismo agente con la capacidad de audio disponible y subtítulos sincronizados. Incluye una selección investigada de plantillas y estilos oficiales con métricas de adopción fechadas. La persistencia MCP continúa en `create-courses`.

## Release

El versionado vive en `plugin.json`. Al mergear a `main`, el workflow crea el GitHub Release (ZIP) **si esa versión aún no existe**. No hace falta crear un tag a mano. Detalle: [docs/release.md](docs/release.md).

**Cada PR debe subir la versión** en `plugin.json` (y manifests alineados). El check `pr-version` lo valida.

## Arquitectura y mantenimiento

- [Arquitectura](docs/architecture.md)
- [Release](docs/release.md)
- [MCP Business](docs/mcp-remote.md)
- [Solución de problemas](docs/troubleshooting.md)
- [Seguridad](SECURITY.md)
- [Changelog](CHANGELOG.md)
