from django import forms
from .models import Reportes


class ReportesModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.nombre

class Reportes_Form(forms.Form):
    reporte = ReportesModelChoiceField(queryset=Reportes.objects.all())
    file = forms.FileField(label="TXT SAFyC")

    def __init__(self, *args, **kwargs):
        super(Reportes_Form, self).__init__(*args, **kwargs)
        self.fields['reporte'].widget.attrs.update({'class': 'form-control'})
        self.fields['file'].widget.attrs.update({'class': 'form-control'})
