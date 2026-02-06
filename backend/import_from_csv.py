"""
CSV Import Script for Job Portal

This script imports job and carrier data from a CSV file into the Django database.

CSV Format:
-----------
carrier_name,job_title,location,zip_code,salary,pay_type,home_time,experience_required,
driver_type,freight_type,equipment_type,states_covered,description

Example:
--------
Swift Transportation,CDL-A Truck Driver,Phoenix AZ,85001,$1200 Weekly,Weekly,Daily,0 Months,
Company Driver,No Touch,Dry Van,"AZ,CA,NV",Long description here...

Usage:
------
python import_from_csv.py jobs.csv
"""

import os
import sys
import django
import csv

# Setup Django environment
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, current_dir)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jobstream_backend.settings')
django.setup()

from jobs.models import Carrier, Job


def get_or_create_carrier(carrier_name):
    """Get existing carrier or create a new one."""
    carrier, created = Carrier.objects.get_or_create(
        name=carrier_name,
        defaults={
            'description': f'{carrier_name} - Imported from CSV',
            'is_active': True
        }
    )
    
    if created:
        print(f"✓ Created new carrier: {carrier_name}")
    else:
        print(f"→ Using existing carrier: {carrier_name}")
    
    return carrier


def import_from_csv(csv_file_path):
    """Import jobs from CSV file."""
    if not os.path.exists(csv_file_path):
        print(f"Error: File not found: {csv_file_path}")
        return
    
    created_count = 0
    skipped_count = 0
    error_count = 0
    
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row_num, row in enumerate(reader, start=2):  # Start at 2 (1 is header)
            try:
                # Get or create carrier
                carrier_name = row.get('carrier_name', '').strip()
                if not carrier_name:
                    print(f"✗ Row {row_num}: Missing carrier name, skipping")
                    skipped_count += 1
                    continue
                
                carrier = get_or_create_carrier(carrier_name)
                
                # Check for required fields
                job_title = row.get('job_title', '').strip()
                if not job_title:
                    print(f"✗ Row {row_num}: Missing job title, skipping")
                    skipped_count += 1
                    continue
                
                # Check if job already exists
                location = row.get('location', '').strip()
                existing_job = Job.objects.filter(
                    carrier=carrier,
                    title=job_title,
                    location=location
                ).first()
                
                if existing_job:
                    print(f"→ Row {row_num}: Duplicate job '{job_title}' at {carrier_name}, skipping")
                    skipped_count += 1
                    continue
                
                # Create new job
                job = Job.objects.create(
                    carrier=carrier,
                    title=job_title,
                    location=location,
                    zip_code=row.get('zip_code', '').strip(),
                    salary=row.get('salary', '').strip(),
                    pay_type=row.get('pay_type', '').strip(),
                    home_time=row.get('home_time', '').strip(),
                    experience_required=row.get('experience_required', '').strip(),
                    driver_type=row.get('driver_type', '').strip(),
                    freight_type=row.get('freight_type', '').strip(),
                    equipment_type=row.get('equipment_type', '').strip(),
                    states_covered=row.get('states_covered', '').strip(),
                    description=row.get('description', '').strip(),
                    job_type='full-time',  # Default
                    is_active=True
                )
                
                print(f"✓ Row {row_num}: Created '{job_title}' at {carrier_name}")
                created_count += 1
                
            except Exception as e:
                print(f"✗ Row {row_num}: Error - {str(e)}")
                error_count += 1
                continue
    
    # Summary
    print("\n" + "=" * 60)
    print("Import Summary")
    print("=" * 60)
    print(f"✓ Created:  {created_count} jobs")
    print(f"→ Skipped:  {skipped_count} jobs (duplicates or missing data)")
    print(f"✗ Errors:   {error_count} jobs")
    print("=" * 60)


def main():
    """Main execution function."""
    if len(sys.argv) < 2:
        print("Usage: python import_from_csv.py <csv_file_path>")
        print("\nExample:")
        print("  python import_from_csv.py jobs.csv")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    
    print("=" * 60)
    print("Job Portal CSV Importer")
    print("=" * 60)
    print(f"Importing from: {csv_file}\n")
    
    import_from_csv(csv_file)


if __name__ == '__main__':
    main()
