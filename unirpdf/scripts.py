from PyPDF2 import PdfFileMerger
from django.http import HttpResponse
from io import BytesIO

def unir(pdfs,filename):
    merger  = PdfFileMerger(strict=False)
    if len(pdfs)>1:
        for pdf in pdfs:
            if pdf.name.endswith('.pdf'):
                merger.append(pdf)

        filestream = BytesIO()
        merger.write(filestream)
        merger.close()
        #filestream.seek(0)
        response = HttpResponse(filestream.getvalue(),content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename= "{}"'.format(filename)
        return response
    else:
        return None
    
