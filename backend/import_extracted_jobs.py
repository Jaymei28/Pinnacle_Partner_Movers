import os
import sys
import django
import csv

# Setup Django environment
base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(base_dir)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jobstream_backend.settings')
django.setup()

from jobs.models import Job, Carrier

def clean_text(text):
    if not text or str(text).lower() in ['n/a', 'nan', 'none', '']:
        return None
    return str(text).strip()

def import_extracted_jobs(csv_file_path):
    print(f"Parsing CSV file: {csv_file_path}")
    
    created_count = 0
    updated_count = 0
    
    with open(csv_file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader):
            try:
                # Get carrier
                c_name = clean_text(row.get('Carrier')) or 'Unknown Carrier'
                # Map to official names if necessary
                if c_name == 'Swift': c_name = 'Swift Transportation'
                if c_name == 'Pam': c_name = 'Pam Transport'
                if c_name == 'Knight': c_name = 'Knight Transportation'
                
                try:
                    carrier = Carrier.objects.get(name=c_name)
                except Carrier.DoesNotExist:
                    carrier, _ = Carrier.objects.get_or_create(name=c_name)
                
                title = clean_text(row.get('Title')) or 'Job Opportunity'
                state = clean_text(row.get('State'))
                zip_code = clean_text(row.get('Zip'))
                pay = clean_text(row.get('Pay'))
                home_time = clean_text(row.get('Home_Time'))
                
                # Build sections
                job_details = f"Home Time: {home_time}" if home_time else ""
                pay_details = f"Pay: {pay}" if pay else ""
                
                defaults = {
                    'state': state,
                    'zip_code': zip_code,
                    'job_details': job_details,
                    'pay_details': pay_details,
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
    csv_file = os.path.join(os.path.dirname(__file__), '..', 'extracted_jobs.csv')
    if os.path.exists(csv_file):
        import_extracted_jobs(csv_file)
    else:
        print(f"CSV not found at {csv_file}")
