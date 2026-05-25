#!/usr/bin/env python3
"""
Publica una imagen en Instagram y Facebook via Meta Graph API.

Requiere variables de entorno:
  META_USER_TOKEN      - User Token con permisos de publicación
  META_PAGE_ID         - ID de la página de Facebook
  META_IG_ACCOUNT_ID   - ID de la cuenta de Instagram Business
"""

import os
import sys
import time
import urllib.request
import urllib.parse
import urllib.error
import json
from pathlib import Path


GRAPH = "https://graph.facebook.com/v21.0"


def _api(method: str, endpoint: str, params: dict = None, data: dict = None) -> dict:
    params = params or {}
    token = os.environ["META_USER_TOKEN"]
    params["access_token"] = token

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


def upload_image_to_imgbb(image_path: Path) -> str:
    """Sube la imagen a imgbb y devuelve la URL pública."""
    api_key = os.environ.get("IMGBB_API_KEY")
    if not api_key:
        raise RuntimeError("Falta IMGBB_API_KEY para subir la imagen")

    import base64
    with open(image_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode()

    data = urllib.parse.urlencode({"key": api_key, "image": img_b64}).encode()
    req = urllib.request.Request("https://api.imgbb.com/1/upload", data=data, method="POST")
    with urllib.request.urlopen(req, timeout=30) as r:
        result = json.loads(r.read().decode())

    if not result.get("success"):
        raise RuntimeError(f"imgbb error: {result}")
    return result["data"]["url"]


def post_to_instagram(image_url: str, caption: str) -> str:
    """Crea un post en Instagram. Devuelve el media ID publicado."""
    ig_id = os.environ["META_IG_ACCOUNT_ID"]

    # Paso 1: crear contenedor
    print("  📤 Creando contenedor IG...")
    container = _api("POST", f"{ig_id}/media",
                     data={"image_url": image_url, "caption": caption})
    container_id = container["id"]

    # Paso 2: esperar a que esté listo
    for _ in range(10):
        status = _api("GET", container_id, params={"fields": "status_code"})
        if status.get("status_code") == "FINISHED":
            break
        if status.get("status_code") == "ERROR":
            raise RuntimeError(f"IG container error: {status}")
        time.sleep(3)
    else:
        raise RuntimeError("Timeout esperando container IG")

    # Paso 3: publicar
    print("  📸 Publicando en Instagram...")
    result = _api("POST", f"{ig_id}/media_publish",
                  data={"creation_id": container_id})
    media_id = result["id"]
    print(f"  ✓ Instagram media ID: {media_id}")
    return media_id


def post_to_facebook(image_path: Path, message: str) -> str:
    """Publica la imagen directamente en el feed de Facebook."""
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


def publish(image_path: Path, caption: str):
    """Publica en Instagram y Facebook. image_path debe ser un JPG local."""
    print(f"\n🌐 Publicando: {image_path.name}")

    # Instagram necesita URL pública — usamos imgbb como host temporal
    print("  ☁️  Subiendo imagen a imgbb...")
    image_url = upload_image_to_imgbb(image_path)
    print(f"  ✓ URL: {image_url}")

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

    if errors:
        print(f"\n⚠️  Hubo errores: {errors}")
    else:
        print("\n✅ Publicado en Instagram y Facebook")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python3 post_meta.py <imagen.jpg> <caption>")
        sys.exit(1)
    publish(Path(sys.argv[1]), sys.argv[2])
