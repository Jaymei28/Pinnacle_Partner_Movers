"""
Django management command to auto-populate missing zip codes for existing jobs.
"""
from django.core.management.base import BaseCommand
from jobs.models import Job
from jobs.zip_utils import auto_populate_zip_code


class Command(BaseCommand):
    help = 'Auto-populate missing zip codes for existing jobs using intelligent extraction'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force update all jobs, even those with existing zip codes',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be updated without making changes',
        )
    
    def handle(self, *args, **options):
        force = options['force']
        dry_run = options['dry_run']
        
        if force:
            jobs = Job.objects.all()
            self.stdout.write(self.style.WARNING('Force mode: Processing ALL jobs'))
        else:
            jobs = Job.objects.filter(zip_code__isnull=True) | Job.objects.filter(zip_code='')
            self.stdout.write(f'Processing {jobs.count()} jobs without zip codes...')
        
        updated_count = 0
        failed_count = 0
        
        for job in jobs:
            zip_code, source, radius = auto_populate_zip_code(job)
            
            if zip_code:
                if dry_run:
                    self.stdout.write(
                        f'[DRY RUN] Would update "{job.title}": '
                        f'{zip_code} ({source})'
                        + (f' with radius {radius} miles' if radius else '')
                    )
                else:
                    job.zip_code = zip_code
                    job.zip_source = source
                    
                    if radius and source == 'extracted':
                        job.hiring_radius_miles = radius
                    
                    job.save()
                    
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'✓ Updated "{job.title}": '
                            f'{zip_code} ({source})'
                            + (f' with radius {radius} miles' if radius else '')
                        )
                    )
                
                updated_count += 1
            else:
                failed_count += 1
                self.stdout.write(
                    self.style.ERROR(
                        f'✗ Could not find zip code for "{job.title}" '
                        f'(Carrier: {job.carrier.name})'
                    )
                )
        
        # Summary
        self.stdout.write('\n' + '='*60)
        if dry_run:
            self.stdout.write(self.style.WARNING('[DRY RUN] No changes were made'))
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully processed: {updated_count}')
        )
        if failed_count > 0:
            self.stdout.write(
                self.style.ERROR(f'Failed to process: {failed_count}')
            )
            self.stdout.write(
                '\nTip: Add headquarters zip codes to carriers in admin '
                'to improve auto-population success rate.'
            )
