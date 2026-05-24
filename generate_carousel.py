#!/usr/bin/env python3
"""
Generador de carruseles de Instagram para Vuelta Rápida Club.

Uso:
  python3 generate_carousel.py "GP de Mónaco 2025"
  python3 generate_carousel.py "Horarios GP España 2025" --tipo horarios
  python3 generate_carousel.py "Lego McLaren MP4/4" --tipo producto

Output: carpeta ./preview/<tema>/ con JPG para revisión.
        Después de aprobado → ./carruseles vuelta rapida club/<tema>/

IMPORTANTE: No inventar información. Solo datos confirmados.
"""

import sys
import os
import re
import json
import base64
import argparse
import random
from pathlib import Path

import anthropic
from playwright.sync_api import sync_playwright

_LOCAL_CHROMIUM = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
CHROMIUM_PATH   = _LOCAL_CHROMIUM if Path(_LOCAL_CHROMIUM).exists() else None
REPO_ROOT     = Path(__file__).parent
LOGO_PATH     = REPO_ROOT / "PNG EN ROJO.png"

# Extensiones de imagen aceptadas como fondos
BG_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
# Archivos que NO son fondos de carrusel (referencias de diseño, etc.)
BG_EXCLUDE = {
    "PNG EN ROJO.png",
    "WhatsApp Image 2026-05-24 at 19.26.57.jpeg",
    "WhatsApp Image 2026-05-24 at 19.26.58.jpeg",
    "WhatsApp Image 2026-05-24 at 19.26.58 (1).jpeg",
    "WhatsApp Image 2026-05-24 at 19.26.59.jpeg",
    "WhatsApp Image 2026-05-24 at 19.26.59 (1).jpeg",
    "refe.jpg",
}


def file_b64(path: Path) -> str:
    ext = path.suffix.lower().lstrip(".")
    mime = "jpeg" if ext in ("jpg", "jpeg") else ext
    with open(path, "rb") as f:
        return f"data:image/{mime};base64," + base64.b64encode(f.read()).decode()


def logo_b64() -> str:
    return file_b64(LOGO_PATH)


def load_bg_images() -> list:
    """Carga todas las fotos de fondo del repo raíz (no las referencias de diseño)."""
    imgs = []
    for p in sorted(REPO_ROOT.iterdir()):
        if p.suffix.lower() in BG_EXTENSIONS and p.name not in BG_EXCLUDE:
            try:
                imgs.append(file_b64(p))
            except Exception:
                pass
    return imgs


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

/* Foto de fondo con baja opacidad */
.bg-photo {
  position: absolute; inset: 0; z-index: 1;
  background-size: cover; background-position: center top;
  opacity: 0.18;
}
/* Overlay oscuro encima de la foto */
.bg-overlay {
  position: absolute; inset: 0; z-index: 2;
  background:
    linear-gradient(170deg, rgba(10,10,10,.55) 0%, rgba(10,10,10,.30) 50%, rgba(10,10,10,.75) 100%),
    radial-gradient(ellipse 65% 55% at 88% 35%, rgba(232,0,45,.18) 0%, transparent 55%),
    repeating-linear-gradient(
      -22deg, transparent 0px, transparent 78px,
      rgba(232,0,45,.04) 78px, rgba(232,0,45,.04) 80px
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


def bg_tag(bg_url: str) -> str:
    if not bg_url:
        return ""
    return f'<div class="bg-photo" style="background-image:url(\'{bg_url}\')"></div><div class="bg-overlay"></div>'


# ─── slide builders ───────────────────────────────────────────────────────────

def build_portada(data: dict, logo_src: str, bg_url: str = "") -> str:
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
/* En la portada la foto se ve un poco más para más impacto */
.portada .bg-photo {{ opacity: 0.28; background-position: center 20%; }}
.portada .bg-overlay {{
  background:
    linear-gradient(170deg, rgba(10,10,10,.30) 0%, rgba(10,10,10,.10) 40%, rgba(10,10,10,.85) 80%),
    radial-gradient(ellipse 60% 50% at 85% 30%, rgba(232,0,45,.20) 0%, transparent 55%),
    repeating-linear-gradient(-22deg, transparent 0px, transparent 78px, rgba(232,0,45,.04) 78px, rgba(232,0,45,.04) 80px);
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
.subtitulo {{ font-size: 30px; color: var(--muted); line-height: 1.55; max-width: 820px; }}
.sep {{ display: flex; align-items: center; gap: 24px; margin-top: 52px; }}
.sep-line {{ width: 52px; height: 2px; background: var(--red); }}
.sep-text {{
  font-family: 'Barlow Condensed', sans-serif; font-weight: 600;
  font-size: 16px; letter-spacing: 5px; text-transform: uppercase; color: var(--muted);
}}
</style></head><body>
<div class="slide portada">
  {bg_tag(bg_url)}
  <div class="bot-stripe"></div>
  {logo_tag(logo_src)}
  <div style="position:relative;z-index:3;">
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


def build_contenido(data: dict, num: int, total: int, logo_src: str, bg_url: str = "") -> str:
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
  position: relative; z-index: 3;
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
  display: flex; align-items: flex-start; gap: 22px; margin-bottom: 22px;
  background: rgba(10,10,10,.65); border: 1px solid var(--box-bd);
  border-left: 4px solid var(--red); border-radius: 8px;
  padding: 18px 26px; backdrop-filter: blur(4px);
}}
.item-dot {{
  width: 12px; height: 12px; border-radius: 50%;
  background: var(--red); flex-shrink: 0; margin-top: 9px;
}}
.item-body {{ display: flex; flex-direction: column; gap: 4px; }}
.item-t {{ font-family: 'Barlow Condensed', sans-serif; font-weight: 700; font-size: 30px; line-height: 1.2; }}
.item-d {{ font-size: 22px; color: var(--muted); line-height: 1.5; }}
</style></head><body>
<div class="slide">
  {bg_tag(bg_url)}
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


def build_horarios(data: dict, num: int, total: int, logo_src: str, bg_url: str = "") -> str:
    titulo   = data.get("titulo", "")
    sesiones = data.get("sesiones", [])
    nota     = data.get("nota", "")

    rows_html = ""
    for s in sesiones:
        hora   = s.get("hora", "")
        sesion = s.get("sesion", "")
        dia    = s.get("dia", "")
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
  position: relative; z-index: 3;
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
.hor-row {{ display: flex; align-items: center; gap: 0; margin-bottom: 16px; }}
.hor-time {{
  background: var(--red); color: var(--white);
  font-family: 'Barlow Condensed', sans-serif; font-weight: 800;
  font-size: 28px; letter-spacing: 1px;
  padding: 14px 24px; border-radius: 8px 0 0 8px;
  min-width: 190px; text-align: center; flex-shrink: 0;
}}
.hor-right {{
  flex: 1; background: rgba(10,10,10,.65); border: 1px solid var(--box-bd);
  border-left: none; border-radius: 0 8px 8px 0;
  padding: 12px 24px; display: flex; flex-direction: column;
  backdrop-filter: blur(4px);
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
  {bg_tag(bg_url)}
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


def build_dato(data: dict, num: int, total: int, logo_src: str, bg_url: str = "") -> str:
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
  position: relative; z-index: 3;
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
.ctx-item {{
  display: flex; align-items: flex-start; gap: 16px; font-size: 24px; color: var(--muted);
  background: rgba(10,10,10,.65); border: 1px solid var(--box-bd);
  border-left: 3px solid var(--red); border-radius: 8px;
  padding: 14px 20px; backdrop-filter: blur(4px);
}}
.arr {{ color: var(--red); flex-shrink: 0; font-weight: 700; }}
</style></head><body>
<div class="slide">
  {bg_tag(bg_url)}
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


def build_cierre(data: dict, logo_src: str, total: int, bg_url: str = "") -> str:
    pregunta  = data.get("pregunta", "¿Cuál es tu opinión?")
    subtitulo = data.get("subtitulo", "Comentá abajo ↓ Seguinos para más F1")
    hashtags  = data.get("hashtags", "#F1 #VueltaRapida #Formula1")

    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8">{FONTS}<style>{BASE_CSS}
/* En el cierre la foto se ve un poco más */
.bg-photo {{ opacity: 0.22; background-position: center 15%; }}
.body {{
  position: relative; z-index: 3;
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  height: 100%; text-align: center; padding: 80px;
}}
.logo-big {{
  display: flex; flex-direction: column; align-items: center;
  gap: 14px; margin-bottom: 72px;
}}
.logo-big img {{ width: 96px; height: 96px; object-fit: contain; }}
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
  {bg_tag(bg_url)}
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

SYSTEM_PROMPT = """Sos experto en contenido de Fórmula 1 para Instagram en español rioplatense.
Generás carruseles para Vuelta Rápida Club: comunidad de F1 + tienda de merch (LEGO, colecciones).

REGLA FUNDAMENTAL: NUNCA INVENTAR INFORMACIÓN.
- Solo usá datos que el usuario confirme o que sean hechos públicos verificados de F1.
- Si no tenés certeza de un dato, no lo incluyas.
- No agregues stats, records ni contexto histórico que no puedas verificar.
- Preferí frases generales y verificables antes que datos inventados.

Tono: apasionado, directo, voseo argentino. Como un fan experto que comparte con amigos.
Solo JSON válido. Sin texto extra, sin markdown, sin bloques de código.
"""

SCHEMAS = {

"info": """
{
  "portada": {
    "titulo": "TÍTULO IMPACTANTE (máx 4 palabras, mayúsculas, saltos con \\n)",
    "subtitulo": "Bajada que amplía el título. 1 oración con los datos confirmados.",
    "tag": "Categoría (ej: GP Canadá 2025)"
  },
  "slides": [
    {
      "tipo": "contenido",
      "label": "ETIQUETA (2-3 palabras en mayúsculas)",
      "titulo": "TÍTULO DEL SLIDE",
      "intro": "Intro opcional (máx 18 palabras, solo datos confirmados)",
      "items": [
        {"titulo": "Punto", "desc": "Solo datos confirmados. Sin inventar."},
        {"titulo": "Punto", "desc": "Solo datos confirmados."},
        {"titulo": "Punto", "desc": "Solo datos confirmados."},
        {"titulo": "Punto", "desc": "Solo datos confirmados."}
      ]
    },
    {
      "tipo": "dato",
      "stat": "número confirmado",
      "unidad": "unidad o cadena vacía",
      "titulo": "QUÉ ES ESE NÚMERO",
      "descripcion": "Contexto verificado del dato.",
      "contexto": ["dato verificado 1", "dato verificado 2", "dato verificado 3"]
    },
    {
      "tipo": "contenido",
      "label": "ETIQUETA",
      "titulo": "TÍTULO SLIDE 4",
      "intro": "",
      "items": [{"titulo":"","desc":""},{"titulo":"","desc":""},{"titulo":"","desc":""},{"titulo":"","desc":""}]
    },
    {
      "tipo": "contenido",
      "label": "ETIQUETA",
      "titulo": "TÍTULO SLIDE 5",
      "intro": "",
      "items": [{"titulo":"","desc":""},{"titulo":"","desc":""},{"titulo":"","desc":""},{"titulo":"","desc":""}]
    }
  ],
  "cierre": {
    "pregunta": "PREGUNTA DE ENGAGEMENT (4-7 palabras, que incite a comentar)",
    "subtitulo": "Invitación a comentar y seguir. 1 oración.",
    "hashtags": "#F1 #VueltaRapida #Formula1 [hashtags del tema]"
  }
}
""",

"horarios": """
{
  "portada": {
    "titulo": "NOMBRE DEL GP (mayúsculas, con \\n si hace falta)",
    "subtitulo": "Fechas y circuito. 1 oración.",
    "tag": "Nombre del circuito"
  },
  "sesiones": [
    {"dia": "VIERNES DD MMM", "hora": "HH:MM HS", "sesion": "PRÁCTICA 1"},
    {"dia": "VIERNES DD MMM", "hora": "HH:MM HS", "sesion": "PRÁCTICA 2"},
    {"dia": "SÁBADO DD MMM",  "hora": "HH:MM HS", "sesion": "PRÁCTICA 3"},
    {"dia": "SÁBADO DD MMM",  "hora": "HH:MM HS", "sesion": "CLASIFICACIÓN"},
    {"dia": "DOMINGO DD MMM", "hora": "HH:MM HS", "sesion": "CARRERA"}
  ],
  "nota": "Horarios en hora Argentina (ART, UTC-3). Pueden sufrir cambios.",
  "cierre": {
    "pregunta": "¿VAS A VER LA CARRERA?",
    "subtitulo": "Comentá tu predicción. Seguinos para más F1.",
    "hashtags": "#F1 #VueltaRapida #Formula1 [hashtag del GP]"
  }
}
""",

"producto": """
{
  "portada": {
    "titulo": "NOMBRE DEL PRODUCTO (máx 4 palabras, con \\n si hace falta)",
    "subtitulo": "Descripción en 1 oración con datos reales del producto.",
    "tag": "Categoría (ej: LEGO F1, Colección)"
  },
  "slides": [
    {
      "tipo": "contenido",
      "label": "QUÉ INCLUYE",
      "titulo": "LO QUE VAS\\nA ARMAR",
      "intro": "",
      "items": [
        {"titulo": "Característica real", "desc": "Dato verificado del producto"},
        {"titulo": "Característica real", "desc": "Dato verificado del producto"},
        {"titulo": "Característica real", "desc": "Dato verificado del producto"},
        {"titulo": "Característica real", "desc": "Dato verificado del producto"}
      ]
    },
    {
      "tipo": "dato",
      "stat": "número real del producto (piezas, año, etc.)",
      "unidad": "unidad",
      "titulo": "DATO REAL DEL PRODUCTO",
      "descripcion": "Por qué ese número importa.",
      "contexto": ["dato real 1", "dato real 2", "dato real 3"]
    },
    {
      "tipo": "contenido",
      "label": "POR QUÉ LO QUERÉS",
      "titulo": "EL AUTO\\nQUE MARCÓ\\nLA HISTORIA",
      "intro": "",
      "items": [{"titulo":"","desc":""},{"titulo":"","desc":""},{"titulo":"","desc":""},{"titulo":"","desc":""}]
    },
    {
      "tipo": "contenido",
      "label": "FICHA TÉCNICA",
      "titulo": "ESPECIFICACIONES",
      "intro": "",
      "items": [{"titulo":"","desc":""},{"titulo":"","desc":""},{"titulo":"","desc":""},{"titulo":"","desc":""}]
    }
  ],
  "cierre": {
    "pregunta": "¿LO AGREGÁS\\nA TU COLECCIÓN?",
    "subtitulo": "Escribinos por DM para precio y disponibilidad.",
    "hashtags": "#LEGO #F1 #VueltaRapida [hashtag del producto]"
  }
}
"""
}


def generate_content(tema: str, tipo: str, extra_context: str = "") -> dict:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("Falta ANTHROPIC_API_KEY en las variables de entorno.")

    client = anthropic.Anthropic(api_key=api_key)
    schema = SCHEMAS.get(tipo, SCHEMAS["info"])

    ctx = f"\n\nContexto adicional confirmado: {extra_context}" if extra_context else ""
    prompt = f"""Generá el contenido para un carrusel de Instagram sobre: "{tema}".{ctx}

IMPORTANTE: Solo incluí información confirmada en el tema o contexto. No inventés datos, records ni estadísticas.

Estructura del carrusel ({tipo}):
{schema}

Solo JSON válido, sin texto extra."""

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

def render_slides(content: dict, tipo: str, logo_src: str, bg_images: list) -> list:
    slides = []
    n_bg = len(bg_images)

    def pick_bg(i: int) -> str:
        return bg_images[i % n_bg] if bg_images else ""

    if tipo == "horarios":
        slides.append(build_portada(content["portada"], logo_src, pick_bg(0)))
        sesiones = content.get("sesiones", [])
        nota     = content.get("nota", "")
        days = {}
        for s in sesiones:
            days.setdefault(s.get("dia", ""), []).append(s)
        slide_n = 2
        total   = 2 + len(days) + 1
        for i, (dia, slist) in enumerate(days.items()):
            slides.append(build_horarios(
                {"titulo": dia, "sesiones": slist,
                 "nota": nota if slide_n == total - 1 else ""},
                slide_n, total, logo_src, pick_bg(i + 1)
            ))
            slide_n += 1
        slides.append(build_cierre(content["cierre"], logo_src, total, pick_bg(slide_n)))

    else:
        total = 6
        slides.append(build_portada(content["portada"], logo_src, pick_bg(0)))
        for i, sd in enumerate(content.get("slides", []), 1):
            if sd.get("tipo") == "dato":
                slides.append(build_dato(sd, i + 1, total, logo_src, pick_bg(i)))
            else:
                slides.append(build_contenido(sd, i + 1, total, logo_src, pick_bg(i)))
        slides.append(build_cierre(content["cierre"], logo_src, total, pick_bg(total - 1)))

    return slides


def capture_slides(slides_html: list, output_dir: Path) -> list:
    output_dir.mkdir(parents=True, exist_ok=True)
    paths = []
    with sync_playwright() as p:
        launch_kwargs = {"args": ["--no-sandbox", "--disable-dev-shm-usage", "--font-render-hinting=none"]}
        if CHROMIUM_PATH:
            launch_kwargs["executable_path"] = CHROMIUM_PATH
        browser = p.chromium.launch(**launch_kwargs)
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
    parser.add_argument("tema",   help="Tema del carrusel")
    parser.add_argument("--tipo", default="info",
                        choices=["info", "horarios", "producto"],
                        help="Tipo de carrusel (default: info)")
    parser.add_argument("--ctx",  default="",
                        help="Contexto adicional confirmado para no inventar datos")
    parser.add_argument("--out",  default="./preview",
                        help="Carpeta de salida (default: ./preview)")
    args = parser.parse_args()

    print(f"\n Generando carrusel [{args.tipo}]: \"{args.tema}\"")
    print(" Cargando assets...")
    logo_src  = logo_b64()
    bg_images = load_bg_images()
    print(f"   {len(bg_images)} imágenes de fondo cargadas")

    print(" Consultando a Claude para generar el contenido...")
    try:
        content = generate_content(args.tema, args.tipo, args.ctx)
    except json.JSONDecodeError as e:
        print(f"Error al parsear respuesta de Claude: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error al consultar Claude API: {e}")
        sys.exit(1)

    titulo = content.get("portada", {}).get("titulo", args.tema)
    print(f" Contenido listo → {titulo}")
    print("\n Renderizando slides...")
    slides_html = render_slides(content, args.tipo, logo_src, bg_images)

    slug = slugify(args.tema)
    output_dir = Path(args.out) / slug
    paths = capture_slides(slides_html, output_dir)

    print(f"\n Preview listo en: {output_dir}/")
    for p in paths:
        print(f"   {p.name}  ({p.stat().st_size // 1024} KB)")
    print(f"\n Si está ok → movelo a: ./carruseles vuelta rapida club/{slug}/")


if __name__ == "__main__":
    main()
