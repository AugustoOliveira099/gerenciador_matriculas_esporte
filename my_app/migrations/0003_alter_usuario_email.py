# Generated by Django 5.0 on 2023-12-09 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0002_usuario_turma_remove_aluno_cpf_remove_aluno_nome_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='email',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]