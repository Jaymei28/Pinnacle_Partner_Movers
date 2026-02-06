from bs4 import BeautifulSoup

# Read HTML file
with open('../Job Search.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

# Find all job items
items = soup.find_all('div', {'role': 'listitem'})

print(f"Analyzing {min(10, len(items))} job items...\n")

all_field_ids = set()

for idx, item in enumerate(items[:10]):
    fields = item.find_all(attrs={'data-softr-field-id': True})
    
    print(f"\n=== Job {idx + 1} ===")
    for elem in fields:
        field_id = elem.get('data-softr-field-id')
        text = elem.get_text(strip=True)
        all_field_ids.add(field_id)
        print(f"{field_id}: {text[:100]}")

print(f"\n\nAll unique field IDs found:")
for field_id in sorted(all_field_ids):
    print(f"  - {field_id}")
