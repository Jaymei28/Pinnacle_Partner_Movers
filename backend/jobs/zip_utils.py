"""
Zip code extraction and auto-population utilities for jobs.
"""
import re
import requests


# State capital zip codes as fallback
STATE_CAPITAL_ZIPS = {
    'AL': '36104', 'AK': '99801', 'AZ': '85001', 'AR': '72201', 'CA': '95814',
    'CO': '80202', 'CT': '06103', 'DE': '19901', 'FL': '32301', 'GA': '30303',
    'HI': '96813', 'ID': '83702', 'IL': '62701', 'IN': '46204', 'IA': '50319',
    'KS': '66612', 'KY': '40601', 'LA': '70802', 'ME': '04330', 'MD': '21401',
    'MA': '02108', 'MI': '48933', 'MN': '55101', 'MS': '39201', 'MO': '65101',
    'MT': '59601', 'NE': '68502', 'NV': '89701', 'NH': '03301', 'NJ': '08608',
    'NM': '87501', 'NY': '12207', 'NC': '27601', 'ND': '58501', 'OH': '43215',
    'OK': '73102', 'OR': '97301', 'PA': '17101', 'RI': '02903', 'SC': '29201',
    'SD': '57501', 'TN': '37201', 'TX': '78701', 'UT': '84111', 'VT': '05602',
    'VA': '23219', 'WA': '98501', 'WV': '25301', 'WI': '53702', 'WY': '82001'
}


def extract_zip_from_description(description):
    """
    Extract zip code from job description text.
    Prioritizes "Must Live Within X miles of ZIPCODE" pattern.
    
    Args:
        description (str): Job description text
        
    Returns:
        tuple: (zip_code, hiring_radius_miles) or (None, None)
    """
    if not description:
        return None, None
    
    # Pattern 1: "Must Live Within: 25 miles of 33982"
    must_live_pattern = r'Must Live Within[:\s]+(\d+)\s*miles?\s*of\s*(\d{5})'
    match = re.search(must_live_pattern, description, re.IGNORECASE)
    if match:
        radius = int(match.group(1))
        zip_code = match.group(2)
        return zip_code, radius
    
    # Pattern 2: "Hiring Area Zip Code(s): 34269"
    hiring_area_pattern = r'Hiring Area Zip Code\(s\)[:\s]+(\d{5})'
    match = re.search(hiring_area_pattern, description, re.IGNORECASE)
    if match:
        return match.group(1), None
    
    # Pattern 3: Any 5-digit zip code in the text
    zip_pattern = r'\b(\d{5})\b'
    match = re.search(zip_pattern, description)
    if match:
        return match.group(1), None
    
    return None, None


def geocode_location_to_zip(location_string):
    """
    Convert location string (e.g., "Arcadia, FL") to zip code.
    Uses US Census Geocoding API (free, no API key needed).
    
    Args:
        location_string (str): Location in format "City, ST"
        
    Returns:
        str: Zip code or None
    """
    if not location_string:
        return None
    
    # Parse location string
    match = re.match(r'([^,]+),\s*([A-Z]{2})', location_string.strip())
    if not match:
        return None
    
    city, state = match.groups()
    
    url = "https://geocoding.geo.census.gov/geocoder/locations/address"
    params = {
        'city': city.strip(),
        'state': state.strip(),
        'benchmark': 'Public_AR_Current',
        'format': 'json'
    }
    
    try:
        response = requests.get(url, params=params, timeout=5)
        data = response.json()
        
        if data.get('result', {}).get('addressMatches'):
            address = data['result']['addressMatches'][0]
            zip_code = address['addressComponents'].get('zip')
            return zip_code
    except Exception as e:
        print(f"Geocoding error for '{location_string}': {e}")
        return None


def auto_populate_zip_code(job):
    """
    Auto-populate zip code for a job using multiple strategies.
    
    Priority:
    1. Extract from description ("Must Live Within X miles of ZIP")
    2. Geocode from location field
    3. Use carrier headquarters zip
    4. Use state capital as last resort
    
    Args:
        job: Job model instance
        
    Returns:
        tuple: (zip_code, source, hiring_radius) or (None, None, None)
    """
    
    # Strategy 1: Extract from consolidated fields (highest priority)
    all_text = " ".join(filter(None, [
        job.job_details,
        job.pay_details,
        job.equipment_details,
        job.key_disqualifiers,
        job.requirements_details
    ]))
    
    if all_text:
        zip_code, radius = extract_zip_from_description(all_text)
        if zip_code:
            return zip_code, 'extracted', radius
    
    # Strategy 2: Geocode from state field
    if job.state:
        zip_code = geocode_location_to_zip(job.state)
        if zip_code:
            return zip_code, 'geocoded', None
    
    # Strategy 3: Use carrier headquarters
    if job.carrier and job.carrier.headquarters_zip:
        return job.carrier.headquarters_zip, 'carrier_hq', None
    
    # Strategy 4: Use state capital (last resort)
    state_to_check = None
    if job.state and len(job.state.strip()) == 2:
        state_to_check = job.state.strip().upper()
    elif job.requirements_details:
        # Check requirements_details for a 2-letter state code at the start or in common patterns
        match = re.search(r'\b([A-Z]{2})\b', job.requirements_details)
        if match:
            state_to_check = match.group(1)
    
    if state_to_check:
        zip_code = STATE_CAPITAL_ZIPS.get(state_to_check)
        if zip_code:
            return zip_code, 'state_capital', None
    
    return None, None, None
