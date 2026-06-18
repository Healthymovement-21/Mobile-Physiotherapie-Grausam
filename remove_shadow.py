#!/usr/bin/env python3
"""Remove only the shadow from the white wall background in IMG_0065.jpeg.
Uses rembg to detect the person, then whitens only the background shadow area."""

from PIL import Image, ImageFilter, ImageEnhance
import numpy as np
from rembg import remove
import io

SRC = "/root/.claude/uploads/39329c57-f482-5ed9-bb4b-a0adc52812cb/1e17c4d3-IMG_0065.jpeg"

img = Image.open(SRC).convert("RGB")
print(f"Original: {img.size}")

# --- Step 1: Get person mask via rembg ---
img_bytes = io.BytesIO()
img.save(img_bytes, format="PNG")
result_bytes = remove(img_bytes.getvalue())
result_rgba = Image.open(io.BytesIO(result_bytes)).convert("RGBA")

# Person mask: alpha > 10 = person
alpha = np.array(result_rgba)[:, :, 3]
person_mask = alpha > 10  # True where person is

# --- Step 2: Whiten background shadow ---
img_arr = np.array(img).astype(np.float32)  # H x W x 3

# For background pixels (not person), whiten the shadow:
# Shadow pixels are grey-ish (low saturation, below full white)
# Strategy: normalize background to white by boosting brightness
# while keeping colour balance (so near-white greys -> pure white)

bg_mask = ~person_mask  # True where background

# For each background pixel: compute luminance, if it's below 255 (grey/shadow),
# scale it up to white. We use a soft "background leveling" approach:
# new_pixel = pixel / (max_background_luminance) * 255
# Find the 99th percentile brightness in the background to normalize against
bg_pixels = img_arr[bg_mask]  # shape (N, 3)
bg_luminance = 0.299 * bg_pixels[:, 0] + 0.587 * bg_pixels[:, 1] + 0.114 * bg_pixels[:, 2]

# Reference white: 99th percentile of background (ignores small highlights)
ref_white = np.percentile(bg_luminance, 99)
print(f"Background reference white luminance: {ref_white:.1f}")

# Scale factor to bring background to white
scale = 255.0 / ref_white if ref_white > 0 else 1.0
print(f"Scale factor: {scale:.4f}")

# Apply scaling to background pixels only, cap at 255
result_arr = img_arr.copy()
result_arr[bg_mask] = np.clip(img_arr[bg_mask] * scale, 0, 255)

# Smooth the transition between person edge and background to avoid harsh boundary
# Create a soft blur on the mask edge
from scipy.ndimage import gaussian_filter
person_mask_f = person_mask.astype(np.float32)
person_mask_blurred = gaussian_filter(person_mask_f, sigma=3)

# Blend original bg pixels and scaled bg pixels using soft mask
for c in range(3):
    orig = img_arr[:, :, c]
    scaled = result_arr[:, :, c]
    result_arr[:, :, c] = person_mask_blurred * orig + (1 - person_mask_blurred) * scaled

result_arr = np.clip(result_arr, 0, 255).astype(np.uint8)
result_img = Image.fromarray(result_arr)

# --- Step 3: Save outputs ---
OUT_DIR = "/home/user/Mobile-Physiotherapie-Grausam"

# 800px wide
ratio = 800 / result_img.width
h = int(result_img.height * ratio)
img_800 = result_img.resize((800, h), Image.LANCZOS)
img_800.save(f"{OUT_DIR}/foto-3-800.jpg", "JPEG", quality=88, optimize=True)
img_800.save(f"{OUT_DIR}/foto-3-800.webp", "WEBP", quality=85)

# 1600px wide
ratio = 1600 / result_img.width
h = int(result_img.height * ratio)
img_1600 = result_img.resize((1600, h), Image.LANCZOS)
img_1600.save(f"{OUT_DIR}/foto-3-1600.jpg", "JPEG", quality=88, optimize=True)
img_1600.save(f"{OUT_DIR}/foto-3-1600.webp", "WEBP", quality=85)

print("Done: foto-3-800.jpg/.webp and foto-3-1600.jpg/.webp saved.")
