from django import forms
from .models import Notificaciones
from django.contrib.auth.models import Group

class Update_form(forms.ModelForm):
	class Meta:
		model = Notificaciones
		fields = ["titulo",
				"descripcion",
				"archivo1",
				"archivo2",
				"archivo3",
				"archivo4",
				"archivo5",
				"anotaciones",
				]


	def __init__(self, *args, **kwargs):
		super(Update_form, self).__init__(*args, **kwargs)
		for field in self.fields:
			# agrega la clase form-control a todos los campos del form
			self.fields[field].widget.attrs.update({'class': 'form-control'})
		"""
		agregar readonly a los campos del formulario  a editar
		la idea es que al editar no se pueda modificar el titulo y la descripción de la notificación original
		"""
		self.fields["titulo"].widget.attrs['readonly'] = True
		self.fields["descripcion"].widget.attrs['readonly'] = True


class CreateForm(forms.ModelForm):
	deptos_destino = forms.ModelMultipleChoiceField(queryset=Group.objects.all(),widget=forms.CheckboxSelectMultiple,
		required=True)
	class Meta:
		model = Notificaciones
		
		fields = ["titulo",
				"descripcion",
				"deptos_destino",
				"archivo1",
				"archivo2",
				"archivo3",
				"archivo4",
				"archivo5",
				"anotaciones",
				]

	def __init__(self, *args, **kwargs):
		super(CreateForm, self).__init__(*args, **kwargs)
		for field in self.fields:
			# agrega la clase form-control a todos los campos del form
			self.fields[field].widget.attrs.update({'class': 'form-control'})
		self.fields["deptos_destino"].widget.attrs.update({'class': 'checkbox'})
