import fitz  # PyMuPDF

pdf_path = r"c:\Users\Jaymei\.gemini\antigravity\scratch\job-portal\ss.pdf"
doc = fitz.open(pdf_path)

print(f"Total pages: {len(doc)}")

# Check first few pages for image content vs text content
for page_num in range(min(5, len(doc))):
    page = doc[page_num]
    text = page.get_text().strip()
    images = page.get_images()
    blocks = page.get_text("blocks")
    print(f"\nPage {page_num+1}: text_len={len(text)}, images_count={len(images)}, blocks_count={len(blocks)}")
    if text:
        print(f"  TEXT: {text[:200]}")
    if images:
        print(f"  Has images: {images[:2]}")

doc.close()
