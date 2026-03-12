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
    if not text or str(text).strip().lower() in ['n/a', 'nan', 'none', '']:
        return None
    return str(text).strip()


def parse_radius(value):
    """Parse hiring radius, defaulting to 50 if invalid."""
    try:
        return int(str(value).strip())
    except (ValueError, TypeError):
        return 50


def import_jobs(csv_file_path):
    """Import jobs from Jobs.csv into the database.
    
    CSV Headers:
        Carrier, Title, State, Zip code, Hiring radius miles,
        Multi zip codes, Job Details, Pay Details, Equipment Details,
        Key Disqualifiers, Requirements
    """
    print(f"Parsing CSV file: {csv_file_path}")

    created_count = 0
    updated_count = 0
    error_count = 0

    with open(csv_file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader):
            try:
                # --- Carrier ---
                carrier_name = clean_text(row.get('Carrier')) or 'Unknown Carrier'
                carrier, _ = Carrier.objects.get_or_create(name=carrier_name)

                # --- Basic Job Info ---
                title = clean_text(row.get('Title')) or 'Job Opportunity'
                state = clean_text(row.get('State'))
                zip_code = clean_text(row.get('Zip code'))
                radius_raw = row.get('Hiring radius miles', '').strip()
                hiring_radius = parse_radius(radius_raw) if radius_raw else 50
                multi_zip = clean_text(row.get('Multi zip codes'))

                # --- Consolidated Detail Fields ---
                job_details = clean_text(row.get('Job Details'))
                pay_details = clean_text(row.get('Pay Details'))
                equipment_details = clean_text(row.get('Equipment Details'))
                key_disqualifiers = clean_text(row.get('Key Disqualifiers'))
                requirements_details = clean_text(row.get('Requirements'))

                # --- Save to DB ---
                defaults = {
                    'state': state,
                    'zip_code': zip_code,
                    'hiring_radius_miles': hiring_radius,
                    'multi_zip_codes': multi_zip,
                    'job_details': job_details,
                    'pay_details': pay_details,
                    'equipment_details': equipment_details,
                    'key_disqualifiers': key_disqualifiers,
                    'requirements_details': requirements_details,
                    'is_active': True,
                }

                job, created = Job.objects.update_or_create(
                    carrier=carrier,
                    title=title,
                    defaults=defaults,
                )

                status = "CREATED" if created else "UPDATED"
                print(f"  [{status}] {carrier_name} — {title}")

                if created:
                    created_count += 1
                else:
                    updated_count += 1

            except Exception as e:
                print(f"  [ERROR] Row {idx + 2}: {e}")
                error_count += 1
                continue

    print(f"\n--- Import Complete ---")
    print(f"  Created : {created_count}")
    print(f"  Updated : {updated_count}")
    print(f"  Errors  : {error_count}")
    print(f"  Total   : {created_count + updated_count + error_count}")


if __name__ == '__main__':
    # Default: Jobs.csv is one level up from this script (project root)
    csv_file = os.path.join(os.path.dirname(__file__), '..', 'Jobs.csv')
    csv_file = os.path.abspath(csv_file)

    if not os.path.exists(csv_file):
        # Fallback: check same directory
        csv_file = os.path.join(os.path.dirname(__file__), 'Jobs.csv')

    if os.path.exists(csv_file):
        import_jobs(csv_file)
    else:
        print(f"ERROR: Jobs.csv not found. Tried: {csv_file}")
        print("Usage: python import_jobs_from_csv.py")
        sys.exit(1)
