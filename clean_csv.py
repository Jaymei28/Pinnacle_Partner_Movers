import csv

with open('extracted_jobs.csv', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

# Remove duplicate (last row is a duplicate of Nestle Waters)
seen = set()
unique_rows = []
for r in rows:
    key = (r['Carrier'], r['Title'], r['State'], r['Zip'])
    if key not in seen:
        seen.add(key)
        unique_rows.append(r)

print(f"Total unique jobs: {len(unique_rows)}")
print()
for i, r in enumerate(unique_rows):
    print(f"{i+1:2}. {r['Carrier']:<30} | {r['Title']:<45} | {r['State']} {r['Zip']}")

# Write clean version
fieldnames = list(rows[0].keys())
with open('extracted_jobs_clean.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(unique_rows)

print(f"\nClean CSV written: extracted_jobs_clean.csv ({len(unique_rows)} jobs)")
