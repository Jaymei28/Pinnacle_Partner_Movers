from django.contrib import admin
from django.utils.html import format_html
from .models import Carrier, Job, JobLocation, Academy


class JobLocationInline(admin.TabularInline):
    model = JobLocation
    extra = 1
    fields = ('city', 'state', 'zip_code', 'latitude', 'longitude')
    readonly_fields = ('latitude', 'longitude')


@admin.register(Carrier)
class CarrierAdmin(admin.ModelAdmin):
    list_display = ('name', 'website', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 50  # Show up to 50 carriers per page
    preserve_filters = False  # Don't preserve filters to avoid caching
    
    def get_queryset(self, request):
        """
        Override to prevent queryset caching and ensure fresh data.
        """
        qs = super().get_queryset(request)
        # Force evaluation to prevent caching issues
        return qs.order_by('name')
    
    fieldsets = (
        ('Company Information', {
            'fields': ('name', 'logo', 'description', 'website', 'is_active')
        }),
        ('Contact Information', {
            'fields': ('contact_email', 'contact_phone')
        }),
        ('Headquarters Location', {
            'fields': ('headquarters_city', 'headquarters_state', 'headquarters_zip'),
            'description': 'Used as fallback location for jobs without specific zip codes'
        }),
        ('Benefits - Retirement & Financial', {
            'fields': ('benefit_401k', 'benefit_stock_purchase')
        }),
        ('Benefits - Health & Insurance', {
            'fields': (
                'benefit_medical_dental_vision',
                'benefit_disability_life',
                'benefit_prescription_drug'
            )
        }),
        ('Benefits - Compensation & Time Off', {
            'fields': (
                'benefit_weekly_paycheck',
                'benefit_paid_vacation',
                'benefit_driver_ranking_bonus'
            )
        }),
        ('Benefits - Education & Special Programs', {
            'fields': (
                'benefit_tuition_program',
                'benefit_military_program',
                'benefit_other'
            )
        }),
        ('Data Tables & Consolidation', {
            'fields': ('benefits', 'presentation', 'pre_qualifications', 'app_process'),
            'description': 'Paste table-formatted data into these fields for specialized rendering in the frontend.'
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Academy)
class AcademyAdmin(admin.ModelAdmin):
    list_display = ('name', 'carrier', 'city', 'state', 'zip_code', 'training_type', 'tuition_cost', 'is_active')
    list_filter = ('carrier', 'state', 'training_type', 'is_active')
    search_fields = ('name', 'city', 'state', 'zip_code', 'carrier__name', 'academy_details')
    readonly_fields = ('created_at', 'updated_at', 'latitude', 'longitude')
    list_per_page = 50
    preserve_filters = False

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('carrier')

    fieldsets = (
        ('SECTION 1: Identification & Location', {
            'fields': ('carrier', 'name', 'city', 'state', 'zip_code', 'is_active'),
            'description': 'Basic academy identification and physical location.'
        }),
        ('SECTION 2: Training Details', {
            'fields': ('training_type', 'program_length_days', 'tuition_cost', 'tuition_notes'),
            'description': 'Type of training offered, duration, and tuition information.'
        }),
        ('SECTION 3: Pay During Training', {
            'fields': ('trainee_pay', 'orientation_pay'),
            'description': 'What the student/trainee is paid during the program.'
        }),
        ('SECTION 4: Requirements & Details', {
            'fields': ('requirements', 'academy_details', 'after_graduation'),
            'description': 'Enrollment requirements, program details, and post-graduation placement info.'
        }),
        ('Location (Geocoding)', {
            'fields': ('latitude', 'longitude'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'carrier', 'state', 'colored_zip_code', 'is_active', 'created_at')
    list_filter = ('carrier', 'is_active', 'created_at')
    search_fields = ('title', 'carrier__name', 'state', 'job_details', 'zip_code')
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 100
    preserve_filters = False
    inlines = [JobLocationInline]
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('carrier')
    
    def colored_zip_code(self, obj):
        """Display zip code with color-coded source indicator"""
        colors = {
            'manual': '#28a745',
            'extracted': '#007bff',
            'geocoded': '#17a2b8',
            'carrier_hq': '#ffc107',
            'state_capital': '#dc3545'
        }
        color = colors.get(obj.zip_source, '#6c757d')
        # Use simple label since zip_source is no longer a choice field with labels
        source_label = obj.zip_source or 'Unknown'
        
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span> <span style="color: #999; font-size: 0.85em;">({})</span>',
            color, obj.zip_code or 'N/A', source_label
        )
    colored_zip_code.short_description = 'Zip Code'
    colored_zip_code.admin_order_field = 'zip_code'
    
    fieldsets = (
        ('SECTION 1: Basic Information', {
            'fields': (
                'carrier', 'title', 'state', 'zip_code', 'hiring_radius_miles', 
                'multi_zip_codes', 'is_active'
            ),
            'description': 'Enter primary location above. Use Multi Zip Codes field below to bulk-add locations.'
        }),
        ('SECTION 2: Job Details', {
            'fields': ('job_details',),
            'description': 'Paste all job description details, account overview, and highlights here.'
        }),
        ('SECTION 3: Pay Details', {
            'fields': ('pay_details',),
            'description': 'Paste all pay details, bonuses, and compensation info here.'
        }),
        ('SECTION 4: Equipment', {
            'fields': ('equipment_details',),
            'description': 'Paste all equipment-related details here.'
        }),
        ('SECTION 5: Key Disqualifiers', {
            'fields': ('key_disqualifiers',),
            'description': 'Key disqualifiers for this job.'
        }),
        ('SECTION 6: Requirements', {
            'fields': ('requirements_details',),
            'description': 'Paste all job requirements and qualification details here.'
        }),
        ('Location Details', {
            'fields': ('latitude', 'longitude'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

