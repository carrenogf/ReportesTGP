import pandas as pd
from io import BytesIO
from django.http import HttpResponse

def descarga_excel(df,filename):
	with BytesIO() as b:
		# Use the StringIO object as the filehandle.
		writer = pd.ExcelWriter(b, engine='xlsxwriter')
		df.to_excel(writer,index=False, sheet_name='Hoja1')
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
	df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')
	df['Fecha'] = df['Fecha'].dt.strftime('%d/%m/%Y')
	filename = 'ResumenBanco'
	return df,filename


def circuitoCerrado(path):
	df = pd.read_excel(path)
	df.columns =['Fecha','Cuenta Credito','Referencia','Numero Transaccion','Importe','Cuenta Debito','Nombre']
	df['Importe'] = df['Importe'].astype(float)
	df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')
	df['Fecha'] = df['Fecha'].dt.strftime('%d/%m/%Y')
	df['Cuenta Debito'] = df['Cuenta Debito'].astype(str)
	#df['Cuenta Debito'].replace('360000200980414','71889988',regex=True, inplace=True)
	filename = 'Complemento SGP'
	return df,filename

def comprobantesPagina(path):
	df = pd.read_csv(path, sep='|', header=None)
	df = df.drop(9,axis=1)
	df = df.dropna(axis=0)
	df.columns = ['Fecha', 'Nref','CBU','Importe','N° OP','tipo','Descripcion','Fecha ent','Usuario']
	df['Usuario'].replace(to_replace='SAF',value="", inplace=True, regex=True)
	df['Usuario'].replace(to_replace='ENT',value="", inplace=True, regex=True)
	df['Usuario']= df['Usuario'].astype(int)
	df['Importe'].replace(to_replace=',',value="", inplace=True, regex=True)
	df['Importe']=df['Importe'].astype(float)
	df['N° OP'] = df['N° OP'].astype(str)
	df['N° OP']= df['N° OP'].str.replace("-","")
	df['N° OP']= df['N° OP'].str[-6:]
	df['CBU']= df['CBU'].str[-23:]
	df['CBU'].replace('0000000360000200970918','2850600130002009709187',regex=True, inplace=True)
	filename='ComprobantesPagina'
	return df, filename

def crucePagSafyc(path1,path2):
	df = pd.DataFrame([{'nombre':'Fran','edad':28},{'nombre':'Franaa','edad':28}])
	df = df.reset_index(drop=True)
	filename = "prueba cruce pagina safyc"
	return df, filename