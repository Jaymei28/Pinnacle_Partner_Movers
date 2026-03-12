import fitz  # PyMuPDF
import os

pdf_path = r"c:\Users\Jaymei\.gemini\antigravity\scratch\job-portal\ss.pdf"
doc = fitz.open(pdf_path)

output_dir = r"c:\Users\Jaymei\.gemini\antigravity\scratch\job-portal\pages"
os.makedirs(output_dir, exist_ok=True)

print(f"Total pages: {len(doc)}")
print("Rendering all pages...")

for page_num in range(len(doc)):
    page = doc[page_num]
    mat = fitz.Matrix(1.5, 1.5)
    pix = page.get_pixmap(matrix=mat)
    out_path = os.path.join(output_dir, f"page_{page_num+1:04d}.png")
    pix.save(out_path)
    if (page_num + 1) % 20 == 0:
        print(f"  Rendered {page_num+1} / {len(doc)}")

doc.close()
print("Done!")
