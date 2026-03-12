from django.db import models
import logging

logger = logging.getLogger(__name__)




class Carrier(models.Model):
    """
    Represents a trucking company/carrier with company-level information and benefits.
    """
    # Basic Company Information
    name = models.CharField(max_length=200, unique=True, help_text="Company name (e.g., Swift Transportation)")
    logo = models.ImageField(upload_to='carrier_logos/', blank=True, null=True, help_text="Company logo")
    description = models.TextField(blank=True, null=True, help_text="Company overview/description")
    website = models.URLField(blank=True, null=True, help_text="Company website URL")
    contact_email = models.EmailField(blank=True, null=True, help_text="Primary contact email")
    contact_phone = models.CharField(max_length=20, blank=True, null=True, help_text="Primary contact phone")
    
    # Company Benefits & Info
    benefit_401k = models.TextField(blank=True, null=True, help_text="401(k) retirement plan details")
    benefit_disability_life = models.TextField(blank=True, null=True, help_text="Disability, life, accident & critical illness coverage")
    benefit_stock_purchase = models.TextField(blank=True, null=True, help_text="Stock purchase program details")
    benefit_medical_dental_vision = models.TextField(blank=True, null=True, help_text="Medical, dental & vision plans")
    benefit_paid_vacation = models.TextField(blank=True, null=True, help_text="Paid vacation policy")
    benefit_prescription_drug = models.TextField(blank=True, null=True, help_text="Prescription drug plans")
    benefit_weekly_paycheck = models.TextField(blank=True, null=True, help_text="Weekly paycheck information")
    benefit_driver_ranking_bonus = models.TextField(blank=True, null=True, help_text="Driver ranking bonus details")
    benefit_military_program = models.TextField(blank=True, null=True, help_text="Military benefits program")
    benefit_tuition_program = models.TextField(blank=True, null=True, help_text="Debt-free tuition program details")
    benefit_other = models.TextField(blank=True, null=True, help_text="Any other benefits")
    
    # Process & Qualifications
    presentation = models.TextField(blank=True, null=True, help_text="Carrier presentation details (paste table data here)")
    pre_qualifications = models.TextField(blank=True, null=True, help_text="Pre-qualification requirements (paste table data here)")
    app_process = models.TextField(blank=True, null=True, help_text="Application process instructions")
    
    # Headquarters Location (for job zip code fallback)
    headquarters_zip = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        help_text="Headquarters zip code (used as fallback for jobs without specific location)"
    )
    headquarters_city = models.CharField(max_length=100, blank=True, null=True)
    headquarters_state = models.CharField(max_length=2, blank=True, null=True)
    
    # Metadata
    is_active = models.BooleanField(default=True, help_text="Whether this carrier is active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        verbose_name = "Carrier"
        verbose_name_plural = "Carriers"


class Job(models.Model):
    """
    Represents a job posting from a carrier.
    """
    
    # Relationship to Carrier
    carrier = models.ForeignKey(
        Carrier, 
        on_delete=models.CASCADE, 
        related_name='jobs',
        help_text="The carrier/company posting this job"
    )
    
    # ========== SECTION 1: BASIC INFORMATION ==========
    title = models.CharField(max_length=200, help_text="Job title/position")
    state = models.CharField(max_length=200, blank=True, null=True, help_text="Primary state for the job")
    zip_code = models.CharField(max_length=10, blank=True, null=True, help_text="Location zip code")
    hiring_radius_miles = models.IntegerField(default=50, help_text="Hiring radius in miles")
    
    # ========== SECTION 2: CONSOLIDATED FIELDS (1 Field Per Section) ==========
    
    # 1. Job Details (Includes highlights, account overview, etc.)
    job_details = models.TextField(
        blank=True, 
        null=True, 
        help_text="Paste all job description details, account overview, and highlights here."
    )
    
    # 2. Pay Details (Includes range, weekly pay, bonuses, etc.)
    pay_details = models.TextField(
        blank=True, 
        null=True, 
        help_text="Paste all pay details, bonuses, and compensation info here."
    )
    
    # 3. Equipment (Includes engine, bunks, transmissions, cameras, etc.)
    equipment_details = models.TextField(
        blank=True, 
        null=True, 
        help_text="Paste all equipment-related details here."
    )
    
    # 4. Key Disqualifiers (Standalone field)
    key_disqualifiers = models.TextField(
        blank=True, 
        null=True, 
        help_text="Key disqualifiers for this job."
    )
    
    multi_zip_codes = models.TextField(
        blank=True, 
        null=True, 
        help_text="Paste multiple locations here. Format: '25401 (Martinsburg), 07001 (Avenel)'. States will be auto-detected."
    )
    
    # 5. Requirements (Includes experience, drug test, sap, states, etc.)
    requirements_details = models.TextField(
        blank=True, 
        null=True, 
        help_text="Paste all job requirements and qualification details here."
    )
    
    HIRING_STATUS_CHOICES = [
        ('open', 'Open to hiring'),
        ('full', 'Marked as full'),
    ]
    hiring_status = models.CharField(
        max_length=10, 
        choices=HIRING_STATUS_CHOICES, 
        default='open',
        help_text="Current hiring status of the job"
    )

    # Metadata & Tracking
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    location_source = models.CharField(max_length=50, blank=True, null=True)
    zip_source = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    source_create_date = models.CharField(max_length=100, blank=True, null=True)
    source_modified_date = models.CharField(max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        # 1. If primary zip is missing but multi-zip is present, take the first one
        if not self.zip_code and self.multi_zip_codes:
            import re
            match = re.search(r'(\d{5})', self.multi_zip_codes)
            if match:
                self.zip_code = match.group(1)
                self.zip_source = 'from_multi'
                
                # Also try to get state if missing
                if not self.state:
                    from .utils import get_geocoder
                    nomi = get_geocoder()
                    loc = nomi.query_postal_code(self.zip_code)
                    if loc is not None and not loc.empty:
                        self.state = loc.get('state_code') or "Unknown"

        # 2. Auto-populate zip code if still missing
        if not self.zip_code or not self.zip_source:
            from .zip_utils import auto_populate_zip_code
            zip_code, source, radius = auto_populate_zip_code(self)
            
            if zip_code and not self.zip_code:
                self.zip_code = zip_code
                self.zip_source = source
                
                # Update hiring radius if extracted from description
                if radius and source == 'extracted':
                    self.hiring_radius_miles = radius
        
        # Auto-populate geocoding fields for distance-based search
        if not self.latitude or not self.longitude:
            from .geocoding import get_job_location
            lat, lng, source = get_job_location(self)
            self.latitude = lat
            self.longitude = lng
            self.location_source = source
        
        super().save(*args, **kwargs)

        # Process multi_zip_codes if present
        if self.multi_zip_codes:
            self.process_multi_zip_codes()

    def process_multi_zip_codes(self):
        """
        Parses multi_zip_codes field and creates JobLocation records.
        Format: "25401 (Martinsburg), 07001 (Avenel)"
        """
        import re
        from .utils import get_geocoder
        
        # Split by comma
        entries = [e.strip() for e in self.multi_zip_codes.split(',') if e.strip()]
        
        # Keep track of existing zips to avoid duplicates
        existing_zips = set(self.additional_locations.values_list('zip_code', flat=True))
        if self.zip_code:
            existing_zips.add(self.zip_code)

        nomi = get_geocoder()
        
        for entry in entries:
            # Match ZIP (City) or just ZIP
            match = re.search(r'(\d{5})(?:\s*\(([^)]+)\))?', entry)
            if match:
                zip_code = match.group(1)
                city_input = match.group(2)
                
                if zip_code in existing_zips:
                    continue
                
                # Get state and city fallback from pgeocode
                location = nomi.query_postal_code(zip_code)
                state = "Unknown"
                city = city_input or "Unknown"
                
                if location is not None and not location.empty:
                    state = location.get('state_code') or "Unknown"
                    if not city_input:
                        city = location.get('place_name') or "Unknown"
                
                # Create the location
                from .models import JobLocation
                JobLocation.objects.create(
                    job=self,
                    zip_code=zip_code,
                    city=city,
                    state=state
                )
                existing_zips.add(zip_code)
    
    def __str__(self):
        return f"{self.title} at {self.carrier.name}"
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Job"
        verbose_name_plural = "Jobs"


class JobLocation(models.Model):
    """
    Represents an additional location for a job posting.
    Supports jobs that hire in multiple cities or zip codes.
    """
    job = models.ForeignKey(
        Job, 
        on_delete=models.CASCADE, 
        related_name='additional_locations',
        help_text="The job this location belongs to"
    )
    city = models.CharField(max_length=100, blank=True, null=True, help_text="City name")
    state = models.CharField(max_length=100, help_text="State (e.g., TX or Texas)")
    zip_code = models.CharField(max_length=10, help_text="Zip code for this location")
    
    # Geocoding data for this specific location
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Auto-populate geocoding fields for this location if missing
        if not self.latitude or not self.longitude:
            try:
                from .utils import get_coordinates_from_zip
                lat, lon = get_coordinates_from_zip(self.zip_code)
                if lat and lon:
                    self.latitude = lat
                    self.longitude = lon
            except Exception as e:
                logger.error(f"Error geocoding JobLocation {self.zip_code}: {e}")
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.city or ''} {self.state} {self.zip_code}".strip()

    class Meta:
        verbose_name = "Additional Location"
        verbose_name_plural = "Additional Locations"


class Academy(models.Model):
    """
    Represents a CDL training academy offered by a carrier (e.g., Swift Academy).
    These are entry-level training programs, NOT job postings for experienced drivers.
    """
    # Relationship to Carrier
    carrier = models.ForeignKey(
        Carrier,
        on_delete=models.CASCADE,
        related_name='academies',
        help_text="The carrier sponsoring this academy"
    )

    # ========== SECTION 1: BASIC IDENTIFICATION & LOCATION ==========
    name = models.CharField(max_length=200, help_text="Academy name (e.g., Swift Academy - Phoenix)")
    city = models.CharField(max_length=100, blank=True, null=True, help_text="City where academy is located")
    state = models.CharField(max_length=2, blank=True, null=True, help_text="State abbreviation")
    zip_code = models.CharField(max_length=10, blank=True, null=True, help_text="Academy zip code")

    # ========== SECTION 2: TRAINING DETAILS ==========
    training_type = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Type of training: In-Person, Streaming/Virtual, ELDT Only, etc."
    )
    program_length_days = models.IntegerField(
        blank=True,
        null=True,
        help_text="Approximate length of the academy program in days"
    )
    tuition_cost = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Tuition cost for the program (e.g., '$1,995')"
    )
    tuition_notes = models.TextField(
        blank=True,
        null=True,
        help_text="Notes on tuition financing, debt-free program, payback terms, etc."
    )

    # ========== SECTION 3: PAY DURING TRAINING ==========
    trainee_pay = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Pay rate while in training (e.g., '$300/week' or 'Unpaid')"
    )
    orientation_pay = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Pay once officially hired for orientation (e.g., '$300 paid if officially hired')"
    )

    # ========== SECTION 4: REQUIREMENTS & NOTES ==========
    requirements = models.TextField(
        blank=True,
        null=True,
        help_text="Requirements to enroll (age, background check, medical, etc.)"
    )
    academy_details = models.TextField(
        blank=True,
        null=True,
        help_text="General academy info, schedule, what to expect, orientations, etc."
    )
    after_graduation = models.TextField(
        blank=True,
        null=True,
        help_text="What happens after graduating - fleet placement, contract requirements, etc."
    )

    # Geocoding
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    # Metadata
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.carrier.name})"

    class Meta:
        ordering = ['carrier', 'state', 'city']
        verbose_name = "Academy"
        verbose_name_plural = "Academies"
