# Vuelta Rápida Club — Reglas de Diseño

## Formato de posteos
- **Siempre 4:5** — 864x1080px (equivale a 1080x1350 en Instagram)
- **Idioma**: español rioplatense (argentino). Nunca usar "pita", "pit", u otras expresiones de España. Usar "parada en boxes", "boxes", "neumático", etc.

## Layout
- **Logo siempre abajo a la derecha** — posición absoluta, bottom: 36px, right: 40px
- **Archivo de logo correcto**: `Otros/vuelta_rapida_club_vuelta_y_club_blanco.png` — es el único con fondo transparente. NUNCA usar `logo-final-crop.png` (fondo blanco) ni `logo-screen-ready.png`.
- El logo muestra: "VUELTA RÁPIDA" (16px) / "CLUB" (14px, blanco visible) / "www.vueltarapida.store" (11px, rojo #e10600)
- Siempre incluir www.vueltarapida.store debajo del logo
- **Márgenes**: padding de al menos 48px en todos los lados. El contenido de texto no debe superar el 70% del ancho de la card.
- **Texto en un solo renglón siempre que sea posible** — usar `white-space: nowrap` en títulos y ajustar font-size si hace falta. Evitar que el texto se parta en dos líneas innecesariamente.

## Foto de fondo
- La foto ocupa toda la card (`inset: 0`, `object-fit: cover`)
- Siempre embeber la imagen en base64 en el HTML para que funcione correctamente en el renderizado con Puppeteer

## Degradé estándar VR — usar siempre este, no inventar otro
```css
background: linear-gradient(
  to bottom,
  rgba(0,0,0,0.08)  0%,
  rgba(0,0,0,0.05) 25%,
  rgba(0,0,0,0.30) 48%,
  rgba(0,0,0,0.78) 62%,
  rgba(0,0,0,0.93) 75%,
  rgba(0,0,0,0.97) 100%
);
```

## Líneas diagonales VR — siempre presentes
```css
background: repeating-linear-gradient(
  -55deg,
  transparent,
  transparent 48px,
  rgba(200,0,0,0.07) 48px,
  rgba(200,0,0,0.07) 50px
);
```

## Contenido del post — regla fundamental
- **Mínimo texto posible.** El post solo tiene que llamar la atención, no explicar nada.
- El detalle, la historia y los datos van en la caption de Instagram, no en la imagen.
- Estructura ideal: pre-label + título grande + dato corto (máx 1 línea) o nada más.
- **Nunca párrafos, nunca bloques de texto largos.** Si tenés ganas de poner más de 2 líneas de cuerpo, es demasiado.

## Tipografía
- **Títulos grandes**: Bebas Neue
- **Texto cuerpo**: Barlow / Barlow Condensed
- **Sombra obligatoria en títulos** para legibilidad sobre foto:
  ```css
  text-shadow: 2px 2px 12px rgba(0,0,0,0.9), 0 0 30px rgba(0,0,0,0.7);
  ```

## Colores
- Rojo principal: `#e10600`
- Fondo oscuro: `#0d0d0d`
- Texto principal: `#ffffff`
- Texto secundario: `rgba(255,255,255,0.75)`

## Stack de renderizado
- El HTML se sirve localmente con `python3 -m http.server 8787` desde `/home/user/Vuelta-rapida/`
- Puppeteer toma screenshot en `/tmp/screenshot.mjs` apuntando a `http://localhost:8787/nombre-post.html`
- El preview se guarda como `.jpg` y se envía al usuario directamente desde acá

## Workflow de imágenes
- Las fotos se suben al repo de GitHub (rama `main`) y se bajan con `git fetch origin main && git checkout origin/main -- archivo.jpg`
- Se convierten a base64 con Python y se embeben en el HTML antes de renderizar
