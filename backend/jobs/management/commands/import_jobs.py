"""
Django management command to import jobs and carriers from CSV file.
Supports all fields in the Job model and handles various CSV formats.

Usage:
    python manage.py import_jobs path/to/jobs.csv
"""

from django.core.management.base import BaseCommand
from jobs.models import Job, Carrier
import csv
import os


class Command(BaseCommand):
    help = 'Import jobs and carriers from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument(
            'csv_file',
            type=str,
            help='Path to the CSV file to import'
        )
        parser.add_argument(
            '--update',
            action='store_true',
            help='Update existing jobs instead of skipping them'
        )

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        update_existing = options['update']

        if not os.path.exists(csv_file):
            # Try root directory if not found in current
            if not os.path.isabs(csv_file):
                root_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..', csv_file)
                if os.path.exists(root_path):
                    csv_file = root_path
                else:
                    self.stdout.write(self.style.ERROR(f'CSV file not found: {csv_file}'))
                    return
            else:
                self.stdout.write(self.style.ERROR(f'CSV file not found: {csv_file}'))
                return

        self.stdout.write(self.style.SUCCESS(f'\n📋 Starting import from: {csv_file}\n'))

        # Read and process CSV
        jobs_created = 0
        jobs_updated = 0
        jobs_skipped = 0
        carriers_created = 0
        errors = []

        # Carrier mapping for consistency
        carrier_mapping = {
            'US Express': 'US Xpress',
            'Swift': 'Swift Transportation'
        }

        try:
            with open(csv_file, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                
                # Check for carrier identity column
                carrier_col = 'carrier_name' if 'carrier_name' in reader.fieldnames else 'carrier'
                title_col = 'title' if 'title' in reader.fieldnames else 'job_title'
                
                if carrier_col not in reader.fieldnames or title_col not in reader.fieldnames:
                    self.stdout.write(self.style.ERROR(
                        f'Missing required columns. Found: {", ".join(reader.fieldnames)}'
                    ))
                    return

                for row_num, row in enumerate(reader, start=2):
                    try:
                        # Get or create carrier
                        raw_carrier_name = row.get(carrier_col, '').strip()
                        if not raw_carrier_name:
                            errors.append(f'Row {row_num}: Missing carrier name')
                            continue

                        # Apply mapping
                        carrier_name = carrier_mapping.get(raw_carrier_name, raw_carrier_name)

                        carrier, created = Carrier.objects.get_or_create(
                            name=carrier_name,
                            defaults={
                                'headquarters_zip': row.get('headquarters_zip', '').strip() or None,
                                'headquarters_city': row.get('headquarters_city', '').strip() or None,
                                'headquarters_state': row.get('headquarters_state', '').strip() or None,
                                'description': row.get('carrier_description', '').strip() or None,
                                'website': row.get('website', '').strip() or None,
                                'contact_email': row.get('contact_email', '').strip() or None,
                                'contact_phone': row.get('contact_phone', '').strip() or None,
                                
                                # Benefits
                                'benefit_401k': row.get('benefit_401k', '').strip() or None,
                                'benefit_disability_life': row.get('benefit_disability_life', '').strip() or None,
                                'benefit_stock_purchase': row.get('benefit_stock_purchase', '').strip() or None,
                                'benefit_medical_dental_vision': row.get('benefit_medical_dental_vision', '').strip() or None,
                                'benefit_paid_vacation': row.get('benefit_paid_vacation', '').strip() or None,
                                'benefit_prescription_drug': row.get('benefit_prescription_drug', '').strip() or None,
                                'benefit_weekly_paycheck': row.get('benefit_weekly_paycheck', '').strip() or None,
                                'benefit_driver_ranking_bonus': row.get('benefit_driver_ranking_bonus', '').strip() or None,
                                'benefit_military_program': row.get('benefit_military_program', '').strip() or None,
                                'benefit_tuition_program': row.get('benefit_tuition_program', '').strip() or None,
                                'benefit_other': row.get('benefit_other', '').strip() or None,
                            }
                        )

                        if created:
                            carriers_created += 1
                            self.stdout.write(f'  ✅ Created carrier: {carrier_name}')

                        # Prepare job data
                        job_title = row.get(title_col, '').strip()
                        if not job_title:
                            errors.append(f'Row {row_num}: Missing job title')
                            continue

                        # Build job data dictionary matching model fields
                        job_data = {
                            'carrier': carrier,
                            'title': job_title[:200],
                            'state': row.get('state', '').strip() or 'Unknown',
                            'zip_code': row.get('zip_code', '').strip() or None,
                            'hiring_radius_miles': int(row.get('hiring_radius_miles', 50) or 50),
                            
                            'pay_range': row.get('pay_range', '').strip() or None,
                            'average_weekly_pay': row.get('average_weekly_pay', '').strip() or None,
                            'salary': row.get('salary', '').strip() or None,
                            'pay_type': row.get('pay_type', '').strip() or None,
                            'short_haul_pay': row.get('short_haul_pay', '').strip() or None,
                            'stop_pay': row.get('stop_pay', '').strip() or None,
                            'bonus_offer': row.get('bonus_offer', '').strip() or None,
                            
                            'exact_home_time': row.get('exact_home_time', '').strip() or None,
                            'home_time': row.get('home_time', '').strip() or None,
                            
                            'load_unload_type': row.get('load_unload_type', '').strip() or None,
                            'unload_pay': row.get('unload_pay', '').strip() or None,
                            
                            'job_details': row.get('job_details', '').strip() or None,
                            'account_overview': row.get('account_overview', '').strip() or None,
                            'administrative_details': row.get('administrative_details', '').strip() or None,
                            'description': row.get('description', '').strip() or None,
                            
                            'orientation_details': row.get('orientation_details', '').strip() or None,
                            'orientation_table': row.get('orientation_table', '').strip() or None,
                            
                            'trainees_accepted': row.get('trainees_accepted', '').strip() or None,
                            'account_type': row.get('account_type', '').strip() or None,
                            'cameras': row.get('cameras', '').strip() or None,
                            'driver_types': row.get('driver_types', '').strip() or None,
                            'drug_test_type': row.get('drug_test_type', '').strip() or None,
                            'experience_levels': row.get('experience_levels', '').strip() or None,
                            'freight_types': row.get('freight_types', '').strip() or None,
                            'sap_required': row.get('sap_required', '').strip() or None,
                            'transmissions': row.get('transmissions', '').strip() or None,
                            'states': row.get('states', '').strip() or None,
                            
                            'is_active': True,
                        }

                        # Find matching job
                        # Using carrier, title, and state/zip for uniqueness
                        query = Job.objects.filter(carrier=carrier, title=job_title)
                        if job_data['state'] != 'Unknown':
                            query = query.filter(state=job_data['state'])
                        
                        existing_job = query.first()

                        if existing_job:
                            if update_existing:
                                for key, value in job_data.items():
                                    if key != 'carrier':
                                        setattr(existing_job, key, value)
                                existing_job.save()
                                jobs_updated += 1
                                self.stdout.write(f'  🔄 Updated: {job_title}')
                            else:
                                jobs_skipped += 1
                                self.stdout.write(self.style.WARNING(f'  ⏭️  Skipped (exists): {job_title}'))
                        else:
                            Job.objects.create(**job_data)
                            jobs_created += 1
                            self.stdout.write(f'  ✅ Created: {job_title}')

                    except Exception as e:
                        errors.append(f'Row {row_num}: {str(e)}')
                        self.stdout.write(self.style.ERROR(f'  ❌ Error row {row_num}: {str(e)}'))
                        continue

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'\n❌ Fatal error: {str(e)}'))
            return

        # Print summary
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS('📊 Import Summary:'))
        self.stdout.write(f'  Carriers created: {carriers_created}')
        self.stdout.write(f'  Jobs created:     {jobs_created}')
        self.stdout.write(f'  Jobs updated:     {jobs_updated}')
        self.stdout.write(f'  Jobs skipped:     {jobs_skipped}')
        self.stdout.write(f'  Errors:           {len(errors)}')
        
        if errors:
            self.stdout.write('\n⚠️  First 5 errors:')
            for error in errors[:5]:
                self.stdout.write(f'    - {error}')
        
        self.stdout.write('='*60 + '\n')

