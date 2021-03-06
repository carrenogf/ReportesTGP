# Generated by Django 3.2.8 on 2022-05-31 11:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import notificaciones.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notificaciones',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=255)),
                ('descripcion', models.TextField()),
                ('archivo1', models.FileField(blank=True, null=True, upload_to=notificaciones.models.content_file_name)),
                ('archivo2', models.FileField(blank=True, null=True, upload_to=notificaciones.models.content_file_name)),
                ('archivo3', models.FileField(blank=True, null=True, upload_to=notificaciones.models.content_file_name)),
                ('archivo4', models.FileField(blank=True, null=True, upload_to=notificaciones.models.content_file_name)),
                ('archivo5', models.FileField(blank=True, null=True, upload_to=notificaciones.models.content_file_name)),
                ('usuarios_notif', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Fecha de edición')),
                ('anotaciones', models.TextField(blank=True, null=True)),
                ('depto_rem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Departamento_Origen', to='auth.group')),
                ('deptos_destino', models.ManyToManyField(related_name='Departamentos_Destino', to='auth.Group')),
                ('deptos_notif', models.ManyToManyField(blank=True, related_name='Departamentos_Notificados', to='auth.Group')),
                ('usuario_remitente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Notificacion',
                'verbose_name_plural': 'Notificaciones',
                'ordering': ['-created'],
            },
        ),
    ]
