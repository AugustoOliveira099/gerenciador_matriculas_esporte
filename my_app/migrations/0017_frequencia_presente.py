# Generated by Django 5.0 on 2023-12-14 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0016_aluno_atestado_apt_esperando_validacao'),
    ]

    operations = [
        migrations.AddField(
            model_name='frequencia',
            name='presente',
            field=models.BooleanField(null=True),
        ),
    ]