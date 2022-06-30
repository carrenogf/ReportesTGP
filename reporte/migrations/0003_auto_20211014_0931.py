# Generated by Django 3.2.4 on 2021-10-14 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reporte', '0002_remove_reportes_prueba'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reportes',
            name='nombre',
            field=models.CharField(max_length=60, unique=True),
        ),
        migrations.AlterField(
            model_name='reportes',
            name='tipo_txt',
            field=models.CharField(choices=[('delimitado', 'delimitado'), ('ancho fijo', 'ancho fijo')], max_length=60),
        ),
    ]