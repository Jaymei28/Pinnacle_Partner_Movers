"""
Django management command to import carriers from XLSX file.
Preserves bold formatting by converting it to markdown-style **bold**.

Usage:
    python manage.py import_carriers_xlsx path/to/carriers.xlsx
"""

from django.core.management.base import BaseCommand
from jobs.models import Carrier
import openpyxl
import os

class Command(BaseCommand):
    help = 'Import carriers from an XLSX file while preserving bold formatting'

    def add_arguments(self, parser):
        parser.add_argument(
            'xlsx_file',
            type=str,
            help='Path to the XLSX file to import'
        )
        parser.add_argument(
            '--update',
            action='store_true',
            help='Update existing carriers instead of skipping them'
        )

    def process_cell(self, cell):
        """
        Process an Excel cell. If it has rich text or bold formatting,
        try to preserve it using markdown markers.
        """
        if cell.value is None:
            return ""
        
        val = str(cell.value).strip()
        if not val:
            return ""

        # Basic bold detection: if the whole cell is bold
        if cell.font and cell.font.bold:
            return f"**{val}**"
        
        # Note: openpyxl doesn't support reading partial bolding (rich text) 
        # as easily as it writes it, but this covers the primary use case
        # (entire lines or headers being bold).
        
        return val

    def handle(self, *args, **options):
        xlsx_file = options['xlsx_file']
        update_existing = options['update']

        if not os.path.exists(xlsx_file):
            self.stdout.write(self.style.ERROR(f'XLSX file not found: {xlsx_file}'))
            return

        self.stdout.write(self.style.SUCCESS(f'\n🏢 Starting carrier import from: {xlsx_file}\n'))

        try:
            wb = openpyxl.load_workbook(xlsx_file, data_only=True)
            sheet = wb.active
            
            # Get headers
            headers = [cell.value for cell in sheet[1]]
            if 'name' not in headers:
                self.stdout.write(self.style.ERROR('Missing required column: name'))
                return

            col_map = {name: i for i, name in enumerate(headers)}
            
            carriers_created = 0
            carriers_updated = 0
            errors = []

            # Iterate rows starting from the second one
            for row_idx, row in enumerate(sheet.iter_rows(min_row=2), start=2):
                try:
                    name_cell = row[col_map['name']]
                    carrier_name = str(name_cell.value or "").strip()
                    
                    if not carrier_name:
                        continue

                    carrier_data = {}
                    for field in headers:
                        if field == 'name': continue
                        cell = row[col_map[field]]
                        
                        # Special handling for potentially multi-line formatted fields
                        multi_line_fields = ['benefit', 'description', 'presentation', 'pre_qualifications', 'app_process']
                        if any(f in field for f in multi_line_fields):
                            # We can't easily get rich text segments from openpyxl
                            # but we can get the whole cell bold status
                            carrier_data[field] = self.process_cell(cell)
                        else:
                            carrier_data[field] = str(cell.value).strip() if cell.value is not None else None

                    # Update or Create
                    existing_carrier = Carrier.objects.filter(name=carrier_name).first()

                    if existing_carrier:
                        if update_existing:
                            for key, value in carrier_data.items():
                                setattr(existing_carrier, key, value)
                            existing_carrier.save()
                            carriers_updated += 1
                            self.stdout.write(f'  🔄 Updated: {carrier_name}')
                        else:
                            self.stdout.write(self.style.WARNING(f'  ⏭️  Skipped: {carrier_name}'))
                    else:
                        Carrier.objects.create(name=carrier_name, **carrier_data)
                        carriers_created += 1
                        self.stdout.write(f'  ✅ Created: {carrier_name}')

                except Exception as e:
                    errors.append(f"Row {row_idx}: {str(e)}")
                    self.stdout.write(self.style.ERROR(f'  ❌ Error in row {row_idx}: {e}'))

            self.stdout.write(f'\n📊 Summary: Created {carriers_created}, Updated {carriers_updated}, Errors {len(errors)}')

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'\n❌ Fatal error: {str(e)}'))
