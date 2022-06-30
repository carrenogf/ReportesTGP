from django.shortcuts import render
from .forms import Reportes_Form
from .scripts import abrir_txt, descarga_excel

def reportesView(request):
    form = Reportes_Form(request.POST, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            
            if request.FILES['file'].name.endswith(('TXT','txt','htm','html')):
                txt = request.FILES['file'].temporary_file_path()
                reporte = request.POST.get('reporte')
            
                return(abrir_txt(txt,reporte))


    form = Reportes_Form(request.POST, request.FILES)
    return render(request, 'reportes_upload.html', {'form': form})
