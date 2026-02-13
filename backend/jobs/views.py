from rest_framework.views import APIView
from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from .models import Carrier, Job
from .serializers import CarrierSerializer, JobSerializer
import re
from .utils import filter_jobs_by_radius


class CarrierViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing Carrier instances.
    Provides list, create, retrieve, update, and delete operations.
    """
    queryset = Carrier.objects.filter(is_active=True)
    serializer_class = CarrierSerializer


class JobList(generics.ListCreateAPIView):
    serializer_class = JobSerializer

    def list(self, request, *args, **kwargs):
        """
        List jobs, optionally filtered by driver's zip code and hiring radius.
        Query params:
            - zip_code: Driver's zip code for location-based filtering
        """
        try:
            driver_zip = request.query_params.get('zip_code')
            
            if driver_zip:
                # Filter jobs by hiring radius with multi-tier location strategy
                queryset = Job.objects.filter(is_active=True)
                filtered_jobs = filter_jobs_by_radius(driver_zip, queryset)
                
                # Serialize with distance and location information
                results = []
                for job_data in filtered_jobs:
                    job_dict = JobSerializer(job_data['job']).data
                    job_dict['distance_miles'] = job_data['distance_miles']
                    job_dict['location_source'] = job_data['location_source']
                    job_dict['match_type'] = job_data['match_type']
                    results.append(job_dict)
                
                return Response(results)
            else:
                # Return all active jobs without distance filtering
                queryset = Job.objects.filter(is_active=True)
                serializer = self.get_serializer(queryset, many=True)
                return Response(serializer.data)
        except Exception as e:
            # Log the error and return empty list
            print(f"Error in JobList.list: {str(e)}")
            import traceback
            traceback.print_exc()
            return Response([])



class JobDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer


class ParseAndCreateJobView(APIView):
    """
    API endpoint to parse raw job text and create a Job record.
    """
    def post(self, request, *args, **kwargs):
        raw_text = request.data.get('raw_text')
        carrier_id = request.data.get('carrier_id')
        
        if not raw_text or not carrier_id:
            return Response(
                {"error": "Both raw_text and carrier_id are required."},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            carrier = Carrier.objects.get(id=carrier_id)
            
            # Basic parsing logic
            lines = raw_text.replace('\\n', '\n').split('\n')
            data = {}
            
            # 1. Extract Title (usually the first non-empty line after "Lane Information" or at top)
            title = "New Job"
            for i, line in enumerate(lines):
                if "Lane Information" in line and i + 1 < len(lines):
                    next_line = lines[i+1].trim() if hasattr(lines[i+1], 'trim') else lines[i+1].strip()
                    if next_line:
                        title = next_line
                        break
            
            # 2. Extract Fields using Key: Value pattern
            field_map = {
                r'Experience Required': 'experience_required',
                r'Home Time': 'home_time',
                r'Average Weekly Pay': 'average_weekly_pay',
                r'Pay Range': 'pay_range',
                r'Hub City': 'state',
                r'Hiring Area Zip Code': 'zip_code',
                r'Trainees Accepted': 'trainees_accepted',
                r'Create Date': 'source_create_date',
                r'Modified Date': 'source_modified_date',
            }
            
            job_fields = {
                'carrier': carrier,
                'title': title,
                'description': raw_text,
                'is_active': True
            }
            
            for line in lines:
                for pattern, model_field in field_map.items():
                    if pattern in line and ':' in line:
                        value = line.split(':', 1)[1].strip()
                        
                        # Handle boolean fields
                        if model_field in ['trainees_accepted', 'teams_accepted', 'owner_operators_accepted', 'leadership_approval_required']:
                            job_fields[model_field] = value.upper() == 'YES'
                        else:
                            job_fields[model_field] = value
            
            # Ensure required fields that might be missing from simple parse
            if not job_fields.get('state'): job_fields['state'] = "See Description"
            if not job_fields.get('zip_code'): job_fields['zip_code'] = "00000"
            
            # Create the job
            job = Job.objects.create(**job_fields)
            
            return Response(JobSerializer(job).data, status=status.HTTP_201_CREATED)
            
        except Carrier.DoesNotExist:
            return Response({"error": "Carrier not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

