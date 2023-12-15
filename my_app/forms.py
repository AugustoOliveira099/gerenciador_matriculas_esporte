from django import forms
from .models import Usuario

# ---------- PROFESSOR ----------
class FormCadastraTurma(forms.Form):
    modalidade = forms.CharField(
        label='Modalidade ensinada',
        widget=forms.TextInput(attrs={
            'title': 'Informe a modalidade que será ensinada.',
            'placeholder': 'Modalidade'
        }),
        required=True
    )
    horario = forms.CharField(
        label='Horário da aula',
        widget=forms.TextInput(attrs={
            'title': 'Informe o horário no padrão UFRN. Ex.: 2T34.',
            'placeholder': 'Horário no padrão UFRN', 
            'pattern': '^[2-7][MTN][1-5][2-6]$'
        }),
        required=True
    )
    vagas = forms.IntegerField(
        label='Vagas',
        min_value=0,
        max_value=100,
        widget=forms.NumberInput(attrs={
            'title': 'Informe um valor entre 0 e 100',
            'placeholder': 'Vagas disponíveis', 
        }),
        required=True
    )
    semestre = forms.FloatField(
        label='Semestre',
        widget=forms.NumberInput(attrs={
            'placeholder': 'Semestre de ensino', 
            'title': 'Semestre que será ensinado o esporte. Ex.: 2023.2',
            'step': '0.1'
        }),
        required=True
    )

class FormCadastraNoticia(forms.Form):
    conteudo = forms.CharField(
        label='Notícia',
        widget=forms.TextInput(attrs={
            'placeholder': 'Digite o conteúdo da notícia',
        }),
        required=True
    )

    turma_id = forms.IntegerField(
        label='Id da turma',
        widget=forms.NumberInput(attrs={
            'title': 'Id da turma que receberá a notícia',
            'placeholder': 'Digite um número inteiro'
        }),
        required=True
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
        }),
        required=True
    )