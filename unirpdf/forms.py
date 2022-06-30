from django import forms

class unirpdfForm(forms.Form):
    files = forms.FileField(label="Pdfs",widget=forms.ClearableFileInput(attrs={'multiple':True}))
    def __init__(self, *args, **kwargs):
        super(unirpdfForm, self).__init__(*args, **kwargs)
        self.fields['files'].widget.attrs.update({'class': 'form-control'})