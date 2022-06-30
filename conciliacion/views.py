from django.shortcuts import render
from .forms import crucePagSafycForm
from reporte.scripts import banco_con_glosa,resumen_banco
from conciliacion.scripts import descarga_excel_2, cruce_conciliacion
# Create your views here.
def conciliacionView(request):
    form = crucePagSafycForm(request.POST, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            if request.FILES['glosa'].name.endswith(('txt','TXT')):
                if request.FILES['macro'].name.endswith(('xls','xlsx','txt','TXT')):
                    #glosa = request.FILES['glosa'].read()
                    #macro = request.FILES['macro'].read()
                    glosa = request.FILES['glosa'].temporary_file_path()
                    macro = request.FILES['macro'].temporary_file_path()

                    df_safyc, df_macro, filename = cruce_conciliacion(glosa,macro)

                    return(descarga_excel_2(df_safyc,df_macro,filename))

    return render(request, 'conciliacion_upload.html', {'form': form})