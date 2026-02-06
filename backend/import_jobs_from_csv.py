import os
import sys
import django
import csv
import re

# Setup Django environment
base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(base_dir)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jobstream_backend.settings')
django.setup()

from jobs.models import Job

def clean_text(text):
    """Clean and normalize text content"""
    if not text or text == 'N/A':
        return None
    # Remove extra whitespace and newlines
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_location_from_lane(lane_info):
    """Extract location from lane information"""
    if not lane_info:
        return "Unknown Location"
    
    # Try to extract location from patterns like "Walmart - Arcadia, FL"
    match = re.search(r'[-–]\s*([A-Za-z\s]+),\s*([A-Z]{2})', lane_info)
    if match:
        city = match.group(1).strip()
        state = match.group(2).strip()
        return f"{city}, {state}"
    
    return lane_info[:100]

def parse_csv_file(file_path):
    """Parse the CSV file and extract job listings"""
    jobs = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        # Read CSV manually to handle duplicate headers
        csv_reader = csv.reader(f)
        headers = next(csv_reader)  # Get headers
        
        print(f"CSV Headers: {headers[:10]}")  # Debug
        
        for idx, row_values in enumerate(csv_reader):
            try:
                # Create a dict manually, using first occurrence of duplicate headers
                row = {}
                for i, header in enumerate(headers):
                    if header not in row and i < len(row_values):  # Only use first occurrence
                        row[header] = row_values[i]
                
                # Extract basic information
                company = clean_text(row.get('Carriers', '')) or 'Unknown Company'
                short_lane_info = clean_text(row.get('Lane Information', ''))  # Now gets column 1
                pay = clean_text(row.get('Pay', ''))
                home_time = clean_text(row.get('Exact Home Time', ''))
                load_unload = clean_text(row.get('Load/Unload', ''))
                driver_type = clean_text(row.get('Driver Type', ''))
                orientation = clean_text(row.get('Orientation', ''))
                benefits = clean_text(row.get('Benefits', ''))
                experience = clean_text(row.get('Experience', ''))
                freight_types = clean_text(row.get('Freight Types', ''))
                state = clean_text(row.get('State', ''))
                additional_pay = clean_text(row.get('Additional Pay Info', ''))
                
                # Get the detailed lane info from column 8 (second "Lane Information")
                detailed_lane_info = row_values[8] if len(row_values) > 8 else ""
                
                # Use short lane info as title
                if short_lane_info:
                    title = short_lane_info
                    location = extract_location_from_lane(title)
                else:
                    title = f"{company} - Unknown Location"
                    location = "Unknown Location"
                
                # Build comprehensive description using detailed lane info
                description_parts = []
                
                if detailed_lane_info:
                    description_parts.append(detailed_lane_info)
                
                if pay:
                    description_parts.append(f"\\n\\n**Pay Information:**\\n{pay}")
                
                if additional_pay:
                    description_parts.append(f"\\n**Additional Pay Info:**\\n{additional_pay}")
                
                if home_time:
                    description_parts.append(f"\\n**Home Time:**\\n{home_time}")
                
                if load_unload:
                    description_parts.append(f"\\n**Load/Unload:**\\n{load_unload}")
                
                if experience:
                    description_parts.append(f"\\n**Experience Required:**\\n{experience}")
                
                if driver_type:
                    description_parts.append(f"\\n**Driver Type:**\\n{driver_type}")
                
                if freight_types:
                    description_parts.append(f"\\n**Freight Types:**\\n{freight_types}")
                
                if orientation:
                    description_parts.append(f"\\n**Orientation:**\\n{orientation}")
                
                description = ''.join(description_parts) if description_parts else "No additional details available."
                
                # Determine equipment type from freight types
                equipment_type = 'Dry Van'  # Default
                if freight_types:
                    if 'Reefer' in freight_types:
                        equipment_type = 'Reefer'
                    elif 'Flatbed' in freight_types:
                        equipment_type = 'Flatbed'
                    elif 'Container' in freight_types or 'Intermodal' in freight_types:
                        equipment_type = 'Intermodal'
                
                # Create job data
                job_data = {
                    'title': title[:200],
                    'company': company[:200],
                    'location': location[:200],
                    'zip_code': '00000',  # Default
                    'description': description,
                    'job_type': 'full-time',
                    
                    # Compensation
                    'salary': pay[:100] if pay else None,
                    'pay_type': 'Weekly' if pay and 'weekly' in pay.lower() else 'CPM' if pay and 'cpm' in pay.lower() else None,
                    
                    # Schedule & Home Time
                    'home_time': home_time[:100] if home_time else None,
                    'schedule_type': home_time[:100] if home_time else None,
                    
                    # Experience & Requirements
                    'experience_required': experience[:100] if experience else None,
                    'requirements': f"Experience: {experience}" if experience else None,
                    
                    # Driver-Specific Fields
                    'driver_type': driver_type[:100] if driver_type else None,
                    'freight_type': load_unload[:100] if load_unload else None,
                    'equipment_type': equipment_type,
                    
                    # Coverage Area
                    'states_covered': state if state else None,
                    
                    # Benefits
                    'benefits': benefits if benefits else None,
                    
                    # Application
                    'apply_link': 'https://classarecruiting.com',
                }
                
                jobs.append(job_data)
                
                # Print first job for debugging
                if idx == 0:
                    print("\\n--- First Job Preview ---")
                    print(f"Title: {job_data['title']}")
                    print(f"Company: {job_data['company']}")
                    print(f"Location: {job_data['location']}")
                    print(f"Salary: {job_data['salary']}")
                    print(f"Home Time: {job_data['home_time']}")
                
            except Exception as e:
                print(f"Error parsing row {idx + 1}: {e}")
                import traceback
                traceback.print_exc()
                continue
    
    return jobs

def import_jobs(csv_file_path):
    """Import jobs from CSV file into database"""
    print(f"Parsing CSV file: {csv_file_path}")
    jobs = parse_csv_file(csv_file_path)
    
    print(f"\\nParsed {len(jobs)} job listings from CSV")
    
    created_count = 0
    updated_count = 0
    
    for job_data in jobs:
        try:
            # Try to find existing job by company and location
            existing_job = Job.objects.filter(
                company=job_data['company'],
                location=job_data['location']
            ).first()
            
            if existing_job:
                # Update existing job
                for key, value in job_data.items():
                    setattr(existing_job, key, value)
                existing_job.save()
                updated_count += 1
                print(f"Updated: {job_data['title']}")
            else:
                # Create new job
                Job.objects.create(**job_data)
                created_count += 1
                print(f"Created: {job_data['title']}")
                
        except Exception as e:
            print(f"Error importing job '{job_data.get('title', 'Unknown')}': {e}")
            import traceback
            traceback.print_exc()
            continue
    
    print(f"\\n{'='*60}")
    print(f"Import Summary:")
    print(f"  Created: {created_count} jobs")
    print(f"  Updated: {updated_count} jobs")
    print(f"  Total:   {created_count + updated_count} jobs")
    print(f"{'='*60}")

if __name__ == '__main__':
    # Path to the CSV file
    csv_file = os.path.join(os.path.dirname(__file__), '..', 'Job Ops.csv')
    
    if not os.path.exists(csv_file):
        print(f"Error: CSV file not found at {csv_file}")
        sys.exit(1)
    
    import_jobs(csv_file)
