from django.shortcuts import render, redirect
from .forms import Upload_Form
from .scripts import carga_sistemas,sueldos_mesaEntrada
import pandas as pd

# Create your views here.
def sistemasView(request):
	form = Upload_Form(request.POST, request.FILES)
	if request.method == 'POST':
		if form.is_valid():
			if request.FILES['file'].name.endswith('xlsx') or request.FILES['file'].name.endswith('xls'):
				liquidacion = request.POST.get('liquidacion')
				request.session['liquidacion'] = liquidacion
				excel = request.FILES['file'].temporary_file_path()
				lista_carga, liquidacion_nombre = carga_sistemas(excel,liquidacion)
				request.session['lista_carga'] = lista_carga
				request.session['liquidacion_nombre'] = liquidacion_nombre
				return redirect('sistemas_succes')

	form = Upload_Form(request.POST, request.FILES)
	return render(request, 'sueldos_sistemas_upload.html', {'form': form})

def sistemas_succes(request):
	context = {
	"liquidacion_nombre":request.session['liquidacion_nombre'] ,
	"lista_carga":request.session['lista_carga'] 
	}
	return render(request, 'sueldos_sistemas_succes.html', context=context)

def mesaEntrada(request):
	form = Upload_Form(request.POST, request.FILES)
	if request.method == 'POST':
		if form.is_valid():
			if request.FILES['file'].name.endswith('txt') or request.FILES['file'].name.endswith('TXT'):
				liquidacion = request.POST.get('liquidacion')
				request.session['liquidacion'] = liquidacion
				excel = request.FILES['file'].temporary_file_path()
				lista_carga, liquidacion_nombre = sueldos_mesaEntrada(excel,liquidacion)
				request.session['lista_carga'] = lista_carga
				request.session['liquidacion_nombre'] = liquidacion_nombre
				return redirect('me_succes')

	form = Upload_Form(request.POST, request.FILES)
	return render(request, 'sueldos_Me_upload.html', {'form': form})


def mesaEntrada_succes(request):
	context = {
	"liquidacion_nombre":request.session['liquidacion_nombre'] ,
	"lista_carga":request.session['lista_carga'] 
	}

	return render(request, 'sueldos_Me_succes.html', context=context)