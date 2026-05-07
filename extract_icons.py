"""
Extract 6 individual multi-tool icons from icon_expert.png,
remove the gray background, and recolor to the site accent (#FF2A2A).
"""
from PIL import Image
import numpy as np
import os

img = Image.open('images/icon_expert.png').convert('RGBA')
arr = np.array(img)

# The image is 2816x1536, RGBA
# Background is dark gray (~75-85 per channel)
# Icons are white outlines (~220-255)

# Step 1: Create alpha mask — keep only bright (white) pixels
# Compute brightness
brightness = arr[:, :, :3].max(axis=2)

# Threshold: pixels with brightness > 160 are icon lines
threshold = 160
mask = brightness > threshold

# Step 2: Find columns with icon content to locate 6 icons
# Sum bright pixels per column
col_sums = mask.sum(axis=0)

# Find regions where there are icon pixels
in_icon = col_sums > 5  # at least 5 bright pixels in a column
regions = []
start = None
for i, val in enumerate(in_icon):
    if val and start is None:
        start = i
    elif not val and start is not None:
        if i - start > 30:  # skip narrow gaps
            regions.append((start, i))
        start = None
if start is not None:
    regions.append((start, arr.shape[1]))

print(f"Found {len(regions)} raw regions")
for i, r in enumerate(regions):
    print(f"  Region {i}: cols {r[0]}-{r[1]}, width={r[1]-r[0]}")

# Merge regions that are close together (< 30px gap)
merged = [regions[0]]
for r in regions[1:]:
    if r[0] - merged[-1][1] < 30:
        merged[-1] = (merged[-1][0], r[1])
    else:
        merged.append(r)

print(f"\nMerged to {len(merged)} regions")
for i, r in enumerate(merged):
    print(f"  Region {i}: cols {r[0]}-{r[1]}, width={r[1]-r[0]}")

# Find vertical bounds (rows with content)
row_sums = mask.sum(axis=1)
row_active = row_sums > 5
row_start = None
row_end = None
for i, val in enumerate(row_active):
    if val:
        if row_start is None:
            row_start = i
        row_end = i
print(f"\nVertical bounds: rows {row_start}-{row_end}")

# Step 3: Extract each icon, remove bg, recolor to accent
accent = (255, 42, 42)  # #FF2A2A
os.makedirs('images/expertise', exist_ok=True)

names = ['blade', 'saw', 'scissors', 'corkscrew', 'ruler', 'fork']

# Add some padding
pad = 15

for idx, (col_start, col_end) in enumerate(merged[:6]):
    # Crop region
    y0 = max(0, row_start - pad)
    y1 = min(arr.shape[0], row_end + pad)
    x0 = max(0, col_start - pad)
    x1 = min(arr.shape[1], col_end + pad)
    
    crop = arr[y0:y1, x0:x1].copy()
    
    # For each pixel:
    # - If bright (icon line), recolor to accent and make opaque
    # - If dark (background), make transparent
    crop_brightness = crop[:, :, :3].max(axis=2)
    
    # Create new RGBA image
    new_img = np.zeros_like(crop)
    
    # Icon pixels: recolor to accent with proportional alpha
    icon_mask = crop_brightness > threshold
    
    # Use brightness as alpha for anti-aliasing
    for y in range(crop.shape[0]):
        for x in range(crop.shape[1]):
            b = int(crop_brightness[y, x])
            if b > threshold:
                # Map brightness 160-255 to alpha 0-255
                alpha = min(255, int((b - threshold) / (255 - threshold) * 255))
                new_img[y, x] = [accent[0], accent[1], accent[2], alpha]
            else:
                new_img[y, x] = [0, 0, 0, 0]
    
    result = Image.fromarray(new_img, 'RGBA')
    
    name = names[idx] if idx < len(names) else f'icon_{idx}'
    path = f'images/expertise/{name}.png'
    result.save(path)
    print(f"Saved {path} ({result.size[0]}x{result.size[1]})")

print("\nDone!")
