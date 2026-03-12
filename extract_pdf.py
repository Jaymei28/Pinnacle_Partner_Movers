import fitz  # PyMuPDF

pdf_path = r"c:\Users\Jaymei\.gemini\antigravity\scratch\job-portal\ss.pdf"
doc = fitz.open(pdf_path)

print(f"Total pages: {len(doc)}")
print("=" * 80)

for page_num in range(len(doc)):
    page = doc[page_num]
    text = page.get_text()
    print(f"\n{'='*80}")
    print(f"PAGE {page_num + 1}")
    print(f"{'='*80}")
    print(text)

doc.close()
