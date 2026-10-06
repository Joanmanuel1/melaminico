import json, re, shutil, sys
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "src"
DEMO = ROOT.parent / "landing-demo" / "assets"

FONTS = "https://fonts.googleapis.com/css2?family=Alfa+Slab+One&family=Archivo+Black&family=Archivo+Narrow:wght@700&display=swap"

SECTIONS = [
    ("01-hero", "melh", ["base", "btn"], ["reveal"]),
    ("02-aprender", "mela", ["base", "foto", "chips"], ["reveal"]),
    ("03-primer-paso", "melp", ["base", "foto", "chips"], ["reveal"]),
    ("04-armado", "melv", ["base", "btn"], ["reveal", "04-armado"]),
    ("05-cursos", "melc", ["base"], ["reveal"]),
    ("06-footer", "melf", ["base", "btn"], ["reveal"]),
]

ASSETS = {
    "logo": (DEMO / "img/logo.png", "01-logo.png"),
    "laptop": (DEMO / "img/laptop.png", "02-laptop.png"),
    "dormitorio": (DEMO / "img/mueble-dormitorio.jpg", "03-dormitorio.jpg"),
    "boceto": (DEMO / "img/foto-3882.jpg", "04-boceto.jpg"),
    "paso": (DEMO / "img/foto-3859.jpg", "05-paso.jpg"),
    "taller": (DEMO / "img/foto-2531.jpg", "06-taller.jpg"),
    "instagram": (DEMO / "img/instagram.png", "07-instagram.png"),
    "armado-poster": (DEMO / "video/armado-poster.jpg", "09-armado-poster.jpg"),
    "armado-video": (DEMO / "video/armado.mp4", "10-armado.mp4"),
}


def split_top(s):
    out, depth, cur = [], 0, ""
    for ch in s:
        if ch in "([":
            depth += 1
        elif ch in ")]":
            depth -= 1
        if ch == "," and depth == 0:
            out.append(cur)
            cur = ""
        else:
            cur += ch
    out.append(cur)
    return out


def prefix_selector(sel, p):
    sel = re.sub(r"\.([A-Za-z_][\w-]*)", lambda m: f".{p}-{m.group(1)}", sel.strip())
    if sel == "&":
        return "." + p
    if sel.startswith("& "):
        return f".{p}.{p} " + sel[2:]
    if sel.startswith("&"):
        return "." + p + sel[1:]
    return f".{p}.{p} {sel}"


VARS = ["naranja-claro", "naranja", "navy", "crema", "blanco", "gris-btn", "f-titulo", "f-texto", "f-slab", "pad", "max", "gutter"]


def prefix_vars(css, p):
    names = "|".join(VARS)
    css = re.sub(r"(?<=var\()--(" + names + r")(?![\w-])", lambda m: f"--{p}-{m.group(1)}", css)
    return re.sub(r"(?<![\w.-])--(" + names + r")(?=\s*:)", lambda m: f"--{p}-{m.group(1)}", css)


def process_css(css, p):
    out, i = [], 0
    while i < len(css):
        j = css.find("{", i)
        if j < 0:
            break
        head = css[i:j].strip()
        depth, k = 1, j + 1
        while depth:
            depth += (css[k] == "{") - (css[k] == "}")
            k += 1
        body = css[j + 1:k - 1]
        if head.startswith(("@media", "@supports")):
            out.append(head + " {\n" + process_css(body, p) + "\n}")
        elif head.startswith("@"):
            out.append(head + " {" + body + "}")
        else:
            sels = ",\n".join(prefix_selector(s, p) for s in split_top(head))
            out.append(sels + " {" + body + "}")
        i = k
    return "\n".join(out)


def prefix_html_classes(html, p):
    def fix(m):
        return 'class="' + " ".join(f"{p}-{c}" for c in m.group(1).split()) + '"'
    return re.sub(r'class="([^"]*)"', fix, html)


def read(path):
    return (SRC / path).read_text(encoding="utf-8")


def build(local):
    cfg = json.loads((ROOT / "config.json").read_text())
    if local:
        cfg["mail"] = cfg["mail"] or "demo@example.com"
    urls = json.loads((ROOT / "urls.json").read_text())
    warnings, errors = [], []

    def img(name):
        if local:
            return "../landing-demo/assets/" + str(ASSETS[name][0].relative_to(DEMO))
        if not urls.get(name):
            errors.append(f"falta la URL de '{name}' en urls.json")
            return ""
        return urls[name]

    yt = cfg.get("armado_youtube", "").strip()
    m = re.search(r"(?:v=|youtu\.be/|shorts/|embed/)([\w-]{11})", yt) or (re.fullmatch(r"[\w-]{11}", yt) and re.match(r"(.+)", yt))
    yt_id = m.group(1) if m else ""
    video_ok = local or bool(urls.get("armado-video"))
    if yt_id:
        video_ok = False
    elif not video_ok:
        warnings.append("sin video: el bloque 04 usa solo el poster (completar armado_youtube en config.json)")

    out_dir = ROOT / ("dist-local" if local else "dist")
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir()

    results = {}
    for name, p, shared, js_parts in SECTIONS:
        if name == "06-footer":
            links = []
            if cfg.get("instagram"):
                links.append(f'<a class="pie__instagram" href="{cfg["instagram"]}" target="_blank" rel="noopener" aria-label="Instagram de Melamínico"><svg aria-hidden="true"><use href="#__P__-instagram"/></svg></a>')
            if cfg.get("mail"):
                links.append(f'<a class="pie__mail" href="mailto:{cfg["mail"]}" aria-label="Escribinos por mail"><svg aria-hidden="true"><use href="#__P__-mail"/></svg></a>')
            if not links:
                warnings.append("06-footer omitido: faltan instagram y mail en config.json")
                continue
            footer_links = "\n      ".join(links)
            words = ["CLASES GRABADAS", "ASESORÍAS PERSONALIZADAS", "DISEÑO 2D / 3D", "ENSAMBLADO"]
            item = lambda w: f'<span class="pie__item"><svg aria-hidden="true"><use href="#__P__-asterisco"/></svg>{w}</span>'
            half = "".join(item(w) for w in words) * 3
            cinta = half + half
        css = "\n".join(read(f"shared/{s}.css") for s in shared)
        if "reveal" in js_parts:
            css += "\n" + read("shared/reveal.css")
        css += "\n" + read(f"{name}.css")
        css = prefix_vars(process_css(css, p), p)

        html = read(f"{name}.html")
        if name == "04-armado":
            poster = '<img class="__P__-armado__video" src="[[img:armado-poster]]" alt="" aria-hidden="true">'
            if yt_id:
                src = (f"https://www.youtube-nocookie.com/embed/{yt_id}?autoplay=1&mute=1&loop=1&playlist={yt_id}"
                       "&controls=0&playsinline=1&rel=0&modestbranding=1&disablekb=1&iv_load_policy=3&fs=0")
                media = (poster + '\n  <div class="__P__-armado__yt" aria-hidden="true"><iframe src="' + src +
                         '" title="Video: armado del mueble" loading="lazy" allow="autoplay; encrypted-media" tabindex="-1"></iframe></div>')
            elif video_ok:
                media = ('<video class="__P__-armado__video" autoplay muted loop playsinline preload="metadata" '
                         'poster="[[img:armado-poster]]" aria-hidden="true">\n    <source src="[[video]]" type="video/mp4">\n  </video>')
            else:
                media = poster
            html = html.replace("[[armado-media]]", media.replace("__P__-", ""))
        if name == "06-footer":
            html = html.replace("[[footer-links]]", footer_links).replace("[[cinta]]", cinta)
        html = prefix_html_classes(html, p)

        scripts = [read("shared/fit.js")]
        for part in js_parts:
            scripts.append(read("shared/reveal.js") if part == "reveal" else read(f"{part}.js"))

        block = f'<link rel="stylesheet" href="{FONTS}">\n<style>\n{css}\n</style>\n\n'
        block += f'<div class="{p}" id="{p}-root">\n{html}\n</div>\n'
        for s in scripts:
            block += f"\n<script>\n{s}</script>\n"

        block = block.replace("__P__", p)
        block = re.sub(r"\[\[img:([\w-]+)\]\]", lambda m: img(m.group(1)), block)
        block = block.replace("[[video]]", urls.get("armado-video", "") if not local else "../landing-demo/assets/video/armado.mp4")
        block = re.sub(r"\[\[link:(\w+)\]\]", lambda m: cfg[m.group(1)], block)

        if "/*" in block or "<!--" in block or re.search(r"^\s*//", block, re.M):
            errors.append(f"{name}: tiene comentarios, Tiendup no los admite")
        left = re.findall(r"\[\[[^\]]+\]\]", block)
        if left:
            errors.append(f"{name}: tokens sin resolver {left}")

        (out_dir / f"{name}.html").write_text(block, encoding="utf-8")
        results[name] = len(block)

    if not local:
        subir = ROOT / "subir"
        if subir.exists():
            shutil.rmtree(subir)
        subir.mkdir()
    for k, (src, dst) in ASSETS.items():
        if not local:
            shutil.copy(src, ROOT / "subir" / dst)

    if local or not errors:
        theme = "https://d3ekkp2oigezer.cloudfront.net/business/91976/themes/lite/assets/css/"
        order = ["01-hero", "02-aprender", "03-primer-paso", "04-armado", "05-cursos", "06-footer"]
        parts = []
        for n in order:
            body = (out_dir / f"{n}.html").read_text(encoding="utf-8")
            parts.append('<div class="page-section uk-section uk-padding-remove-vertical uk-section-muted">'
                         '<div class="uk-container uk-width-5-6@l"><div class="uk-width-1-1 custom-code-container">'
                         + body + "</div></div></div>")
        page = ('<!doctype html><html lang="es"><head><meta charset="utf-8">'
                '<meta name="viewport" content="width=device-width, initial-scale=1"><title>Preview Tiendup</title>'
                + "".join(f'<link rel="stylesheet" href="{theme}{c}">' for c in ["metropolis.css?v=2", "uikit.lite2.min.css?v=2", "style.css?v=2"])
                + '</head><body><div class="home-page-wrapper">' + "\n".join(parts) + "</div>"
                + '<script>var s=location.hash.slice(1)||"muted";document.querySelectorAll(".custom-code-container").forEach(function(c){var e=c.closest(".page-section");e.className=e.className.replace(/uk-section-\\w+/,"uk-section-"+s);});</script></body></html>')
        (ROOT / ("preview.html" if local else "preview-final.html")).write_text(page, encoding="utf-8")

    if errors and not local:
        shutil.rmtree(out_dir)
        results = {}

    for n, size in results.items():
        print(f"  {n}.html  {size/1024:.1f} KB")
    for w in warnings:
        print("AVISO:", w)
    for e in errors:
        print("ERROR:", e)
    return not errors


if __name__ == "__main__":
    local = "--local" in sys.argv
    ok = build(local)
    if not ok:
        sys.exit(1)
