# Generated by Django 5.0 on 2023-12-14 04:41

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0013_alter_leciona_data_inicio_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leciona',
            name='data_inicio',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='noticia',
            name='data_publicacao',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='turma',
            name='data_abertura',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
