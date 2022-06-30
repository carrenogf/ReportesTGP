from django.shortcuts import render
from .forms import unirpdfForm
from .scripts import unir
from django.contrib import messages 

# Create your views here. 
def unirpdfView(request):
    form = unirpdfForm(request.POST, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            files = request.FILES.getlist('files')
            filename = "pdf-unido.pdf"
            response = unir(files,filename)
            if response:
                return response
            else:
                messages.error(request, "Debe seleccionar más de un archivo pdf")

    form = unirpdfForm(request.POST, request.FILES)
    return render(request, 'pdfs_upload.html', {'form': form})
