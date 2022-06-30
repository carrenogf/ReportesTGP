import pandas as pd
from .models import Liquidacion, Registro, Reparticion
import json
import numpy as np


def carga_sistemas(path,liquidacion):
	#l = Liquidacion.objects.get(id = int(liquidacion))
	df = pd.read_html(path,decimal=',', thousands='.')[0]
	df['LIQPEN'] = df['LIQPEN'].astype(float) 
	df['DEVGAN'] = df['DEVGAN'].astype(float) 
	df['IMPORTE'] = df['LIQPEN']-df['DEVGAN'].round(2)
	tabla = df.to_dict('records')
	lista_carga = []
	liquidacion_nombre = Liquidacion.objects.get(id=liquidacion).liquidacion
	for line in tabla:
		if Reparticion.objects.filter(nro=line['REP']).exists():
			id_reparticion = Reparticion.objects.get(nro=line['REP']).id
			if not Registro.objects.filter(liquidacion=liquidacion).filter(reparticion=id_reparticion).exists():
				r = Registro()
				r.liquidacion = Liquidacion.objects.get(id=liquidacion)
				r.reparticion = Reparticion.objects.get(id=id_reparticion)
				r.importe = line['IMPORTE']
				lista_carga.append(line)
				r.save()

	return lista_carga, liquidacion_nombre


def sueldos_mesaEntrada(txt,liquidacion):
	df = pd.read_csv(txt,encoding='cp1252',error_bad_lines=False,header=None, sep='\t',engine='python',decimal=',')
	df = df.iloc[:,15:30]
	df.columns = ['N° orden','Tipo cpte','Tipo gasto','Migrado','PT','Fecha ME','Entidad',
	'Descripcion','Cod','Fecha Comp','Monto','Monto pagado','Saldo','Liquido','Retenciones']
	df = df.drop(df[df['Monto']=="N"].index ,axis = 0)
	df = df.reset_index()
	df = df[(df['Cod']=='391')|(df['Entidad']=='50')]
	df['Fecha ME'] = pd.to_datetime(df['Fecha ME'], errors='coerce')
	df['Fecha ME'] = df['Fecha ME'].dt.strftime('%Y-%m-%d')
	df['N° orden']=df['N° orden'].astype(int,errors='ignore')
	for c in ['Monto','Monto pagado','Saldo','Liquido','Retenciones']:
		df[c]=df[c].str.strip()
		df[c]=df[c].str.replace(',','')
		df[c] = df[c].astype(float,errors='raise')
	df = df.fillna('')
	liquidacion_nombre = Liquidacion.objects.get(id=liquidacion).liquidacion
	carga = Registro.objects.filter(liquidacion=liquidacion)
	lista_carga = []
	for r in carga:
		busqueda = None
		op = None
		fMe = None
		pagado = None
		saldo = None
		if not r.op: #el registro no tiene cargado el nro de op, se actualiza todo
			try:
				#busca por el monto en cada registro agregado previamente de la planilla de sistemas
				busqueda = df[df['Monto']==float(r.importe)].iloc[0] # busca por monto
				op = busqueda['N° orden']
				fMe = busqueda['Fecha ME']
				pagado = busqueda['Monto pagado']
				saldo = busqueda['Saldo']
			except: 
				pass
			if op!=None:
				print(op)
				#r.update(op=op)
				if fMe=='':
					Registro.objects.filter(id=r.id).update(op=op,pagado=pagado,saldo=saldo)
				else:
					Registro.objects.filter(id=r.id).update(op=op,fechaME=fMe,pagado=pagado,saldo=saldo)

				lista_carga.append({'Rep':str(r.reparticion.denominacion),'Op':int(op)})
		else: #el regisro ya tiene cargado el nro de op, puede ser cargado manualmente, se actualiza todo menos el nro op
			try:
				busqueda = df[df['N° orden']==int(r.op)].iloc[0] # busca por op
				op = busqueda['N° orden']
				fMe = busqueda['Fecha ME']
				pagado = busqueda['Monto pagado']
				saldo = busqueda['Saldo']
			except:
				pass
			if op!=None:
				if fMe=='':
					Registro.objects.filter(id=r.id).update(pagado=pagado,saldo=saldo)
				else:
					Registro.objects.filter(id=r.id).update(fechaME=fMe,pagado=pagado,saldo=saldo)
				lista_carga.append({'Rep':str(r.reparticion.denominacion),'Op':int(op)})

	return lista_carga, liquidacion_nombre