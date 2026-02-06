import csv

# Read and analyze the CSV structure
with open('../Job Ops.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    
    # Get the headers
    headers = reader.fieldnames
    print(f"Total headers: {len(headers)}")
    print("\nHeaders with indices:")
    for idx, header in enumerate(headers):
        print(f"  {idx}: '{header}'")
    
    # Read first row
    first_row = next(reader)
    print("\n\nFirst row values:")
    for idx, (key, value) in enumerate(first_row.items()):
        print(f"  {idx}: {key} = {value[:50] if value else 'None'}...")
