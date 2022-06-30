from django.db import models
from django.contrib.auth.models import User, Group
# Create your models here.
def content_file_name(instance, filename):
    return '/'.join(['content', str(instance.pk), filename])

class Notificaciones(models.Model):
	
	titulo = models.CharField(max_length=255)
	descripcion = models.TextField()
	archivo1 = models.FileField(
		upload_to=content_file_name,
		blank=True,null=True)
	archivo2 = models.FileField(
		upload_to=content_file_name,
		blank=True,null=True)
	archivo3 = models.FileField(
		upload_to=content_file_name,
		blank=True,null=True)
	archivo4 = models.FileField(
		upload_to=content_file_name,
		blank=True,null=True)
	archivo5 = models.FileField(
		upload_to=content_file_name,
		blank=True,null=True)
	usuario_remitente = models.ForeignKey(User,on_delete=models.CASCADE)
	depto_rem = models.ForeignKey(Group,on_delete=models.CASCADE,related_name='Departamento_Origen')
	usuarios_notif = models.TextField(blank=True,null=True) #diccionario con el usuario y la fecha
	deptos_destino = models.ManyToManyField(Group,related_name='Departamentos_Destino')
	deptos_notif = models.ManyToManyField(Group,related_name='Departamentos_Notificados',blank=True)
	created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
	updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")
	anotaciones = models.TextField(blank=True,null=True)

	class Meta:
		verbose_name = "Notificacion"
		verbose_name_plural = "Notificaciones"
		ordering = ['-created']

