import pandas as pd
from .models import Reportes
from ast import literal_eval
from io import BytesIO
import pandas as pd
from django.http import HttpResponse
import re

def descarga_excel(df,filename,col_float=[]):
	with BytesIO() as b:
		# Use the StringIO object as the filehandle.
		writer = pd.ExcelWriter(b, engine='xlsxwriter',
			datetime_format='dd/mm/yyyy',
			date_format='dd/mm/yyyy')
		df.to_excel(writer,index=False, sheet_name='Hoja1')
		# aplica formato a las columnas que se le indican
		wb = writer.book
		ws = writer.sheets['Hoja1']
		float_format = wb.add_format({'num_format': '#,##0.00'})
		for col in col_float:
			ws.set_column(col, col, None, float_format)
		writer.save()
		# Set up the Http response.
		response = HttpResponse(
			b.getvalue(),
			content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
		)
		response['Content-Disposition'] = 'attachment; filename=%s' % filename
		return response

def descarga_txt(df,filename):
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = f'attachment; filename={filename}.txt'
	df.to_csv(path_or_buf=response,sep='\t',index=False, header=False, decimal=',')
	return response

def abrir_txt(txt,reporte):
	if len(txt)>1:
		float_cols=[]
		r = Reportes.objects.get(id = int(reporte))
		tipoTxt = r.tipo_txt
		filename = f'{r.nombre}.xlsx'
		# archivos de ancho fijo----------------------------------------------------------
		if tipoTxt == "ancho fijo":
			if r.columnas:
				titulos = literal_eval(r.columnas)
				if r.nombre == "Pagos archivo plano":
					df = pd.read_fwf(txt,encoding='cp1252',header=None,sep='delimiter', colspecs=list(titulos.values()))
					df.columns = list(titulos.keys())
					df = df.drop(['F_Fact','Tipo_Fact','Pto_Vta','N_Fact','Monto_Fact'],axis=1)
					df = df.drop_duplicates(keep='last')
					df= df.drop(df[df['Anulado_(S/N)']=='S'].index)
					df= df.drop(df[df['Monto']=='#############'].index)
					df=df.apply(lambda x: pd.to_datetime(x,errors = 'ignore', format = '%Y%m%d'))
					df['Monto'] = df['Monto'].astype('float',errors='ignore')/100
					df = df[df["Monto"] >0].reset_index()
					df = df.drop('index',axis=1)

					return descarga_excel(df,filename,float_cols)

				if r.nombre == "Pagos archivo plano con facturas":
					df = pd.read_fwf(txt,encoding='cp1252',header=None,sep='delimiter', colspecs=list(titulos.values()))
					df.columns = list(titulos.keys())
					#df = df.drop(['F_Fact','Tipo_Fact','Pto_Vta','N_Fact','Monto_Fact'],axis=1)
					#df = df.drop_duplicates(keep='last') esto saca las facturas
					df= df.drop(df[df['Anulado_(S/N)']=='S'].index)
					df= df.drop(df[df['Monto']=='#############'].index)
					df=df.apply(lambda x: pd.to_datetime(x,errors = 'ignore', format = '%Y%m%d'))
					df['Monto'] = df['Monto'].astype('float',errors='ignore')/100
					df = df[df["Monto"] >0].reset_index()
					df = df.drop('index',axis=1)

					return descarga_excel(df,filename,float_cols)

				#ir agregando los otros casos
		# archivos delimitados------------------------------------------------------------
		if tipoTxt == "delimitado":
			if r.delimitador:
				if r.delimitador=='tab':
					delim = '\t'

				if r.nombre == "Reporte de Mesa de Entrada":
					df,float_cols = mesaEntrada(txt,delim)
					
				if r.nombre == "Detalle de Gastos de Ej Anteriores":
					df = detalleGA(txt,delim)

				if r.nombre == "Detalle de Movimientos de Anticipos":
					df = detalleMovAnticipos(txt,delim)

				if r.nombre == "Detalle MIE por cod HTML":
					df = detalleMieHtml(txt)

				if r.nombre == "Libro Banco detallado con Glosa":
					df,float_cols = banco_con_glosa(txt)

				if r.nombre == "Detalle de Conciliaciones Bancarias":
					df = detalle_conciliciones(txt)

				if r.nombre == "Detalle de Pagos por Fecha":
					df = pagos_por_fecha(txt)

				if r.nombre == "Detalle de la Deuda":
					df = detalle_deuda(txt)

				if r.nombre == "Detalle de Transacciones de Tesorería":
					df = transacciones_tesoreria(txt)

				if r.nombre == "Ejec. Rec. c/Afec. Esp. c/Est. Presup.":
					df, float_cols = ejec_pres_afec_esp_estruc(txt)

				if r.nombre == "Detalle de Comprobantes de Gasto":
					df, float_cols = detalle_gastos(txt)

				df = df.drop('index',axis=1)
				

				return descarga_excel(df,filename,float_cols)

		return None
	return None # txt vacio	

def resumen_banco(path):
	df = pd.read_excel(path)
	cuenta = df.iloc[4][2]
	df =df.drop(df.columns[[1,2,7,8,9]],axis=1)
	df.insert(0, 'cuenta', cuenta)
	df=df.drop(range(7),axis=0)
	df=df.dropna(axis=0)
	df = df.reset_index(drop=True)
	df.columns=['Cuenta','Fecha','Nro. de Referencia','Causal','Concepto','Importe','Saldo']
	df['Importe'] = df['Importe'].astype(float)
	df['Saldo'] = df['Saldo'].astype(float) 
	df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce',dayfirst=True)
	df['Fecha'] = df['Fecha'].dt.strftime('%d/%m/%Y')
	filename = 'ResumenBanco'
	return df,filename

def resumen_banco_txt(txt):
	titulos = {
				'Fecha':(0,12),
				'Nro. de Referencia':(12,21),
				'Causal':(25,29),
				'Concepto':(32,63),
				'Importe':(63,80),
				'Saldo':(80,98)
				}

	df = pd.read_fwf(txt,header=None,sep='delimiter', colspecs=list(titulos.values()))
	cuenta = str(df.iloc[3][0])+str(df.iloc[3][1])
	cuenta = cuenta.split(' ')[1]
	df=df.drop(range(8),axis=0)
	df.insert(0, 'cuenta', cuenta)
	df=df.dropna(axis=0)
	df.columns=['Cuenta','Fecha','Nro. de Referencia','Causal','Concepto','Importe','Saldo']
	for c in ['Importe','Saldo']:
		df[c] = df[c].str.replace("$","")
		df[c] = df[c].str.replace(" ","")
		df[c] = df[c].str.replace(".","")
		df[c] = df[c].str.replace(",",".")

	df.loc[df['Importe']=="",'Importe']=0
	df.loc[df['Saldo']=="",'Saldo']=0

	df['Importe'] = df['Importe'].astype(float)
	df['Saldo'] = df['Saldo'].astype(float) 
	df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')
	df['Fecha'] = df['Fecha'].dt.strftime('%d/%m/%Y')
	filename = 'ResumenBanco'
	return df,filename

def mesaEntrada(txt,delim):
	df = pd.read_csv(txt,encoding='cp1252',error_bad_lines=False,header=None, sep=delim,engine='python',decimal=',')
	df = df.iloc[:,15:30]
	df.columns = ['N° orden','Tipo cpte','Tipo gasto','Migrado','PT','Fecha ME','Entidad',
	'Descripcion','Cod','Fecha Comp','Monto','Monto pagado','Saldo','Liquido','Retenciones']
	df = df.drop(df[df['Monto']=="N"].index ,axis = 0)
	df = df.reset_index()
	df['Fecha ME'] = pd.to_datetime(df['Fecha ME'], errors='coerce',dayfirst=True)
	df['Fecha Comp'] = pd.to_datetime(df['Fecha Comp'], errors='coerce',dayfirst=True)
	for c in ['Monto','Monto pagado','Saldo','Liquido','Retenciones']:
		df[c] = df[c].replace(" ","",regex=True)
		df[c] = df[c].replace(",","",regex=True)
		df[c] = df[c].astype(float,errors='ignore')
	float_cols=[10,11,12,13,14]
	return df,float_cols


def detalleGA(txt,delim):
	df = pd.read_csv(txt,encoding='cp1252',error_bad_lines=False,header=None, sep=delim,engine='python',decimal=',')
	df = df.drop([2,3,4,5,6,8,9,10,11,12,27,33,34,35,36,37,38,39],axis=1) #elimina columna vacia
	df.columns = ['Entidad','Descripcion','Fecha',
			  'Rev','Saldo','Monto pagado',
			  'A','PT ret','Monto total',
			  'N° Entrada','Fte fin','Org fin',
			  'Expte','Monto liquido',
			  'Monto ret','Reg','Clase',
			  'Glosa','N° orig','Gasto',
			  'N° cuenta','PT liq']

	# Reordena las columnas
	df= df[['Entidad','Descripcion','Fecha',
		  'N° cuenta','N° Entrada','N° orig',
		  'Fte fin','Org fin','Expte',
		  'Reg','Clase','Gasto',
		  'Glosa','A','Rev','PT liq','PT ret',
		  'Monto total','Monto liquido','Monto ret','Monto pagado','Saldo']]

	for c in ['Monto total','Monto liquido','Monto ret','Monto pagado','Saldo']:
		df[c] = df[c].replace(" ","",regex=True)
		df[c] = df[c].replace(",","",regex=True)
		df[c] = df[c].astype(float)

	df = df.reset_index()
	df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce',dayfirst=True)
	#df['Fecha'] = df['Fecha'].dt.strftime('%d/%m/%Y')
	return df

def detalleMovAnticipos(txt,delim):
	texto_lista = []
	with open(txt,'r') as archivo:
		for linea in archivo:
			renglon = linea[0:500].split('\t')[26:51]
			texto_lista.append(renglon)
			
	df = pd.DataFrame(texto_lista)
	ent = 0
	lista_entidades = []
	for i in range(len(df)):
		if df.iloc[i,0]=='JURISDICCION:':
			ent = df.iloc[i,1]
		lista_entidades.append(ent)
		
	df['Entidad'] = lista_entidades
	df = df.drop(df[df[0]=='JURISDICCION:'].index)
	df_dev = df[df[13]=='DEV']
	df_reg = df[df[12]=='REG']
	df = df.drop(df[df[13]=='DEV'].index)
	df = df.drop(df[df[12]=='REG'].index)
	df = df.drop([3,4,11,12],axis=1)
	df.columns = range(len(df.columns))

	#REG
	df_reg['N° reg'] = df_reg[0]
	df_reg = df_reg.drop([0,9,11,24],axis=1)
	df_reg.columns = range(len(df_reg.columns))
	#DEV
	df_dev = df_dev.drop([3,4,11,12],axis=1)
	df_dev.columns = range(len(df_dev.columns))

	df = pd.concat([df,df_reg,df_dev],ignore_index=True).fillna('0')
	df.columns=['N° entrada','Descripción',
			'EJ','N° orig','Expte','Fecha','Cod',
			'Fte fin','Cuit','Tipo','Clase','A','R','C',
			'N° cta','N° cta dev','Monto','Monto ent',
			'Monto canc','Monto dev','Monto rev','Entidad','N° Reg']
	df = df.reset_index()
	df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce',dayfirst=True)
	#df['Fecha'] = df['Fecha'].dt.strftime('%d/%m/%Y')
	for c in ['Monto','Monto ent','Monto canc','Monto dev','Monto rev']:
		try:
			df[c] = df[c].replace(" ","",regex=True)
			df[c] = df[c].replace(",","",regex=True)
			df[c] = df[c].astype(float)
		except:
			pass

	for c in ['N° entrada','N° orig','Cod','Fte fin','N° cta','N° cta dev','Entidad','N° Reg']:
		try:
			df[c] = df[c].astype(int)
		except:
			pass
	return df

def detalleMieHtml(path):
	with open(path) as file:
		text = file.read()
		text = text.replace("\n","")
		regex = ">([ \w\-,\.\/\)\(°&º'\%:\$#!\?¿=\+\"\&;\|`·\*']*[^>])<\/"
		result = re.findall(regex,text)

	ncuenta = ""
	cuenta = ""
	ent = ""
	nent = ""
	op = ""
	iop = 0
	final = []
	for i, val in enumerate(result):
		if val=="Cuenta:":
			ncuenta=result[i+1]
			cuenta=result[i+2]
			continue
		if val=="Entidad:":
			ent=result[i+1]
			nent=result[i+2]
			continue
		if val=="Operación:":
			j=i+1
			while not (result[j].isdigit() and len(result[j])==3):
				j=j+1
			op=result[j]
			iop = j+5
			continue
		if i==iop:
			if not val.isdigit():
				iop=iop+1
			else:
				final.append([ncuenta,cuenta,ent,nent,op]+result[i:i+16])
				if result[i+15]==result[i+16]:#tomo el nro de op siguiente como glosa por lo q debería empezar antes el sig reg
					iop=i+15
				else:
					iop=i+16
			
	columnas = [ 'Nro Cuenta','Cuenta','Nro Ent','Entidad','Cod','Nro. Entrada', 'Nro. Original', 'Tip. Mov.', 'Fecha','I', 'C', 'C', 'A', 'Doc','Nro Doc','Fecha doc','Monto Ingresos',
				'Monto Egresos', 'Monto Cancelado', 'Monto Saldo','Glosa']
	df = pd.DataFrame(final[1:],columns=columnas)
	df_corregir = df[(df['Nro. Original']=="MI")|(df['Nro. Original']=="ME")]
	df = df.drop(df[(df['Nro. Original']=="MI")|(df['Nro. Original']=="ME")|(df['Nro. Original']=="Fecha :")].index)
	corregir = ['Nro. Original','Tip. Mov.','Fecha','I','C','C','A','Doc','Nro Doc','Fecha doc','Monto Ingresos',
				'Monto Egresos','Monto Cancelado','Monto Saldo','Glosa']
	corregir=corregir[::-1]
	for i in range(len(corregir)-1):
		df_corregir[corregir[i]]=df_corregir[corregir[i+1]]
	df_corregir["Nro. Original"]= df_corregir["Nro. Entrada"]

	final = pd.concat([df,df_corregir])
	for c in ['Monto Ingresos','Monto Egresos','Monto Cancelado','Monto Saldo']:
		try:
			final[c] = final[c].replace(" ","",regex=True)
			final[c] = final[c].replace(",","",regex=True)
			final[c] = pd.to_numeric(final[c],errors='coerce')
			#final[c] = final[c].astype(float,errors='ignore')
		except:
			pass


	final = final.reset_index()
	return final

def banco_con_glosa(txt,datos=0):

	# Libro banco con glosa: ---------------------------------------------------------
	# En este reporte, dependiendo del tipo de movimiento o comprobante, tiene más o menos columnas, que no están alineadas
	# la solución será hacer diferentes data frames aplicando filtros, y organizarlos para luego unirlos.
	# por este motivo, no se puede crear directamente el dataframe del txt.

	# abrir el txt, separar por tabulaciones y eliminar espacios y saltos de linea.
	with open(txt,'r') as f:
		lines = f.readlines()
		data = []
		for line in lines:
			row = [i.strip() for i in line.split('\t')]
			data.append(row)
	# columnas finales
	columnas = ["Fecha","Nº Pago","Tipo Mov.","Conf.","FConf.","Ent.","FEnt.","Conc.","Fconc","Exped",
				"Cla. Gto.","CUIT","Glosa","Codigo","N° Ord.","Tipo Pago","Nº Ch Lote","Egreso","Ingreso"]
	# Dataframe, una vez creada la lista y separada por columnas se puede crear el dataframe para trabajar matricialmente
	df = pd.DataFrame(data)
	# Datos de la cuenta-------------------------------------------------------------
	# extraidos de la primera fila, estos datos, excepto el saldo final, se muestran igual en todos los casos
	# como el archivo tiene distintas columnas, el saldo final puede variar en su posición, así que se calculará luego

	ncta = df[1][0] # n° de cuenta
	cta = df[2][0] # Nombre de la Cta
	si = df[4][0] # Saldo Inicial de la cuenta
	sf = None # Se calculará luego

	df = df.drop([0,1,2,3,4,6],axis=1) # elimina las columnas que tenian los datos que ya fueron recolectados previamente
	df['orden'] = range(len(df))
	# Movimientos de cuenta: ---------------------------------------------------------
	# los mov de cta no tienen la columna de n° de pago
	mov_cta = df[df[8]=="Mov. de Ctas."]
	if len(mov_cta)>0: # verifica si hay movimientos de cuenta antes de proceder
		if not sf:
			sf = mov_cta.iloc[0][38] # si el saldo final no fue asignado lo asigna ahora

		col_mov_cta = ["Fecha","E/I","Tipo Mov.","Conf.","FConf.","Ent.","FEnt.","Conc.","Fconc","Exped",
				"Cla. Gto.","CUIT","Glosa","Codigo","N° Ord.","Tipo Pago","Nº Ch Lote","Egreso","Ingreso","orden"]
		mov_cta = mov_cta[[5,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,"orden"]]
		mov_cta.columns = col_mov_cta
	else:
		mov_cta=None

	# MIE: ---------------------------------------------------------------------------
	# los MIE no tinen n° pago ni n° de cheque o lote
	mie = df[(df[8]=="MIE - E")|(df[8]=="MIE - I")]
	if len(mie)>0: # verifica si hay movimientos de cuenta antes de proceder
		if not sf:
			sf = mie.iloc[0][37] # si el saldo final no fue asignado lo asigna ahora
		col_mie = ["Fecha","E/I","Tipo Mov.","Conf.","FConf.","Ent.","FEnt.","Conc.","Fconc","Exped",
			"Cla. Gto.","CUIT","Glosa","Codigo","N° Ord.","Tipo Pago","Egreso","Ingreso","orden"]
		mie = mie[[5,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,"orden"]]
		mie.columns = col_mie
	else:
		mie=None

	# I. Presupuestario: --------------------------------------------------------------
	# el I pres tiene n° de pago, y no tiene n° cheque
	i_presup = df[df[9]=="I.Presupuestario"]
	if len(i_presup)>0: # verifica si hay movimientos de cuenta antes de proceder
		if not sf:
			sf = i_presup.iloc[0][38] # si el saldo final no fue asignado lo asigna ahora
		col_i_presup = ["Fecha","E/I","Nº Pago","Tipo Mov.","Conf.","FConf.","Ent.","FEnt.","Conc.","Fconc","Exped",
				"Cla. Gto.","CUIT","Glosa","Codigo","N° Ord.","Tipo Pago","Egreso","Ingreso","orden"]
		i_presup = i_presup[[5,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,"orden"]]
		i_presup.columns = col_i_presup
	else:
		i_presup=None

	# AF - Dev: ----------------------------------------------------------------------
	af_dev = df[df[8]=="AF - Dev"]
	if len(af_dev)>0:
		if not sf:
			sf = af_dev.iloc[0][37]
		col_af_dev = ["Fecha","E/I","Tipo Mov.","Conf.","FConf.","Ent.","FEnt.","Conc.","Fconc","Exped",
			"Cla. Gto.","CUIT","Glosa","Codigo","N° Ord.","Egreso","Ingreso","orden"]
		af_dev = af_dev[[5,7,8,9,10,11,12,13,14,15,16,17,18,19,20,22,23,"orden"]]
		af_dev.columns = col_af_dev
	else:
		af_dev=None
	
	# Pagos: -------------------------------------------------------------------------
	# los mov de cta no tienen la columna de n° de pago
	pagos = df[(df[24]=="E")|(df[24]=="C")|(df[24]=="A")] #lotes, cheques y automaticos
	if len(pagos)>0: # verifica si hay movimientos de cuenta antes de proceder
		if not sf:
			sf = i_presup.iloc[0][41] # si el saldo final no fue asignado lo asigna ahora
		col_pagos = ["Fecha","E/I","Nº Pago","Tipo Mov.","Conf.","FConf.","Ent.","FEnt.","Conc.","Fconc","Exped",
			"Cla. Gto.","CUIT","Glosa","Codigo","N° Ord.","Tipo Pago","Nº Ch Lote","Egreso","Ingreso","orden"]
		pagos = pagos[[5,7,8,10,11,12,13,14,15,16,17,18,19,20,21,22,24,25,26,27,"orden"]]
		pagos.columns = col_pagos
	else:
		pagos=None

	# concatenar todos los DataFrames
	final = pd.concat([mov_cta,mie,i_presup,af_dev,pagos],ignore_index=True).fillna('-')
	final = final.sort_values(by="orden", ascending=True)
	final = final.drop(['orden'],axis=1)
	for c in ['Egreso','Ingreso']:
		try:
			final[c] = final[c].replace(" ","",regex=True)
			final[c] = final[c].replace(",","",regex=True)
			final[c] = pd.to_numeric(final[c],errors='coerce')
		except:
			pass
	final['Fecha'] = pd.to_datetime(final['Fecha'], errors='coerce',dayfirst=True,format="%d/%m/%Y")
	final['Fecha'] = final['Fecha'].dt.strftime('%d/%m/%Y')
	final['N° Ord.'] = final['N° Ord.'].astype('int64')
	float_cols = [17,18]
	if datos == 0:
		return final.reset_index(),float_cols
	else:
		return final.reset_index(), ncta, cta, si, sf


def detalle_conciliciones(txt):
	with open(txt) as file:
		lines = file.readlines()
		lista = []
		for line in lines:
			row = line.split('\t')
			lista.append(row)

	df = pd.DataFrame(lista)
	df = df.drop([0,18,20],axis=1)
	df.columns = ['N° cta','Cuenta','Ent','N° Ent','N° Conc','F. Inicio','F. Final','Sdo. Inic. lib','Ing. lib',
				'Eg. lib','Sdo. Fin. lib','Sdo Fin. Extracto','No Acred.','No Deb.','Ajustes','F. inf.', 'Anul.','Obs.']
	#Montos
	for c in ['Sdo. Inic. lib','Ing. lib','Eg. lib','Sdo. Fin. lib','Sdo Fin. Extracto','No Acred.','No Deb.','Ajustes']:
		try:
			df[c] = df[c].replace(" ","",regex=True)
			df[c] = df[c].replace(",","",regex=True)
			df[c] = pd.to_numeric(df[c],errors='coerce')
		except:
			pass
	df['F. Inicio'] = pd.to_datetime(df['F. Inicio'], errors='coerce',dayfirst=True)
	df['F. Final'] = pd.to_datetime(df['F. Final'], errors='coerce',dayfirst=True)
	df['F. inf.'] = pd.to_datetime(df['F. inf.'], errors='coerce',dayfirst=True)

	return df.reset_index()

def pagos_por_fecha(txt):
	df = pd.read_csv(txt,encoding='cp1252',engine='python',sep='\t',header=None)
	df = df.fillna('-')

	cuenta = df[19].replace('CUENTA BANCARIA:',"",regex=True).str.split("  ",1,expand=True)
	df[1] = cuenta[0].str.strip()
	df[19] = cuenta[1].str.strip()
	entidad = df[21].replace('ENTIDAD:',"",regex=True).str.split("  ",1,expand=True)
	df[2] = entidad[0].str.strip()
	df[21] = entidad[1].str.strip()
	df[23] = df[23].replace('ORIGEN DEL GASTO: ','',regex=True)
	df[25] = df[25].replace('CLASE DE REGISTRO: ','',regex=True)
	df[27] = df[27].replace('CLASE DE GASTO: ','',regex=True)
	df[29] = df[29].replace('CONCEPTO: ','',regex=True)
	df[32] = df[32].replace('TIPO DE PAGO: ','',regex=True)
	df =df[[1, 19, 2, 21, 23, 25, 27, 29, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41,
				42, 43, 44, 45, 46, 47, 48, 49, 50, 51]]
	df.columns = ["N° cta.","Cuenta","N° Ent.","Entidad","Orig.","Clase Reg.","Clase Gto.","Cpto.","Tipo",
				  "Imputacion","Conf.","F.M.E.","Anul.","Rev.","Cla. mod.","Cod. Ret.","Cuit","Benef.",
				  "N° Ch. o Pe.","Cta. Recept.","N° Ord","N° pago","Impreso","Entreg.","Conciliado",
				  "Expte.","Fte. Fin.","Monto"]
	df["Monto"] = df["Monto"].replace(",","",regex=True)
	df["Monto"] = df["Monto"].astype(float,errors='ignore')
	return df.reset_index()

def detalle_deuda(txt):
	df = pd.read_csv(txt,encoding='cp1252',engine='python',sep='\t',header=None)
	df = df.fillna('-')
	df = df[[1,2,6,10,15,20,24,28,32,33,34,35,36,37,38,39,40,46,43,44,45]]
	df.columns= ["N° Cta.","Cta.","N° Ent.","Ent.","Tipo Gto.","Clase Reg.","Clase Gto.",
			"Cpto.","N° Entrada","N° Orig.","Fecha","Expte","Cla. Mod.","Cod.","Fte. Fin.",
			"Desc.","Cuit","Benef.","Monto Total","Monto Pagado","Saldo"]
	for c in ["Monto Total","Monto Pagado","Saldo"]:
		try:
			df[c] = df[c].replace(" ","",regex=True)
			df[c] = df[c].replace(",","",regex=True)
			df[c] = pd.to_numeric(df[c],errors='coerce')
		except:
			pass
	return df.reset_index()

def transacciones_tesoreria(txt):
	df = pd.read_csv(txt,encoding='cp1252',engine='python',sep='\t',header=None)
	df = df.fillna('-')
	df = df[[0,3,4,5,9,11,12,13,14,15,16,17,19,20,21,18]]
	df.columns = ["Cta.","N° Cta.","N° Ent.","Ent.","Fecha","Deb. Op. Bco.","N° Entrada","N° Ent. Recept.",
				"N° Cta. Recept.","Glosa","Cred. Op. Bco.","I","C","A","C","Monto"]
	df["Monto"] = df["Monto"].replace(",","",regex=True)
	df["Monto"] = df["Monto"].astype(float,errors='ignore')
	return df.reset_index()

def ejec_pres_afec_esp_estruc(txt):
	df = pd.read_csv(txt,encoding='cp1252',header=None, sep='\t',engine='python')
	df=df.reset_index()
	df = df.drop(['level_1','level_2','level_3'],axis=1)

	df_cod = []
	df_denom = []
	df_saldo = []
	cod = 0
	denom = 0
	for i in range(len(df[0])):
		if df[3][i]=='0':
			cod = df[2][i]
			denom = df[4][i]
			saldo = df[9][i]
		df_cod.append(cod)
		df_denom.append(denom)
		df_saldo.append(saldo)

	df[0]=df_cod
	df[1]=df_denom
	df[15] = df_saldo
	df = df.drop(df[df[3]=='0'].index,axis=0)
	df.columns = ["N° Ent","Desc. Ent.","Cod.","Denom. Org.","Cuenta Bco.","Vinc. Cont.",
					"Denom. Bco.","Prog.","SubProg.","Proyec.","Act./Obra","Cta. Esp.",
					"Recaudado","Ordenado","Anticipo","Fdo. Fijo","Saldo","Saldo Tot. Rec."]
	for c in ["Recaudado","Ordenado","Anticipo","Fdo. Fijo","Saldo","Saldo Tot. Rec."]:
		try:
			df[c] = df[c].replace(" ","",regex=True)
			df[c] = df[c].replace(",","",regex=True)
			df[c] = pd.to_numeric(df[c],errors='coerce')
		except:
			pass
	float_cols = [12,13,14,15,16,17]
	return df.reset_index(),float_cols


def detalle_gastos(txt):
	df = pd.read_csv(txt,encoding='cp1252',engine='python',sep='\t',header=None)
	df = df[[0,1,5,9,10,11,12,13,14,15,16,17,18,20,21,22,23,26,27,28,29,30]]
	df.columns = ["N° Ent","Entidad","Fecha","Total","Nro Orig","Fte","Org fin","Expte","Liquido",
	            "Deducciones","REG","MOD","GTO CLA","C","V","O","P","Descripcion","Nro Ord","A","Cuenta","Cod Err",]
	# orden de las columnas
	df = df[["N° Ent","Entidad","Nro Ord","Nro Orig","Cuenta","Fecha","Fte","Org fin","Expte","Total","Liquido",
	            "Deducciones","REG","MOD","GTO CLA","A","C","V","O","P","Descripcion","Cod Err"]]

	for c in ["Total","Liquido","Deducciones"]:
		try:
			df[c] = df[c].replace(" ","",regex=True)
			df[c] = df[c].replace(",","",regex=True)
			df[c] = pd.to_numeric(df[c],errors='coerce')
		except:
			pass
	float_cols = [9,10,11]
	return df.reset_index(),float_cols
