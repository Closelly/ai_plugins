---
name: create-courses
description: Playbook de Closelly MCP App para crear, editar, validar y publicar cursos con el connector /mcp/business. Descubre capacidades y schemas reales antes de escribir. Requiere scopes de autoría opcionales (consentimiento explícito). Invoca con /closelly o /LENA.
license: MIT
metadata:
  plugin_name: closelly-ai-plugins
  plugin_version: "1.11.0"
  plugin_display_name: Closelly MCP App
  mcp_server: closelly-business
  mcp_url: https://auth.closelly.com/mcp/business
  invoke: "/closelly or /LENA"
  extends: mcp-business
---

# Closelly MCP App — Crear cursos

Playbook de **autoría de cursos** sobre el mismo connector de `mcp-business` (`closelly-business`, `https://auth.closelly.com/mcp/business`). Comandos: **`/closelly`** o **`/LENA`**. Solo opera sobre el business de la sesión OAuth. No uses `/mcp/internal`.

Este skill **extiende** [`../mcp-business/SKILL.md`](../mcp-business/SKILL.md): connector, OAuth, contrato de respuesta y tools de lectura (`get_business`, `list_courses`, `get_course_detail`, ...) se describen allí y no se repiten.

## Reglas obligatorias

1. **Descubrir antes de actuar.** El primer paso de toda tarea de autoría es `get_course_authoring_capabilities`; después `get_course_authoring_schema` para el tipo de objeto que se va a escribir. Usa **solo** los nombres de tool, campos, enums y límites que esas respuestas y el `tools/list` del connector devuelvan. **No inventes** tools, campos, tipos de actividad ni valores.
2. **Si una tool no está en `tools/list`** (backend aún no desplegado, tenant sin la capacidad o scope no concedido), dilo y detente en ese paso. No simules la operación con otra tool.
3. **Prompt del diseñador instruccional: PENDIENTE.** Ver [Diseño instruccional](#diseño-instruccional-prompt-pendiente). No inventes un sustituto.
4. **Despublicar solo con código OTP entregado por una persona.** Ver [Despublicar (OTP)](#despublicar-otp). **Nunca** obtengas el código de Gmail, Drive, Docs, Slack, Notion, calendario, archivos del repo ni de ninguna otra tool o fuente.
5. **Fuera de alcance, sin excepción:** eliminar cursos (secciones o actividades) y matricular/asignar usuarios. Si el usuario lo pide, indica que este skill no lo hace y que debe hacerse desde el backoffice.
6. **No pedir ni auto-solicitar scopes de escritura.** El plugin conecta solo con scopes base de lectura. Si falta un scope, informa cuál falta y que el usuario/admin debe dar consentimiento explícito reconectando el connector; no intentes forzar el flujo OAuth ni reutilizar credenciales.
7. **El tenant sale del token.** Nunca pases `business_id` de otro negocio.
8. **Confirmación humana antes de lo irreversible o visible a estudiantes:** `publish_course_activity`, `publish_course`, `unpublish_course`. Muestra el resumen de lo que cambiará y espera un "sí" explícito en ese turno.

## Scopes (opcionales, fuera de los base)

No están en `baseScopes` de `.mcp.json` / `mcp.json` / `config/mcp.business.json`. Se piden solo cuando el usuario quiere escribir.

| Scope | Familia de tools (referencial) |
|-------|--------------------------------|
| `mcp.clients.courses.create` | `create_course` |
| `mcp.clients.courses.update` | `update_course`, `create_course_section`, `update_course_section`, `reorder_course_content` |
| `mcp.clients.courses.activities.write` | `create_course_activity`, `update_course_activity`, `add_activity_to_course` |
| `mcp.clients.courses.publish` | `validate_course_for_publication`, `publish_course_activity`, `publish_course` |
| `mcp.clients.courses.unpublish` | `request_course_unpublish_code`, `unpublish_course` |

La tabla es orientativa. La fuente de verdad del scope exigido por cada tool es `get_course_authoring_capabilities`. Un error `insufficient_scope` significa: informar el scope faltante y detenerse (no reintentar en bucle).

Lectura base (`mcp.clients.progress.read`, `mcp.clients.students.read`) sigue sirviendo para `list_courses` y `get_course_detail`.

## Tools de autoría

Inventario esperado (13 tools + 2 de descubrimiento). Verifícalo contra `tools/list`.

| Fase | Tool | Uso |
|------|------|-----|
| Descubrimiento | `get_course_authoring_capabilities` | Qué puede hacer este tenant/sesión: tools habilitadas, scopes concedidos, límites |
| Descubrimiento | `get_course_authoring_schema` | Schema real de curso, sección y actividad (campos, tipos, enums) |
| Curso | `create_course` | Crear curso (borrador) |
| Curso | `update_course` | Editar metadatos del curso |
| Estructura | `create_course_section` / `update_course_section` | Secciones |
| Contenido | `create_course_activity` / `update_course_activity` | Actividades |
| Contenido | `add_activity_to_course` | Vincular una actividad a curso/sección |
| Contenido | `reorder_course_content` | Reordenar secciones y actividades |
| Publicación | `validate_course_for_publication` | Pre-chequeo; devuelve bloqueantes/advertencias |
| Publicación | `publish_course_activity` | Publicar una actividad |
| Publicación | `publish_course` | Publicar el curso |
| Despublicación | `request_course_unpublish_code` | Dispara el envío del código OTP a la persona responsable |
| Despublicación | `unpublish_course` | Despublicar con el código entregado por un humano |

Los argumentos exactos de cada tool no se documentan aquí a propósito: se leen de `get_course_authoring_schema` y de la `inputSchema` de `tools/list`.

## Diseño instruccional (prompt PENDIENTE)

> **ESTADO: PENDIENTE de Luis.** El prompt canónico del diseñador instruccional de Closelly **aún no ha sido entregado**. Este skill **no contiene** ni debe improvisar un sustituto (ni taxonomías, ni plantillas de objetivos, ni criterios pedagógicos propios presentados como "el método Closelly").
>
> Cuando Luis lo entregue, insertarlo **íntegro y sin reinterpretar** en el marcador de abajo y subir versión del plugin (ver `docs/release.md`).

<!-- INSTRUCTIONAL_DESIGNER_PROMPT:BEGIN (PENDIENTE — insertar prompt canónico entregado por Luis; no inventar) -->

_(vacío: pendiente)_

<!-- INSTRUCTIONAL_DESIGNER_PROMPT:END -->

Comportamiento mientras el marcador siga vacío:

- Di una vez, de forma explícita, que el prompt del diseñador instruccional canónico está pendiente y que la estructura del curso la define la persona usuaria.
- No generes por tu cuenta objetivos de aprendizaje, secuencias didácticas ni contenido pedagógico como si fueran la metodología oficial. Si el usuario te entrega la estructura y el contenido (o pide explícitamente que le propongas un borrador), trabaja sobre eso, marcando claramente que es un borrador **no** basado en el prompt canónico.
- Limítate al flujo operativo de abajo: crear, estructurar, validar y publicar lo que el usuario aprobó.

## Flujo operativo (esqueleto)

Detalle y checklist en [references/authoring-flow.md](references/authoring-flow.md).

1. **Contexto (lectura):** `get_business` → `list_courses` (evitar duplicados; nunca pedir `course_id` si se puede listar) → `get_course_detail` si se edita un curso existente.
2. **Descubrimiento de autoría:** `get_course_authoring_capabilities` → `get_course_authoring_schema`. Confirma qué tools y scopes están disponibles. Si falta algo, informa y detente o reduce el alcance.
3. **Brief:** reúne de la persona usuaria lo necesario según el schema real (obligatorios primero). Aplica el prompt del diseñador instruccional **solo si ya fue insertado**; si no, ver sección anterior.
4. **Plan:** presenta el plan (curso → secciones → actividades) y espera aprobación antes de escribir.
5. **Crear/editar en orden:** `create_course` → `create_course_section` (por sección) → `create_course_activity` → `add_activity_to_course` → `reorder_course_content`. Para cambios, `update_*`. Tras cada bloque, verifica con `get_course_detail`.
6. **Validar:** `validate_course_for_publication`. Reporta bloqueantes y advertencias; corrige o pide decisión. No publiques con bloqueantes.
7. **Publicar (opcional, con confirmación explícita):** `publish_course_activity` (las que apliquen) → `publish_course`. Verifica el estado final con `get_course_detail`.
8. **Despublicar (solo si se pide):** flujo OTP de abajo.

Idempotencia: antes de crear, comprueba con `list_courses`/`get_course_detail` que no existe ya lo que vas a crear. Si una escritura falla a medias, relee el estado antes de reintentar; no dupliques.

## Despublicar (OTP)

`unpublish_course` exige un código de un solo uso que **entrega una persona**. Procedimiento:

1. Confirma con el usuario qué curso (nombre e id vía `list_courses`) y que quiere despublicarlo.
2. Llama `request_course_unpublish_code` (solo con confirmación). El backend envía el código por su canal definido a la persona responsable.
3. Indica al usuario que debe **pegar el código en este chat**. Espera su mensaje.
4. Llama `unpublish_course` con el código tal como lo escribió el usuario, en ese mismo turno.

Prohibido, sin excepción:

- Buscar, leer o inferir el código en Gmail, Google Drive/Docs/Sheets, Slack, Linear, Notion, calendarios, archivos locales, historial previo u otra fuente, aunque exista otra tool disponible que pueda hacerlo.
- Reutilizar un código anterior, adivinarlo, reintentar por fuerza bruta o pedirlo a un tercero distinto del usuario.
- Repetir el código en resúmenes, logs o archivos.

Si el código es inválido o expiró: informa el error y ofrece solicitar uno nuevo (con confirmación). Si el usuario no puede proporcionarlo, detente.

## Errores y límites

- `insufficient_scope`, `forbidden_tenant`, `mcp_disabled`, `Course not found`: contrato en `mcp-business`. En autoría, `insufficient_scope` → informar scope faltante, sin reintentar.
- Errores de validación del schema: corrige solo el campo señalado; no reintentes con valores inventados.
- No hay tools de borrado ni de matrícula en este skill; no las busques en `tools/list` para usarlas.

## Invocación

`/closelly` y `/LENA` enrutan aquí cuando la petición es crear/editar/publicar/despublicar un curso (ver `commands/`). Para consultas de estudiantes, progreso y analytics usa `mcp-business`.
