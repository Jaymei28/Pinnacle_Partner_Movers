import os
import json
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jobstream_backend.settings')
django.setup()

from jobs.models import Job, Carrier

def import_from_json(file_path):
    if not os.path.exists(file_path):
        print(f"File {file_path} not found.")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    carriers_data = [item for item in data if item['model'] == 'jobs.carrier']
    jobs_data = [item for item in data if item['model'] == 'jobs.job']

    # 1. Import Carriers
    carrier_map = {} # Maps local PK -> Remote Instance
    for c_item in carriers_data:
        fields = c_item['fields']
        carrier, created = Carrier.objects.update_or_create(
            name=fields['name'],
            defaults={
                'description': fields.get('description', ''),
                'website': fields.get('website'),
                'contact_email': fields.get('contact_email'),
                'contact_phone': fields.get('contact_phone'),
                'presentation': fields.get('presentation'),
                'pre_qualifications': fields.get('pre_qualifications'),
                'app_process': fields.get('app_process'),
                'benefit_401k': fields.get('benefit_401k', ''),
                'benefit_medical_dental_vision': fields.get('benefit_medical_dental_vision', ''),
                'benefit_paid_vacation': fields.get('benefit_paid_vacation', ''),
                'benefit_other': fields.get('benefit_other', ''),
            }
        )
        carrier_map[c_item['pk']] = carrier
        print(f"{'Created' if created else 'Updated'} Carrier: {carrier.name}")

    # 2. Import Jobs
    for j_item in jobs_data:
        fields = j_item['fields']
        local_carrier_pk = fields['carrier']
        carrier = carrier_map.get(local_carrier_pk)
        
        if not carrier:
            # Try to find by name if pk not in map (unlikely but safe)
            continue

        job, created = Job.objects.update_or_create(
            carrier=carrier,
            title=fields['title'],
            state=fields.get('state'),
            defaults={
                'zip_code': fields.get('zip_code'),
                'hiring_radius_miles': fields.get('hiring_radius_miles', 50),
                'job_details': fields.get('job_details', ''),
                'pay_details': fields.get('pay_details', ''),
                'equipment_details': fields.get('equipment_details', ''),
                'key_disqualifiers': fields.get('key_disqualifiers', ''),
                'requirements_details': fields.get('requirements_details', ''),
                'multi_zip_codes': fields.get('multi_zip_codes'),
                'is_active': fields.get('is_active', True),
            }
        )
        print(f"{'Created' if created else 'Updated'} Job: {job.title} ({carrier.name})")

if __name__ == '__main__':
    import_from_json('local_jobs_dump_utf8.json')
