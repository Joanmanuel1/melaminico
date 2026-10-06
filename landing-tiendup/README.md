# Landing Melamínico para Tiendup

Genera los bloques "Código HTML" del diseño nuevo (versión de `landing-demo/`) listos para pegar en el editor de Tiendup. **Fuente de verdad: `src/` + `config.json` + `urls.json`; los archivos de `dist/`, `dist-local/`, `preview*.html` y `subir/` se regeneran con `build.py` y no se editan a mano.**

## Estado (2026-10-06)

Publicado en https://melaminico.tiendup.com/ en 6 bloques (01 hero, 02 aprender, 03 primer paso, 04 armado, 05 cursos, 06 footer). Imágenes en el CDN de Tiendup (`urls.json` completo), video en YouTube (`armado_youtube`), mail e Instagram en `config.json`. Cada cambio de contenido se hace en `src/`, se corre `python3 build.py` y se repega solo el bloque afectado. Historial en `../docs/01-bitacora.md`.

## Pasos

1. **Subir las imágenes.** Los archivos de `subir/` van en orden. Para cada uno: en el editor de Tiendup agregar una sección temporal "Imágenes", subir el archivo, guardar, abrir la página pública, clic derecho sobre la imagen → "Copiar dirección de imagen", y pegar la URL en `urls.json` bajo el nombre correspondiente (01-logo → `logo`, 02-laptop → `laptop`, 03-dormitorio → `dormitorio`, 04-boceto → `boceto`, 05-paso → `paso`, 06-taller → `taller`, 07-instagram → `instagram`, 09-armado-poster → `armado-poster`). Después borrar la sección temporal.
2. **Video.** Subir `../youtube/armado-sin-audio.mp4` (el mismo video sin pista de audio; con el audio original YouTube reclama la canción "Inside of My Eyelids") a YouTube (no listado o público, con inserción permitida) y pegar el link en `armado_youtube` de `config.json`. El bloque 04 lo incrusta como fondo mudo en bucle, con el poster debajo mientras carga. Sin link, queda solo el poster. (También se puede usar `armado-video` en `urls.json` si Tiendup acepta MP4.)
3. **Contacto.** El footer lleva el mail y el Instagram de `config.json` (`mail`, `instagram`); el cliente decidió no incluir WhatsApp. Sin ninguno de los dos el bloque 06 no se genera.
4. **Generar:** `python3 build.py`. Crea `dist/` con un archivo por bloque. Falla y lista lo que falte si hay una URL vacía.
5. **Pegar** cada archivo de `dist/` en su propio bloque "Código HTML", en este orden: 01, 02, 03, 04, 05, 06 (el texto "Este curso es para vos si:" y la pregunta sobre herramientas/experiencia son una banda translúcida al pie del hero, dentro del bloque 01). La sección nativa de Tiendup "¡Mira nuestros cursos!" se eliminó de la página: el diseño no lista cursos y las dos tarjetas de 05 ya llevan a cada producto.

## Vista previa local

`python3 build.py --local` arma `preview.html` con imágenes locales; `python3 build.py` (build final) arma `preview-final.html` con las URLs reales de Tiendup. 
`python3 build.py --local` y abrir `preview.html` con un servidor desde la raíz del proyecto (`python3 -m http.server 8765`, luego `http://localhost:8765/landing-tiendup/preview.html`). Usa el CSS real del tema de Tiendup, datos de contacto de ejemplo (solo en local).

## Ajustes del editor en cada bloque

- **Separación de la sección:** ponerla en cero, o aparece una franja del color de la sección entre bloques.
- El esquema de color de la sección da igual: los bloques se verificaron en default, muted, primary y secondary.

## Cómo está armado

- `src/NN-*.html|css|js`: una sección por archivo; `src/shared/`: reglas repetidas en cada bloque (reset, botón, chips, fotos, reveal).
- `build.py` antepone un prefijo propio a cada bloque (`melh-`, `mela-`...) en clases, ids y selectores, de modo que ningún bloque pisa a otro ni al tema de Tiendup, y arma cada bloque autocontenido (sin comentarios, como exige el editor).
- Contenido destacado de `src/`: `01-hero` (hero + banda de deseo con el texto del cliente), `02-aprender` (banner + grilla de chips; el programa es SketchCut), `04-armado` (video de YouTube como fondo, con poster), `06-footer` (cinta animada, marca, frase de cierre, botón a `/c`, íconos de Instagram y mail).
- Los links están en `config.json`: hero y "Visita nuestra página" van a `/c`; los botones Comprar van a los dos productos (`compra_inicial`, `compra_completo`). Si cambia el nombre de un producto, actualizar ahí y regenerar.
- Fuentes por Google Fonts (el sitio no tiene CSP que las bloquee).

## Pendientes conocidos

- Ninguno técnico abierto. Mejora opcional: reemplazar el logo del hero (367 px) por `../youtube/logo-hd-transparente.png` (4113 px) subiéndolo al CDN.
