#!/usr/bin/env python3
"""High-quality composite: full-res rembg + edge refinement + color matching."""
from PIL import Image, ImageFilter, ImageEnhance, ImageChops
from rembg import remove, new_session
from scipy.ndimage import gaussian_filter
import numpy as np, io

SRC_PERSON = "/root/.claude/uploads/39329c57-f482-5ed9-bb4b-a0adc52812cb/17b08860-IMG_0071.jpeg"
SRC_BG     = "/root/.claude/uploads/39329c57-f482-5ed9-bb4b-a0adc52812cb/9cef381f-IMG_3793.jpeg"
OUT        = "/home/user/Mobile-Physiotherapie-Grausam"

# --- 1. Load person at full resolution ---
img = Image.open(SRC_PERSON).convert("RGB")
W, H = img.size
print(f"Person: {W}x{H}")

# --- 2. rembg at full res (u2net_human_seg = best for people) ---
session = new_session("u2net_human_seg")
buf = io.BytesIO()
img.save(buf, "PNG")
cutout_bytes = remove(buf.getvalue(), session=session)
cutout = Image.open(io.BytesIO(cutout_bytes)).convert("RGBA")
print("Full-res cutout done.")

# --- 3. Refine alpha: soften edge 1px, keep interior hard ---
alpha = np.array(cutout.split()[3]).astype(np.float32)
# Slightly erode then blur edge for natural fringe removal
from scipy.ndimage import binary_erosion
hard = alpha > 200
eroded = binary_erosion(hard, iterations=2)
soft_edge = gaussian_filter(alpha / 255.0, sigma=1.2)
# Blend: eroded core = 1.0, transition = soft_edge, exterior = 0
refined = np.where(eroded, 1.0, soft_edge)
refined = np.clip(refined * 255, 0, 255).astype(np.uint8)
r, g, b, _ = cutout.split()
cutout = Image.merge("RGBA", (r, g, b, Image.fromarray(refined)))

# --- 4. Background: scale to fill person canvas, center-crop, blur ---
bg_raw = Image.open(SRC_BG).convert("RGB")
bw, bh = bg_raw.size
s = max(W / bw, H / bh)
bg = bg_raw.resize((int(bw * s), int(bh * s)), Image.LANCZOS)
x = (bg.width  - W) // 2
y = (bg.height - H) // 2
bg = bg.crop((x, y, x + W, y + H))
# Gentle blur (background is already blurred in the source photo)
bg = bg.filter(ImageFilter.GaussianBlur(radius=12))

# --- 5. Colour-match person to background ambient light ---
# Sample background colour in the lower-centre (where feet would be)
bg_arr = np.array(bg).astype(np.float32)
person_arr = np.array(img).astype(np.float32)
alpha_f = np.array(refined).astype(np.float32) / 255.0

# Ambient colour from background (region behind person)
sample = bg_arr[int(H*0.6):int(H*0.9), int(W*0.2):int(W*0.8)]
bg_ambient = sample.mean(axis=(0,1))  # (R, G, B)
person_ambient = np.array([200, 198, 196], dtype=np.float32)  # approx white-wall

# Subtle tint shift (only 15% blend to avoid over-correction)
tint = (bg_ambient - person_ambient) * 0.15
person_tinted = np.clip(person_arr + tint[np.newaxis, np.newaxis, :], 0, 255).astype(np.uint8)
person_tinted_img = Image.fromarray(person_tinted)

r2, g2, b2 = person_tinted_img.split()
cutout = Image.merge("RGBA", (r2, g2, b2, Image.fromarray(refined)))

# --- 6. Composite ---
canvas = bg.convert("RGBA")
canvas.paste(cutout, (0, 0), mask=Image.fromarray(refined))
result = canvas.convert("RGB")
result = ImageEnhance.Contrast(result).enhance(1.05)
result = ImageEnhance.Sharpness(result).enhance(1.1)

# --- 7. Save at 800 and 1600px, high quality ---
for w in [800, 1600]:
    r = w / W
    out = result.resize((w, int(H * r)), Image.LANCZOS)
    out.save(f"{OUT}/foto-3-{w}.jpg",  "JPEG", quality=92, optimize=True, subsampling=0)
    out.save(f"{OUT}/foto-3-{w}.webp", "WEBP", quality=88, method=6)
    print(f"Saved {w}px: {out.size}")

print("Done.")
