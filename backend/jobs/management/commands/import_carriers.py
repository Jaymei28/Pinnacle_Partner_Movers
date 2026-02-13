"""
Django management command to import carriers from CSV file.

Usage:
    python manage.py import_carriers path/to/carriers.csv
"""

from django.core.management.base import BaseCommand
from jobs.models import Carrier
import csv
import os


class Command(BaseCommand):
    help = 'Import carriers from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument(
            'csv_file',
            type=str,
            help='Path to the CSV file to import'
        )
        parser.add_argument(
            '--update',
            action='store_true',
            help='Update existing carriers instead of skipping them'
        )

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        update_existing = options['update']

        if not os.path.exists(csv_file):
            self.stdout.write(self.style.ERROR(f'CSV file not found: {csv_file}'))
            return

        self.stdout.write(self.style.SUCCESS(f'\n🏢 Starting carrier import from: {csv_file}\n'))

        # Read and process CSV
        carriers_created = 0
        carriers_updated = 0
        carriers_skipped = 0
        errors = []

        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                # Validate required columns
                if 'name' not in reader.fieldnames:
                    self.stdout.write(self.style.ERROR('Missing required column: name'))
                    return

                for row_num, row in enumerate(reader, start=2):  # Start at 2 (header is row 1)
                    try:
                        # Get carrier name
                        carrier_name = row.get('name', '').strip()
                        if not carrier_name:
                            errors.append(f'Row {row_num}: Missing carrier name')
                            continue

                        # Prepare carrier data
                        carrier_data = {
                            'description': row.get('description', '').strip() or None,
                            'website': row.get('website', '').strip() or None,
                            'contact_email': row.get('contact_email', '').strip() or None,
                            'contact_phone': row.get('contact_phone', '').strip() or None,
                            'headquarters_zip': row.get('headquarters_zip', '').strip() or None,
                            'headquarters_city': row.get('headquarters_city', '').strip() or None,
                            'headquarters_state': row.get('headquarters_state', '').strip() or None,
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

                        # Check if carrier already exists
                        existing_carrier = Carrier.objects.filter(name=carrier_name).first()

                        if existing_carrier:
                            if update_existing:
                                # Update existing carrier
                                for key, value in carrier_data.items():
                                    setattr(existing_carrier, key, value)
                                existing_carrier.save()
                                carriers_updated += 1
                                self.stdout.write(f'  🔄 Updated: {carrier_name}')
                            else:
                                carriers_skipped += 1
                                self.stdout.write(self.style.WARNING(f'  ⏭️  Skipped (exists): {carrier_name}'))
                        else:
                            # Create new carrier
                            carrier = Carrier.objects.create(name=carrier_name, **carrier_data)
                            carriers_created += 1
                            self.stdout.write(f'  ✅ Created: {carrier_name}')

                    except Exception as e:
                        error_msg = f'Row {row_num}: {str(e)}'
                        errors.append(error_msg)
                        self.stdout.write(self.style.ERROR(f'  ❌ Error: {error_msg}'))
                        continue

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'\n❌ Fatal error reading CSV: {str(e)}'))
            return

        # Print summary
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS('📊 Import Summary:'))
        self.stdout.write(f'  Carriers created: {carriers_created}')
        self.stdout.write(f'  Carriers updated: {carriers_updated}')
        self.stdout.write(f'  Carriers skipped: {carriers_skipped}')
        
        if errors:
            self.stdout.write(self.style.WARNING(f'  Errors:          {len(errors)}'))
            self.stdout.write('\n⚠️  Errors encountered:')
            for error in errors[:10]:  # Show first 10 errors
                self.stdout.write(f'    - {error}')
            if len(errors) > 10:
                self.stdout.write(f'    ... and {len(errors) - 10} more')
        
        self.stdout.write('='*60 + '\n')
        
        if carriers_created > 0 or carriers_updated > 0:
            self.stdout.write(self.style.SUCCESS('✅ Carrier import completed successfully!\n'))
        else:
            self.stdout.write(self.style.WARNING('⚠️  No carriers were imported.\n'))
