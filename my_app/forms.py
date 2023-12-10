from django import forms

class FormsCadastraTurma(forms.Form):
    intervalo_horario = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'HH:MM às HH:MM', 'pattern': '^[0-2][0-9]:[0-5][0-9] às [0-2][0-9]:[0-5][0-9]$'})
    )

    # <h2>Cadastrar administrador</h2>
    # <form method="post" action="{% url 'sua_view' %}">
    #     {% csrf_token %}
    #     {{ formulario.seu_campo.label_tag }}
    #     {{ formulario.seu_campo }}
    #     {{ formulario.seu_campo.errors }}
    #     <button type="submit">Enviar</button>
    # </form>


# class FormsAdm(forms.Form):
    