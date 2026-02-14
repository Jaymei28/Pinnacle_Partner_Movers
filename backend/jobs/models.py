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

