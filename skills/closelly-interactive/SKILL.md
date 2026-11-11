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

## Escenario fijo y una sola escala

Elige **una sola orientación para todo el paquete**, según lo solicitado para la actividad:

| Orientación del paquete | Ancho fijo | Alto fijo |
| --- | --- | --- |
| Horizontal | 1600 px | 900 px |
| Vertical | 900 px | 1600 px |

Ambas son válidas y usan el mismo algoritmo de ajuste. Configura la actividad con la orientación elegida. Todas las pantallas y ventanas de ese paquete comparten un único escenario con esas dimensiones, en la miniatura y en la pestaña o modal completo. Diseña la composición para esa orientación antes de escalarla.

La orientación del paquete es una decisión de autoría: no se deduce del tamaño del iframe ni de cómo se sostenga el teléfono. Rotar el dispositivo solo cambia la escala y el centrado. No alternes entre horizontal y vertical mediante media queries, JavaScript ni un segundo escenario.

- `html` y `body`: ancho y alto `100%`, margen y padding `0`, `overflow: hidden`.
- El contenedor del iframe ocupa toda la ventana. El escenario tiene `position: absolute`, ancho y alto fijos según la tabla y `transform-origin: top left`.
- Mantén el mismo par de dimensiones en CSS y JavaScript: 1600×900 para horizontal o 900×1600 para vertical. No uses un escenario cuadrado ni un `100vw` para maquetar las pantallas.
- El escenario y sus contenedores estructurales no llevan `max-width`, anchos de columna de escritorio ni un segundo contenedor que reduzca el área útil. El contenido puede usar grid, flex, padding y separaciones dentro del escenario elegido.
- Aplica `transform: scale(...)` **solo al escenario**. No vuelvas a escalar `html`, `body`, el contenedor del iframe, las pantallas ni el contenedor principal del contenido. No uses `zoom` ni un segundo ajuste de tipo `contain`.
- Calcula siempre la mayor escala que permite ver todo: `Math.min(window.innerWidth / stageWidth, window.innerHeight / stageHeight)`. No la limites a `1`, no uses `Math.max` y no restes márgenes externos antes de calcularla.
- Centra el rectángulo escalado. Debe tocar dos bordes opuestos del iframe; en el otro eje puede sobrar fondo. Conservar la proporción elegida (16:9 o 9:16) sin recortar puede dejar franjas: no estires el contenido para quitarlas.
- El texto, las ilustraciones y las acciones deben caber dentro del escenario antes de escalarlo. No ocultes desbordes para disimular una composición que no cabe. Comprueba también el texto ampliado.

`window` dentro del iframe ya es el contenedor. No uses `window.parent`, dimensiones de la pantalla del teléfono ni mensajes de la app para calcular la escala.

### Base de HTML y CSS

`index.html` contiene este escenario. Añade el contenido y sus acciones dentro del mismo rectángulo; las ventanas de detalle también viven dentro de él.

```html
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Interactivo Closelly</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <div class="viewport">
    <main class="stage">
      <h1>IA tradicional y generativa</h1>
      <p>Explora las capacidades y los ejemplos de cada una.</p>
    </main>
  </div>
  <script src="app.js" defer></script>
</body>
</html>
```

`styles.css` define el lienzo completo. Esta base es horizontal (1600×900); para un paquete vertical cambia únicamente el ancho a `900px` y el alto a `1600px`, y usa esos mismos valores en JavaScript. Los tamaños de diseño no dependen del ancho de un teléfono o escritorio.

```css
* { box-sizing: border-box; }
html, body {
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 0;
  overflow: hidden;
}
body { background: #e8eef5; font-family: system-ui, sans-serif; }
.viewport { position: fixed; inset: 0; overflow: hidden; }
.stage {
  position: absolute;
  left: 0;
  top: 0;
  width: 1600px;
  height: 900px;
  transform-origin: top left;
  padding: 64px;
  background: #fff;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 32px;
  font-size: 2rem;
}
h1 { margin: 0; font-size: 4rem; }
p { margin: 0; line-height: 1.4; }
```

### Ajuste del escenario

Inicializa este ajuste en `app.js` antes de la lógica de interacción. `defer` asegura que el escenario ya exista. Si el iframe empieza oculto y mide cero, conserva la última escala válida y vuelve a medir cuando aparezca. No lo dejes oculto indefinidamente esperando una acción del alumno.

```javascript
(function () {
  var stage = document.querySelector('.stage');
  // Horizontal: 1600 × 900. Para un paquete vertical: 900 × 1600.
  var stageWidth = 1600;
  var stageHeight = 900;

  function fitStage() {
    var width = window.innerWidth;
    var height = window.innerHeight;
    if (width < 1 || height < 1) return;
    var scale = Math.min(width / stageWidth, height / stageHeight);
    stage.style.transform = 'scale(' + scale + ')';
    stage.style.left = ((width - stageWidth * scale) / 2) + 'px';
    stage.style.top = ((height - stageHeight * scale) / 2) + 'px';
  }

  fitStage();
  window.addEventListener('load', fitStage);
  window.addEventListener('resize', fitStage);
  window.addEventListener('pageshow', fitStage);
  document.addEventListener('visibilitychange', function () {
    if (!document.hidden) fitStage();
  });
  if (typeof ResizeObserver === 'function') {
    var viewportObserver = new ResizeObserver(fitStage);
    viewportObserver.observe(document.documentElement);
  }
})();
```

Los [ejemplos incluidos](references/examples.md) aplican la misma estructura: `assets/examples/ia-tradicional-vs-generativa/` es horizontal (1600×900) y `assets/examples/example-two/` es vertical (900×1600). Sus archivos se copian sin modificaciones del backend. Puedes usar también la base autocontenida anterior.

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

## Verificación de la entrega

- Revisa el paquete dentro de un iframe, no solo en una ventana de escritorio. Prueba al menos `360×200` (miniatura), `1158×540` (teléfono horizontal), `393×852` (vertical), `1600×900` y `1920×1080`.
- En todos, el escenario conserva el par de dimensiones elegido antes del transform: 1600×900 o 900×1600. Al girar o redimensionar el iframe, nunca intercambia ancho y alto. Su rectángulo visible cabe entero, está centrado y ocupa todo el ancho o todo el alto disponible. No hay scroll global, recortes ni un escalado adicional.
- Comprueba por separado las referencias horizontal y vertical: un paquete no alterna entre ellas. Redimensiona el mismo iframe sin recargarlo y comprueba una carga inicialmente oculta. Todas las pantallas, ventanas y acciones deben seguir funcionando.
- Prueba el texto al 136%: ningún texto ni acción principal queda fuera del escenario.
- Comprueba que inicio, progreso y finalización parten de acciones concretas. No incluyas un runtime falso ni peticiones directas en el ZIP.

## Subida

En el curso, actividad **Interactivo Closelly**. Subir un ZIP nuevo reemplaza el paquete anterior. La URL del reproductor la define Closelly.
