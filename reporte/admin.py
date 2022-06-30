from django.contrib import admin
from .models import Reportes
# Register your models here.
class ReportesAdmin(admin.ModelAdmin):
    list_display = ('nombre','descripcion','columnas')

admin.site.register(Reportes, ReportesAdmin)