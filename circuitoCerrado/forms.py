from django import forms

class uploadOneFileForm(forms.Form):
    file = forms.FileField(label="Archivo")
    def __init__(self, *args, **kwargs):
        super(uploadOneFileForm, self).__init__(*args, **kwargs)
        self.fields['file'].widget.attrs.update({'class': 'form-control'})

class crucePagSafycForm(forms.Form):
    pag = forms.FileField(label="Archivo Página")
    safyc = forms.FileField(label="Archivo Safyc")
    def __init__(self, *args, **kwargs):
        super(crucePagSafycForm, self).__init__(*args, **kwargs)
        self.fields['pag'].widget.attrs.update({'class': 'form-control'})
        self.fields['safyc'].widget.attrs.update({'class': 'form-control'})