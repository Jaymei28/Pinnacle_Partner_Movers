from django.db import models


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
    state = models.CharField(max_length=200, help_text="Primary state for the job")
    zip_code = models.CharField(max_length=10, help_text="Location zip code")
    hiring_radius_miles = models.IntegerField(default=50, help_text="Hiring radius in miles")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    # Pay Details
    pay_range = models.CharField(max_length=100, blank=True, null=True, help_text="Pay range (e.g., $0.43-$0.51 CPM)")
    average_weekly_pay = models.CharField(max_length=50, blank=True, null=True, help_text="Average weekly pay")
    salary = models.CharField(max_length=100, blank=True, null=True, help_text="General pay information")
    pay_type = models.CharField(max_length=50, blank=True, null=True, help_text="Weekly, Hourly, Per Mile, etc.")
    short_haul_pay = models.CharField(max_length=100, blank=True, null=True, help_text="Pay for short hauls")
    stop_pay = models.CharField(max_length=50, blank=True, null=True, help_text="Pay per stop")
    bonus_offer = models.CharField(max_length=200, blank=True, null=True, help_text="Bonus offers")
    
    # Exact Home Time
    exact_home_time = models.CharField(max_length=200, blank=True, null=True, help_text="Specific home time details")
    home_time = models.CharField(max_length=100, blank=True, null=True, help_text="General home time (Daily, Weekly, etc.)")
    
    # Load/Unload
    load_unload_type = models.CharField(max_length=100, blank=True, null=True, help_text="Live Load, Drop and Hook, etc.")
    unload_pay = models.CharField(max_length=50, blank=True, null=True, help_text="Pay for unloading")
    
    # ========== SECTION 2: LANE INFORMATION ==========
    # Consolidated text areas for easy copy-paste data entry
    job_details = models.TextField(
        blank=True,
        null=True,
        help_text="Paste all job details here (routes, schedule, equipment, etc.)"
    )
    
    account_overview = models.TextField(
        blank=True,
        null=True,
        help_text="Paste all account overview information here"
    )
    
    administrative_details = models.TextField(
        blank=True,
        null=True,
        help_text="Paste all administrative details here (managers, contacts, cost center, etc.)"
    )
    
    # Keep description for general lane information
    description = models.TextField(
        blank=True,
        null=True,
        help_text="General job description and lane information"
    )
    
    # ========== SECTION 3: COMPANY BENEFITS & INFO ==========
    # Benefits are pulled from the related Carrier model
    # No additional fields needed here
    
    # ========== SECTION 4: ORIENTATION ==========
    # Consolidated fields for easy data entry
    orientation_details = models.TextField(
        blank=True,
        null=True,
        help_text="Paste all orientation details here (location, duration, pay, lodging, meals, transportation)"
    )
    
    orientation_table = models.TextField(
        blank=True,
        null=True,
        help_text="Optional: Paste orientation table data here"
    )
    
    # ========== SECTION 5: JOB REQUIREMENTS ==========
    # Multi-Select Fields (stored as comma-separated values)
    trainees_accepted = models.CharField(
        max_length=200, 
        blank=True, 
        null=True,
        help_text="Trainee acceptance options (comma-separated): Yes, No, Conditional"
    )
    
    account_type = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Account types (comma-separated): Dedicated, OTR, Regional, Local"
    )
    
    cameras = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Camera types (comma-separated): Inward Facing, Outward Facing, Both, None"
    )
    
    driver_types = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Driver types (comma-separated): Company Driver, Owner Operator, Lease Purchase"
    )
    
    drug_test_type = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Drug test types (comma-separated): Hair Follicle, Urinalysis, Both"
    )
    
    experience_levels = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Experience levels (comma-separated): 0 months, 3 months, 6 months, 12 months, 24 months"
    )
    
    freight_types = models.CharField(
        max_length=300,
        blank=True,
        null=True,
        help_text="Freight types (comma-separated): Dry Van, Reefer, Flatbed, Tanker, Intermodal, etc."
    )
    
    sap_required = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="SAP requirement (comma-separated): Yes, No, Conditional"
    )
    
    transmissions = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Transmission types (comma-separated): Automatic, Manual, Both"
    )
    
    states = models.CharField(
        max_length=1000,
        blank=True,
        null=True,
        help_text="States covered (comma-separated state codes): AL, AK, AZ, etc."
    )
    
    # Geocoding fields for distance-based search
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True,
        help_text="Auto-populated from ZIP code or carrier HQ"
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True,
        help_text="Auto-populated from ZIP code or carrier HQ"
    )
    location_source = models.CharField(
        max_length=20,
        choices=[
            ('job_zip', 'Job ZIP Code'),
            ('carrier_hq', 'Carrier Headquarters'),
            ('state_only', 'State Level Only'),
        ],
        blank=True,
        null=True,
        help_text="Source of location data for transparency"
    )
    
    # Zip Code Source Tracking
    zip_source = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        choices=[
            ('manual', 'Manually Entered'),
            ('extracted', 'Extracted from Description'),
            ('geocoded', 'Auto-Geocoded from Location'),
            ('carrier_hq', 'Carrier Headquarters'),
            ('state_capital', 'State Capital Default')
        ],
        help_text="Source of zip code data"
    )
    
    # Metadata
    is_active = models.BooleanField(default=True, help_text="Whether this job is active/visible")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Track the raw dates from the data source
    source_create_date = models.CharField(max_length=100, blank=True, null=True)
    source_modified_date = models.CharField(max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Auto-populate zip code if missing
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
    
    def __str__(self):
        return f"{self.title} at {self.carrier.name}"
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Job"
        verbose_name_plural = "Jobs"

