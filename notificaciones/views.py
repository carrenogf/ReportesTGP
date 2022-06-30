#from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import UpdateView, CreateView
from .models import Notificaciones
from .forms import Update_form, CreateForm
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from core.mails import enviar_mail_notificacion,enviar_mail
from django.contrib.auth.models import User, Group
import re
from django.db.models import Q

# Create your views here.
@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
class NotificaionesListView(ListView):
	model = Notificaciones
	paginate_by = 10
	def get_queryset(self):
		grupo_user = self.request.user.groups.all()[0]
		queryset = Notificaciones.objects.filter(deptos_destino=grupo_user)

		# Here we try to filter by status
		status = self.kwargs.get('status', None)
		# If a the key 'status' is set in the url
		if status:
			if status == 'pendientes':
				queryset = Notificaciones.objects.filter(deptos_destino=grupo_user).exclude(deptos_notif=grupo_user)
			
			elif status == 'notificadas':
				queryset = Notificaciones.objects.filter(deptos_destino=grupo_user).filter(deptos_notif=grupo_user)

			elif status == 'enviadas':
				queryset = Notificaciones.objects.filter(depto_rem=grupo_user)
			else:
				queryset = Notificaciones.objects.filter(deptos_destino=grupo_user)

		return queryset

	def get_context_data(self,**kwargs):
		context = super(NotificaionesListView,self).get_context_data(**kwargs)
		status = self.kwargs.get('status', None)
		if status:
			context['filtro'] = status
		return context

@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
class NotificacionesUpdateView(UpdateView):
	model = Notificaciones
	template_name_suffix = '_update_form'
	form_class = Update_form
	success_url  = reverse_lazy('notificaciones')

	def form_valid(self, form):
		if 'notificado' in self.request.POST or 'guardar' in self.request.POST :
			# marca como notificado al guardar o con el boton de notificado
			instance = form.save(commit=False)
			usuarios_previos = str(instance.usuarios_notif)
			instance.usuarios_notif=usuarios_previos+str(self.request.user)
			grupo_user = self.request.user.groups.all()[0]
			instance.deptos_notif.add(grupo_user)
		return super(NotificacionesUpdateView, self).form_valid(form)
	
	def get_context_data(self,**kwargs):
		context = super(NotificacionesUpdateView,self).get_context_data(**kwargs)
		grupo_user = str(self.request.user.groups.all()[0])
		objeto = Notificaciones.objects.get(pk=self.kwargs.get('pk'))
		patern="<Group: ([A-Za-z0-9 _]+)>"
		
		lista_obj = objeto.deptos_notif.all()
		lista_dptos_notif = []
		for i in lista_obj:
			lista_dptos_notif.append(str(i))

		lista_obj_dest = objeto.deptos_destino.all()
		lista_dptos_dest = []
		for i in lista_obj_dest:
			lista_dptos_dest.append(str(i))

		context['grupo_user'] = grupo_user
		context['lista_dptos_notif'] = lista_dptos_notif
		context['lista_dptos_dest'] = lista_dptos_dest
		anterior = self.request.META.get('HTTP_REFERER')
		context['anterior'] = anterior
		return context

@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
class NotificacionesCreateView(CreateView):
	model = Notificaciones
	form_class = CreateForm
	success_url = reverse_lazy('notificaciones')

	def form_valid(self, form):
		obj = form.save(commit=False)
		obj.usuario_remitente = self.request.user
		obj.depto_rem = self.request.user.groups.all()[0]
		obj.save()
		response = super(NotificacionesCreateView, self).form_valid(form)
		#Enviar mail al guardar:
		
		lista_mails = []

		notificacion = Notificaciones.objects.get(id=obj.pk)
		lista_dest = notificacion.deptos_destino.all()
		lista_dptos_dest = []

		for i in lista_dest:
			lista_dptos_dest.append(str(i))

		for depto in lista_dptos_dest:
			print(depto)
			users = User.objects.filter(groups__name=depto)
			for user in users:
				lista_mails.append(user.email)

		n_notif = obj.pk
		tit_notif = obj.titulo
		enviar_mail_notificacion(lista_mails,n_notif,tit_notif)

		return response
