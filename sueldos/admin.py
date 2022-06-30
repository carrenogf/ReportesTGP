from django.contrib import admin
from .models import TipoLiquidacion,Liquidacion,Reparticion,Registro

class TipoLiquidacionAdmin(admin.ModelAdmin):
	readonly_fields = ('created', 'updated')
	list_display = ('tipo','updated','created')

class LiquidacionAdmin(admin.ModelAdmin):
	readonly_fields = ('created', 'updated')
	list_display = ('tipo','liquidacion','observación','updated','created')

class ReparticionAdmin(admin.ModelAdmin):
	readonly_fields = ('created', 'updated')
	list_display = ('nro','saf','denominacion','updated')

class RegistroAdmin(admin.ModelAdmin):
	readonly_fields = ('created', 'updated')
	list_display = ('liquidacion','get_nro_repaticion','get_denominacion','op','importe','fechaME','pagado')

	def get_denominacion(self, obj):
		return obj.reparticion.denominacion
	get_denominacion.admin_order_field = "reparticion__denominacion"
	get_denominacion.short_description = "Reparticion"
	def get_nro_repaticion(self,obj):
		return obj.reparticion.nro  
	get_nro_repaticion.admin_order_field = "reparticion__nro"
	get_nro_repaticion.short_description = "Nro Rep"


	list_filter = ('liquidacion__abierta','liquidacion',)
	search_fields = ('liquidacion__liquidacion','reparticion__denominacion')

	list_editable = ['importe','op','fechaME','pagado']

admin.site.register(TipoLiquidacion, TipoLiquidacionAdmin)
admin.site.register(Liquidacion, LiquidacionAdmin)
admin.site.register(Reparticion, ReparticionAdmin)
admin.site.register(Registro, RegistroAdmin)
