from django.urls import path
from . import views

urlpatterns = [
    path('sistemas/',views.sistemasView, name='sueldosSistemas'),
    path('sistemas-success/',views.sistemas_succes, name='sistemas_succes'),
    path('me/',views.mesaEntrada, name='sueldosMe'),
    path('me-success/',views.mesaEntrada_succes, name='me_succes'),
]
    