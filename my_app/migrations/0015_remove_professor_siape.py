# Generated by Django 5.0 on 2023-12-14 05:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0014_alter_leciona_data_inicio_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='professor',
            name='siape',
        ),
    ]