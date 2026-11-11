# Remotion: plugins, estilos y adopción

## Elegir la herramienta correcta

Remotion ofrece [plugins para agentes](https://www.remotion.dev/docs/ai/plugins), [skills oficiales](https://www.remotion.dev/docs/ai/skills), [plantillas de proyecto](https://www.remotion.dev/templates) y paquetes de código. Un plugin del host no es un estilo visual: el estilo se construye con una plantilla, sus recursos y la composición.

Empieza por el plugin oficial que corresponda al host, si está disponible, o por `remotion-dev/skills`. El skill `remotion-best-practices` sirve como entrada general; `remotion-create`, `remotion-markup`, `remotion-captions` y `remotion-render` cubren creación, composición, subtítulos y render. La instalación documentada de los skills es `npx skills add remotion-dev/skills`; usa el flujo de instalación del host cuando corresponda y no confundas documentar una opción con que ya esté instalada.

## Selección con evidencia de adopción

Consulta realizada el **11 de noviembre de 2026** con la API pública de GitHub. Entre las seis plantillas oficiales de estilos comparadas, este es el orden por estrellas. Las estrellas son una señal de adopción/interés, no una medición de usuarios, descargas ni un ranking global de todos los plugins.

| Plantilla oficial | Estrellas observadas | Uso educativo posible |
| --- | ---: | --- |
| [template-tiktok](https://github.com/remotion-dev/template-tiktok) | 307 | Cápsulas de texto y subtítulos animados; adaptar el ritmo y la identidad a un curso. |
| [template-prompt-to-motion-graphics-saas](https://github.com/remotion-dev/template-prompt-to-motion-graphics-saas) | 293 | Motion graphics, diagramas y explicaciones visuales; es una base de proyecto, no un servicio Closelly. |
| [template-audiogram](https://github.com/remotion-dev/template-audiogram) | 278 | Podcast o explicación centrada en voz, texto y forma de onda. |
| [template-code-hike](https://github.com/remotion-dev/template-code-hike) | 222 | Demostraciones de código y tutoriales de programación. |
| [template-prompt-to-video](https://github.com/remotion-dev/template-prompt-to-video) | 171 | Relato con imágenes y voz en off; adaptar la síntesis a las herramientas del agente. |
| [template-three](https://github.com/remotion-dev/template-three) | 119 | Explicaciones espaciales o 3D cuando ayuden a comprender el tema. |

El repositorio de [skills oficiales](https://github.com/remotion-dev/skills) tenía 6.840 estrellas en la misma consulta. No se compara directamente con una plantilla: aporta instrucciones para todos los estilos.

Revisa el catálogo, la actividad reciente, compatibilidad y condiciones de uso al crear un video nuevo. Actualiza la fecha y las métricas si las usas para justificar qué está más adoptado; no presentes estos conteos como permanentes. Las métricas se consultan en `https://api.github.com/repos/remotion-dev/<repositorio>` y su campo `stargazers_count`.

## Aplicar el estilo

Propón una o dos direcciones adecuadas al contenido, usando los colores y diseño entregados por el usuario. Adapta títulos, ilustraciones, diagramas y subtítulos a esa identidad. Una lección explicativa puede usar una composición propia con formas y transiciones sin necesitar una plantilla de producto o una app SaaS completa. Conserva la producción como video educativo: objetivo claro, ejemplo, narración y cierre o pregunta de aplicación.
