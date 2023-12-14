from django import forms
from .models import Usuario

# ---------- PROFESSOR ----------
class FormCadastraTurma(forms.Form):
    intervalo_horario = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'HH:MM às HH:MM', 
            'pattern': '^[0-2][0-9]:[0-5][0-9] às [0-2][0-9]:[0-5][0-9]$'
        })
    )

# ---------- ADMINISTRADOR ----------
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

# ---------- USUÁRIO ----------
class UsuarioCadastroForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['cpf', 'email', 'nome', 'senha', 'nascimento']
        widgets = {
            'cpf': forms.TextInput(attrs={'type': 'hidden'}),  # Campo oculto
        }

# ---------- ALUNO ----------
class FormAptFisica(forms.Form):
    atestado = forms.CharField(
        label='Atestado de aptidão física',
        widget=forms.TextInput(attrs={
            'title': 'Informe o link para o seu atestado de aptidão física',
            'placeholder': 'Link para o atestado'
        })
    )
    