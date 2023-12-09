from django.urls import path
from .views import Listar

urlpatterns = [
    path('', Listar.as_view(), name='adm_inicial'),
]