
import os
import sys
import django
import csv

# Setup Django environment
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jobstream_backend.settings')
django.setup()

from jobs.models import Carrier

def import_carriers(csv_file_path):
    if not os.path.exists(csv_file_path):
        print(f"Error: File not found: {csv_file_path}")
        return

    with open(csv_file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            name = row.get('name', '').strip()
            if not name:
                continue
            
            carrier, created = Carrier.objects.update_or_create(
                name=name,
                defaults={
                    'description': row.get('description'),
                    'website': row.get('website'),
                    'contact_email': row.get('contact_email'),
                    'contact_phone': row.get('contact_phone'),
                    'headquarters_zip': row.get('headquarters_zip'),
                    'headquarters_city': row.get('headquarters_city'),
                    'headquarters_state': row.get('headquarters_state'),
                    'benefit_401k': row.get('benefit_401k'),
                    'benefit_disability_life': row.get('benefit_disability_life'),
                    'benefit_stock_purchase': row.get('benefit_stock_purchase'),
                    'benefit_medical_dental_vision': row.get('benefit_medical_dental_vision'),
                    'benefit_paid_vacation': row.get('benefit_paid_vacation'),
                    'benefit_prescription_drug': row.get('benefit_prescription_drug'),
                    'benefit_weekly_paycheck': row.get('benefit_weekly_paycheck'),
                    'benefit_driver_ranking_bonus': row.get('benefit_driver_ranking_bonus'),
                    'benefit_military_program': row.get('benefit_military_program'),
                    'benefit_tuition_program': row.get('benefit_tuition_program'),
                    'benefit_other': row.get('benefit_other'),
                }
            )
            action = "Created" if created else "Updated"
            print(f"{action} carrier: {name}")

if __name__ == '__main__':
    csv_path = os.path.join(current_dir, '..', 'Carriers.csv')
    import_carriers(csv_path)
