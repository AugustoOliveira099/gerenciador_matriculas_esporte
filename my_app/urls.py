from django.urls import path
from .views import Admin

urlpatterns = [
    path('', Admin.as_view(), name='adm_inicial'),
]