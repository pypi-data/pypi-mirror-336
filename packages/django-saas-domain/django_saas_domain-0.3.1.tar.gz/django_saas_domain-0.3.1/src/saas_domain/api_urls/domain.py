from django.urls import path
from ..endpoints.domain import DomainListEndpoint, DomainItemEndpoint

urlpatterns = [
    path('', DomainListEndpoint.as_view()),
    path('<pk>/', DomainItemEndpoint.as_view()),
]
