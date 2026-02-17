"""
Geocoding and distance calculation utilities for job location filtering.
"""
from math import radians, cos, sin, asin, sqrt
import pgeocode


# Initialize the geocoder (singleton pattern)
_nomi = None

def get_geocoder():
    """Get or create the pgeocode Nominatim instance for US zip codes."""
    global _nomi
    if _nomi is None:
        _nomi = pgeocode.Nominatim('us')
    return _nomi


def get_coordinates_from_zip(zip_code):
    """
    Convert a US zip code to latitude and longitude coordinates.
    
    Args:
        zip_code (str): 5-digit US zip code
        
    Returns:
        tuple: (latitude, longitude) or (None, None) if not found
    """
    if not zip_code:
        return None, None
    
    nomi = get_geocoder()
    location = nomi.query_postal_code(str(zip_code).strip())
    
    if location is not None and not location.empty:
        lat = location.get('latitude')
        lon = location.get('longitude')
        if lat and lon and not (str(lat) == 'nan' or str(lon) == 'nan'):
            return float(lat), float(lon)
    
    return None, None


def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points on Earth.
    Uses the Haversine formula.
    
    Args:
        lat1, lon1: Latitude and longitude of first point
        lat2, lon2: Latitude and longitude of second point
        
    Returns:
        float: Distance in miles
    """
    if None in [lat1, lon1, lat2, lon2]:
        return None
    
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [float(lat1), float(lon1), float(lat2), float(lon2)])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    
    # Radius of Earth in miles
    miles = 3956 * c
    return round(miles, 1)


def filter_jobs_by_radius(driver_zip, jobs_queryset, max_radius=250):
    """
    Filter and sort jobs using a flexible multi-tier strategy:
    1. Distance Match (In Radius): Jobs within their specific hiring radius or 250 miles.
    2. Proximity Match (Nearest): Top nearest jobs even if slightly outside radius.
    3. State Match: Jobs in the driver's state.
    
    Args:
        driver_zip (str): Driver's zip code
        jobs_queryset: Django QuerySet of Job objects
        max_radius (int): Maximum default search radius in miles (default: 250)
        
    Returns:
        list: List of dicts with job data, distance, and location_source information
    """
    driver_lat, driver_lon = get_coordinates_from_zip(driver_zip)
    
    if driver_lat is None or driver_lon is None:
        # If driver ZIP is invalid, we can only do state-level match if we can find the state
        nomi = get_geocoder()
        driver_location = nomi.query_postal_code(str(driver_zip).strip())
        driver_state = driver_location.get('state_code') if driver_location is not None else None
        
        if not driver_state:
            return []
    else:
        # Get driver's state for state-level matching
        nomi = get_geocoder()
        driver_location = nomi.query_postal_code(str(driver_zip).strip())
        driver_state = driver_location.get('state_code') if driver_location is not None else None
    
    all_scored_jobs = []
    
    for job in jobs_queryset:
        # Collect all possible locations for this job
        locations = []
        
        # 1. Main location from Job model
        locations.append({
            'lat': job.latitude,
            'lon': job.longitude,
            'zip': job.zip_code,
            'state': job.state,
            'source': job.location_source,
            'hiring_radius': job.hiring_radius_miles
        })
        
        # 2. Additional locations from JobLocation model
        for loc in job.additional_locations.all():
            locations.append({
                'lat': loc.latitude,
                'lon': loc.longitude,
                'zip': loc.zip_code,
                'state': loc.state,
                'source': 'additional_location',
                'hiring_radius': job.hiring_radius_miles # Use job's global hiring radius
            })

        best_job_score = None

        for loc_data in locations:
            job_lat = loc_data['lat']
            job_lon = loc_data['lon']
            location_source = loc_data['source']
            job_state_raw = loc_data['state']
            job_zip = loc_data['zip']
            
            # If coordinates are missing, try to geocode if it's the main location or additional location
            if (job_lat is None or job_lon is None) and location_source != 'state_only':
                # For main location, we can try to geocode and save it
                if location_source != 'additional_location':
                    from .geocoding import get_job_location
                    job_lat, job_lon, location_source = get_job_location(job)
                    if job_lat and job_lon:
                        job.latitude = job_lat
                        job.longitude = job_lon
                        job.location_source = location_source
                        job.save(update_fields=['latitude', 'longitude', 'location_source'])
                # For additional locations, they should be geocoded on save, but we can try fallback
                elif job_zip:
                    job_lat, job_lon = get_coordinates_from_zip(job_zip)

            distance = None
            if driver_lat is not None and job_lat is not None:
                distance = calculate_distance(driver_lat, driver_lon, job_lat, job_lon)

            match_type = None
            priority = 99

            # Tier 1: In Radius
            if distance is not None:
                job_radius = loc_data['hiring_radius'] if loc_data['hiring_radius'] else max_radius
                if distance <= job_radius:
                    match_type = 'distance'
                    priority = 1
                else:
                    # Tier 2: Proximity (Nearest fallback)
                    match_type = 'proximity'
                    priority = 2
            
            # Tier 3: State Level
            if not match_type or match_type == 'proximity':
                job_state = job_state_raw.upper() if job_state_raw else None
                if job_state and ',' in job_state:
                    job_state = job_state.split(',')[-1].strip()
                
                if driver_state and job_state == driver_state:
                    if not match_type:
                        match_type = 'state_level'
                        priority = 3
                    if match_type == 'proximity':
                        priority = 1.5 

            if match_type:
                MAX_PROXIMITY_MILES = 500
                is_far = distance is not None and distance > MAX_PROXIMITY_MILES
                is_state_match = (match_type == 'state_level' or priority == 1.5)
                
                if is_far and not is_state_match:
                    continue

                # Store the score for this location
                score = {
                    'distance_miles': distance,
                    'location_source': location_source,
                    'match_type': match_type,
                    'priority': priority,
                    'zip_code': job_zip
                }
                
                # Check if this location is better than previously found locations for THIS job
                if best_job_score is None or \
                   score['priority'] < best_job_score['priority'] or \
                   (score['priority'] == best_job_score['priority'] and 
                    (score['distance_miles'] or 9999) < (best_job_score['distance_miles'] or 9999)):
                    best_job_score = score

        # If any location for this job matched, add it to the final result
        if best_job_score:
            all_scored_jobs.append({
                'job': job,
                **best_job_score
            })
    
    # Sorting across ALL jobs
    all_scored_jobs.sort(key=lambda x: (x['priority'], x['distance_miles'] if x['distance_miles'] is not None else 9999))
    return all_scored_jobs[:50]
