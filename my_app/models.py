from django.db import models
from django.utils import timezone

class Usuario(models.Model):
    cpf = models.IntegerField(primary_key=True)
    email = models.CharField(max_length=255, unique=True)
    nome = models.CharField(max_length=255)
    senha = models.CharField(max_length=255)
    nascimento = models.DateTimeField()

class Aluno(models.Model):
    user_cpf = models.OneToOneField(Usuario, default=123456789, on_delete=models.CASCADE, primary_key=True)
    atestado_apt = models.CharField(max_length=255, null=True, help_text='Link para o documento')
    atestado_apt_validado_por = models.ForeignKey('Administrador', null=True, on_delete=models.SET_NULL)
    atestado_apt_validado_em = models.DateTimeField(null=True)
    atestado_apt_esperando_validacao = models.BooleanField(default=False)
    turma_id = models.ForeignKey('Turma', null=True, on_delete=models.SET_NULL)

class Professor(models.Model):
    user_cpf = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)

class Administrador(models.Model):
    user_cpf = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)
    cadastrado_por = models.ForeignKey('self', null=True, on_delete=models.SET_NULL)

class Turma(models.Model):
    id = models.AutoField(primary_key=True)
    modalidade = models.CharField(max_length=255)
    horario = models.CharField(max_length=255, null=True)
    is_open = models.BooleanField()
    data_fechamento = models.DateTimeField(null=True)
    data_abertura = models.DateTimeField(default=timezone.now)
    semestre = models.FloatField(help_text='Ex.: 2023.2')
    vagas = models.IntegerField(default=0)

class Noticia(models.Model):
    id = models.AutoField(primary_key=True)
    prof_cpf = models.ForeignKey(Professor, null=True, on_delete=models.SET_NULL)
    turma_id = models.ForeignKey(Turma, null=True, on_delete=models.SET_NULL)
    conteudo = models.TextField()
    data_publicacao = models.DateTimeField(default=timezone.now)

class Leciona(models.Model):
    id = models.AutoField(primary_key=True)
    prof_cpf = models.ForeignKey(Professor, on_delete=models.CASCADE)
    turma_id = models.ForeignKey(Turma, on_delete=models.CASCADE)
    data_inicio = models.DateTimeField(default=timezone.now)
    data_termino = models.DateTimeField(null=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['turma_id', 'prof_cpf'], name='unique_leciona')
        ]

class Matricula(models.Model):
    id = models.AutoField(primary_key=True)
    aluno_cpf = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    turma_id = models.ForeignKey(Turma, on_delete=models.CASCADE)
    prof_cpf = models.ForeignKey(Professor, on_delete=models.CASCADE)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['aluno_cpf', 'turma_id', 'prof_cpf'], name='unique_matricula')
        ]

class Frequencia(models.Model):
    matric_id = models.ForeignKey(Matricula, on_delete=models.CASCADE)
    data = models.DateTimeField()
    presente = models.BooleanField(null=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['matric_id', 'data'], name='unique_frequencia')
        ]
