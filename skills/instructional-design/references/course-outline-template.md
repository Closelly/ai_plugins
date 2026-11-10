# Plantilla de plan de curso (entregable)

Copia y completa una por curso. Usa **sección** (no “módulo”).

```markdown
## Curso: <nombre ≤ 60 caracteres>

**Objetivos de aprendizaje**
1. …
2. …

**Descripción al estudiante** (≤ 300 caracteres)
…

**Tiempo estimado:** NN minutos (meta 45–60; máx. 70 con OK)

**Estilo / personajes / humor:** …

### Secciones

#### 1. <nombre de sección>
- Objetivo de la sección: …
- Actividades:

| # | Nombre | content_type | Duración (min) | Entregable pedagógico |
|---|--------|--------------|----------------|------------------------|
| 1 | … | ContentArticle | 2 | Flashcards: … |
| 2 | … | ContentVideo | 3 | Storyboard: … |
| 3 | … | ContentTest | 2 | Preguntas: … |

#### 2. …

### Totales
- Actividades: N
- Duración sumada: NN min
- ¿Dentro de 45–60? sí/no

### Handoff MCP (cuando el usuario confirme el plan)
- [ ] create_course
- [ ] create_course_section × N
- [ ] create_course_activity / add_activity_to_course × N (`content_type` reales del schema)
- [ ] get_course_detail
- [ ] validate_course_for_publication (opcional)
- [ ] publish_course solo con segundo “sí”
```

