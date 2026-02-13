"""
Geocoding utilities for ZIP code-based job search.
Uses ZipCodeAPI for converting ZIP codes to lat/long coordinates.
"""

import requests
from typing import Tuple, Optional


def geocode_zip(zip_code: str) -> Tuple[Optional[float], Optional[float]]:
    """
    Convert ZIP code to latitude/longitude using pgeocode (local) with external fallback.
    
    Args:
        zip_code: US ZIP code (5 digits)
    
    Returns:
        Tuple of (latitude, longitude) or (None, None) if geocoding fails
    """
    if not zip_code:
        return None, None
    
    clean_zip = str(zip_code).strip()[:5]
    if not clean_zip.isdigit() or len(clean_zip) < 5:
        return None, None

    # Try local pgeocode first for speed and consistency
    try:
        from .utils import get_coordinates_from_zip
        lat, lng = get_coordinates_from_zip(clean_zip)
        if lat is not None and lng is not None:
            return lat, lng
    except ImportError:
        pass

    # Fallback: Use Zippopotam.us (free, no key required)
    try:
        url = f"https://api.zippopotam.us/us/{clean_zip}"
        response = requests.get(url, timeout=3)
        
        if response.status_code == 200:
            data = response.json()
            if 'places' in data and len(data['places']) > 0:
                place = data['places'][0]
                return float(place.get('latitude')), float(place.get('longitude'))
    except Exception as e:
        print(f"Geocoding fallback error for ZIP {clean_zip}: {e}")
    
    return None, None


def get_job_location(job) -> Tuple[Optional[float], Optional[float], str]:
    """
    Determine best location for a job using multi-tier strategy.
    
    Tier 1: Use job's ZIP code (if available)
    Tier 2: Use carrier's headquarters ZIP (if available)
    Tier 3: State-level only (no geocoding)
    
    Args:
        job: Job model instance
    
    Returns:
        Tuple of (latitude, longitude, location_source)
        location_source will be: 'job_zip', 'carrier_hq', or 'state_only'
    """
    
    # Tier 1: Job ZIP Code
    if job.zip_code:
        lat, lng = geocode_zip(job.zip_code)
        if lat is not None and lng is not None:
            return lat, lng, 'job_zip'
    
    # Tier 2: Carrier Headquarters ZIP
    if job.carrier and job.carrier.headquarters_zip:
        lat, lng = geocode_zip(job.carrier.headquarters_zip)
        if lat is not None and lng is not None:
            return lat, lng, 'carrier_hq'
    
    # Tier 3: State-level only (no specific coordinates)
    return None, None, 'state_only'


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great circle distance between two points on Earth.
    Uses the Haversine formula.
    
    Args:
        lat1, lon1: Latitude and longitude of first point (in degrees)
        lat2, lon2: Latitude and longitude of second point (in degrees)
    
    Returns:
        Distance in miles
    """
    from math import radians, cos, sin, asin, sqrt
    
    # Convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    
    # Radius of Earth in miles
    r = 3956
    
    return c * r
