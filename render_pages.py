import fitz  # PyMuPDF

pdf_path = r"c:\Users\Jaymei\.gemini\antigravity\scratch\job-portal\ss.pdf"
doc = fitz.open(pdf_path)

# Render pages 4-8 to see more jobs
for page_num in range(3, 8):
    page = doc[page_num]
    mat = fitz.Matrix(1.5, 1.5)
    pix = page.get_pixmap(matrix=mat)
    out_path = f"c:/Users/Jaymei/.gemini/antigravity/scratch/job-portal/page_{page_num+1}.png"
    pix.save(out_path)
    print(f"Saved page {page_num+1}")

doc.close()
print("Done!")
