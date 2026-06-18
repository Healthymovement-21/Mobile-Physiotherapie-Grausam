#!/usr/bin/env python3
from PIL import Image, ImageFilter, ImageEnhance
from rembg import remove
import numpy as np, io

SRC_PERSON = "/root/.claude/uploads/39329c57-f482-5ed9-bb4b-a0adc52812cb/fe4aa862-IMG_0074.jpeg"
SRC_BG     = "/root/.claude/uploads/39329c57-f482-5ed9-bb4b-a0adc52812cb/9cef381f-IMG_3793.jpeg"
OUT        = "/home/user/Mobile-Physiotherapie-Grausam"

# 1. Load + rotate person photo
img = Image.open(SRC_PERSON).convert("RGB")
img = img.rotate(-90, expand=True)          # fix 90° CCW tilt
print(f"Person after rotate: {img.size}")

# 2. Downscale for rembg (faster, still high quality)
scale = 1600 / img.width
thumb = img.resize((1600, int(img.height * scale)), Image.LANCZOS)

buf = io.BytesIO()
thumb.save(buf, "PNG")
cutout_bytes = remove(buf.getvalue())
cutout_thumb = Image.open(io.BytesIO(cutout_bytes)).convert("RGBA")

# Scale cutout back to full resolution
cutout = cutout_thumb.resize(img.size, Image.LANCZOS)
print("Cutout done.")

# 3. Prepare background — scale to match person dimensions (fill + center crop)
bg_raw = Image.open(SRC_BG).convert("RGB")
W, H = img.size
bw, bh = bg_raw.size
scale_bg = max(W / bw, H / bh)
bg_scaled = bg_raw.resize((int(bw * scale_bg), int(bh * scale_bg)), Image.LANCZOS)
# center crop
x = (bg_scaled.width  - W) // 2
y = (bg_scaled.height - H) // 2
bg = bg_scaled.crop((x, y, x + W, y + H))
# apply additional blur for depth-of-field
bg = bg.filter(ImageFilter.GaussianBlur(radius=18))

# 4. Composite
canvas = bg.convert("RGBA")
canvas.paste(cutout, (0, 0), mask=cutout.split()[3])
result = canvas.convert("RGB")
result = ImageEnhance.Contrast(result).enhance(1.06)

# 5. Save at 800 and 1600px wide
for w in [800, 1600]:
    r = w / result.width
    out_img = result.resize((w, int(result.height * r)), Image.LANCZOS)
    out_img.save(f"{OUT}/foto-3-{w}.jpg",  "JPEG", quality=88, optimize=True)
    out_img.save(f"{OUT}/foto-3-{w}.webp", "WEBP", quality=85)
    print(f"Saved foto-3-{w}: {out_img.size}")

print("Done.")
