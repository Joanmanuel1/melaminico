# Melamínico

Melamínico es una escuela online de carpintería en melamina: enseña a diseñar y armar muebles (por ejemplo, una mesita de luz) con cursos grabados y asesoría. Los cursos se venden en una tienda de **Tiendup**:

**Sitio en vivo:** https://melaminico.tiendup.com/

Este repositorio guarda los archivos finales de la **landing page**, que es la página principal de la tienda: el diseño, las imágenes y el código que está publicado.

---

## Qué hay en cada carpeta

```
.
├── diseño/            Diseño original de la landing (PDF). Es la referencia visual.
├── imagenes/          Material gráfico original: fotos de la diseñadora, piezas de Canva y capturas.
└── landing-tiendup/   El código de la landing que está publicada. Es la carpeta más importante.
    ├── src/           ✏️  CÓDIGO FUENTE: acá se hacen los cambios.
    │   └── shared/        Estilos y scripts que comparten todas las secciones.
    ├── config.json    ✏️  Links, mail, Instagram y video de YouTube.
    ├── urls.json      ✏️  Direcciones de las imágenes ya subidas a Tiendup.
    ├── build.py       Script que arma los bloques finales a partir de src/.
    ├── dist/          ⚙️  GENERADO: los bloques listos para pegar en Tiendup.
    ├── dist-local/    ⚙️  GENERADO: lo mismo, con imágenes locales (solo para probar).
    ├── subir/         Imágenes que se subieron al CDN de Tiendup.
    ├── preview.html        ⚙️  GENERADO: vista previa local.
    └── preview-final.html  ⚙️  GENERADO: vista previa con las imágenes reales.
```

> **Regla de oro:** solo se editan los archivos marcados con ✏️. Los marcados con ⚙️ se generan solos con `build.py`. Si los editás a mano, el próximo build pisa tus cambios.

---

## Cómo funciona (la idea general)

Tiendup no nos deja subir un sitio web propio. Lo que sí permite es agregar a la página bloques de tipo **"Código HTML"**, donde se pega HTML, CSS y JavaScript.

La landing está dividida en **6 bloques**, uno por sección:

| Nº | Archivo | Qué muestra |
|----|---------|-------------|
| 01 | `01-hero` | Portada: logo, título y botón principal |
| 02 | `02-aprender` | Qué vas a aprender (incluye el programa SketchCut) |
| 03 | `03-primer-paso` | Tu primer proyecto |
| 04 | `04-armado` | Video del armado de fondo |
| 05 | `05-cursos` | Las dos opciones de curso con botón para comprar |
| 06 | `06-footer` | Cierre: mail, Instagram y link al catálogo |

Escribir todo en un solo archivo por bloque sería incómodo, así que el código está separado en `src/` (un `.html`, un `.css` y a veces un `.js` por sección). El script `build.py`:

1. Junta el HTML, el CSS y el JS de cada sección en **un solo archivo**.
2. Le agrega un **prefijo único** a todas las clases (por ejemplo `melh-` en el hero) para que los estilos de un bloque no rompan a otro ni al tema de Tiendup.
3. Reemplaza los links y las imágenes con los valores de `config.json` y `urls.json`.
4. Guarda el resultado en `dist/`.

```
src/ + config.json + urls.json  ──►  python3 build.py  ──►  dist/01-hero.html ... dist/06-footer.html  ──►  se pega en Tiendup
```

---

## Requisitos

- **Python 3** (no hace falta instalar librerías). Para verificarlo, ejecutá `python3 --version`.
- Un editor de código, por ejemplo [VS Code](https://code.visualstudio.com/).
- Acceso de administrador a la tienda de Tiendup, solo para publicar cambios.

---

## Ver la landing en tu computadora

```bash
git clone https://github.com/Joanmanuel1/melaminico.git
cd melaminico/landing-tiendup
python3 build.py --local          # genera preview.html
python3 -m http.server 8765       # levanta un servidor local
```

Después abrí en el navegador: http://localhost:8765/preview.html

La vista previa usa los mismos estilos que el tema real de Tiendup, así que se ve igual que en el sitio publicado. Para cortar el servidor, apretá `Ctrl + C`.

---

## Cómo hacer un cambio, paso a paso

**Ejemplo: cambiar un texto del hero.**

1. Abrí `landing-tiendup/src/01-hero.html` y cambiá el texto.
2. Revisalo en tu computadora: `python3 build.py --local` y recargá `preview.html`.
3. Generá la versión final: `python3 build.py`.
   - Si falta algún dato (por ejemplo, una URL de imagen), el script lo indica con `ERROR:` y no genera nada. Corregilo y volvé a correrlo.
4. Abrí `landing-tiendup/dist/01-hero.html`, seleccioná todo y copialo.
5. En el editor de Tiendup, buscá el bloque "Código HTML" del hero, borrá lo que tiene, pegá el código nuevo y guardá.
6. Revisá el sitio en vivo en la computadora y en el celular.
7. Guardá el cambio en el repositorio:
   ```bash
   git add .
   git commit -m "Cambio el texto del hero"
   git push
   ```

Solo se vuelve a pegar el bloque que cambiaste. El resto queda como está.

### Cambios habituales

| Quiero cambiar… | Dónde |
|-----------------|-------|
| Un texto | `src/NN-seccion.html` |
| Colores, tamaños o espaciados | `src/NN-seccion.css` (los colores generales están en `src/shared/base.css`) |
| El link de un botón de compra | `config.json` → `compra_inicial` / `compra_completo` |
| El mail o el Instagram | `config.json` → `mail` / `instagram` |
| El video | `config.json` → `armado_youtube` (link de YouTube) |
| Una imagen | Subirla a Tiendup y pegar su dirección en `urls.json` (ver abajo) |

### Cambiar una imagen

Tiendup no permite referenciar imágenes desde este repositorio: tienen que estar subidas a su servidor (CDN).

1. En el editor de Tiendup, agregá una sección temporal de tipo "Imágenes" y subí la imagen.
2. Abrí la página pública, hacé clic derecho sobre la imagen y elegí **"Copiar dirección de imagen"**.
3. Pegá esa dirección en `urls.json`, en la clave correspondiente (`logo`, `laptop`, `taller`, etc.).
4. Borrá la sección temporal, corré `python3 build.py` y volvé a pegar el bloque que usa esa imagen.

---

## Cosas a tener en cuenta (aprendidas en el proyecto)

- **El editor de Tiendup no acepta comentarios** (`<!-- -->`, `/* */`, `//`). No los uses en `src/`: si `build.py` encuentra uno, frena con un `ERROR:` que indica en qué bloque está.
- En `src/`, las imágenes y los links se escriben como marcadores que `build.py` reemplaza: `[[img:logo]]` toma la dirección de `urls.json` y `[[link:mail]]` toma el valor de `config.json`.
- **No hay backend:** no se pueden hacer formularios que guarden datos ni conexiones a una base de datos. Todo es HTML, CSS y JS que corre en el navegador.
- En cada bloque de Tiendup, la **separación de la sección tiene que estar en cero**. Si no, aparece una franja de color entre bloques.
- Los bloques **se pegan en orden**: 01, 02, 03, 04, 05, 06.
- No renombres las clases a mano agregando el prefijo: `build.py` se encarga. En `src/` se escriben normales (`.titulo`, `.btn`).
- Las fuentes (Alfa Slab One, Archivo Black y Archivo Narrow) se cargan desde Google Fonts.

En [`landing-tiendup/README.md`](landing-tiendup/README.md) está la guía técnica detallada. Algunas carpetas que menciona (`landing-demo/`, `youtube/`, `docs/`) son de trabajo interno y no forman parte de este repositorio. El build funciona igual sin ellas.

---

## Glosario rápido

- **Landing page:** la página principal que presenta el producto e invita a comprar.
- **Tiendup:** la plataforma donde está la tienda y se venden los cursos.
- **CDN:** el servidor donde Tiendup guarda las imágenes. Por eso se usan sus direcciones (`https://bu-cdn.tiendup.com/...`).
- **Build:** el proceso de transformar el código fuente (`src/`) en los archivos finales (`dist/`).
- **Melamina:** un tablero de madera aglomerada con recubrimiento plástico, muy usado en muebles.

---

## Contacto

- Mail: adn.melaminico@gmail.com
- Instagram: [@_melaminico](https://www.instagram.com/_melaminico/)
