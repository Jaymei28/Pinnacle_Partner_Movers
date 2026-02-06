from rest_framework import serializers
from .models import Carrier, Job


class CarrierSerializer(serializers.ModelSerializer):
    """Serializer for Carrier model with all company and benefits information"""
    class Meta:
        model = Carrier
        fields = '__all__'


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

