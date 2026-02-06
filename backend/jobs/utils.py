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


def filter_jobs_by_radius(driver_zip, jobs_queryset):
    """
    Filter jobs to only include those within their hiring radius of the driver's location.
    Also annotates each job with the distance from the driver.
    
    Args:
        driver_zip (str): Driver's zip code
        jobs_queryset: Django QuerySet of Job objects
        
    Returns:
        list: List of dicts with job data and distance information
    """
    driver_lat, driver_lon = get_coordinates_from_zip(driver_zip)
    
    if driver_lat is None or driver_lon is None:
        return []
    
    filtered_jobs = []
    
    for job in jobs_queryset:
        # Get job coordinates
        job_lat = job.latitude
        job_lon = job.longitude
        
        # If job doesn't have coordinates, try to get them from zip code
        if job_lat is None or job_lon is None:
            job_lat, job_lon = get_coordinates_from_zip(job.zip_code)
            
            # Update the job model with coordinates for future use
            if job_lat and job_lon:
                job.latitude = job_lat
                job.longitude = job_lon
                job.save(update_fields=['latitude', 'longitude'])
        
        # Calculate distance
        distance = calculate_distance(driver_lat, driver_lon, job_lat, job_lon)
        
        if distance is not None and distance <= job.hiring_radius_miles:
            job_data = {
                'job': job,
                'distance_miles': distance
            }
            filtered_jobs.append(job_data)
    
    # Sort by distance (closest first)
    filtered_jobs.sort(key=lambda x: x['distance_miles'])
    
    return filtered_jobs
