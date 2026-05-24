#!/usr/bin/env python3
"""
Monitor @alpineclub_esp via Nitter RSS y genera un posteo automático
cuando hay un tweet nuevo.

Corre como GitHub Action cada 5 minutos.
Guarda el ID del último tweet procesado en .last_tweet_id
"""

import os
import re
import sys
import json
import base64
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

# ─── configuración ────────────────────────────────────────────────────────────

HANDLE     = "autosport"
LAST_ID    = Path(".last_tweet_id")
OUTPUT_DIR = Path("carruseles vuelta rapida club")

NITTER_INSTANCES = [
    "https://nitter.privacydev.net",
    "https://nitter.poast.org",
    "https://nitter.1d4.us",
    "https://nitter.net",
]


# ─── RSS helpers ──────────────────────────────────────────────────────────────

def fetch_rss(handle: str) -> str | None:
    for instance in NITTER_INSTANCES:
        url = f"{instance}/{handle}/rss"
        try:
            req = urllib.request.Request(
                url, headers={"User-Agent": "Mozilla/5.0 (compatible; VRC-bot/1.0)"}
            )
            with urllib.request.urlopen(req, timeout=10) as r:
                content = r.read().decode("utf-8")
                print(f"  ✓ RSS OK desde {instance}")
                return content
        except Exception as e:
            print(f"  ✗ {instance}: {e}")
    return None


def parse_latest_tweet(rss_xml: str) -> dict | None:
    try:
        root    = ET.fromstring(rss_xml)
        channel = root.find("channel")
        if channel is None:
            return None
        item = channel.find("item")
        if item is None:
            return None

        title = item.findtext("title", "").strip()
        link  = item.findtext("link",  "").strip()
        desc  = item.findtext("description", "").strip()
        pub   = item.findtext("pubDate", "").strip()

        # ID del tweet = último segmento de la URL
        tweet_id = re.search(r"/status/(\d+)", link)
        tweet_id = tweet_id.group(1) if tweet_id else link.split("/")[-1]

        # Limpiar HTML de la descripción
        text = re.sub(r"<[^>]+>", "", desc).strip() or title

        return {"id": tweet_id, "text": text, "title": title, "link": link, "pubDate": pub}

    except ET.ParseError as e:
        print(f"RSS parse error: {e}")
        return None


def should_skip(tweet: dict) -> bool:
    """Ignora respuestas (@mention al inicio) y retweets (RT @)."""
    text = tweet.get("text", "").strip()
    title = tweet.get("title", "").strip()
    if re.match(r"^R(T)? @", title):
        print("  ↷ Skipping retweet")
        return True
    if text.startswith("@"):
        print("  ↷ Skipping reply")
        return True
    return False


# ─── generación de contenido ──────────────────────────────────────────────────

def generate_post_content(tweet_text: str) -> dict:
    import anthropic
    client = anthropic.Anthropic()

    msg = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=400,
        messages=[{
            "role": "user",
            "content": f"""Sos el community manager de Vuelta Rápida Club, comunidad argentina de F1.

Este tweet fue publicado por @autosport (medio internacional de motorsport):
"{tweet_text}"

Generá el contenido para una imagen de Instagram de Vuelta Rápida Club que comparta esta info.
IMPORTANTE: Solo usá lo que dice el tweet. No inventes datos.

Respondé SOLO con JSON válido, sin texto extra:
{{
  "titulo": "TITULAR IMPACTANTE en mayúsculas (máx 4 palabras, puede tener salto con \\n)",
  "subtitulo": "Desarrollo en 1 oración (máx 14 palabras, voseo argentino)",
  "tag": "Categoría breve (ej: ALPINE F1, NOTICIAS, TEMPORADA 2025)"
}}"""
        }]
    )

    raw = msg.content[0].text.strip()
    raw = re.sub(r'^```(?:json)?\s*', '', raw)
    raw = re.sub(r'\s*```$', '', raw)
    return json.loads(raw)


# ─── render ───────────────────────────────────────────────────────────────────

def render_post(content: dict, tweet_id: str) -> Path:
    sys.path.insert(0, str(Path(__file__).parent))
    from generate_carousel import logo_b64, load_bg_images, capture_slides, FONTS, slugify

    logo    = logo_b64()
    bg_imgs = load_bg_images()
    bg_url  = bg_imgs[int(tweet_id[-1]) % len(bg_imgs)] if bg_imgs else ""

    titulo    = content["titulo"]
    subtitulo = content["subtitulo"]
    tag       = content["tag"]

    def img_tag(url):
        return (
            f'<div class="photo" style="background-image:url(\'{url}\')"></div>'
            f'<div class="grad"></div>'
        ) if url else '<div class="grad" style="background:radial-gradient(ellipse 70% 55% at 80% 35%,rgba(232,0,45,.22) 0%,transparent 55%)"></div>'

    html = f"""<!DOCTYPE html><html><head><meta charset="UTF-8">{FONTS}
<style>
* {{ box-sizing:border-box; margin:0; padding:0; }}
html, body {{ width:1080px; height:1350px; overflow:hidden; background:#0A0A0A; }}
.slide {{ width:1080px; height:1350px; position:relative; overflow:hidden; display:flex; flex-direction:column; }}
.photo {{
  position:absolute; inset:0;
  background-size:cover; background-position:center 18%;
  opacity:0.45;
}}
.grad {{
  position:absolute; inset:0;
  background:
    linear-gradient(180deg,
      rgba(10,10,10,.65) 0%,
      rgba(10,10,10,.05) 30%,
      rgba(10,10,10,.10) 55%,
      rgba(10,10,10,.85) 100%
    ),
    radial-gradient(ellipse 70% 60% at 80% 30%, rgba(232,0,45,.15) 0%, transparent 55%);
}}
.speed {{
  position:absolute; inset:0;
  background: repeating-linear-gradient(
    -22deg, transparent 0, transparent 80px,
    rgba(232,0,45,.035) 80px, rgba(232,0,45,.035) 82px
  );
}}
.logo {{
  position:absolute; top:44px; left:52px; z-index:10;
  display:flex; align-items:center; gap:14px;
}}
.logo img {{ width:60px; height:60px; object-fit:contain; }}
.logo-txt {{ display:flex; flex-direction:column; line-height:1; }}
.logo-top {{
  font-family:'Barlow Condensed',sans-serif; font-weight:800;
  font-size:22px; letter-spacing:3px; color:#fff;
}}
.logo-bot {{
  font-family:'Barlow Condensed',sans-serif; font-weight:600;
  font-size:13px; letter-spacing:6px; color:#E8002D; margin-top:3px;
}}
.content {{
  position:relative; z-index:5;
  display:flex; flex-direction:column;
  justify-content:flex-end;
  height:100%; padding:0 72px 108px;
}}
.bars {{ display:flex; gap:7px; margin-bottom:14px; }}
.bars span {{ display:block; width:9px; height:52px; background:#E8002D; border-radius:3px; }}
.tag {{
  display:inline-block; margin-bottom:28px;
  font-family:'Barlow Condensed',sans-serif; font-weight:600;
  font-size:18px; letter-spacing:6px; text-transform:uppercase;
  color:#E8002D; border:2px solid #E8002D;
  padding:9px 28px; border-radius:6px; width:fit-content;
}}
.titulo {{
  font-family:'Barlow Condensed',sans-serif; font-weight:900;
  font-style:italic; font-size:148px; line-height:.86;
  color:#FFFFFF; text-transform:uppercase;
  text-shadow: 0 4px 40px rgba(0,0,0,.8);
}}
.subtitulo {{
  font-family:'Barlow Condensed',sans-serif; font-weight:600;
  font-size:36px; color:rgba(255,255,255,.82);
  line-height:1.35; margin-top:20px; max-width:860px;
}}
.sep {{ display:flex; align-items:center; gap:22px; margin-top:40px; }}
.sep-line {{ width:52px; height:2px; background:#E8002D; }}
.sep-text {{
  font-family:'Barlow Condensed',sans-serif; font-weight:600;
  font-size:16px; letter-spacing:5px; text-transform:uppercase;
  color:rgba(255,255,255,.50);
}}
.stripe {{
  position:absolute; bottom:0; left:0; right:0; height:6px;
  background:#E8002D; z-index:6;
}}
</style></head><body>
<div class="slide">
  {img_tag(bg_url)}
  <div class="speed"></div>
  <div class="stripe"></div>
  <div class="logo">
    <img src="{logo}">
    <div class="logo-txt">
      <span class="logo-top">VUELTA RÁPIDA</span>
      <span class="logo-bot">CLUB</span>
    </div>
  </div>
  <div class="content">
    <div class="tag">{tag}</div>
    <div class="bars"><span></span><span></span><span></span></div>
    <div class="titulo">{titulo}</div>
    <div class="subtitulo">{subtitulo}</div>
    <div class="sep">
      <div class="sep-line"></div>
      <span class="sep-text">vueltarapidaclub</span>
      <div class="sep-line"></div>
    </div>
  </div>
</div>
</body></html>"""

    date_str = datetime.now().strftime("%Y-%m-%d")
    slug = slugify(titulo.replace("\n", " "))
    out_dir = OUTPUT_DIR / f"{date_str}-{slug}"
    paths = capture_slides([html], out_dir)
    return paths[0]


# ─── main ─────────────────────────────────────────────────────────────────────

def main():
    print(f"\n🏎  Monitor @{HANDLE} — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    print("\n📡 Buscando tweets nuevos...")
    rss = fetch_rss(HANDLE)
    if not rss:
        print("❌ No se pudo obtener el RSS. Todos los servidores Nitter fallaron.")
        sys.exit(0)  # exit 0 para no romper el workflow

    tweet = parse_latest_tweet(rss)
    if not tweet:
        print("❌ No se pudo parsear el RSS.")
        sys.exit(0)

    last_id = LAST_ID.read_text().strip() if LAST_ID.exists() else ""
    print(f"   Último procesado: {last_id or '(ninguno)'}")
    print(f"   Tweet más reciente: {tweet['id']}")

    if tweet["id"] == last_id:
        print("✅ Sin tweets nuevos.")
        sys.exit(0)

    if should_skip(tweet):
        LAST_ID.write_text(tweet["id"])
        sys.exit(0)

    print(f"\n🆕 Tweet nuevo: {tweet['text'][:120]}...")

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ Falta ANTHROPIC_API_KEY.")
        sys.exit(1)

    print("\n✍️  Generando contenido con Claude...")
    try:
        content = generate_post_content(tweet["text"])
        print(f"   Título: {content['titulo']}")
    except Exception as e:
        print(f"❌ Error generando contenido: {e}")
        sys.exit(1)

    print("\n🖼  Renderizando imagen...")
    try:
        out_path = render_post(content, tweet["id"])
        print(f"   ✓ Guardado en: {out_path}")
    except Exception as e:
        print(f"❌ Error renderizando: {e}")
        sys.exit(1)

    LAST_ID.write_text(tweet["id"])
    print(f"\n✅ Listo. ID guardado: {tweet['id']}")


if __name__ == "__main__":
    main()
