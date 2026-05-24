#!/usr/bin/env python3
"""
Generador de carruseles de Instagram para Vuelta Rápida Club.

Uso:
  python3 generate_carousel.py "GP de Mónaco 2025: todo lo que tenés que saber"
  python3 generate_carousel.py "Las 5 poles más rápidas de la historia"

Output: carpeta ./carruseles/<tema>/ con 6 JPG 1080x1350 (4:5)
"""

import sys
import os
import re
import json
import argparse
from pathlib import Path

import anthropic
from playwright.sync_api import sync_playwright

CHROMIUM_PATH = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"

FONTS = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap" rel="stylesheet">
"""

BASE_CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
:root {
  --bg:      #0D0D0D;
  --red:     #E8002D;
  --red-lt:  #FF3355;
  --red-dim: rgba(232,0,45,0.14);
  --white:   #F5F5F5;
  --muted:   rgba(245,245,245,0.58);
  --line:    rgba(232,0,45,0.30);
  --line-w:  rgba(245,245,245,0.10);
}
html, body {
  width: 1080px; height: 1350px; overflow: hidden;
  background: var(--bg); color: var(--white);
  font-family: 'DM Sans', sans-serif;
}
.slide {
  width: 1080px; height: 1350px;
  position: relative; overflow: hidden;
  display: flex; flex-direction: column;
}
.brand-pill {
  position: absolute; top: 52px; left: 64px; z-index: 10;
  display: flex; align-items: center; gap: 12px;
}
.brand-dot {
  width: 10px; height: 10px; border-radius: 50%; background: var(--red); flex-shrink: 0;
}
.brand-name {
  font-family: 'Bebas Neue', sans-serif;
  font-size: 21px; letter-spacing: 4px; color: var(--white);
}
.num-badge {
  position: absolute; top: 56px; right: 64px; z-index: 10;
  font-family: 'Bebas Neue', sans-serif;
  font-size: 17px; letter-spacing: 3px; color: var(--muted);
}
.sec-label {
  font-size: 15px; letter-spacing: 6px; text-transform: uppercase;
  color: var(--red); margin-bottom: 16px; display: block;
}
.deco-line { width: 48px; height: 3px; background: var(--red); margin-bottom: 32px; }
.display { font-family: 'Bebas Neue', sans-serif; letter-spacing: 1px; line-height: 0.90; }
"""

BRAND_PILL = """<div class="brand-pill">
  <div class="brand-dot"></div>
  <span class="brand-name">VUELTA RÁPIDA</span>
</div>"""


def num_badge(n, total=6):
    return f'<div class="num-badge">{n} / {total}</div>'


def build_portada(data: dict) -> str:
    titulo = data.get("titulo", "")
    subtitulo = data.get("subtitulo", "")
    tag = data.get("tag", "F1")

    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8">{FONTS}<style>{BASE_CSS}
.portada {{
  background:
    radial-gradient(ellipse 80% 55% at 60% 45%, rgba(232,0,45,.22) 0%, rgba(13,13,13,.96) 60%),
    linear-gradient(170deg, rgba(232,0,45,.06) 0%, transparent 50%),
    var(--bg);
  align-items: center; justify-content: center; text-align: center; padding: 80px 72px;
}}
.speed-lines {{
  position: absolute; inset: 0; z-index: 0;
  background:
    repeating-linear-gradient(
      -20deg,
      transparent,
      transparent 120px,
      rgba(232,0,45,.04) 120px,
      rgba(232,0,45,.04) 122px
    );
}}
.check-bar {{
  position: absolute; bottom: 0; left: 0; right: 0; height: 18px; z-index: 2;
  background: repeating-linear-gradient(
    90deg,
    var(--red) 0px, var(--red) 36px,
    #0D0D0D 36px, #0D0D0D 72px
  );
  opacity: 0.85;
}}
.content {{ position: relative; z-index: 2; }}
.tag-pill {{
  display: inline-block;
  font-size: 15px; letter-spacing: 6px; text-transform: uppercase; color: var(--red);
  border: 1px solid var(--line); padding: 10px 32px; border-radius: 40px; margin-bottom: 52px;
}}
.titulo {{ font-size: 118px; line-height: 0.88; margin-bottom: 36px; }}
.subtitulo {{ font-size: 30px; color: var(--muted); line-height: 1.6; max-width: 800px; margin: 0 auto; }}
.sep {{
  display: flex; align-items: center; gap: 28px; margin-top: 60px; justify-content: center;
}}
.sep-line {{ width: 56px; height: 1px; background: var(--line); }}
.sep-text {{ font-size: 15px; letter-spacing: 5px; text-transform: uppercase; color: var(--muted); }}
</style></head><body>
<div class="slide portada">
  <div class="speed-lines"></div>
  <div class="check-bar"></div>
  {BRAND_PILL}
  <div class="content">
    <div class="tag-pill">{tag}</div>
    <h1 class="display titulo">{titulo}</h1>
    <p class="subtitulo">{subtitulo}</p>
    <div class="sep">
      <div class="sep-line"></div>
      <span class="sep-text">Vuelta Rápida Club</span>
      <div class="sep-line"></div>
    </div>
  </div>
</div>
</body></html>"""


def build_contenido(data: dict, num: int, total: int) -> str:
    titulo = data.get("titulo", "")
    items = data.get("items", [])
    intro = data.get("intro", "")
    label = data.get("label", "")

    items_html = ""
    for i, it in enumerate(items[:4]):
        t = it.get("titulo", "") if isinstance(it, dict) else str(it)
        d = it.get("desc", "") if isinstance(it, dict) else ""
        items_html += f"""
        <div class="item">
          <div class="item-num">{str(i + 1).zfill(2)}</div>
          <div class="item-body">
            <h4>{t}</h4>
            {f'<p>{d}</p>' if d else ''}
          </div>
        </div>"""

    label_html = f'<span class="sec-label">{label}</span>' if label else ""

    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8">{FONTS}<style>{BASE_CSS}
.cont {{
  background:
    linear-gradient(160deg, rgba(232,0,45,.12) 0%, rgba(13,13,13,.96) 35%, transparent 100%),
    radial-gradient(ellipse 65% 50% at 92% 10%, rgba(232,0,45,.18) 0%, transparent 55%),
    var(--bg);
  padding: 148px 80px 80px;
  justify-content: center;
}}
.side-stripe {{
  position: absolute; top: 0; left: 0; bottom: 0; width: 5px;
  background: linear-gradient(180deg, var(--red) 0%, rgba(232,0,45,.0) 100%);
}}
.speed-lines {{
  position: absolute; inset: 0; z-index: 0;
  background: repeating-linear-gradient(
    -15deg, transparent, transparent 140px,
    rgba(232,0,45,.03) 140px, rgba(232,0,45,.03) 142px
  );
}}
.body {{ position: relative; z-index: 2; }}
.titulo {{ font-size: 80px; margin-bottom: 36px; }}
.titulo em {{ color: var(--red); font-style: normal; }}
.intro {{ font-size: 24px; color: var(--muted); line-height: 1.65; margin-bottom: 48px; max-width: 880px; }}
.item {{ display: flex; align-items: flex-start; gap: 26px; margin-bottom: 30px; }}
.item-num {{
  width: 60px; height: 60px; border-radius: 50%; flex-shrink: 0;
  border: 1px solid var(--red); background: var(--red-dim);
  display: flex; align-items: center; justify-content: center;
  font-family: 'Bebas Neue', sans-serif; font-size: 24px; color: var(--red);
}}
.item-body h4 {{ font-size: 26px; font-weight: 500; margin-bottom: 5px; line-height: 1.3; }}
.item-body p  {{ font-size: 21px; color: var(--muted); line-height: 1.55; }}
</style></head><body>
<div class="slide cont">
  <div class="side-stripe"></div>
  <div class="speed-lines"></div>
  {BRAND_PILL}
  {num_badge(num, total)}
  <div class="body">
    {label_html}
    <div class="deco-line"></div>
    <h2 class="display titulo">{titulo}</h2>
    {f'<p class="intro">{intro}</p>' if intro else ''}
    {items_html}
  </div>
</div>
</body></html>"""


def build_dato(data: dict, num: int, total: int) -> str:
    stat = data.get("stat", "")
    unidad = data.get("unidad", "")
    titulo = data.get("titulo", "")
    descripcion = data.get("descripcion", "")
    contexto = data.get("contexto", [])

    ctx_html = ""
    for c in contexto[:3]:
        ctx_html += f'<div class="ctx-item"><span class="ctx-arr">→</span><span>{c}</span></div>'

    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8">{FONTS}<style>{BASE_CSS}
.dato {{
  background:
    radial-gradient(ellipse 75% 60% at 50% 50%, rgba(232,0,45,.20) 0%, rgba(13,13,13,.96) 58%),
    var(--bg);
  align-items: center; justify-content: center; text-align: center; padding: 100px 80px;
}}
.check-bar-top {{
  position: absolute; top: 0; left: 0; right: 0; height: 12px; z-index: 2;
  background: repeating-linear-gradient(
    90deg, var(--red) 0px, var(--red) 36px, #0D0D0D 36px, #0D0D0D 72px
  );
  opacity: 0.7;
}}
.check-bar-bot {{
  position: absolute; bottom: 0; left: 0; right: 0; height: 12px; z-index: 2;
  background: repeating-linear-gradient(
    90deg, var(--red) 0px, var(--red) 36px, #0D0D0D 36px, #0D0D0D 72px
  );
  opacity: 0.7;
}}
.content {{ position: relative; z-index: 3; display: flex; flex-direction: column; align-items: center; }}
.big-stat {{
  font-family: 'Bebas Neue', sans-serif;
  font-size: 240px; line-height: 0.82; color: var(--red-lt);
  letter-spacing: 2px;
}}
.unidad {{
  font-family: 'Bebas Neue', sans-serif;
  font-size: 68px; color: var(--red); letter-spacing: 4px; display: block; margin-bottom: 20px;
}}
.stat-titulo {{ font-size: 52px; line-height: 1.05; margin-bottom: 20px; max-width: 780px; }}
.stat-desc {{ font-size: 24px; color: var(--muted); line-height: 1.6; max-width: 720px; margin-bottom: 44px; }}
.ctx-list {{ display: flex; flex-direction: column; gap: 14px; max-width: 700px; text-align: left; }}
.ctx-item {{ display: flex; align-items: center; gap: 16px; font-size: 22px; color: var(--muted); }}
.ctx-arr {{ color: var(--red); flex-shrink: 0; }}
</style></head><body>
<div class="slide dato">
  <div class="check-bar-top"></div>
  <div class="check-bar-bot"></div>
  {BRAND_PILL}
  {num_badge(num, total)}
  <div class="content">
    <span class="big-stat">{stat}</span>
    {f'<span class="unidad">{unidad}</span>' if unidad else ''}
    <h2 class="display stat-titulo">{titulo}</h2>
    {f'<p class="stat-desc">{descripcion}</p>' if descripcion else ''}
    {f'<div class="ctx-list">{ctx_html}</div>' if ctx_html else ''}
  </div>
</div>
</body></html>"""


def build_cierre(data: dict) -> str:
    pregunta = data.get("pregunta", "¿Cuál es tu equipo favorito?")
    subtitulo = data.get("subtitulo", "Comentá abajo y seguinos para más F1")
    hashtags = data.get("hashtags", "#F1 #VueltaRapida #Formula1")

    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8">{FONTS}<style>{BASE_CSS}
.cierre {{
  background:
    radial-gradient(ellipse 90% 70% at 50% 50%, rgba(232,0,45,.18) 0%, rgba(13,13,13,.97) 62%),
    var(--bg);
  align-items: center; justify-content: center; text-align: center; padding: 80px;
}}
.speed-lines {{
  position: absolute; inset: 0; z-index: 0;
  background: repeating-linear-gradient(
    -20deg, transparent, transparent 120px,
    rgba(232,0,45,.04) 120px, rgba(232,0,45,.04) 122px
  );
}}
.check-bar {{
  position: absolute; bottom: 0; left: 0; right: 0; height: 18px; z-index: 2;
  background: repeating-linear-gradient(
    90deg, var(--red) 0px, var(--red) 36px, #0D0D0D 36px, #0D0D0D 72px
  );
  opacity: 0.85;
}}
.content {{ position: relative; z-index: 3; display: flex; flex-direction: column; align-items: center; }}
.logo-mark {{
  display: flex; flex-direction: column; align-items: center; gap: 14px; margin-bottom: 72px;
}}
.logo-dot-row {{ display: flex; gap: 12px; }}
.logo-dot {{ width: 16px; height: 16px; border-radius: 50%; background: var(--red); }}
.logo-name-row {{
  font-family: 'Bebas Neue', sans-serif; font-size: 36px; letter-spacing: 10px; color: var(--white);
}}
.logo-sub-row {{
  font-size: 14px; letter-spacing: 7px; text-transform: uppercase; color: var(--muted);
}}
.pregunta {{ font-size: 88px; line-height: 0.92; margin-bottom: 40px; }}
.pregunta em {{ color: var(--red); font-style: normal; }}
.sub {{ font-size: 28px; color: var(--muted); line-height: 1.55; max-width: 760px; margin-bottom: 48px; }}
.tags {{ font-size: 20px; color: var(--red); letter-spacing: 2px; }}
</style></head><body>
<div class="slide cierre">
  <div class="speed-lines"></div>
  <div class="check-bar"></div>
  <div class="content">
    <div class="logo-mark">
      <div class="logo-dot-row">
        <div class="logo-dot"></div>
        <div class="logo-dot" style="background:var(--white);opacity:.35"></div>
        <div class="logo-dot"></div>
      </div>
      <div class="logo-name-row">VUELTA RÁPIDA</div>
      <div class="logo-sub-row">Club · F1 Community</div>
    </div>
    <h2 class="display pregunta">{pregunta}</h2>
    <p class="sub">{subtitulo}</p>
    <p class="tags">{hashtags}</p>
  </div>
</div>
</body></html>"""


SYSTEM_PROMPT = """Sos un experto en contenido de Fórmula 1 para redes sociales en español (Argentina).
Generás contenido para carruseles de Instagram de Vuelta Rápida Club, una comunidad de F1 apasionada.

El tono es: apasionado, informativo y cercano. Como un fanático experto que comparte data con amigos.
El público son fans de F1 de habla hispana, especialmente argentinos.

Usás datos reales de F1: estadísticas, records, pilotos, equipos, circuitos, temporadas.
El lenguaje es coloquial pero preciso. Usás el voseo argentino cuando el tono lo permite.

Devolvés ÚNICAMENTE JSON válido, sin texto adicional, sin markdown, sin bloques de código.
"""

SLIDE_SCHEMA = """
{
  "portada": {
    "titulo": "TÍTULO EN MAYÚSCULAS (máx 5 palabras, impactante y conciso)",
    "subtitulo": "Desarrollo del título en 1 oración (15-20 palabras)",
    "tag": "Categoría breve (ej: GP Mónaco 2025, Records Históricos, Análisis Técnico)"
  },
  "slides": [
    {
      "tipo": "contenido",
      "label": "Etiqueta de sección (2-3 palabras en mayúsculas, ej: LO QUE PASÓ)",
      "titulo": "TÍTULO DEL SLIDE (3-5 palabras en mayúsculas)",
      "intro": "Oración introductoria opcional (máx 18 palabras)",
      "items": [
        {"titulo": "Punto clave breve", "desc": "Descripción en 1-2 oraciones (máx 22 palabras)"},
        {"titulo": "Punto clave breve", "desc": "Descripción en 1-2 oraciones (máx 22 palabras)"},
        {"titulo": "Punto clave breve", "desc": "Descripción en 1-2 oraciones (máx 22 palabras)"},
        {"titulo": "Punto clave breve", "desc": "Descripción en 1-2 oraciones (máx 22 palabras)"}
      ]
    },
    {
      "tipo": "dato",
      "stat": "número impactante (solo dígitos, ej: 7 o 91 o 1.2)",
      "unidad": "unidad del dato (ej: poles, años, seg, victorias) o vacío",
      "titulo": "QUÉ REPRESENTA ESE NÚMERO (3-5 palabras en mayúsculas)",
      "descripcion": "Explicación del dato en 1-2 oraciones (máx 25 palabras)",
      "contexto": ["dato relacionado 1", "dato relacionado 2", "dato relacionado 3"]
    },
    {
      "tipo": "contenido",
      "label": "Etiqueta de sección",
      "titulo": "TÍTULO DEL TERCER SLIDE",
      "intro": "",
      "items": [
        {"titulo": "Punto", "desc": "Descripción"},
        {"titulo": "Punto", "desc": "Descripción"},
        {"titulo": "Punto", "desc": "Descripción"},
        {"titulo": "Punto", "desc": "Descripción"}
      ]
    },
    {
      "tipo": "contenido",
      "label": "Etiqueta de sección",
      "titulo": "TÍTULO DEL CUARTO SLIDE",
      "intro": "",
      "items": [
        {"titulo": "Punto", "desc": "Descripción"},
        {"titulo": "Punto", "desc": "Descripción"},
        {"titulo": "Punto", "desc": "Descripción"},
        {"titulo": "Punto", "desc": "Descripción"}
      ]
    }
  ],
  "cierre": {
    "pregunta": "PREGUNTA DE ENGAGEMENT (4-7 palabras en mayúsculas, que incite a comentar)",
    "subtitulo": "Invitación a comentar y/o seguir la cuenta (1 oración, max 12 palabras)",
    "hashtags": "#F1 #VueltaRapida #Formula1 [2-3 hashtags específicos del tema]"
  }
}
"""


def generate_content(tema: str) -> dict:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("Falta ANTHROPIC_API_KEY en las variables de entorno.")

    client = anthropic.Anthropic(api_key=api_key)

    prompt = f"""Generá el contenido para un carrusel de Instagram de 6 slides sobre el tema: "{tema}".

El carrusel tiene esta estructura exacta:
- Slide 1: Portada (título + subtítulo + tag de categoría)
- Slide 2: Primer bloque de contenido con 4 puntos
- Slide 3: Dato estadístico impactante de F1
- Slide 4: Segundo bloque de contenido con 4 puntos
- Slide 5: Tercer bloque de contenido con 4 puntos
- Slide 6: Cierre con pregunta de engagement

Devolvé el JSON con esta estructura exacta:
{SLIDE_SCHEMA}

IMPORTANTE:
- Usá datos reales y verificados de F1
- El tono es apasionado y cercano, como entre fans
- Solo JSON válido, sin ningún texto extra"""

    message = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=2048,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = message.content[0].text.strip()
    raw = re.sub(r'^```(?:json)?\s*', '', raw)
    raw = re.sub(r'\s*```$', '', raw)
    return json.loads(raw)


def render_slides(content: dict) -> list:
    slides_html = []
    slides_html.append(build_portada(content["portada"]))

    slide_num = 2
    total = 6
    for slide_data in content.get("slides", []):
        tipo = slide_data.get("tipo", "contenido")
        if tipo == "dato":
            slides_html.append(build_dato(slide_data, slide_num, total))
        else:
            slides_html.append(build_contenido(slide_data, slide_num, total))
        slide_num += 1

    slides_html.append(build_cierre(content["cierre"]))
    return slides_html


def capture_slides(slides_html: list, output_dir: Path) -> list:
    output_dir.mkdir(parents=True, exist_ok=True)
    paths = []

    with sync_playwright() as p:
        browser = p.chromium.launch(
            executable_path=CHROMIUM_PATH,
            args=["--no-sandbox", "--disable-dev-shm-usage", "--font-render-hinting=none"]
        )
        page = browser.new_page(viewport={"width": 1080, "height": 1350})

        for i, html in enumerate(slides_html, 1):
            page.set_content(html, wait_until="networkidle")
            out_path = output_dir / f"slide_{i:02d}.jpg"
            page.screenshot(
                path=str(out_path),
                type="jpeg",
                quality=95,
                full_page=False,
                clip={"x": 0, "y": 0, "width": 1080, "height": 1350}
            )
            paths.append(out_path)
            print(f"  ✓ Slide {i}/6 → {out_path.name}")

        browser.close()

    return paths


def slugify(text: str) -> str:
    text = text.lower()
    for src, dst in [('á','a'),('à','a'),('ä','a'),('é','e'),('è','e'),('ë','e'),
                     ('í','i'),('ì','i'),('ï','i'),('ó','o'),('ò','o'),('ö','o'),
                     ('ú','u'),('ù','u'),('ü','u'),('ñ','n')]:
        text = text.replace(src, dst)
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')[:50]


def main():
    parser = argparse.ArgumentParser(description="Generador de carruseles Vuelta Rápida Club")
    parser.add_argument("tema", help="Tema del carrusel (ej: 'GP de Mónaco 2025')")
    parser.add_argument("--out", default="./carruseles", help="Carpeta de salida")
    args = parser.parse_args()

    print(f"\n Generando carrusel: \"{args.tema}\"")
    print("\n Consultando a Claude para generar el contenido...")

    try:
        content = generate_content(args.tema)
    except json.JSONDecodeError as e:
        print(f"Error al parsear la respuesta de Claude: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error al consultar Claude API: {e}")
        sys.exit(1)

    portada_titulo = content.get("portada", {}).get("titulo", args.tema)
    print(f" Contenido generado: {portada_titulo}")

    print("\n Renderizando slides...")
    slides_html = render_slides(content)

    slug = slugify(args.tema)
    output_dir = Path(args.out) / slug
    paths = capture_slides(slides_html, output_dir)

    print(f"\n Listo. {len(paths)} slides en: {output_dir}/")
    print("\nArchivos:")
    for p in paths:
        size_kb = p.stat().st_size // 1024
        print(f"  {p.name}  ({size_kb} KB)")


if __name__ == "__main__":
    main()
