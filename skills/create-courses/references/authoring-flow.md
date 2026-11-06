# create-courses — checklist operativo

Esqueleto de flujo. Los campos de cada objeto **no** se definen aquí: se leen de `get_course_authoring_schema`. Las tools disponibles se leen de `get_course_authoring_capabilities` y `tools/list`.

> El prompt canónico del diseñador instruccional está **PENDIENTE de Luis**. Este documento no lo sustituye. Cuando se entregue, se inserta en `SKILL.md` (marcador `INSTRUCTIONAL_DESIGNER_PROMPT`) y se invoca en el paso 3.

## 0. Pre-vuelo

- [ ] Connector `closelly-business` conectado (OAuth de User, `business.mcp_enabled = true`).
- [ ] `tools/list` incluye las tools de autoría. Si no, informar y parar.
- [ ] Scopes de escritura concedidos por consentimiento explícito. Si no, informar cuáles faltan; no solicitarlos automáticamente.

## 1. Contexto

| Paso | Tool | Resultado |
|------|------|-----------|
| 1.1 | `get_business` | Confirmar tenant |
| 1.2 | `list_courses` | Evitar duplicados; obtener ids |
| 1.3 | `get_course_detail` | Solo si se edita un curso existente |

## 2. Descubrimiento de autoría

| Paso | Tool | Resultado |
|------|------|-----------|
| 2.1 | `get_course_authoring_capabilities` | Tools habilitadas, scopes, límites |
| 2.2 | `get_course_authoring_schema` | Schema real de curso/sección/actividad |

Registrar qué operaciones están disponibles y recortar el plan a ellas.

## 3. Brief

- [ ] Reunir campos obligatorios según el schema real.
- [ ] Si el prompt del diseñador instruccional ya fue insertado: aplicarlo tal cual. Si no: avisar que está pendiente y trabajar solo con lo que el usuario define o aprueba.

## 4. Plan y aprobación

- [ ] Mostrar árbol propuesto: curso → secciones → actividades.
- [ ] Obtener aprobación explícita antes de escribir.

## 5. Escritura (orden)

| Orden | Tool | Scope referencial |
|-------|------|-------------------|
| 1 | `create_course` | `mcp.clients.courses.create` |
| 2 | `create_course_section` | `mcp.clients.courses.update` |
| 3 | `create_course_activity` | `mcp.clients.courses.activities.write` |
| 4 | `add_activity_to_course` | `mcp.clients.courses.activities.write` |
| 5 | `reorder_course_content` | `mcp.clients.courses.update` |
| edición | `update_course`, `update_course_section`, `update_course_activity` | según tool |

- [ ] Verificar con `get_course_detail` tras cada bloque.
- [ ] Ante fallo parcial: releer estado antes de reintentar (sin duplicar).

## 6. Validación

- [ ] `validate_course_for_publication` (`mcp.clients.courses.publish`).
- [ ] Sin bloqueantes antes de continuar. Advertencias: decisión del usuario.

## 7. Publicación (confirmación explícita)

- [ ] Resumen de lo que se publicará y quién lo verá.
- [ ] "Sí" explícito del usuario.
- [ ] `publish_course_activity` (las que apliquen) → `publish_course`.
- [ ] Verificar estado final con `get_course_detail`.

## 8. Despublicación (OTP humano)

- [ ] Confirmar curso e intención con el usuario.
- [ ] `request_course_unpublish_code`.
- [ ] El usuario pega el código en el chat. **Nunca** buscarlo en Gmail, Drive, Docs, Slack ni otra fuente.
- [ ] `unpublish_course` con ese código, mismo turno.
- [ ] Verificar estado con `get_course_detail`.

## Fuera de alcance

- Eliminar cursos, secciones o actividades.
- Matricular o asignar usuarios.
- Solicitar scopes automáticamente o modificar la conexión OAuth.
