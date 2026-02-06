"""
Web Scraping Script for Job Portal Data Import

This script scrapes job and carrier data from an existing website
and imports it into the Django database.

Usage:
    python scrape_jobs.py <website_url>

Requirements:
    pip install beautifulsoup4 requests
"""

import os
import sys
import django
import requests
from bs4 import BeautifulSoup

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from jobs.models import Carrier, Job


def scrape_website(url):
    """
    Scrape job data from the provided URL.
    
    Args:
        url (str): The URL of the website to scrape
    
    Returns:
        list: List of job dictionaries
    """
    print(f"Scraping data from: {url}")
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        jobs_data = []
        
        # TODO: Customize these selectors based on the actual website structure
        # Example: Find all job listings
        job_listings = soup.find_all('div', class_='job-listing')  # Adjust selector
        
        for job_element in job_listings:
            try:
                job_data = {
                    'title': job_element.find('h2', class_='job-title').text.strip(),
                    'carrier_name': job_element.find('span', class_='company-name').text.strip(),
                    'location': job_element.find('span', class_='location').text.strip(),
                    'salary': job_element.find('span', class_='salary').text.strip(),
                    'description': job_element.find('div', class_='description').text.strip(),
                    # Add more fields as needed
                }
                jobs_data.append(job_data)
            except AttributeError as e:
                print(f"Error parsing job element: {e}")
                continue
        
        print(f"Found {len(jobs_data)} jobs")
        return jobs_data
        
    except requests.RequestException as e:
        print(f"Error fetching URL: {e}")
        return []


def get_or_create_carrier(carrier_name):
    """
    Get existing carrier or create a new one.
    
    Args:
        carrier_name (str): Name of the carrier
    
    Returns:
        Carrier: Carrier instance
    """
    carrier, created = Carrier.objects.get_or_create(
        name=carrier_name,
        defaults={
            'description': f'{carrier_name} - Imported from website',
            'is_active': True
        }
    )
    
    if created:
        print(f"Created new carrier: {carrier_name}")
    else:
        print(f"Using existing carrier: {carrier_name}")
    
    return carrier


def import_jobs(jobs_data):
    """
    Import jobs into the database.
    
    Args:
        jobs_data (list): List of job dictionaries
    
    Returns:
        tuple: (created_count, skipped_count)
    """
    created_count = 0
    skipped_count = 0
    
    for job_data in jobs_data:
        try:
            # Get or create carrier
            carrier = get_or_create_carrier(job_data['carrier_name'])
            
            # Check if job already exists
            existing_job = Job.objects.filter(
                carrier=carrier,
                title=job_data['title'],
                location=job_data.get('location', '')
            ).first()
            
            if existing_job:
                print(f"Skipping duplicate: {job_data['title']} at {carrier.name}")
                skipped_count += 1
                continue
            
            # Create new job
            job = Job.objects.create(
                carrier=carrier,
                title=job_data['title'],
                location=job_data.get('location', ''),
                salary=job_data.get('salary', ''),
                description=job_data.get('description', ''),
                # Map additional fields as needed
                job_type='full-time',  # Default
                is_active=True
            )
            
            print(f"Created job: {job.title} at {carrier.name}")
            created_count += 1
            
        except Exception as e:
            print(f"Error creating job: {e}")
            skipped_count += 1
            continue
    
    return created_count, skipped_count


def main():
    """Main execution function."""
    if len(sys.argv) < 2:
        print("Usage: python scrape_jobs.py <website_url>")
        sys.exit(1)
    
    url = sys.argv[1]
    
    print("=" * 60)
    print("Job Portal Data Scraper")
    print("=" * 60)
    
    # Scrape the website
    jobs_data = scrape_website(url)
    
    if not jobs_data:
        print("No jobs found. Please check the URL and CSS selectors.")
        sys.exit(1)
    
    # Import jobs
    print("\nImporting jobs into database...")
    created, skipped = import_jobs(jobs_data)
    
    print("\n" + "=" * 60)
    print(f"Import complete!")
    print(f"Created: {created} jobs")
    print(f"Skipped: {skipped} jobs (duplicates or errors)")
    print("=" * 60)


if __name__ == '__main__':
    main()
