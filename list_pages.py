"""
Scan all pages to find each job header by checking for carrier name banners.
We'll check every page and log any that contain a new job header.
"""
import os

pages_dir = r"c:\Users\Jaymei\.gemini\antigravity\scratch\job-portal\pages"
pages = sorted(os.listdir(pages_dir))
print(f"Total page files: {len(pages)}")
for p in pages:
    num = int(p.replace("page_","").replace(".png",""))
    print(num, p)
