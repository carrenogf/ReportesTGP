from django import template
from .models import Notificaciones

register = template.Library()

@register.filter
def n_notif(Notificaciones, category):
    return len(Notificaciones.filter(category=category))