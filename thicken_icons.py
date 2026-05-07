"""
Thicken the extracted multi-tool icons by dilating them (morphological expansion).
"""
from PIL import Image, ImageFilter
import numpy as np
import os

names = ['blade', 'saw', 'scissors', 'corkscrew', 'ruler', 'fork']
accent = (255, 42, 42)  # #FF2A2A

for name in names:
    path = f'images/expertise/{name}.png'
    img = Image.open(path).convert('RGBA')
    arr = np.array(img)
    
    # Extract alpha channel
    alpha = arr[:, :, 3]
    
    # Dilate alpha channel to make lines thicker
    # Use PIL MaxFilter which expands bright areas
    alpha_img = Image.fromarray(alpha, 'L')
    
    # Apply dilation twice for noticeable thickening
    alpha_thick = alpha_img.filter(ImageFilter.MaxFilter(3))
    alpha_thick = alpha_thick.filter(ImageFilter.MaxFilter(3))
    
    # Slight smooth to keep anti-aliased edges
    alpha_thick = alpha_thick.filter(ImageFilter.SMOOTH)
    
    # Rebuild the image with accent color and thickened alpha
    alpha_arr = np.array(alpha_thick)
    
    new_arr = np.zeros_like(arr)
    new_arr[:, :, 0] = accent[0]
    new_arr[:, :, 1] = accent[1]
    new_arr[:, :, 2] = accent[2]
    new_arr[:, :, 3] = alpha_arr
    
    result = Image.fromarray(new_arr, 'RGBA')
    result.save(path)
    print(f"Thickened {path}")

print("Done!")
