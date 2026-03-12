import fitz  # PyMuPDF

pdf_path = r"c:\Users\Jaymei\.gemini\antigravity\scratch\job-portal\ss.pdf"
doc = fitz.open(pdf_path)

# Render ALL pages at very low resolution just to scan for job headers
# We need to find where the orange/blue header bar appears at the top right
# Job headers appear at roughly y=430 (bottom half) or y=0 (top of page)

# Instead, let's render just a thin strip from top and bottom of each page
# to detect job card beginnings (which have the colored label + title)

print("Scanning all pages for job card headers...")
print("="*60)

for page_num in range(len(doc)):
    page = doc[page_num]
    # Get just a thin strip from different vertical positions
    rect = page.rect
    height = rect.height
    
    # Check top section (y: 0-200) and bottom section (y: height-200 to height)
    # Look for the orange/badge area that starts a job card
    
    # Get pixmap at low res for speed
    mat = fitz.Matrix(0.5, 0.5)  # half resolution
    pix = page.get_pixmap(matrix=mat)
    
    # Save small versions
    if page_num < 20 or page_num % 20 == 0:
        out_path = f"c:/Users/Jaymei/.gemini/antigravity/scratch/job-portal/scan_{page_num+1}.png"
        pix.save(out_path)

print("Done scanning")
doc.close()
