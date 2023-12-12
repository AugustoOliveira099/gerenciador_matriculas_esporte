from django.urls import path
from .views import AlunoCadastroView

urlpatterns = [
    path('', AlunoCadastroView.as_view(), name='cadastro_aluno'),
]
