from django.contrib import admin
from .models import Notificaciones

# Register your models here.
class NotificacionesAdmin(admin.ModelAdmin):
	list_display = ('created','titulo','descripcion','depto_rem','get_dep')

	def get_dep(self, obj):
		return "\n".join([d.name for d in obj.deptos_notif.all()])

admin.site.register(Notificaciones, NotificacionesAdmin)