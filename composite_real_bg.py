#!/usr/bin/env python3
"""Composite Nick (cutout from IMG_0065.jpeg) onto the real physiotherapy background photo."""

from PIL import Image, ImageFilter, ImageEnhance
import numpy as np
from rembg import remove
import io

SRC_PERSON = "/root/.claude/uploads/39329c57-f482-5ed9-bb4b-a0adc52812cb/1e17c4d3-IMG_0065.jpeg"
SRC_BG = "/root/.claude/uploads/39329c57-f482-5ed9-bb4b-a0adc52812cb/3b19f856-IMG_3790.png"

# --- Cut out person ---
img = Image.open(SRC_PERSON).convert("RGB")
W, H = img.size
print(f"Person original: {W}x{H}")

img_bytes = io.BytesIO()
img.save(img_bytes, format="PNG")
result_bytes = remove(img_bytes.getvalue())
person_rgba = Image.open(io.BytesIO(result_bytes)).convert("RGBA")
print("Cutout done.")

# --- Prepare background ---
bg = Image.open(SRC_BG).convert("RGB")
# Scale background to match person dimensions (fill, crop to center)
bg_ratio = bg.width / bg.height
person_ratio = W / H

if bg_ratio > person_ratio:
    # bg is wider — scale by height
    new_h = H
    new_w = int(H * bg_ratio)
else:
    # bg is taller — scale by width
    new_w = W
    new_h = int(W / bg_ratio)

bg = bg.resize((new_w, new_h), Image.LANCZOS)
# Center crop
left = (new_w - W) // 2
top = (new_h - H) // 2
bg = bg.crop((left, top, left + W, top + H))

# Blur background for depth-of-field effect
bg = bg.filter(ImageFilter.GaussianBlur(radius=22))

print("Background prepared.")

# --- Composite ---
bg_rgba = bg.convert("RGBA")
bg_rgba.paste(person_rgba, (0, 0), mask=person_rgba.split()[3])
result = bg_rgba.convert("RGB")

# Slight contrast/color boost
result = ImageEnhance.Contrast(result).enhance(1.06)

# --- Save ---
OUT = "/home/user/Mobile-Physiotherapie-Grausam"

r800 = result.resize((800, int(H * 800 / W)), Image.LANCZOS)
r800.save(f"{OUT}/foto-3-800.jpg", "JPEG", quality=88, optimize=True)
r800.save(f"{OUT}/foto-3-800.webp", "WEBP", quality=85)

r1600 = result.resize((1600, int(H * 1600 / W)), Image.LANCZOS)
r1600.save(f"{OUT}/foto-3-1600.jpg", "JPEG", quality=88, optimize=True)
r1600.save(f"{OUT}/foto-3-1600.webp", "WEBP", quality=85)

print("Done.")
