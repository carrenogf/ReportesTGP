"""ReportesTGP URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from core.views import home
from reporte.views import reportesView
from circuitoCerrado.views import resumenBancoView, circuitoCerradoView, comprobantesPaginaView,crucePagSafycView
from sueldos.views import sistemasView, sistemas_succes, mesaEntrada, mesaEntrada_succes
from unirpdf.views import unirpdfView
from conciliacion.views import conciliacionView
#from saldos_especiales.views import saldosView
from notificaciones.views import NotificaionesListView
from django.conf.urls.static import static
from django.conf import settings
 

urlpatterns = [
    path('accounts/',include('django.contrib.auth.urls')),
    url(r'^jet/', include('jet.urls', 'jet')),  # Django JET URLS
    path('admin/', admin.site.urls),
    path('',home.as_view(), name='home'),
    path('reportes/',reportesView, name='reportes'),
    path('resumenbanco/',resumenBancoView, name='resumenbanco'),
    path('circuito-cerrado/',circuitoCerradoView, name='circuitoCerrado' ),
    path('comprobantes-pagina',comprobantesPaginaView, name='comprobantesPagina'),
    path('pag-safyc/',crucePagSafycView, name='crucePagSafyc'),
    path('unirpdf/',unirpdfView,name='unirpdf'),
    path('conciliacion/',conciliacionView,name='conciliacion'),
    #path('saldos-especiales',saldosView,name='saldos_especiales'),
    path('sueldos/', include('sueldos.urls')),
    path('notificaciones/', include('notificaciones.urls')),
    path('instructivos/', include('instructivos.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)