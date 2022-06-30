from django.db import models

# Create your models here.
STATUS_CHOICES = (
    ("delimitado","delimitado"),
    ("ancho fijo","ancho fijo"),
)

class Reportes(models.Model):
    nombre = models.CharField(max_length=60,unique=True)
    tipo_txt = models.CharField(max_length=60,choices=STATUS_CHOICES)
    delimitador = models.CharField(max_length=10, blank=True, null=True)
    columnas = models.TextField(blank=True, null=True)
    descripcion = models.TextField()

    class Meta:
        verbose_name = "Reporte"
        verbose_name_plural = "reportes"