from django.urls import path
from .views import UsuarioCadastroView

urlpatterns = [
    path('', UsuarioCadastroView.as_view(), name='cadastro_user'),
]