from django.db import models

# Create your models here.
class TipoLiquidacion(models.Model):
	tipo = models.CharField(max_length=100)
	created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
	updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")
	
	class Meta:
		verbose_name = "Tipo de liquidacion"
		verbose_name_plural = "Tipos de Liquidacion"

	def __str__(self):
		return self.tipo

class Liquidacion(models.Model):
	tipo = models.ForeignKey(TipoLiquidacion,on_delete=models.CASCADE)
	liquidacion = models.CharField(max_length=200,unique=True)
	observación = models.TextField(blank=True,null=True)
	abierta = models.BooleanField(default=True)
	created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
	updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

	class Meta:
		verbose_name = "Liquidacion"
		verbose_name_plural = "Liquidaciones"

	def __str__(self):
		return self.liquidacion

class Reparticion(models.Model):
	nro = models.IntegerField(unique=True)
	saf = models.IntegerField()
	denominacion = models.CharField(max_length=300)
	created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
	updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

	class Meta:
		verbose_name = "Reparticion"
		verbose_name_plural = "Reparticiones"
		ordering = ["nro"]

	def __str__(self):
		return self.denominacion

class Registro(models.Model):
	liquidacion = models.ForeignKey(Liquidacion,on_delete=models.CASCADE)
	reparticion = models.ForeignKey(Reparticion,on_delete=models.CASCADE)
	importe = models.DecimalField(decimal_places=2,max_digits=50,default=0)
	op = models.IntegerField(blank=True,null=True)
	fechaME = models.DateField(blank=True,null=True,verbose_name="Fecha ME")
	pagado = models.DecimalField(decimal_places=2,max_digits=50,blank=True,null=True)
	saldo = models.DecimalField(decimal_places=2,max_digits=50,blank=True,null=True)
	created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
	updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

	class Meta:
		verbose_name = "Registro"
		verbose_name_plural = "Registros"
		ordering = ["-created"]

	def __str__(self):
		return (f'{self.reparticion.tipo} - {self.liquidacion.liquidacion}') 