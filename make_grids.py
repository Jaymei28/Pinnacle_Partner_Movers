"""
Create a tall strip combining ALL 314 header crops stacked vertically,
grouped in rows of 10 for easier reading.
Also create individual composite images per 50 pages for manageability.
"""
from PIL import Image, ImageDraw, ImageFont
import os

headers_dir = r"c:\Users\Jaymei\.gemini\antigravity\scratch\job-portal\headers"
out_dir = r"c:\Users\Jaymei\.gemini\antigravity\scratch\job-portal\grids"
os.makedirs(out_dir, exist_ok=True)

files = sorted(os.listdir(headers_dir))
print(f"Total header images: {len(files)}")

# Load all images resized to same width
TARGET_W = 900
imgs = []
for fname in files:
    path = os.path.join(headers_dir, fname)
    img = Image.open(path)
    w, h = img.size
    # Resize to target width keeping aspect ratio
    new_h = int(h * TARGET_W / w)
    img = img.resize((TARGET_W, new_h), Image.LANCZOS)
    imgs.append((fname, img))

print(f"Loaded {len(imgs)} images")

# Group into chunks of 50 pages per grid file
CHUNK = 50
for chunk_idx in range(0, len(imgs), CHUNK):
    chunk = imgs[chunk_idx:chunk_idx+CHUNK]
    chunk_h = sum(im.height + 20 for _, im in chunk)  # 20px label space
    combined = Image.new('RGB', (TARGET_W, chunk_h), (240, 240, 240))
    
    y = 0
    draw = ImageDraw.Draw(combined)
    for fname, im in chunk:
        page_num = fname.replace("page_","").replace(".png","")
        # Draw page number label
        draw.rectangle([0, y, TARGET_W, y+18], fill=(50,50,50))
        draw.text((4, y+2), f"PAGE {page_num}", fill=(255,255,0))
        y += 20
        combined.paste(im, (0, y))
        y += im.height

    out_name = f"grid_{chunk_idx+1:04d}_{chunk_idx+CHUNK:04d}.jpg"
    out_path = os.path.join(out_dir, out_name)
    combined.save(out_path, quality=85)
    print(f"Saved {out_name} ({chunk_h}px tall)")

print("All grids created!")
