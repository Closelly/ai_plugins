# Audio y voz en off

## Generación con el mismo agente

El mismo LLM/agente que prepara la actividad redacta el guion y genera la voz en off usando su capacidad de audio o la herramienta de síntesis de voz disponible en la sesión. Reutiliza el idioma, tono y voz elegidos para que todas las escenas mantengan continuidad.

Un LLM que solo devuelve texto no puede producir un archivo de audio por sí solo. Comprueba la herramienta disponible: si falta salida de audio, indícalo y solicita una herramienta TTS compatible o un audio del usuario. Puedes terminar el guion mientras se resuelve ese paso; no presentes texto renombrado a `.mp3`, silencio o un placeholder como locución generada. Si una plantilla trae integrado otro proveedor, adapta la síntesis a la herramienta disponible en vez de asumir credenciales o cambiar de proveedor sin indicarlo.

## Flujo

1. Extrae el objetivo y prepara un guion oral breve, con frases naturales y pronunciación de siglas o nombres relevantes. No leas instrucciones de escena ni marcas de Markdown.
2. Usa el idioma y la variante del usuario; reúne tono y preferencias de voz si no están definidos. Una duración inicial de 1–3 minutos sirve como referencia pedagógica, no como límite de Closelly.
3. Sintetiza la locución real. Escucha una muestra y después la salida completa; corrige pronunciación, silencios o cortes. Si la voz es para video, crea el audio antes de cerrar las duraciones de las escenas.
4. Conserva un máster WAV/PCM cuando la herramienta lo produzca y exporta una copia MP3 para `ContentAudio`. Como recomendación de producción, usa 44,1 o 48 kHz y 128–192 kbps para voz; confirma la calidad escuchando el archivo exportado. Estos parámetros no son validaciones documentadas del backend.
5. Entrega el MP3 reproducible y la transcripción fiel; indica duración y cualquier pronunciación especial. Para video, entrega además marcas de tiempo o una transcripción alineada para los subtítulos.

## Requisito de `ContentAudio`

El modelo consultado valida una URL HTTP(S) terminada en `.mp3` y el flujo de children comprueba el nombre del archivo MP3. Que el selector de la interfaz acepte `audio/*` no garantiza que WAV, M4A o una URL con parámetros al final pasen esa validación. Produce MP3 y usa una referencia alojada que acepte el flujo real; no inventes una URL ni envíes una ruta local como `content.url`.

La evidencia de audio del alumno es otro tipo (`ContentAudioEvidence`); revisa sus reglas antes de trasladar esta restricción.

Fuente: [ContentAudio del backend](https://github.com/Closelly/backend/blob/4fe159f491ed76a82e137c24fbffaf2f2d021b00/app/models/content_audio.rb).
