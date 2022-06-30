from django.contrib import admin
from .models import Instructivo

# Register your models here.
class InstructivoAdmin(admin.ModelAdmin):
	list_display = ('titulo','departamento','descripcion','created')

admin.site.register(Instructivo, InstructivoAdmin)