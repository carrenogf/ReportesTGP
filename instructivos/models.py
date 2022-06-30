from django.db import models
from django.contrib.auth.models import Group
from ckeditor.fields import RichTextField
# Create your models here.
def content_file_name(instance, filename):
    return '/'.join(['instructivos', str(instance.pk), filename])

class Instructivo(models.Model):
	departamento = models.ForeignKey(Group,on_delete=models.CASCADE,related_name='Departamento')
	titulo = models.CharField(max_length=255, verbose_name="Título")
	descripcion = models.TextField(verbose_name="Breve Descripción")
	contenido = RichTextField(verbose_name="Contenido")
	archivo1 = models.FileField(upload_to=content_file_name,blank=True,null=True)
	archivo2 = models.FileField(upload_to=content_file_name,blank=True,null=True)
	archivo3 = models.FileField(upload_to=content_file_name,blank=True,null=True)
	created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
	updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

	class Meta:
		verbose_name = "Instructivo"
		verbose_name_plural = "Instructivos"
		ordering = ['-created']