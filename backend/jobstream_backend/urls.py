from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token
from django.urls import re_path
from django.views.static import serve
from django.http import HttpResponse

def home(request):
    return HttpResponse("JobStream API is Online and Running! 🚀")

urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path('api/', include('jobs.urls')),
    path('api/login/', obtain_auth_token, name='api_token_auth'),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

