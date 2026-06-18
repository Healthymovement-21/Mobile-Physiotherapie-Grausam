#!/usr/bin/env python3
"""Cut out Nick from IMG_0065.jpeg and composite on a physiotherapy clinic background."""

from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import numpy as np
from rembg import remove
import io

SRC = "/root/.claude/uploads/39329c57-f482-5ed9-bb4b-a0adc52812cb/1e17c4d3-IMG_0065.jpeg"

# --- Load and cut out person ---
img = Image.open(SRC).convert("RGB")
W, H = img.size
print(f"Original: {W}x{H}")

img_bytes = io.BytesIO()
img.save(img_bytes, format="PNG")
result_bytes = remove(img_bytes.getvalue())
person_rgba = Image.open(io.BytesIO(result_bytes)).convert("RGBA")
print("Person cutout done.")

# --- Build physiotherapy clinic background at same resolution ---
bg = Image.new("RGB", (W, H), (0, 0, 0))
draw = ImageDraw.Draw(bg)

# Wall: warm light grey/beige, gradient top to bottom
for y in range(H):
    t = y / H
    # Top: warm white (245,242,237) → bottom: warm beige-grey (210,205,195)
    r = int(245 - t * 35)
    g = int(242 - t * 37)
    b = int(237 - t * 42)
    draw.line([(0, y), (W, y)], fill=(r, g, b))

# Subtle warm light glow from upper-left (window light simulation)
glow = Image.new("RGB", (W, H), (0, 0, 0))
glow_draw = ImageDraw.Draw(glow)
glow_draw.ellipse([(-W//4, -H//4), (W//1.2, H//1.8)], fill=(255, 248, 230))
glow = glow.filter(ImageFilter.GaussianBlur(radius=W//3))
bg = Image.blend(bg, glow, alpha=0.18)

# Floor: darker warm tone at the very bottom
for y in range(int(H * 0.88), H):
    t = (y - H * 0.88) / (H * 0.12)
    r = int(180 - t * 20)
    g = int(172 - t * 20)
    b = int(160 - t * 18)
    draw2 = ImageDraw.Draw(bg)
    draw2.line([(0, y), (W, y)], fill=(r, g, b))

# Floor/wall divider baseboard
bh = int(H * 0.02)
for y in range(int(H * 0.88), int(H * 0.88) + bh):
    t = (y - H * 0.88) / bh
    r = int(200 - t * 30)
    g = int(195 - t * 30)
    b = int(185 - t * 28)
    draw3 = ImageDraw.Draw(bg)
    draw3.line([(0, y), (W, y)], fill=(r, g, b))

# ── Treatment table (Behandlungsbank) ──
# Positioned in lower-right background, partially behind person
table_x1 = int(W * 0.42)
table_x2 = W + 50  # extends off-right edge
table_top = int(H * 0.60)
table_bot = int(H * 0.75)

draw4 = ImageDraw.Draw(bg)
# Table surface: warm dark grey (medical table color — dark charcoal/teal)
table_col = (58, 72, 80)
table_highlight = (72, 88, 96)
draw4.rectangle([table_x1, table_top, table_x2, table_bot], fill=table_col)
# Highlight edge on top of table
draw4.rectangle([table_x1, table_top, table_x2, table_top + int(H*0.015)], fill=table_highlight)
# Side of table
draw4.rectangle([table_x1, table_top, table_x1 + int(W*0.025), table_bot + int(H*0.12)], fill=(45, 56, 62))
# Table leg
leg_x = int(W * 0.72)
leg_w = int(W * 0.02)
draw4.rectangle([leg_x, table_bot, leg_x + leg_w, table_bot + int(H*0.12)], fill=(50, 60, 66))

# Table pillow/cushion on top
pillow_top = table_top - int(H * 0.018)
pillow_bot = table_top + int(H * 0.012)
draw4.rounded_rectangle(
    [table_x1 + int(W*0.03), pillow_top, table_x2 - int(W*0.05), pillow_bot],
    radius=int(H*0.008), fill=(235, 230, 218)
)

# ── Plant pot (left background) ──
# Pot
pot_cx = int(W * 0.08)
pot_by = int(H * 0.88)
pot_w = int(W * 0.09)
pot_h = int(H * 0.10)
draw4.rounded_rectangle(
    [pot_cx - pot_w//2, pot_by - pot_h, pot_cx + pot_w//2, pot_by],
    radius=int(pot_w*0.15), fill=(180, 130, 100)
)
# Soil
draw4.ellipse(
    [pot_cx - pot_w//2 + 4, pot_by - pot_h, pot_cx + pot_w//2 - 4, pot_by - int(pot_h*0.82)],
    fill=(80, 55, 35)
)
# Plant leaves
leaf_col = (72, 120, 72)
leaf_col2 = (55, 100, 60)
for i, (ox, oy, r, col) in enumerate([
    (-pot_w*0.3, -pot_h*1.6, pot_w*0.45, leaf_col),
    (pot_w*0.25, -pot_h*1.9, pot_w*0.40, leaf_col2),
    (0, -pot_h*2.2, pot_w*0.50, leaf_col),
    (-pot_w*0.5, -pot_h*2.5, pot_w*0.38, leaf_col2),
    (pot_w*0.45, -pot_h*2.0, pot_w*0.35, leaf_col),
]):
    cx = pot_cx + int(ox)
    cy = pot_by + int(oy)
    rr = int(r)
    draw4.ellipse([cx-rr, cy-int(rr*1.8), cx+rr, cy+int(rr*0.6)], fill=col)

# ── Wall decoration (framed certificate / picture, upper right) ──
frame_x1 = int(W * 0.78)
frame_y1 = int(H * 0.10)
frame_x2 = int(W * 0.95)
frame_y2 = int(H * 0.32)
# Frame border
draw4.rectangle([frame_x1, frame_y1, frame_x2, frame_y2], fill=(160, 145, 125))
# Inner mat
draw4.rectangle([frame_x1+8, frame_y1+8, frame_x2-8, frame_y2-8], fill=(248, 244, 236))
# Inner image placeholder (light blue-grey like anatomy poster)
draw4.rectangle([frame_x1+20, frame_y1+20, frame_x2-20, frame_y2-20], fill=(210, 220, 228))

# Blur the entire background for a shallow-depth-of-field look
bg = bg.filter(ImageFilter.GaussianBlur(radius=28))

# Slight warm tone overlay
warm = Image.new("RGB", (W, H), (255, 240, 210))
bg = Image.blend(bg, warm, alpha=0.06)

print("Background built.")

# --- Composite person onto background ---
bg_rgba = bg.convert("RGBA")
bg_rgba.paste(person_rgba, (0, 0), mask=person_rgba.split()[3])
result = bg_rgba.convert("RGB")

# Slight overall warmth/contrast boost
result = ImageEnhance.Contrast(result).enhance(1.08)
result = ImageEnhance.Color(result).enhance(1.05)

# --- Save outputs ---
OUT = "/home/user/Mobile-Physiotherapie-Grausam"

r800 = result.resize((800, int(H * 800/W)), Image.LANCZOS)
r800.save(f"{OUT}/foto-3-800.jpg", "JPEG", quality=88, optimize=True)
r800.save(f"{OUT}/foto-3-800.webp", "WEBP", quality=85)

r1600 = result.resize((1600, int(H * 1600/W)), Image.LANCZOS)
r1600.save(f"{OUT}/foto-3-1600.jpg", "JPEG", quality=88, optimize=True)
r1600.save(f"{OUT}/foto-3-1600.webp", "WEBP", quality=85)

print("Saved foto-3-800/1600 .jpg/.webp")
