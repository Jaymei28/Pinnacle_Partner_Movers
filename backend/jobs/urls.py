from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CarrierViewSet, JobList, JobDetail, ParseAndCreateJobView, ImportCSVView

# Router for viewsets
router = DefaultRouter()
router.register(r'carriers', CarrierViewSet, basename='carrier')

urlpatterns = [
    path('', include(router.urls)),
    path('jobs/', JobList.as_view(), name='job-list'),
    path('jobs/<int:pk>/', JobDetail.as_view(), name='job-detail'),
    path('jobs/parse/', ParseAndCreateJobView.as_view(), name='job-parse-create'),
    path('jobs/import-csv/', ImportCSVView.as_view(), name='job-import-csv'),
]


