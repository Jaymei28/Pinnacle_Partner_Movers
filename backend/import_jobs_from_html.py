import os
import sys
import django
from bs4 import BeautifulSoup
import re

# Setup Django environment
base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(base_dir)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jobstream_backend.settings')
django.setup()

from jobs.models import Job

def clean_text(text):
    """Clean and normalize text content"""
    if not text:
        return ""
    # Remove extra whitespace and newlines
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_location_and_state(location_text):
    """Extract location and state from location text"""
    # Pattern: "City, State" or "Company - City, State"
    match = re.search(r'([A-Za-z\s]+),\s*([A-Z]{2})', location_text)
    if match:
        city = match.group(1).strip()
        state = match.group(2).strip()
        return f"{city}, {state}", state
    return location_text, ""

def extract_company_name(location_text, company_tag):
    """Extract company name from tags or location text"""
    if company_tag:
        return clean_text(company_tag)
    
    # Try to extract from location text (e.g., "Walmart - Harrisonville, MO")
    match = re.match(r'([^-]+)\s*-', location_text)
    if match:
        return match.group(1).strip()
    
    return "Class A Recruiting"

def parse_html_file(file_path):
    """Parse the HTML file and extract job listings"""
    with open(file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find all job listing items
    job_items = soup.find_all('div', {'role': 'listitem', 'data-testid': 'list-item'})
    
    print(f"\nFound {len(job_items)} job items in HTML")
    
    jobs = []
    
    for idx, item in enumerate(job_items):
        try:
            # Extract all fields using flexible search
            company_elem = item.find(attrs={'data-softr-field-id': '_gicjcwgov'})
            company_text = company_elem.get_text(strip=True) if company_elem else ""
            
            title_elem = item.find(attrs={'data-softr-field-id': '_nr67crtk9'})
            title_text = title_elem.get_text(strip=True) if title_elem else ""
            
            # Salary fields - try both basic and detailed
            salary_elem = item.find(attrs={'data-softr-field-id': '_uxv926gfo'})
            salary_text = salary_elem.get_text(strip=True) if salary_elem else ""
            
            pay_details_elem = item.find(attrs={'data-softr-field-id': '_v1qt13aoq'})
            pay_details = pay_details_elem.get_text(strip=True) if pay_details_elem else ""
            
            # Use detailed pay info if available, otherwise use basic salary
            if pay_details and 'Pay Details' in pay_details:
                salary_text = pay_details.replace('Pay Details', '').strip() or salary_text
            
            # Home time fields - try both
            home_time_elem = item.find(attrs={'data-softr-field-id': '_ws49360zq'})
            home_time_text = home_time_elem.get_text(strip=True) if home_time_elem else ""
            
            exact_home_time_elem = item.find(attrs={'data-softr-field-id': '_w0q9cb9mz'})
            exact_home_time = exact_home_time_elem.get_text(strip=True) if exact_home_time_elem else ""
            
            if exact_home_time and 'Exact Home Time' in exact_home_time:
                home_time_text = exact_home_time.replace('Exact Home Time', '').strip() or home_time_text
            
            # Experience
            experience_elem = item.find(attrs={'data-softr-field-id': '_0mezxqo33'})
            experience_text = experience_elem.get_text(strip=True) if experience_elem else ""
            
            # Driver type - try both fields
            driver_type_elem = item.find(attrs={'data-softr-field-id': '_saga7u800'})
            driver_type_text = driver_type_elem.get_text(strip=True) if driver_type_elem else ""
            
            driver_type_detailed_elem = item.find(attrs={'data-softr-field-id': '_fwf1wek87'})
            driver_type_detailed = driver_type_detailed_elem.get_text(strip=True) if driver_type_detailed_elem else ""
            
            if driver_type_detailed and 'Driver Type' in driver_type_detailed:
                driver_type_text = driver_type_detailed.replace('Driver Type', '').strip() or driver_type_text
            
            # Freight type
            freight_type_elem = item.find(attrs={'data-softr-field-id': '_jeqx1ya4b'})
            freight_type_text = freight_type_elem.get_text(strip=True) if freight_type_elem else ""
            
            load_unload_elem = item.find(attrs={'data-softr-field-id': '_cis5bvzg2'})
            load_unload = load_unload_elem.get_text(strip=True) if load_unload_elem else ""
            
            if load_unload and 'Load/Unload' in load_unload:
                freight_type_text = load_unload.replace('Load/Unload', '').strip() or freight_type_text
            
            # States
            state_elems = item.find_all(attrs={'data-softr-field-id': '_e6sd7p6ya'})
            states = [elem.get_text(strip=True) for elem in state_elems]
            # Split combined states like "ALGA" into ["AL", "GA"]
            expanded_states = []
            for state in states:
                if len(state) > 2:
                    # Split into 2-character chunks
                    expanded_states.extend([state[i:i+2] for i in range(0, len(state), 2)])
                else:
                    expanded_states.append(state)
            states_covered = ', '.join(expanded_states) if expanded_states else None
            
            # Lane Information / Full Description
            lane_info_elem = item.find(attrs={'data-softr-field-id': '_lksgonkue'})
            lane_info = lane_info_elem.get_text(strip=True) if lane_info_elem else ""
            
            # Additional Pay Info
            additional_pay_elem = item.find(attrs={'data-softr-field-id': '_eceq879ao'})
            additional_pay = additional_pay_elem.get_text(strip=True) if additional_pay_elem else ""
            
            # Orientation
            orientation_elem = item.find(attrs={'data-softr-field-id': '_1xl3peqa8'})
            orientation = orientation_elem.get_text(strip=True) if orientation_elem else ""
            
            # Benefits
            benefits_elem = item.find(attrs={'data-softr-field-id': '_590iwtqgx'})
            benefits_text = benefits_elem.get_text(strip=True) if benefits_elem else ""
            
            # Debug output for first 3 jobs
            if idx < 3:
                print(f"\n--- Job {idx + 1} Debug ---")
                print(f"Company: '{company_text}'")
                print(f"Title: '{title_text}'")
                print(f"Salary: '{salary_text}'")
                print(f"Home Time: '{home_time_text}'")
                print(f"Experience: '{experience_text}'")
                print(f"Driver Type: '{driver_type_text}'")
                print(f"Freight Type: '{freight_type_text}'")
                print(f"States: {expanded_states}")
                print(f"Lane Info: '{lane_info[:100]}'...")
                print(f"Benefits: '{benefits_text[:100]}'...")
            
            # Parse location and extract state
            location, state = extract_location_and_state(title_text)
            company = extract_company_name(title_text, company_text)
            
            # Build comprehensive description
            description_parts = []
            
            # Add lane information as primary description if available
            if lane_info:
                # Clean up lane info
                lane_info_clean = lane_info.replace('Lane Information', '').strip()
                if lane_info_clean:
                    description_parts.append(lane_info_clean)
            
            # Add structured information
            if salary_text:
                description_parts.append(f"**Pay:** {salary_text}")
            if additional_pay:
                additional_pay_clean = additional_pay.replace('Additional Pay Info', '').strip()
                if additional_pay_clean:
                    description_parts.append(f"**Additional Pay Info:** {additional_pay_clean}")
            if home_time_text:
                description_parts.append(f"**Home Time:** {home_time_text}")
            if experience_text:
                description_parts.append(f"**Experience Required:** {experience_text}")
            if driver_type_text:
                description_parts.append(f"**Driver Type:** {driver_type_text}")
            if freight_type_text:
                description_parts.append(f"**Freight Type:** {freight_type_text}")
            if expanded_states:
                description_parts.append(f"**States:** {', '.join(expanded_states)}")
            if orientation:
                orientation_clean = orientation.replace('Orientation', '').strip()
                if orientation_clean:
                    description_parts.append(f"**Orientation:** {orientation_clean}")
            
            description = "\n\n".join(description_parts) if description_parts else "No additional details available."
            
            # Determine equipment type from title or freight type
            equipment_type = None
            if 'reefer' in title_text.lower():
                equipment_type = 'Reefer'
            elif 'flatbed' in title_text.lower():
                equipment_type = 'Flatbed'
            elif 'intermodal' in title_text.lower():
                equipment_type = 'Intermodal'
            else:
                equipment_type = 'Dry Van'
            
            # Create job data with all fields
            job_data = {
                'title': clean_text(title_text)[:200],
                'company': company[:200],
                'location': location[:200],
                'zip_code': '00000',  # Default zip code
                'description': description,
                'job_type': 'full-time',
                
                # Compensation
                'salary': salary_text[:100] if salary_text else None,
                'pay_type': 'Weekly' if salary_text and 'weekly' in salary_text.lower() else 'Hourly' if salary_text and 'hour' in salary_text.lower() else None,
                
                # Schedule & Home Time
                'home_time': home_time_text[:100] if home_time_text else None,
                'schedule_type': home_time_text[:100] if home_time_text else None,
                
                # Experience & Requirements
                'experience_required': experience_text[:100] if experience_text else None,
                'requirements': f"Experience: {experience_text}" if experience_text else None,
                
                # Driver-Specific Fields
                'driver_type': driver_type_text[:100] if driver_type_text else None,
                'freight_type': freight_type_text[:100] if freight_type_text else None,
                'equipment_type': equipment_type,
                
                # Coverage Area
                'states_covered': states_covered,
                
                # Benefits
                'benefits': benefits_text if benefits_text else None,
                
                # Application
                'apply_link': 'https://classarecruiting.com',
            }
            
            jobs.append(job_data)
            
        except Exception as e:
            print(f"Error parsing job item {idx}: {e}")
            import traceback
            traceback.print_exc()
            continue
    
    return jobs

def import_jobs(html_file_path):
    """Import jobs from HTML file into database"""
    print(f"Parsing HTML file: {html_file_path}")
    jobs = parse_html_file(html_file_path)
    
    print(f"\nParsed {len(jobs)} job listings")
    
    created_count = 0
    updated_count = 0
    
    for job_data in jobs:
        try:
            # Try to find existing job by title and company
            existing_job = Job.objects.filter(
                title=job_data['title'],
                company=job_data['company']
            ).first()
            
            if existing_job:
                # Update existing job with all new fields
                for key, value in job_data.items():
                    setattr(existing_job, key, value)
                existing_job.save()
                updated_count += 1
            else:
                # Create new job
                Job.objects.create(**job_data)
                created_count += 1
                
        except Exception as e:
            print(f"Error importing job '{job_data.get('title', 'Unknown')}': {e}")
            import traceback
            traceback.print_exc()
            continue
    
    print(f"\n{'='*60}")
    print(f"Import Summary:")
    print(f"  Created: {created_count} jobs")
    print(f"  Updated: {updated_count} jobs")
    print(f"  Total:   {created_count + updated_count} jobs")
    print(f"{'='*60}")

if __name__ == '__main__':
    # Path to the HTML file
    html_file = os.path.join(os.path.dirname(__file__), '..', 'Job Search.html')
    
    if not os.path.exists(html_file):
        print(f"Error: HTML file not found at {html_file}")
        sys.exit(1)
    
    import_jobs(html_file)
