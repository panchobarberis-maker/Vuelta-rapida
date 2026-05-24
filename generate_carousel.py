#!/usr/bin/env python3
"""
Generador de carruseles de Instagram para Vuelta Rápida Club.

Uso:
  python3 generate_carousel.py "GP de Mónaco 2025"
  python3 generate_carousel.py "Horarios GP España 2025" --tipo horarios
  python3 generate_carousel.py "Lego McLaren MP4/4" --tipo producto

Output: carpeta ./preview/<tema>/ con JPG para revisión.
        Después de aprobado → ./carruseles vuelta rapida club/<tema>/
"""

import sys
import os
import re
import json
import base64
import argparse
from pathlib import Path

import anthropic
from playwright.sync_api import sync_playwright

CHROMIUM_PATH = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
LOGO_PATH = Path(__file__).parent / "PNG EN ROJO.png"


def logo_b64() -> str:
    with open(LOGO_PATH, "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode()


# ─── shared assets ───────────────────────────────────────────────────────────

FONTS = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:ital,wght@0,400;0,600;0,700;0,800;0,900;1,600;1,700;1,800;1,900&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">
"""

BASE_CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
:root {
  --bg:     #0A0A0A;
  --red:    #E8002D;
  --white:  #FFFFFF;
  --muted:  rgba(255,255,255,0.60);
  --box-bg: rgba(255,255,255,0.06);
  --box-bd: rgba(255,255,255,0.13);
}
html, body {
  width: 1080px; height: 1350px; overflow: hidden;
  background: var(--bg); color: var(--white);
  font-family: 'DM Sans', sans-serif;
}
.slide { width: 1080px; height: 1350px; position: relative; overflow: hidden; }

/* Speed-lines background layer */
.spd {
  position: absolute; inset: 0; z-index: 0;
  background:
    radial-gradient(ellipse 65% 55% at 88% 35%, rgba(232,0,45,.20) 0%, transparent 55%),
    radial-gradient(ellipse 45% 40% at 10% 80%, rgba(232,0,45,.10) 0%, transparent 50%),
    repeating-linear-gradient(
      -22deg,
      transparent 0px,   transparent 78px,
      rgba(232,0,45,.045) 78px, rgba(232,0,45,.045) 80px
    );
}

/* Logo block — top-left */
.logo-wrap {
  position: absolute; top: 40px; left: 52px; z-index: 10;
  display: flex; align-items: center; gap: 14px;
}
.logo-img  { width: 62px; height: 62px; object-fit: contain; }
.logo-text { display: flex; flex-direction: column; line-height: 1; }
.logo-top  {
  font-family: 'Barlow Condensed', sans-serif; font-weight: 800;
  font-size: 23px; letter-spacing: 3px; color: var(--white);
}
.logo-bot  {
  font-family: 'Barlow Condensed', sans-serif; font-weight: 600;
  font-size: 14px; letter-spacing: 6px; color: var(--red); margin-top: 3px;
}

/* Slide number pill — top-right */
.num-pill {
  position: absolute; top: 46px; right: 52px; z-index: 10;
  background: rgba(255,255,255,.11); border-radius: 40px;
  padding: 8px 24px;
  font-family: 'Barlow Condensed', sans-serif; font-weight: 600;
  font-size: 18px; letter-spacing: 3px; color: var(--muted);
}

/* III decorative bars before section titles */
.bars { display: flex; gap: 7px; margin-bottom: 12px; }
.bars span { display: block; width: 9px; height: 52px; background: var(--red); border-radius: 3px; }

/* Bottom accent stripe */
.bot-stripe {
  position: absolute; bottom: 0; left: 0; right: 0; height: 6px; z-index: 5;
  background: var(--red);
}
"""


def logo_tag(logo_src: str) -> str:
    return f"""<div class="logo-wrap">
  <img class="logo-img" src="{logo_src}">
  <div class="logo-text">
    <span class="logo-top">VUELTA RÁPIDA</span>
    <span class="logo-bot">CLUB</span>
  </div>
</div>"""


def num_tag(n: int, total: int) -> str:
    return f'<div class="num-pill">{n} / {total}</div>'


# ─── slide builders ───────────────────────────────────────────────────────────

def build_portada(data: dict, logo_src: str) -> str:
    titulo    = data.get("titulo", "")
    subtitulo = data.get("subtitulo", "")
    tag       = data.get("tag", "F1")

    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8">{FONTS}<style>{BASE_CSS}
.portada {{
  background: var(--bg);
  display: flex; flex-direction: column;
  align-items: flex-start; justify-content: flex-end;
  padding: 0 72px 120px;
}}
.tag-pill {{
  display: inline-block; margin-bottom: 32px;
  font-family: 'Barlow Condensed', sans-serif; font-weight: 600;
  font-size: 18px; letter-spacing: 5px; text-transform: uppercase;
  color: var(--red); border: 2px solid var(--red);
  padding: 10px 30px; border-radius: 6px;
}}
.titulo {{
  font-family: 'Barlow Condensed', sans-serif; font-weight: 900;
  font-style: italic; font-size: 148px; line-height: .86;
  color: var(--white); margin-bottom: 36px; text-transform: uppercase;
}}
.titulo em {{ color: var(--red); font-style: italic; }}
.subtitulo {{
  font-size: 30px; color: var(--muted); line-height: 1.55; max-width: 820px;
}}
.sep {{
  display: flex; align-items: center; gap: 24px; margin-top: 52px;
}}
.sep-line {{ width: 52px; height: 2px; background: var(--red); }}
.sep-text {{
  font-family: 'Barlow Condensed', sans-serif; font-weight: 600;
  font-size: 16px; letter-spacing: 5px; text-transform: uppercase; color: var(--muted);
}}
</style></head><body>
<div class="slide portada">
  <div class="spd"></div>
  <div class="bot-stripe"></div>
  {logo_tag(logo_src)}
  <div style="position:relative;z-index:2;">
    <div class="tag-pill">{tag}</div>
    <h1 class="titulo">{titulo}</h1>
    <p class="subtitulo">{subtitulo}</p>
    <div class="sep">
      <div class="sep-line"></div>
      <span class="sep-text">vueltarapidaclub</span>
      <div class="sep-line"></div>
    </div>
  </div>
</div>
</body></html>"""


def build_contenido(data: dict, num: int, total: int, logo_src: str) -> str:
    titulo = data.get("titulo", "")
    label  = data.get("label", "")
    intro  = data.get("intro", "")
    items  = data.get("items", [])

    items_html = ""
    for it in items[:5]:
        t = it.get("titulo", "") if isinstance(it, dict) else str(it)
        d = it.get("desc", "")  if isinstance(it, dict) else ""
        items_html += f"""<div class="item">
          <div class="item-dot"></div>
          <div class="item-body">
            <span class="item-t">{t}</span>
            {f'<span class="item-d">{d}</span>' if d else ""}
          </div>
        </div>"""

    label_html = f'<span class="label">{label}</span>' if label else ""
    intro_html = f'<p class="intro">{intro}</p>' if intro else ""

    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8">{FONTS}<style>{BASE_CSS}
.body {{
  position: relative; z-index: 2;
  display: flex; flex-direction: column;
  justify-content: center; height: 100%;
  padding: 160px 72px 80px;
}}
.label {{
  font-family: 'Barlow Condensed', sans-serif; font-weight: 700;
  font-size: 16px; letter-spacing: 6px; text-transform: uppercase;
  color: var(--red); display: block; margin-bottom: 10px;
}}
.titulo {{
  font-family: 'Barlow Condensed', sans-serif; font-weight: 900;
  font-style: italic; font-size: 96px; line-height: .88;
  color: var(--white); text-transform: uppercase; margin-bottom: 40px;
}}
.titulo em {{ color: var(--red); font-style: italic; }}
.intro {{ font-size: 26px; color: var(--muted); line-height: 1.55; margin-bottom: 40px; max-width: 860px; }}
.item {{
  display: flex; align-items: flex-start; gap: 22px; margin-bottom: 26px;
  background: var(--box-bg); border: 1px solid var(--box-bd);
  border-left: 4px solid var(--red); border-radius: 8px;
  padding: 20px 28px;
}}
.item-dot {{
  width: 12px; height: 12px; border-radius: 50%;
  background: var(--red); flex-shrink: 0; margin-top: 8px;
}}
.item-body {{ display: flex; flex-direction: column; gap: 4px; }}
.item-t {{ font-family: 'Barlow Condensed', sans-serif; font-weight: 700; font-size: 30px; line-height: 1.2; }}
.item-d {{ font-size: 22px; color: var(--muted); line-height: 1.5; }}
</style></head><body>
<div class="slide">
  <div class="spd"></div>
  <div class="bot-stripe"></div>
  {logo_tag(logo_src)}
  {num_tag(num, total)}
  <div class="body">
    {label_html}
    <div class="bars"><span></span><span></span><span></span></div>
    <h2 class="titulo">{titulo}</h2>
    {intro_html}
    {items_html}
  </div>
</div>
</body></html>"""


def build_horarios(data: dict, num: int, total: int, logo_src: str) -> str:
    titulo   = data.get("titulo", "")
    sesiones = data.get("sesiones", [])
    nota     = data.get("nota", "")

    rows_html = ""
    for s in sesiones:
        hora    = s.get("hora", "")
        sesion  = s.get("sesion", "")
        dia     = s.get("dia", "")
        dia_html = f'<span class="row-day">{dia}</span>' if dia else ""
        rows_html += f"""<div class="hor-row">
          <div class="hor-time">{hora}</div>
          <div class="hor-right">
            {dia_html}
            <span class="hor-name">{sesion}</span>
          </div>
        </div>"""

    nota_html = f'<p class="nota"><span style="color:var(--red)">⚠</span> {nota}</p>' if nota else ""

    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8">{FONTS}<style>{BASE_CSS}
.body {{
  position: relative; z-index: 2;
  display: flex; flex-direction: column;
  justify-content: center; height: 100%;
  padding: 155px 72px 80px;
}}
.titulo {{
  font-family: 'Barlow Condensed', sans-serif; font-weight: 900;
  font-style: italic; font-size: 112px; line-height: .86;
  text-transform: uppercase; color: var(--white); margin-bottom: 48px;
}}
.titulo em {{ color: var(--red); font-style: italic; }}
.hor-row {{
  display: flex; align-items: center; gap: 0;
  margin-bottom: 16px;
}}
.hor-time {{
  background: var(--red); color: var(--white);
  font-family: 'Barlow Condensed', sans-serif; font-weight: 800;
  font-size: 28px; letter-spacing: 1px;
  padding: 14px 24px; border-radius: 8px 0 0 8px;
  min-width: 190px; text-align: center; flex-shrink: 0;
}}
.hor-right {{
  flex: 1; background: var(--box-bg); border: 1px solid var(--box-bd);
  border-left: none; border-radius: 0 8px 8px 0;
  padding: 12px 24px; display: flex; flex-direction: column;
}}
.row-day {{
  font-size: 15px; letter-spacing: 3px; text-transform: uppercase;
  color: var(--red); font-weight: 500; margin-bottom: 3px;
}}
.hor-name {{
  font-family: 'Barlow Condensed', sans-serif; font-weight: 700;
  font-size: 26px; text-transform: uppercase; line-height: 1.2;
}}
.nota {{ font-size: 20px; color: var(--muted); margin-top: 24px; line-height: 1.5; }}
</style></head><body>
<div class="slide">
  <div class="spd"></div>
  <div class="bot-stripe"></div>
  {logo_tag(logo_src)}
  {num_tag(num, total)}
  <div class="body">
    <div class="bars"><span></span><span></span><span></span></div>
    <h2 class="titulo">{titulo}</h2>
    {rows_html}
    {nota_html}
  </div>
</div>
</body></html>"""


def build_dato(data: dict, num: int, total: int, logo_src: str) -> str:
    stat        = data.get("stat", "")
    unidad      = data.get("unidad", "")
    titulo      = data.get("titulo", "")
    descripcion = data.get("descripcion", "")
    contexto    = data.get("contexto", [])

    ctx_html = ""
    for c in contexto[:3]:
        ctx_html += f'<div class="ctx-item"><span class="arr">→</span><span>{c}</span></div>'

    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8">{FONTS}<style>{BASE_CSS}
.body {{
  position: relative; z-index: 2;
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  height: 100%; text-align: center; padding: 80px;
}}
.big {{
  font-family: 'Barlow Condensed', sans-serif; font-weight: 900;
  font-style: italic; font-size: 260px; line-height: .80;
  color: var(--red); letter-spacing: -4px;
}}
.unidad {{
  font-family: 'Barlow Condensed', sans-serif; font-weight: 800;
  font-size: 72px; color: var(--white); letter-spacing: 4px;
  text-transform: uppercase; display: block; margin-bottom: 20px;
}}
.titulo {{
  font-family: 'Barlow Condensed', sans-serif; font-weight: 800;
  font-style: italic; font-size: 58px; line-height: 1.05;
  text-transform: uppercase; margin-bottom: 18px; max-width: 780px;
}}
.desc {{ font-size: 26px; color: var(--muted); line-height: 1.55; max-width: 740px; margin-bottom: 40px; }}
.ctx-list {{ display: flex; flex-direction: column; gap: 14px; max-width: 720px; text-align: left; }}
.ctx-item {{ display: flex; align-items: flex-start; gap: 16px; font-size: 24px; color: var(--muted); }}
.arr {{ color: var(--red); flex-shrink: 0; font-weight: 700; }}
</style></head><body>
<div class="slide">
  <div class="spd"></div>
  <div class="bot-stripe"></div>
  {logo_tag(logo_src)}
  {num_tag(num, total)}
  <div class="body">
    <span class="big">{stat}</span>
    {f'<span class="unidad">{unidad}</span>' if unidad else ''}
    <h2 class="titulo">{titulo}</h2>
    {f'<p class="desc">{descripcion}</p>' if descripcion else ''}
    {f'<div class="ctx-list">{ctx_html}</div>' if ctx_html else ''}
  </div>
</div>
</body></html>"""


def build_cierre(data: dict, logo_src: str, total: int) -> str:
    pregunta = data.get("pregunta", "¿Cuál es tu opinión?")
    subtitulo = data.get("subtitulo", "Comentá abajo ↓ Seguinos para más F1")
    hashtags  = data.get("hashtags", "#F1 #VueltaRapida #Formula1")

    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8">{FONTS}<style>{BASE_CSS}
.body {{
  position: relative; z-index: 2;
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  height: 100%; text-align: center; padding: 80px;
}}
.logo-big {{
  display: flex; flex-direction: column; align-items: center;
  gap: 16px; margin-bottom: 80px;
}}
.logo-big img {{ width: 100px; height: 100px; object-fit: contain; }}
.lb-top {{
  font-family: 'Barlow Condensed', sans-serif; font-weight: 800;
  font-size: 42px; letter-spacing: 5px; color: var(--white);
}}
.lb-bot {{
  font-family: 'Barlow Condensed', sans-serif; font-weight: 600;
  font-size: 20px; letter-spacing: 8px; color: var(--red);
}}
.pregunta {{
  font-family: 'Barlow Condensed', sans-serif; font-weight: 900;
  font-style: italic; font-size: 96px; line-height: .90;
  text-transform: uppercase; color: var(--white); margin-bottom: 36px;
}}
.pregunta em {{ color: var(--red); font-style: italic; }}
.sub {{ font-size: 28px; color: var(--muted); line-height: 1.55; max-width: 760px; margin-bottom: 40px; }}
.tags {{ font-size: 22px; color: var(--red); letter-spacing: 1px; }}
</style></head><body>
<div class="slide">
  <div class="spd"></div>
  <div class="bot-stripe"></div>
  {num_tag(total, total)}
  <div class="body">
    <div class="logo-big">
      <img src="{logo_src}">
      <span class="lb-top">VUELTA RÁPIDA</span>
      <span class="lb-bot">CLUB</span>
    </div>
    <h2 class="pregunta">{pregunta}</h2>
    <p class="sub">{subtitulo}</p>
    <p class="tags">{hashtags}</p>
  </div>
</div>
</body></html>"""


# ─── Claude content generation ────────────────────────────────────────────────

SYSTEM_PROMPT = """Sos un experto en contenido de Fórmula 1 para redes sociales en español rioplatense.
Generás contenido para carruseles de Instagram de Vuelta Rápida Club: comunidad de F1 + tienda de merch y productos de colección (ej: sets LEGO de F1).

Tonos según tipo:
- noticias/info F1: apasionado, directo, como un fan experto que comparte data con amigos. Voseo.
- horarios: informativo y claro, preciso.
- producto/oferta: entusiasta, destacando el valor y la rareza del producto.

Solo datos reales y verificados de F1.
Devolvés ÚNICAMENTE JSON válido. Sin texto extra, sin markdown, sin bloques de código.
"""

SCHEMAS = {

"info": """
{
  "portada": {
    "titulo": "TÍTULO IMPACTANTE (máx 4 palabras, mayúsculas, puede tener salto con \\n)",
    "subtitulo": "Bajada que amplía el título. 1 oración, 15-20 palabras.",
    "tag": "Categoría (ej: Temporada 2025, Traspasos, Record Histórico)"
  },
  "slides": [
    {
      "tipo": "contenido",
      "label": "ETIQUETA DE SECCIÓN (2-3 palabras, mayúsculas)",
      "titulo": "TÍTULO DEL SLIDE (3-5 palabras, itálica bold)",
      "intro": "Oración introductoria opcional (máx 18 palabras)",
      "items": [
        {"titulo": "Punto clave", "desc": "Descripción en 1-2 oraciones (máx 22 palabras)"},
        {"titulo": "Punto clave", "desc": "Descripción en 1-2 oraciones"},
        {"titulo": "Punto clave", "desc": "Descripción en 1-2 oraciones"},
        {"titulo": "Punto clave", "desc": "Descripción en 1-2 oraciones"}
      ]
    },
    {
      "tipo": "dato",
      "stat": "número impactante (solo dígitos, ej: 7)",
      "unidad": "unidad (ej: poles, victorias, años) o cadena vacía",
      "titulo": "QUÉ ES ESE NÚMERO (3-5 palabras mayúsculas)",
      "descripcion": "Contexto del dato (1-2 oraciones, máx 25 palabras)",
      "contexto": ["dato extra 1", "dato extra 2", "dato extra 3"]
    },
    {
      "tipo": "contenido",
      "label": "ETIQUETA",
      "titulo": "TÍTULO SLIDE 4",
      "intro": "",
      "items": [
        {"titulo": "Punto", "desc": "Desc"},
        {"titulo": "Punto", "desc": "Desc"},
        {"titulo": "Punto", "desc": "Desc"},
        {"titulo": "Punto", "desc": "Desc"}
      ]
    },
    {
      "tipo": "contenido",
      "label": "ETIQUETA",
      "titulo": "TÍTULO SLIDE 5",
      "intro": "",
      "items": [
        {"titulo": "Punto", "desc": "Desc"},
        {"titulo": "Punto", "desc": "Desc"},
        {"titulo": "Punto", "desc": "Desc"},
        {"titulo": "Punto", "desc": "Desc"}
      ]
    }
  ],
  "cierre": {
    "pregunta": "PREGUNTA DE ENGAGEMENT (4-7 palabras, que incite a comentar)",
    "subtitulo": "Invitación a comentar y seguir. 1 oración, máx 12 palabras.",
    "hashtags": "#F1 #VueltaRapida #Formula1 [2 hashtags del tema]"
  }
}
""",

"horarios": """
{
  "portada": {
    "titulo": "TÍTULO DEL GP (ej: GP MÓNACO 2025, puede tener \\n entre palabras)",
    "subtitulo": "Descripción breve del evento y fechas. 1 oración.",
    "tag": "Nombre del circuito o ciudad"
  },
  "sesiones": [
    {"dia": "VIERNES 23 MAYO", "hora": "12:30 HS", "sesion": "PRÁCTICA 1"},
    {"dia": "VIERNES 23 MAYO", "hora": "16:00 HS", "sesion": "PRÁCTICA 2"},
    {"dia": "SÁBADO 24 MAYO",  "hora": "11:30 HS", "sesion": "PRÁCTICA 3"},
    {"dia": "SÁBADO 24 MAYO",  "hora": "15:00 HS", "sesion": "CLASIFICACIÓN"},
    {"dia": "DOMINGO 25 MAYO", "hora": "15:00 HS", "sesion": "CARRERA"}
  ],
  "nota": "Horarios en hora Argentina (ART, UTC-3). Pueden sufrir cambios.",
  "cierre": {
    "pregunta": "¿VAS A VER LA CARRERA?",
    "subtitulo": "Comentá tu predicción abajo. Seguinos para más F1.",
    "hashtags": "#F1 #VueltaRapida #Formula1 [hashtag del GP]"
  }
}
""",

"producto": """
{
  "portada": {
    "titulo": "NOMBRE DEL PRODUCTO (máx 4 palabras, mayúsculas, puede tener \\n)",
    "subtitulo": "Descripción tentadora en 1 oración (15-20 palabras).",
    "tag": "Categoría (ej: LEGO F1, Colección, Oferta)"
  },
  "slides": [
    {
      "tipo": "contenido",
      "label": "QUÉ INCLUYE",
      "titulo": "LO QUE VAS\\nA ARMAR",
      "intro": "",
      "items": [
        {"titulo": "Característica 1", "desc": "Detalle del producto"},
        {"titulo": "Característica 2", "desc": "Detalle del producto"},
        {"titulo": "Característica 3", "desc": "Detalle del producto"},
        {"titulo": "Característica 4", "desc": "Detalle del producto"}
      ]
    },
    {
      "tipo": "dato",
      "stat": "número relevante del producto (piezas, año, escala, etc.)",
      "unidad": "unidad (ej: piezas, cm, 1:8)",
      "titulo": "DATO CLAVE DEL PRODUCTO",
      "descripcion": "Por qué ese número importa o qué representa.",
      "contexto": ["dato coleccionable 1", "dato coleccionable 2", "dato histórico del auto/piloto"]
    },
    {
      "tipo": "contenido",
      "label": "POR QUÉ LO QUERÉS",
      "titulo": "EL AUTO\\nQUE MARCÓ\\nLA HISTORIA",
      "intro": "",
      "items": [
        {"titulo": "Razón 1", "desc": "Por qué es especial"},
        {"titulo": "Razón 2", "desc": "Por qué es especial"},
        {"titulo": "Razón 3", "desc": "Por qué es especial"},
        {"titulo": "Razón 4", "desc": "Por qué es especial"}
      ]
    },
    {
      "tipo": "contenido",
      "label": "FICHA TÉCNICA",
      "titulo": "ESPECIFICACIONES",
      "intro": "",
      "items": [
        {"titulo": "Spec 1", "desc": "Valor"},
        {"titulo": "Spec 2", "desc": "Valor"},
        {"titulo": "Spec 3", "desc": "Valor"},
        {"titulo": "Spec 4", "desc": "Valor"}
      ]
    }
  ],
  "cierre": {
    "pregunta": "¿LO AGREGAS\\nA TU COLECCIÓN?",
    "subtitulo": "Escribinos por DM para precio y disponibilidad.",
    "hashtags": "#LEGO #F1 #VueltaRapida [hashtag del auto/equipo]"
  }
}
"""
}


def generate_content(tema: str, tipo: str) -> dict:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("Falta ANTHROPIC_API_KEY en las variables de entorno.")

    client = anthropic.Anthropic(api_key=api_key)
    schema = SCHEMAS.get(tipo, SCHEMAS["info"])

    if tipo == "horarios":
        prompt = f"""Generá el contenido para un carrusel de horarios de Instagram sobre: "{tema}".

El carrusel tiene:
- Slide 1: Portada con título del GP, subtítulo y tag del circuito
- Slides 2-N: Una slide de horarios por día (viernes / sábado / domingo)
- Último slide: Cierre con pregunta de engagement

Devolvé el JSON con esta estructura exacta:
{schema}

IMPORTANTE:
- Los horarios son en hora Argentina (ART, UTC-3). Si no tenés los horarios exactos, calculalos desde UTC.
- Solo JSON válido, sin ningún texto extra."""

    elif tipo == "producto":
        prompt = f"""Generá el contenido para un carrusel de producto de Instagram sobre: "{tema}".

El carrusel tiene 6 slides: portada + 4 content slides + cierre.

Devolvé el JSON con esta estructura exacta:
{schema}

IMPORTANTE:
- Usá datos reales del producto si es un set LEGO conocido o un producto oficial de F1.
- Tono entusiasta y cercano.
- Solo JSON válido, sin ningún texto extra."""

    else:
        prompt = f"""Generá el contenido para un carrusel de F1 para Instagram sobre: "{tema}".

El carrusel tiene 6 slides: portada + 4 content/dato slides + cierre.

Devolvé el JSON con esta estructura exacta:
{schema}

IMPORTANTE:
- Usá datos reales y verificados de F1.
- Tono apasionado, voseo argentino.
- Solo JSON válido, sin ningún texto extra."""

    msg = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=2048,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = msg.content[0].text.strip()
    raw = re.sub(r'^```(?:json)?\s*', '', raw)
    raw = re.sub(r'\s*```$', '', raw)
    return json.loads(raw)


# ─── slide rendering ──────────────────────────────────────────────────────────

def render_slides(content: dict, tipo: str, logo_src: str) -> list:
    slides = []

    if tipo == "horarios":
        portada = content["portada"]
        slides.append(build_portada(portada, logo_src))

        # Group sessions by day
        sesiones = content.get("sesiones", [])
        nota     = content.get("nota", "")
        days = {}
        for s in sesiones:
            d = s.get("dia", "")
            days.setdefault(d, []).append(s)

        slide_n = 2
        total   = 2 + len(days) + 1
        for dia, slist in days.items():
            slides.append(build_horarios(
                {"titulo": dia, "sesiones": slist, "nota": nota if slide_n == total - 1 else ""},
                slide_n, total, logo_src
            ))
            slide_n += 1

        slides.append(build_cierre(content["cierre"], logo_src, total))

    else:
        total = 6
        slides.append(build_portada(content["portada"], logo_src))

        slide_n = 2
        for sd in content.get("slides", []):
            if sd.get("tipo") == "dato":
                slides.append(build_dato(sd, slide_n, total, logo_src))
            else:
                slides.append(build_contenido(sd, slide_n, total, logo_src))
            slide_n += 1

        slides.append(build_cierre(content["cierre"], logo_src, total))

    return slides


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
            out = output_dir / f"slide_{i:02d}.jpg"
            page.screenshot(
                path=str(out), type="jpeg", quality=95, full_page=False,
                clip={"x": 0, "y": 0, "width": 1080, "height": 1350}
            )
            paths.append(out)
            print(f"  ✓ Slide {i}/{len(slides_html)} → {out.name}")

        browser.close()

    return paths


def slugify(text: str) -> str:
    text = text.lower()
    for s, d in [('á','a'),('é','e'),('í','i'),('ó','o'),('ú','u'),('ü','u'),('ñ','n')]:
        text = text.replace(s, d)
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')[:50]


# ─── main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Generador de carruseles Vuelta Rápida Club")
    parser.add_argument("tema",  help="Tema del carrusel")
    parser.add_argument("--tipo", default="info",
                        choices=["info", "horarios", "producto"],
                        help="Tipo de carrusel (default: info)")
    parser.add_argument("--out",  default="./preview",
                        help="Carpeta de salida para preview (default: ./preview)")
    args = parser.parse_args()

    print(f"\n Generando carrusel [{args.tipo}]: \"{args.tema}\"")
    print(" Cargando logo...")
    logo_src = logo_b64()

    print(" Consultando a Claude para generar el contenido...")
    try:
        content = generate_content(args.tema, args.tipo)
    except json.JSONDecodeError as e:
        print(f"Error al parsear respuesta de Claude: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error al consultar Claude API: {e}")
        sys.exit(1)

    titulo = content.get("portada", {}).get("titulo", args.tema)
    print(f" Contenido listo → {titulo}")

    print("\n Renderizando slides...")
    slides_html = render_slides(content, args.tipo, logo_src)

    slug = slugify(args.tema)
    output_dir = Path(args.out) / slug
    paths = capture_slides(slides_html, output_dir)

    print(f"\n Preview listo en: {output_dir}/")
    print(" Archivos:")
    for p in paths:
        print(f"   {p.name}  ({p.stat().st_size // 1024} KB)")
    print(f"\n Revisá los slides y si están ok, movelos a:")
    print(f"   ./carruseles vuelta rapida club/{slug}/")


if __name__ == "__main__":
    main()
