import os
import django
import csv

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jobstream_backend.settings')
django.setup()

from jobs.models import Academy, Carrier

def import_academies(csv_file_path):
    print(f"Parsing CSV file: {csv_file_path}")
    
    created_count = 0
    updated_count = 0
    
    with open(csv_file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader):
            try:
                c_name = row.get('carrier')
                if not c_name: continue
                
                # Map names
                if c_name == 'Swift': c_name = 'Swift Transportation'
                if c_name == 'Mast': c_name = 'Mast Trucking'
                
                try:
                    carrier = Carrier.objects.get(name=c_name)
                except Carrier.DoesNotExist:
                    print(f"Carrier {c_name} not found for academy {row.get('name')}")
                    continue
                
                defaults = {
                    'city': row.get('city'),
                    'state': row.get('state'),
                    'zip_code': row.get('zip_code'),
                    'training_type': row.get('training_type'),
                    'tuition_cost': row.get('tuition_cost'),
                    'trainee_pay': row.get('trainee_pay'),
                    'orientation_pay': row.get('orientation_pay'),
                    'requirements': row.get('requirements'),
                    'academy_details': row.get('academy_details'),
                    'after_graduation': row.get('after_graduation'),
                    'is_active': True
                }
                
                obj, created = Academy.objects.update_or_create(
                    name=row.get('name'),
                    carrier=carrier,
                    defaults=defaults
                )
                
                if created: created_count += 1
                else: updated_count += 1
                
            except Exception as e:
                print(f"Error on row {idx+1}: {e}")
                continue
                
    print(f"\nImport Finished: {created_count} created, {updated_count} updated.")

if __name__ == '__main__':
    # 1. Import from CSV
    csv_file = os.path.join(os.path.dirname(__file__), '..', 'extracted_academies.csv')
    if os.path.exists(csv_file):
        import_academies(csv_file)
    
    # 2. Add Mast manually if not in CSV (it wasn't in the snippet I saw)
    mast, _ = Carrier.objects.get_or_create(name='Mast Trucking')
    obj, created = Academy.objects.update_or_create(
        name='Mast 1.0 (School Phase)',
        carrier=mast,
        defaults={
            'city': 'Millersburg',
            'state': 'OH',
            'zip_code': '44663',
            'training_type': 'In-Person',
            'tuition_cost': 'Varies',
            'trainee_pay': '$9.30 per hour during Mast 1.0 classroom and hands-on training.',
            'orientation_pay': 'Transitions to $0.22 per mile upon entering Mast 2.0.',
            'requirements': 'Must obtain Class A CDL permit prior to or during week one of Mast 1.0. Commit to 100,000 miles with Mast after signing training agreement.',
            'academy_details': 'Program focuses on CDL training, safety, and DTW preparation. Training held at the Mast Trucking Training Center and Mast terminals. Lodging provided Monday-Friday for Mast 1.0 participants.'
        }
    )
    if created: print("Added Mast Academy.")
