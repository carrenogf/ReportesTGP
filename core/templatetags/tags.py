from django import template
from notificaciones.models import Notificaciones
from django.contrib.auth.models import Group

register = template.Library()

@register.filter
def n_notif(dpto):
	try:
	    notif = Notificaciones.objects.filter(deptos_destino=dpto)
	    notif = notif.exclude(deptos_notif=dpto)
	    return len(notif)
	except:
		return 0

@register.filter(name='has_group')
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False