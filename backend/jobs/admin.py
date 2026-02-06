from django.contrib import admin
from django.utils.html import format_html
from .models import Carrier, Job


@admin.register(Carrier)
class CarrierAdmin(admin.ModelAdmin):
    list_display = ('name', 'website', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    
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
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'carrier', 'state', 'colored_zip_code', 'salary', 'home_time', 'is_active', 'created_at')
    list_filter = ('zip_source', 'carrier', 'is_active', 'created_at', 'account_type')
    search_fields = ('title', 'carrier__name', 'state', 'description', 'zip_code')
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 100  # Show up to 100 jobs per page
    preserve_filters = False  # Don't preserve filters across requests
    
    def get_queryset(self, request):
        """
        Override to prevent queryset caching and ensure fresh data.
        Uses select_related to optimize database queries.
        """
        qs = super().get_queryset(request)
        # Use select_related to optimize the query and prevent caching issues
        return qs.select_related('carrier')
    
    def colored_zip_code(self, obj):
        """Display zip code with color-coded source indicator"""
        colors = {
            'manual': '#28a745',        # Green - manually entered (best)
            'extracted': '#007bff',     # Blue - extracted from description (good)
            'geocoded': '#17a2b8',      # Cyan - geocoded (good)
            'carrier_hq': '#ffc107',    # Orange - carrier headquarters (okay)
            'state_capital': '#dc3545'  # Red - state capital (needs review)
        }
        color = colors.get(obj.zip_source, '#6c757d')  # Gray for unknown
        source_label = dict(obj._meta.get_field('zip_source').choices).get(obj.zip_source, 'Unknown')
        
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span> <span style="color: #999; font-size: 0.85em;">({})</span>',
            color, obj.zip_code or 'N/A', source_label
        )
    colored_zip_code.short_description = 'Zip Code'
    colored_zip_code.admin_order_field = 'zip_code'
    
    fieldsets = (
        ('SECTION 1: Basic Information', {
            'fields': ('carrier', 'title', 'state', 'zip_code', 'hiring_radius_miles', 'is_active')
        }),
        ('Pay Details', {
            'fields': ('pay_range', 'average_weekly_pay', 'salary', 'pay_type', 'short_haul_pay', 'stop_pay', 'bonus_offer')
        }),
        ('Home Time', {
            'fields': ('exact_home_time', 'home_time')
        }),
        ('Load/Unload', {
            'fields': ('load_unload_type', 'unload_pay')
        }),
        ('SECTION 2: Lane Information', {
            'fields': ('description', 'job_details', 'account_overview', 'administrative_details'),
            'description': 'Paste blocks of text for each section'
        }),
        ('SECTION 3: Company Benefits & Info', {
            'description': 'Benefits are automatically pulled from the selected Carrier',
            'fields': (),
            'classes': ('collapse',)
        }),
        ('SECTION 4: Orientation', {
            'fields': ('orientation_details', 'orientation_table'),
            'description': 'Paste orientation information. Table field is optional.'
        }),
        ('SECTION 5: Job Requirements (Multi-Select - Comma Separated)', {
            'fields': (
                'trainees_accepted',
                'account_type',
                'cameras',
                'driver_types',
                'drug_test_type',
                'experience_levels',
                'freight_types',
                'sap_required',
                'transmissions',
                'states'
            ),
            'description': 'Enter multiple values separated by commas (e.g., "Company Driver, Owner Operator")'
        }),
        ('Location Details', {
            'fields': ('latitude', 'longitude'),
            'classes': ('collapse',)
        }),
        ('Source Tracking', {
            'fields': ('source_create_date', 'source_modified_date'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

