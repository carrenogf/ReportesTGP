# Generated by Django 3.2.4 on 2021-10-14 00:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reporte', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reportes',
            name='prueba',
        ),
    ]