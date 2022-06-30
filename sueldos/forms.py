from django import forms
from .models import Liquidacion

class LiquidacionModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.liquidacion

class Upload_Form(forms.Form):
    liquidacion = LiquidacionModelChoiceField(queryset=Liquidacion.objects.filter(abierta=True))
    file = forms.FileField(label="Archivo a subir")

    def __init__(self, *args, **kwargs):
        super(Upload_Form, self).__init__(*args, **kwargs)
        self.fields['liquidacion'].widget.attrs.update({'class': 'form-control'})
        self.fields['file'].widget.attrs.update({'class': 'form-control'})