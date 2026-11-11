---
name: create-activities
description: "Crea actividades de Closelly y sus recursos finales a partir de un objetivo o plan aprobado: tarjetas, videos educativos con Remotion, audio, documentos, preguntas e interactivos. Consulta formatos reales y deriva la persistencia MCP a create-courses."
license: MIT
metadata:
  plugin_name: closelly-ai-plugins
  plugin_version: "1.12.0"
  plugin_display_name: Closelly MCP App
---

# Crear actividades y sus recursos para Closelly

Convierte el objetivo de una actividad en contenido listo para revisar o cargar. Si el usuario pide archivos, produce los archivos finales cuando las herramientas lo permitan: un storyboard no sustituye un video, ni un guion sustituye un MP3.

Para diseñar el curriculum completo o un brief pedagógico desde cero, usa [instructional-design](../instructional-design/SKILL.md). Para crear o editar registros en Closelly, usa [create-courses](../create-courses/SKILL.md) y su descubrimiento de capacidades y schema. Preparar recursos localmente no requiere una conexión MCP.

## Selección del formato

Lee [formatos por actividad](references/activity-formats.md) antes de fijar tamaños, extensiones o `content_type`. Distingue requisitos comprobados del producto de recomendaciones de producción. Si el schema vivo difiere de esta referencia, prevalece el schema y se informa la diferencia.

| Recurso solicitado | Guía que debes aplicar |
| --- | --- |
| Tarjetas de contenido, imágenes, artículos, documentos o preguntas | [Formatos de actividad y tarjetas](references/activity-formats.md) |
| Video educativo, animación explicativa o video con locución | [Video educativo con Remotion](references/video-remotion.md) y [estilos y herramientas](references/remotion-options.md) |
| Audio, podcast o voz en off | [Generación y entrega de audio](references/audio.md) |
| ZIP HTML de Interactivo Closelly | [closelly-interactive](../closelly-interactive/SKILL.md), con sus ejemplos horizontal y vertical |

## Brief de la actividad

Aprovecha el material ya entregado y pregunta solo lo que falte para producir el recurso:

- Objetivo observable, audiencia, idioma y fuentes de contenido.
- Tipo de actividad, duración objetivo y orientación de diseño.
- Identidad visual: paleta de colores, tipografías, logo y referencias que aporte el usuario. Para video, solicita estos datos antes de fijar el diseño final; puedes avanzar el guion mientras llegan.
- Para locución: tono, variante de idioma y preferencias de voz. Comprueba qué herramienta de audio ofrece realmente la sesión.

Mantén la orientación elegida durante todo el recurso. No confundas las medidas del ZIP interactivo con las de una tarjeta, una imagen de curso o un video.

## Producción

1. Define el entregable y el `content_type` real de la referencia. Si se va a guardar en Closelly, confirma los campos disponibles mediante el flujo de `create-courses`; no copies el payload del backoffice como si fuera el schema MCP.
2. Organiza el contenido por unidades cortas con una explicación, un ejemplo y una acción o pregunta cuando corresponda. Conserva las fuentes y la información del usuario.
3. Produce el recurso con la guía del formato. Para videos, **usa Remotion**, selecciona herramientas o plantillas de estilos con adopción verificable y aplica la paleta/diseño del usuario. El mismo agente prepara el guion y genera la voz en off mediante la capacidad de audio disponible, y añade subtítulos sincronizados.
4. Revisa la salida real: legibilidad móvil, dimensiones, reproducción, duración, audio y concordancia entre voz y subtítulos. Corrige los problemas observados antes de entregar.
5. Entrega archivos utilizables, sus editables cuando existan y una ficha breve con tipo de actividad, formato, tamaño o duración y estado de validación. Identifica cualquier recurso pendiente; no presentes un archivo simulado como renderizado.

## Guardar la actividad en Closelly

Cuando el usuario solicite persistirla, continúa con [create-courses](../create-courses/SKILL.md): capacidades y schema reales, tenant de la conexión, permisos y reglas de publicación de ese flujo. La disponibilidad de `ContentCanvas` o `ContentIframe` en un catálogo no garantiza que exista una herramienta para cargar sus archivos o children.

El MCP de autoría consultado admite referencias de archivos: no envíes binarios, base64, rutas locales ni URLs inventadas como si fueran recursos ya alojados. Descubre una carga compatible si existe; si falta, entrega los archivos y explica el paso de carga que queda en el backoffice. Verifica la actividad creada con una lectura posterior antes de informar su estado.
