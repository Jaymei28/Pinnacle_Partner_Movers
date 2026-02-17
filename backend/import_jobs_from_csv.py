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
    if not text or str(text).lower() in ['n/a', 'nan', 'none', '']:
        return None
    return str(text).strip()

def import_jobs(csv_file_path):
    """Import jobs from CSV file into database using exact headers found in Jobs.csv"""
    print(f"Parsing CSV file: {csv_file_path}")
    
    created_count = 0
    updated_count = 0
    
    with open(csv_file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader):
            try:
                # 1. Get exact carrier name
                c_name = clean_text(row.get('carrier_name')) or 'Unknown Carrier'
                carrier, _ = Carrier.objects.get_or_create(name=c_name)
                
                # 2. Extract job title and location
                title = clean_text(row.get('title')) or 'Job Opportunity'
                state = clean_text(row.get('state'))
                zip_code = clean_text(row.get('zip_code'))
                
                # 3. Build Consolidated Sections
                
                # Job Details Section
                job_details_parts = []
                if clean_text(row.get('home_time')): job_details_parts.append(f"Home Time: {row['home_time']}")
                if clean_text(row.get('exact_home_time')): job_details_parts.append(f"Precise Schedule: {row['exact_home_time']}")
                if clean_text(row.get('account_type')): job_details_parts.append(f"Account: {row['account_type']}")
                if clean_text(row.get('freight_types')): job_details_parts.append(f"Freight: {row['freight_types']}")
                if clean_text(row.get('experience_levels')): job_details_parts.append(f"Experience: {row['experience_levels']}")
                job_details = "\n\n".join(job_details_parts)
                
                # Pay Details Section
                pay_parts = []
                if clean_text(row.get('pay_range')): pay_parts.append(f"Range: {row['pay_range']}")
                if clean_text(row.get('average_weekly_pay')): pay_parts.append(f"Average Weekly: {row['average_weekly_pay']}")
                if clean_text(row.get('salary')): pay_parts.append(f"Salary: {row['salary']}")
                if clean_text(row.get('bonus_offer')): pay_parts.append(f"Bonus: {row['bonus_offer']}")
                pay_details = "\n\n".join(pay_parts)
                
                # Equipment Section
                equip_parts = []
                if clean_text(row.get('transmissions')): equip_parts.append(f"Transmission: {row['transmissions']}")
                if clean_text(row.get('cameras')): equip_parts.append(f"Cameras: {row['cameras']}")
                if clean_text(row.get('orientation_details')): equip_parts.append(f"Orientation: {row['orientation_details']}")
                equipment_details = "\n\n".join(equip_parts)

                # 4. Save to Database
                defaults = {
                    'state': state,
                    'zip_code': zip_code,
                    'hiring_radius_miles': int(row.get('hiring_radius_miles', 50) or 50),
                    'job_details': job_details,
                    'pay_details': pay_details,
                    'equipment_details': equipment_details,
                    'apply_link': 'https://classarecruiting.com',
                    'is_active': True
                }
                
                job, created = Job.objects.update_or_create(
                    carrier=carrier,
                    title=title,
                    defaults=defaults
                )
                
                if created: created_count += 1
                else: updated_count += 1
                
            except Exception as e:
                print(f"Error on row {idx+1}: {e}")
                continue
                
    print(f"\nImport Finished: {created_count} created, {updated_count} updated.")

if __name__ == '__main__':
    csv_file = os.path.join(os.path.dirname(__file__), '..', 'Jobs.csv')
    if os.path.exists(csv_file):
        import_jobs(csv_file)
    else:
        print("CSV not found.")
