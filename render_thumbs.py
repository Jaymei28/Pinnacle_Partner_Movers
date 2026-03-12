import fitz  # PyMuPDF
from PIL import Image
import io

pdf_path = r"c:\Users\Jaymei\.gemini\antigravity\scratch\job-portal\ss.pdf"
doc = fitz.open(pdf_path)

# Render every 10th page starting header areas to find new job starts
# We'll save thumbnails at lower resolution to quickly scan
pages_to_check = list(range(0, len(doc), 5))  # every 5 pages

for page_num in pages_to_check:
    page = doc[page_num]
    # Get just the top portion of the page (to see job headers)
    # Clip to top 200 pixels
    rect = page.rect
    clip = fitz.Rect(rect.x0, rect.y0, rect.x1, min(rect.y1, rect.y0 + 150))
    mat = fitz.Matrix(1.0, 1.0)
    pix = page.get_pixmap(matrix=mat, clip=clip)
    out_path = f"c:/Users/Jaymei/.gemini/antigravity/scratch/job-portal/thumb_{page_num+1}.png"
    pix.save(out_path)

doc.close()
print(f"Saved {len(pages_to_check)} thumbnails")
print("Pages checked:", pages_to_check)
