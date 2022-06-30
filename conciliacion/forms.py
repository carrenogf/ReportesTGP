from django import forms

class uploadOneFileForm(forms.Form):
    file = forms.FileField(label="Archivo")
    def __init__(self, *args, **kwargs):
        super(uploadOneFileForm, self).__init__(*args, **kwargs)
        self.fields['file'].widget.attrs.update({'class': 'form-control'})

class crucePagSafycForm(forms.Form):
    glosa = forms.FileField(label="Libro Banco con Glosa")
    macro = forms.FileField(label="Resumen Mov. bancarios")
    def __init__(self, *args, **kwargs):
        super(crucePagSafycForm, self).__init__(*args, **kwargs)
        self.fields['glosa'].widget.attrs.update({'class': 'form-control'})
        self.fields['macro'].widget.attrs.update({'class': 'form-control'})