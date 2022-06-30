from django.shortcuts import render
from django.views.generic.edit import UpdateView, CreateView
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from .models import Instructivo
from django.contrib.auth.models import Group
# Create your views here.

class InstructivoListView(ListView):
	model = Instructivo
	paginate_by = 10

	def get_context_data(self,**kwargs):
		context = super(InstructivoListView,self).get_context_data(**kwargs)
		grupos = Group.objects.all()
		lista_grupos = [grupo.name for grupo in grupos]
		if 'departamentos' in self.request.GET:
			dpto_filtro = self.request.GET['departamentos']
			context['dpto_filtro'] = dpto_filtro
		context['grupos'] = lista_grupos
		return context

	def get_queryset(self):
		queryset = Instructivo.objects.all()
		if 'departamentos' in self.request.GET:
			dpto_name = self.request.GET['departamentos']
			if dpto_name!="todos":
				dpto = Group.objects.get(name=str(dpto_name))
				queryset = Instructivo.objects.filter(departamento=dpto.id)

		return queryset

class InstructivoDetailView(DetailView):
	model = Instructivo
	def get_context_data(self,**kwargs):
		context = super(InstructivoDetailView,self).get_context_data(**kwargs)
		objeto = Instructivo.objects.get(pk=self.kwargs.get('pk'))
		if objeto.archivo1:
			context['archivo1_nombre'] = str(objeto.archivo1).split('/')[2]
		if objeto.archivo2:
			context['archivo2_nombre'] = str(objeto.archivo2).split('/')[2]
		if objeto.archivo3:
			context['archivo3_nombre'] = str(objeto.archivo3).split('/')[2]
		return context
	