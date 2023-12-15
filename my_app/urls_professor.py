from django.urls import path
from .views import ProfessorView

urlpatterns = [
    path('', ProfessorView.as_view(), name='professor_inicial'),
]
