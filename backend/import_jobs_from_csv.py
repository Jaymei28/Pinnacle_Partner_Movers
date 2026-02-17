import os
import sys
import django
import csv
import re

# Setup Django environment
base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(base_dir)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jobstream_backend.settings')
django.setup()

from jobs.models import Job, Carrier

def clean_text(text):
    """Clean and normalize text content"""
    if not text or text == 'N/A' or str(text).lower() == 'nan':
        return None
    # Remove extra whitespace and newlines
    text = re.sub(r'\s+', ' ', str(text))
    return text.strip()

def parse_csv_file(file_path):
    """Parse the CSV file and extract job listings"""
    jobs = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        csv_reader = csv.reader(f)
        headers = next(csv_reader)
        
        for idx, row_values in enumerate(csv_reader):
            try:
                # Map row to headers
                row = {}
                for i, header in enumerate(headers):
                    if i < len(row_values):
                        # Handle duplicate headers by appending index if needed, 
                        # but we know Col 0 is short Lane Info and Col 8 is detailed Lane Info
                        key = header if header not in row else f"{header}_{i}"
                        row[key] = row_values[i]
                
                # Extract fields
                carrier_name = clean_text(row.get('Carriers', 'Unknown Carrier'))
                title = clean_text(row.get('Lane Information', 'Job Opportunity'))
                location_details = row_values[8] if len(row_values) > 8 else ""
                pay = clean_text(row.get('Pay', ''))
                home_time = clean_text(row.get('Exact Home Time', ''))
                experience = clean_text(row.get('Experience', ''))
                freight_types = clean_text(row.get('Freight Types', ''))
                benefits = clean_text(row.get('Benefits', ''))
                orientation = clean_text(row.get('Orientation', ''))
                load_unload = clean_text(row.get('Load/Unload', ''))
                multi_zip = clean_text(row.get('Location Zip Codes', ''))
                state = clean_text(row.get('State', ''))
                
                # Construct combined fields for the new model sections
                
                # 1. Job Details
                job_details_parts = []
                if location_details: job_details_parts.append(location_details)
                if home_time: job_details_parts.append(f"Home Time: {home_time}")
                if freight_types: job_details_parts.append(f"Freight Types: {freight_types}")
                if experience: job_details_parts.append(f"Experience Required: {experience}")
                job_details = "\n\n".join(job_details_parts)
                
                # 2. Pay Details
                pay_details_parts = []
                if pay: pay_details_parts.append(pay)
                if benefits: pay_details_parts.append(f"Benefits: {benefits}")
                pay_details = "\n\n".join(pay_details_parts)
                
                # 3. Equipment
                equipment_parts = []
                if load_unload: equipment_parts.append(f"Load/Unload: {load_unload}")
                if orientation: equipment_parts.append(f"Orientation: {orientation}")
                equipment_details = "\n\n".join(equipment_parts)
                
                # 4. Additional Info
                additional_info = f"Source: CSV Import - Row {idx+1}"

                job_data = {
                    'carrier_name': carrier_name,
                    'title': title[:200],
                    'state': state[:200] if state else None,
                    'job_details': job_details,
                    'pay_details': pay_details,
                    'equipment_details': equipment_details,
                    'additional_info': additional_info,
                    'multi_zip_codes': multi_zip,
                    'apply_link': 'https://classarecruiting.com',
                }
                
                jobs.append(job_data)
                
            except Exception as e:
                print(f"Error parsing row {idx + 1}: {e}")
                continue
    
    return jobs

def import_jobs(csv_file_path):
    """Import jobs from CSV file into database"""
    print(f"Parsing CSV file: {csv_file_path}")
    jobs_to_import = parse_csv_file(csv_file_path)
    
    print(f"\nParsed {len(jobs_to_import)} job listings from CSV")
    
    created_count = 0
    updated_count = 0
    
    for data in jobs_to_import:
        try:
            # 1. Get or create Carrier
            carrier, _ = Carrier.objects.get_or_create(name=data.pop('carrier_name'))
            
            # 2. Try to find existing job by carrier, title, and state to deduplicate
            existing_job = Job.objects.filter(
                carrier=carrier,
                title=data['title'],
                state=data['state']
            ).first()
            
            if existing_job:
                for key, value in data.items():
                    setattr(existing_job, key, value)
                existing_job.save()
                updated_count += 1
            else:
                Job.objects.create(carrier=carrier, **data)
                created_count += 1
                
        except Exception as e:
            print(f"Error importing job: {e}")
            continue
    
    print(f"\nImport Summary: Created {created_count}, Updated {updated_count}")

if __name__ == '__main__':
    csv_file = os.path.join(os.path.dirname(__file__), '..', 'Jobs.csv')
    if not os.path.exists(csv_file):
        print(f"Error: CSV file not found at {csv_file}")
        sys.exit(1)
    import_jobs(csv_file)
