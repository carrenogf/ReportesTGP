from reporte.scripts import descarga_excel, banco_con_glosa,resumen_banco, resumen_banco_txt
import pandas as pd
from io import BytesIO
from django.http import HttpResponse

def descarga_excel_2(df1,df2,filename):
	with BytesIO() as b:
		# Use the StringIO object as the filehandle.
		writer = pd.ExcelWriter(b, engine='xlsxwriter',
			datetime_format='dd/mm/yyyy',
			date_format='dd/mm/yyyy')
		df1.to_excel(writer,index=False, sheet_name='Safyc')
		df2.to_excel(writer,index=False, sheet_name='Banco')
		writer.save()
		# Set up the Http response.
		response = HttpResponse(
			b.getvalue(),
			content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
		)
		response['Content-Disposition'] = 'attachment; filename=%s' % filename
		return response


def cruce_conciliacion(glosa,macro):
	pd.options.display.float_format = '{:.2f}'.format
	pd.options.mode.chained_assignment = None
	df_safyc, ncta, cta, si, sf = banco_con_glosa(glosa,datos=1)
	
	df_safyc = df_safyc.drop('index',axis=1)

	if macro.endswith(('xls','xlsx')):
		df_macro = resumen_banco(macro)[0]

	if  macro.endswith(('txt','TXT')):
		df_macro = resumen_banco_txt(macro)[0]

	df_macro['Importe'] = df_macro['Importe'].round(2)
	df_safyc['Ingreso'] = df_safyc['Ingreso'].round(2)
	df_safyc['Egreso'] = df_safyc['Egreso'].round(2)

	df_safyc['indice'] = df_safyc.index
	df_macro['indice'] = df_macro.index

	df_safyc['Fecha'] = pd.to_datetime(df_safyc['Fecha'],format="%d/%m/%Y")
	df_macro['Fecha'] = pd.to_datetime(df_macro['Fecha'],format="%d/%m/%Y")
	df_macro['Fecha'] = df_macro['Fecha'].dt.strftime('%d/%m/%Y')
	df_safyc['Fecha'] = df_safyc['Fecha'].dt.strftime('%d/%m/%Y')

	df_safyc['Coincidencia'] = 0
	df_macro['Coincidencia'] = 0
	# eliminar los anulados del safyc
	# elimina los comprobantes cuya suma de importe da cero, lo que indica que está anulado
	#no_pago = (df_safyc['Tipo Pago']!="E")&(df_safyc['Tipo Pago']!="C")&(df_safyc['Tipo Pago']!="A")
	df_safyc_no_pago = df_safyc[df_safyc['Tipo Pago']==""]

	xcomp = pd.DataFrame(df_safyc_no_pago.groupby("N° Ord.").sum()[['Ingreso','Egreso']])
	xcomp_0 = xcomp[(xcomp['Ingreso']==0)&(xcomp['Egreso']==0)]

	xlote = pd.DataFrame(df_safyc.groupby("Nº Ch Lote").sum().round(2)[['Ingreso','Egreso']])
	xlote_0 = xlote[(xlote['Ingreso']==0)&(xlote['Egreso']==0)]

	if len(xcomp_0)>0:
		df_safyc = df_safyc.drop(df_safyc[(df_safyc['N° Ord.'].isin(xcomp_0.index))].index,axis=0)
	if len(xlote_0)>0:
		df_safyc = df_safyc.drop(df_safyc[df_safyc['Nº Ch Lote'].isin(xlote_0.index)].index,axis=0)
	# Eliminar recursos anulados
	# solo se eliminan los recursos que tienen la misma fecha y monto en negativo
	xrecurso = df_safyc[df_safyc['Tipo Mov.']=='I.Presupuestario']
	xrecurso_neg = xrecurso[xrecurso['Ingreso']<0]

	if len(xrecurso_neg)>0:
		for index, r in xrecurso_neg.iterrows():
			monto_pos = r['Ingreso']*(-1)
			fecha = r['Fecha']
			rec_coincidencia = xrecurso[(xrecurso['Ingreso']==monto_pos)&(xrecurso['Fecha']==fecha)]
			rec_coincidencia_neg = xrecurso_neg[(xrecurso_neg['Ingreso']==r['Ingreso'])&(xrecurso_neg['Fecha']==fecha)]
			print(len(rec_coincidencia),len(rec_coincidencia_neg))
			if len(rec_coincidencia)==len(rec_coincidencia_neg):
				indice_borrar = df_safyc.loc[df_safyc['indice'].isin(list(rec_coincidencia['indice']))].index
				df_safyc=df_safyc.drop(df_safyc.loc[df_safyc['indice'].isin(list(rec_coincidencia['indice']))].index,axis=0)
				df_safyc=df_safyc.drop(df_safyc.loc[df_safyc['indice'].isin(list(rec_coincidencia_neg['indice']))].index,axis=0)
	
	# Cruce lotes
	# lm = lotes macro / ls = lotes safyc

	lm = df_macro[df_macro['Causal']=='40'][['Nro. de Referencia','Importe']]
	lm = lm.rename(columns={'Nro. de Referencia':'Lote','Importe':'Importe_m'}).set_index('Lote')
	lm['Importe_m'] = lm['Importe_m'].abs()

	lotes_safyc = df_safyc[df_safyc['Tipo Pago']=='E']
	lotes_safyc = lotes_safyc.rename(columns={'Egreso':'Importe_s','Nº Ch Lote':'Lote'})
	ls = pd.DataFrame(lotes_safyc.groupby("Lote").sum()['Importe_s'])

	l_ok = lm.join(ls).round(2)
	l_ok['dif']=l_ok['Importe_m']-l_ok['Importe_s']
	l_ok = l_ok[l_ok['dif']==0]

	# tildar los lotes ok

	df_safyc.loc[(df_safyc['Nº Ch Lote'].isin(l_ok.index))&(df_safyc['Tipo Pago']=='E'),'Coincidencia']=1
	df_macro.loc[(df_macro['Nro. de Referencia'].isin(l_ok.index))&(df_macro['Causal']=='40'),'Coincidencia']=1 
	#cruce safyc por monto:

	df_safyc_0 = df_safyc[df_safyc['Coincidencia']==0]
	df_macro_0 = df_macro[df_macro['Coincidencia']==0]
	m_ing = df_macro_0[df_macro_0['Importe']>0]
	m_eg = df_macro_0[df_macro_0['Importe']<0]
	m_eg['Importe'] = m_eg['Importe'].abs()

	for index, s in df_safyc_0.iterrows():
		if s['Ingreso']>0:
			coincidencia_ing = m_ing[m_ing['Importe']==s['Ingreso']]
			coincidencia_safyc = df_safyc_0[df_safyc_0['Ingreso']==s['Ingreso']]
			if len(coincidencia_ing)>0:
				if len(coincidencia_safyc)==len(coincidencia_ing):
					df_safyc.loc[df_safyc['indice'].isin(list(coincidencia_safyc['indice'])),'Coincidencia']=1
				else:
					coincidencia_fecha = coincidencia_ing[coincidencia_ing['Fecha']==s['Fecha']]
					coincidencia_safyc_fecha = coincidencia_safyc[coincidencia_safyc['Fecha']==s['Fecha']]
					if len(coincidencia_fecha)==len(coincidencia_safyc_fecha):
						df_safyc.loc[df_safyc['indice'].isin(list(coincidencia_safyc_fecha['indice'])),'Coincidencia']=1
					
		if s['Egreso']>0:
			coincidencia_eg = m_eg[m_eg['Importe']==s['Egreso']]
			coincidencia_safyc = df_safyc_0[df_safyc_0['Egreso']==s['Egreso']]
			if len(coincidencia_eg)>0:
				if len(coincidencia_safyc)==len(coincidencia_eg):
					df_safyc.loc[df_safyc['indice'].isin(list(coincidencia_safyc['indice'])),'Coincidencia']=1
				else:
					coincidencia_fecha = coincidencia_eg[coincidencia_eg['Fecha']==s['Fecha']]
					coincidencia_safyc_fecha = coincidencia_safyc[coincidencia_safyc['Fecha']==s['Fecha']]
					if len(coincidencia_fecha)==len(coincidencia_safyc_fecha):
						df_safyc.loc[df_safyc['indice'].isin(list(coincidencia_safyc_fecha['indice'])),'Coincidencia']=1

	#cruce macro por monto:
	s_ing = df_safyc_0[df_safyc_0['Ingreso']>0]
	s_eg = df_safyc_0[df_safyc_0['Egreso']>0]

	for index, m in df_macro_0.iterrows():
		if m['Importe']>0:
			coincidencia_ing = s_ing[s_ing['Ingreso']==m['Importe']]
			coincidencia_macro = df_macro_0[df_macro_0['Importe']==m['Importe']]
			if len(coincidencia_ing)>0:
				if len(coincidencia_macro)==len(coincidencia_ing):
					df_macro.loc[df_macro['indice'].isin(list(coincidencia_macro['indice'])),'Coincidencia']=1
				else:
					coincidencia_fecha = coincidencia_ing[coincidencia_ing['Fecha']==m['Fecha']]
					coincidencia_macro_fecha = coincidencia_macro[coincidencia_macro['Fecha']==m['Fecha']]
					if len(coincidencia_fecha)==len(coincidencia_macro_fecha):
						df_macro.loc[df_macro['indice'].isin(list(coincidencia_macro_fecha['indice'])),'Coincidencia']=1
					
		if m['Importe']<0:
			importe_pos = m['Importe']*(-1)
			coincidencia_eg = s_eg[s_eg['Egreso']==importe_pos]
			coincidencia_macro = df_macro_0[df_macro_0['Importe']==m['Importe']]
			if len(coincidencia_eg)>0:
				if len(coincidencia_macro)==len(coincidencia_eg):
					df_macro.loc[df_macro['indice'].isin(list(coincidencia_macro['indice'])),'Coincidencia']=1
				else:
					coincidencia_fecha = coincidencia_eg[coincidencia_eg['Fecha']==m['Fecha']]
					coincidencia_macro_fecha = coincidencia_macro[coincidencia_macro['Fecha']==m['Fecha']]
					if len(coincidencia_fecha)==len(coincidencia_macro_fecha):
						df_macro.loc[df_macro['indice'].isin(list(coincidencia_macro_fecha['indice'])),'Coincidencia']=1

	df_safyc = df_safyc.drop(columns=['indice'],axis=1).reset_index().drop(columns='index',axis=1)
	df_macro = df_macro.drop(columns=['indice'],axis=1).reset_index().drop(columns='index',axis=1)
	filename = f"Resultado {ncta}.xlsx"
	return df_safyc, df_macro, filename