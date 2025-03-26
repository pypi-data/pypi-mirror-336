from django.urls import path, include
from drf_spectacular.views import SpectacularJSONAPIView

urlpatterns = [
    path('m/domains/', include('saas_domain.api_urls.domain')),
    path('schema/openapi', SpectacularJSONAPIView.as_view(), name='schema'),
]
