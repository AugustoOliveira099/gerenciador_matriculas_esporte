from django import forms
from .models import Aluno

class FormCadastraTurma(forms.Form):
    intervalo_horario = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'HH:MM às HH:MM', 
            'pattern': '^[0-2][0-9]:[0-5][0-9] às [0-2][0-9]:[0-5][0-9]$'
        })
    )


class FormCPF(forms.Form):
    cpf = forms.CharField(
        label='CPF',
        max_length=14,
        widget=forms.TextInput(attrs={
            'title': 'Informe o CPF de um usuário.',
            'placeholder': 'Digite o CPF do novo administrador',
            # 'pattern': r'\d{3}\.\d{3}\.\d{3}-\d{2}',
            'id': 'cpf-input'
        })
    )

class AlunoCadastroForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = ['user_cpf', 'atestado_apt', 'turma_id']
        widgets = {
            'user_cpf': forms.TextInput(attrs={'type': 'hidden'}),  # Campo oculto
        }

    