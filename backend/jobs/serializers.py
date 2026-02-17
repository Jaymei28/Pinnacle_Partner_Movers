from rest_framework import serializers
from .models import Carrier, Job, JobLocation


class CarrierSerializer(serializers.ModelSerializer):
    """Serializer for Carrier model with all company and benefits information"""
    active_jobs_count = serializers.SerializerMethodField()

    class Meta:
        model = Carrier
        fields = '__all__'

    def get_active_jobs_count(self, obj):
        return obj.jobs.filter(is_active=True).count()


class JobLocationSerializer(serializers.ModelSerializer):
    """Serializer for JobLocation model"""
    class Meta:
        model = JobLocation
        fields = ['id', 'city', 'state', 'zip_code', 'latitude', 'longitude']


class JobSerializer(serializers.ModelSerializer):
    """Serializer for Job model with nested carrier information"""
    carrier = CarrierSerializer(read_only=True)
    carrier_id = serializers.PrimaryKeyRelatedField(
        queryset=Carrier.objects.all(),
        source='carrier',
        write_only=True
    )
    additional_locations = JobLocationSerializer(many=True, read_only=True)
    
    # Dynamic fields extracted from text
    average_weekly_pay = serializers.SerializerMethodField()
    experience_required = serializers.SerializerMethodField()
    driver_type = serializers.SerializerMethodField()
    freight_type = serializers.SerializerMethodField()
    home_time = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = [
            'id', 'title', 'state', 'zip_code', 'hiring_radius_miles', 
            'average_weekly_pay', 'experience_required', 'driver_type', 'freight_type', 'home_time',
            'job_details', 'pay_details', 'equipment_details', 'key_disqualifiers', 'requirements_details',
            'hiring_status', 'latitude', 'longitude', 'location_source', 'zip_source',
            'is_active', 'created_at', 'updated_at', 'carrier', 'carrier_id', 'additional_locations'
        ]

    def _get_combined_text(self, obj):
        return "\n".join(filter(None, [
            obj.title or "",
            obj.job_details or "",
            obj.pay_details or "",
            obj.requirements_details or ""
        ]))

    def _find_value(self, keywords, text):
        import re
        for kw in keywords:
            # Match "Keyword: Value" or "Keyword, Value"
            # We allow everything until the end of the line, but strip trailing commas/whitespace
            pattern = rf'(?:{kw})[:,\s]+([^\n]{{2,100}})'
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                val = match.group(1).strip()
                # If there's a comma that looks like a delimiter (e.g. "Value, Keyword"), 
                # we might need to be careful, but for now let's allow commas for currency
                return val
        return None

    def get_average_weekly_pay(self, obj):
        text = self._get_combined_text(obj)
        val = self._find_value(['Average Weekly Pay', 'Avg Weekly Pay', 'Weekly Pay', 'Pay'], text)
        if val and '$' in val: return val
        import re
        match = re.search(r'(\$[\d,]+(?:\s*-\s*\$[\d,]+)?)', text)
        return match.group(1).strip() if match else None

    def get_experience_required(self, obj):
        text = self._get_combined_text(obj)
        val = self._find_value(['Experience Required', 'Experience', 'Exp'], text)
        if val: return val if any(x in val.lower() for x in ['mo', 'yr']) else f"{val} months"
        import re
        match = re.search(r'([\d\+]+(?:\s*(?:months?|years?|mo|yrs?)))', text, re.IGNORECASE)
        return match.group(1).strip() if match else None

    def get_home_time(self, obj):
        text = self._get_combined_text(obj)
        val = self._find_value(['Home Time', 'Exact Home Time', 'Schedule'], text)
        if val: return val
        import re
        if re.search(r'\bDaily\b', text, re.IGNORECASE): return "Daily"
        if re.search(r'\bBi-Weekly\b', text, re.IGNORECASE): return "Bi-Weekly"
        if re.search(r'\bWeekly\b', text, re.IGNORECASE): return "Weekly"
        return None

    def get_driver_type(self, obj):
        text = self._get_combined_text(obj)
        val = self._find_value(['Driver Type'], text)
        if val: return val
        import re
        if re.search(r'\bLease Purchase\b', text, re.IGNORECASE): return "Lease Purchase"
        if re.search(r'\bOwner Operator\b', text, re.IGNORECASE): return "Owner Operator"
        if re.search(r'\bCompany Driver\b', text, re.IGNORECASE): return "Company"
        return None

    def get_freight_type(self, obj):
        text = self._get_combined_text(obj)
        val = self._find_value(['Freight Type', 'Equipment', 'Load/Unload'], text)
        if val: return val
        import re
        if re.search(r'\bDry Van\b', text, re.IGNORECASE): return "Dry Van"
        if re.search(r'\bReefer\b', text, re.IGNORECASE): return "Reefer"
        if re.search(r'\bFlatbed\b', text, re.IGNORECASE): return "Flatbed"
        return None

