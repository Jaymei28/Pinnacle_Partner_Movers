
import os
import sys
import django
import csv

# Setup Django environment
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jobstream_backend.settings')
django.setup()

from jobs.models import Carrier, Job

def import_jobs(csv_file_path):
    if not os.path.exists(csv_file_path):
        print(f"Error: File not found: {csv_file_path}")
        return

    with open(csv_file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            carrier_name = row.get('carrier_name', '').strip()
            if not carrier_name:
                continue
            
            carrier, _ = Carrier.objects.get_or_create(name=carrier_name)
            
            title = row.get('title', '').strip()
            if not title:
                continue

            # Map CSV fields to Job model fields
            job_data = {
                'carrier': carrier,
                'title': title,
                'state': row.get('state', ''),
                'zip_code': row.get('zip_code', '00000'),
                'hiring_radius_miles': int(row.get('hiring_radius_miles', 50) or 50),
                'pay_range': row.get('pay_range'),
                'average_weekly_pay': row.get('average_weekly_pay'),
                'salary': row.get('salary'),
                'pay_type': row.get('pay_type'),
                'short_haul_pay': row.get('short_haul_pay'),
                'stop_pay': row.get('stop_pay'),
                'bonus_offer': row.get('bonus_offer'),
                'exact_home_time': row.get('exact_home_time'),
                'home_time': row.get('home_time'),
                'load_unload_type': row.get('load_unload_type'),
                'unload_pay': row.get('unload_pay'),
                'job_details': row.get('job_details'),
                'account_overview': row.get('account_overview'),
                'administrative_details': row.get('administrative_details'),
                'description': row.get('description'),
                'orientation_details': row.get('orientation_details'),
                'orientation_table': row.get('orientation_table'),
                'trainees_accepted': row.get('trainees_accepted'),
                'account_type': row.get('account_type'),
                'cameras': row.get('cameras'),
                'driver_types': row.get('driver_types'),
                'drug_test_type': row.get('drug_test_type'),
                'experience_levels': row.get('experience_levels'),
                'freight_types': row.get('freight_types'),
                'sap_required': row.get('sap_required'),
                'transmissions': row.get('transmissions'),
                'states': row.get('states'),
            }
            
            job, created = Job.objects.update_or_create(
                carrier=carrier,
                title=title,
                state=job_data['state'],
                defaults=job_data
            )
            action = "Created" if created else "Updated"
            print(f"{action} job: {title} at {carrier_name}")

if __name__ == '__main__':
    csv_path = os.path.join(current_dir, 'TEMPLATE_COMPLETE.csv')
    import_jobs(csv_path)
