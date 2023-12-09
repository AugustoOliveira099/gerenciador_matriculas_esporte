from django.urls import path
from .views import Listar

urlpatterns = [
    path('listar/', Listar.as_view(), name='listar'),
]