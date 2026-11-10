---
name: closelly-interactive
description: Arma un ZIP compatible con la actividad Interactivo Closelly. Úsalo cuando un cliente pida a su AI crear o adaptar un interactivo HTML para un curso de Closelly.
---

# Interactivo Closelly

Construye un ZIP estático. El cliente lo sube en la actividad **Interactivo Closelly** del backoffice. Closelly lo guarda y lo muestra dentro de un iframe. No diseñes una app de Closelly, no llames a su API y no inventes la URL del reproductor.

## Qué entregas

Un archivo `.zip` con `index.html` en la raíz. Si todo el paquete está dentro de una sola carpeta, Closelly aplana esa carpeta.

## Archivos

- Rutas relativas: `styles.css`, `app.js`, `audio/`, `images/`, `fonts/`.
- Extensiones permitidas: `.html`, `.htm`, `.css`, `.js`, `.mjs`, `.json`, `.map`, `.txt`, `.vtt`, `.svg`, `.png`, `.jpg`, `.jpeg`, `.gif`, `.webp`, `.ico`, `.woff`, `.woff2`, `.ttf`, `.otf`, `.mp3`, `.wav`, `.ogg`, `.m4a`, `.mp4`, `.webm`, `.pdf`.
- Sin `..`, sin enlaces simbólicos y sin ejecutables.
- Límites: 40 MB comprimido, 150 MB descomprimido, 400 archivos.
- No pongas tokens, correos ni credenciales.
- No cargues scripts remotos. Una hoja de estilos `https`, por ejemplo Google Fonts, sí es válida. Si el paquete trae fuentes, van en `fonts/`.

## Dónde se ve

Closelly no escala el documento. La miniatura del curso es un iframe bajo, de unos 200 px. En la versión web se abre en una pestaña. En la app nativa se abre en un modal. El HTML tiene que caber solo en esa ventana.

## Ajuste al contenedor

Horizontal y vertical usan la misma regla. No hay un segundo algoritmo para vertical. El escenario tiene el tamaño con el que se diseñó y no cambia cuando rota el teléfono. Ese tamaño sigue la orientación elegida en la actividad:

- Horizontal: más ancho que alto, por ejemplo `1600×900`.
- Vertical: más alto que ancho, por ejemplo `900×1600`.

`html` y `body` ocupan el 100 % del iframe, con `margin: 0` y `overflow: hidden`. El escenario va en posición absoluta. No lo maquetes al ancho de un escritorio ni con un `100vw` suelto.

Al cargar, en `resize`, en `pageshow` y cuando el documento pasa a visible, calcula la escala y centra el escenario. Si el iframe todavía mide 0 porque está oculto, no guardes `scale(0)`: vuelve a medir cuando tenga tamaño. El espacio que sobra es fondo, no un recorte. Un escenario vertical en la miniatura cabe entero, con espacio a los lados. Uno horizontal en una pestaña alta cabe entero, con espacio arriba y abajo. `window` dentro del iframe ya es el contenedor. La app no envía el tamaño.

```javascript
function fitStage() {
  if (window.innerWidth < 1 || window.innerHeight < 1) return;
  var scale = Math.min(window.innerWidth / stageWidth, window.innerHeight / stageHeight);
  if (!scale) return;
  stage.style.transform = 'scale(' + scale + ')';
  stage.style.transformOrigin = 'top left';
  stage.style.left = ((window.innerWidth - stageWidth * scale) / 2) + 'px';
  stage.style.top = ((window.innerHeight - stageHeight * scale) / 2) + 'px';
}
window.addEventListener('resize', fitStage);
window.addEventListener('pageshow', fitStage);
document.addEventListener('visibilitychange', fitStage);
fitStage();
```

## Lo que inyecta Closelly

No incluyas tu propio `window.ClosellyInteractive`. Closelly lo inserta en `index.html` y solo entrega el nombre preferido y el idioma. No recibe correo, id de alumno ni credenciales.

```javascript
ClosellyInteractive.context.preferred_name // texto, puede ir vacío
ClosellyInteractive.context.locale         // idioma, por defecto "es"
ClosellyInteractive.start()
ClosellyInteractive.progress('id-del-paso')
ClosellyInteractive.complete()
```

`loaded` lo envía Closelly al abrir el HTML. Llama a los otros tres desde una acción concreta del alumno. Cambiar de pantalla no es progreso. `complete()` no cierra la actividad del curso ni asigna puntos.

## Interacción

- Botones y enlaces se alcanzan con teclado y muestran el foco.
- El audio y el video empiezan solo después de un gesto del usuario.
- El texto puede crecer sin tapar la acción principal.

## Subida

En el curso, actividad **Interactivo Closelly**. Subir un ZIP nuevo reemplaza el paquete anterior. La URL del reproductor la define Closelly.
