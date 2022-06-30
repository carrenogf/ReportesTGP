from django.shortcuts import render
from .forms import uploadOneFileForm, crucePagSafycForm
from .scripts import resumen_banco, descarga_txt, circuitoCerrado,comprobantesPagina,crucePagSafyc

# Create your views here.
def resumenBancoView(request):
    form = uploadOneFileForm(request.POST, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            if request.FILES['file'].name.endswith(('xlsx','xls')):
                excel = request.FILES['file'].temporary_file_path()
                df, filename = resumen_banco(excel)

                return(descarga_txt(df,filename))

    form = uploadOneFileForm(request.POST, request.FILES)
    return render(request, 'resumen_upload.html', {'form': form})

def circuitoCerradoView(request):
    form = uploadOneFileForm(request.POST, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            if request.FILES['file'].name.endswith(('xlsx','xls')):
                excel = request.FILES['file'].temporary_file_path()
                df, filename = circuitoCerrado(excel)

                return(descarga_txt(df,filename))

    form = uploadOneFileForm(request.POST, request.FILES)
    return render(request, 'circuitoCerrado_upload.html', {'form': form})

def comprobantesPaginaView(request):
    form = uploadOneFileForm(request.POST, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            if request.FILES['file'].name.endswith(('txt','TXT')):
                txt = request.FILES['file'].temporary_file_path()
                df, filename = comprobantesPagina(txt)

                return(descarga_txt(df,filename))

    form = uploadOneFileForm(request.POST, request.FILES)
    return render(request, 'comprobantesPagina_upload.html', {'form': form})

def crucePagSafycView(request):
    form = crucePagSafycForm(request.POST, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            if request.FILES['pag'].name.endswith(('txt','TXT')):
                pag = request.FILES['pag'].temporary_file_path()

                if request.FILES['safyc'].name.endswith(('txt','TXT')):
                    safyc = request.FILES['safyc'].temporary_file_path()
                    df, filename = crucePagSafyc(pag,safyc)

                    return(descarga_txt(df,filename))

    form = crucePagSafycForm(request.POST, request.FILES)
    return render(request, 'crucePagSafyc_upload.html', {'form': form})