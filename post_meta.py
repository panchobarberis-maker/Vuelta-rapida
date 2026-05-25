#!/usr/bin/env python3
"""
Publica una imagen en Instagram y Facebook via Meta Graph API.

Requiere variables de entorno:
  META_USER_TOKEN      - Page Token con permisos de publicación
  META_PAGE_ID         - ID de la página de Facebook
  META_IG_ACCOUNT_ID   - ID de la cuenta de Instagram Business
  GITHUB_REPOSITORY    - seteado automáticamente por GitHub Actions
"""

import os
import sys
import time
import urllib.request
import urllib.parse
import json
from pathlib import Path


GRAPH = "https://graph.facebook.com/v21.0"
GITHUB_RAW = "https://raw.githubusercontent.com"


def _api(method: str, endpoint: str, params: dict = None, data: dict = None) -> dict:
    params = params or {}
    params["access_token"] = os.environ["META_USER_TOKEN"]

    qs = urllib.parse.urlencode(params)
    url = f"{GRAPH}/{endpoint}?{qs}"

    if method == "POST":
        body = urllib.parse.urlencode(data or {}).encode()
        req = urllib.request.Request(url, data=body, method="POST")
    else:
        req = urllib.request.Request(url)

    req.add_header("User-Agent", "VRC-bot/1.0")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())


def github_raw_url(image_path: Path) -> str:
    """Construye la URL pública de la imagen en el repo de GitHub."""
    repo = os.environ.get("GITHUB_REPOSITORY", "panchobarberis-maker/vuelta-rapida")
    # La imagen ya fue pusheada a main antes de llamar a esta función
    rel = str(image_path).lstrip("/")
    # Codificar espacios en el path
    encoded = urllib.parse.quote(rel, safe="/")
    return f"{GITHUB_RAW}/{repo}/main/{encoded}"


def post_to_instagram(image_url: str, caption: str) -> str:
    ig_id = os.environ["META_IG_ACCOUNT_ID"]

    print("  📤 Creando contenedor IG...")
    container = _api("POST", f"{ig_id}/media",
                     data={"image_url": image_url, "caption": caption})
    container_id = container["id"]

    for _ in range(15):
        status = _api("GET", container_id, params={"fields": "status_code"})
        if status.get("status_code") == "FINISHED":
            break
        if status.get("status_code") == "ERROR":
            raise RuntimeError(f"IG container error: {status}")
        time.sleep(4)
    else:
        raise RuntimeError("Timeout esperando container IG")

    print("  📸 Publicando en Instagram...")
    result = _api("POST", f"{ig_id}/media_publish",
                  data={"creation_id": container_id})
    media_id = result["id"]
    print(f"  ✓ Instagram media ID: {media_id}")
    return media_id


def post_to_facebook(image_path: Path, message: str) -> str:
    page_id = os.environ["META_PAGE_ID"]

    print("  📘 Subiendo a Facebook...")
    with open(image_path, "rb") as f:
        img_data = f.read()

    boundary = "----VRCBoundary"
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="message"\r\n\r\n'
        f"{message}\r\n"
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="source"; filename="post.jpg"\r\n'
        f"Content-Type: image/jpeg\r\n\r\n"
    ).encode() + img_data + f"\r\n--{boundary}--\r\n".encode()

    token = os.environ["META_USER_TOKEN"]
    url = f"{GRAPH}/{page_id}/photos?access_token={token}"
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")
    req.add_header("User-Agent", "VRC-bot/1.0")

    with urllib.request.urlopen(req, timeout=60) as r:
        result = json.loads(r.read().decode())

    post_id = result.get("post_id") or result.get("id")
    print(f"  ✓ Facebook post ID: {post_id}")
    return post_id


def publish_from_pending():
    """Lee .pending_post.json y publica. Llamado por el workflow después del push."""
    pending_file = Path(".pending_post.json")
    if not pending_file.exists():
        print("ℹ️  No hay post pendiente.")
        return

    pending = json.loads(pending_file.read_text())
    image_path = Path(pending["path"])
    caption = pending["caption"]

    print(f"\n🌐 Publicando: {image_path.name}")

    image_url = github_raw_url(image_path)
    print(f"  🔗 URL: {image_url}")

    errors = []

    try:
        post_to_instagram(image_url, caption)
    except Exception as e:
        print(f"  ❌ Instagram: {e}")
        errors.append(f"Instagram: {e}")

    try:
        post_to_facebook(image_path, caption)
    except Exception as e:
        print(f"  ❌ Facebook: {e}")
        errors.append(f"Facebook: {e}")

    pending_file.unlink()

    if errors:
        print(f"\n⚠️  Errores: {errors}")
        sys.exit(1)
    else:
        print("\n✅ Publicado en Instagram y Facebook")


if __name__ == "__main__":
    publish_from_pending()
