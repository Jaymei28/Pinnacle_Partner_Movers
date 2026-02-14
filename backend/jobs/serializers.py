from rest_framework import serializers
from .models import Carrier, Job


class CarrierSerializer(serializers.ModelSerializer):
    """Serializer for Carrier model with all company and benefits information"""
    active_jobs_count = serializers.SerializerMethodField()

    class Meta:
        model = Carrier
        fields = '__all__'

    def get_active_jobs_count(self, obj):
        return obj.jobs.filter(is_active=True).count()


class JobSerializer(serializers.ModelSerializer):
    """Serializer for Job model with nested carrier information"""
    carrier = CarrierSerializer(read_only=True)
    carrier_id = serializers.PrimaryKeyRelatedField(
        queryset=Carrier.objects.all(),
        source='carrier',
        write_only=True
    )
    
    class Meta:
        model = Job
        fields = '__all__'

