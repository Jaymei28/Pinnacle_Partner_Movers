import csv

with open('extracted_jobs.csv', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

print(f"Total jobs: {len(rows)}")
print(f"Columns: {list(rows[0].keys())}")
print()
for i, r in enumerate(rows):
    print(f"{i+1}. {r['Carrier']} | {r['Title']} | {r['State']} {r['Zip']}")
