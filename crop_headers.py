"""
Crop just the top 120px (header area) of each page where new job cards start.
Save as individual small header images for quick review.
This allows us to identify which pages start a NEW job posting.
"""
from PIL import Image
import os

pages_dir = r"c:\Users\Jaymei\.gemini\antigravity\scratch\job-portal\pages"
headers_dir = r"c:\Users\Jaymei\.gemini\antigravity\scratch\job-portal\headers"
os.makedirs(headers_dir, exist_ok=True)

pages = sorted(os.listdir(pages_dir))
print(f"Processing {len(pages)} pages...")

for fname in pages:
    src = os.path.join(pages_dir, fname)
    img = Image.open(src)
    w, h = img.size
    # Crop top 15% to capture any job header banners
    crop_h = int(h * 0.15)
    cropped = img.crop((0, 0, w, crop_h))
    # Save at same name
    out = os.path.join(headers_dir, fname)
    cropped.save(out)

print("Done! All header crops saved.")
