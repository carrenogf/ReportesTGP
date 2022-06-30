from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.NotificaionesListView.as_view(), name='notificaciones'),
    path('f/<str:status>', views.NotificaionesListView.as_view(), name='notificaciones_f'),
    path('update/<int:pk>/', views.NotificacionesUpdateView.as_view(), name='notificaciones_update'),
    path('create/',views.NotificacionesCreateView.as_view(),name='notificaciones_create'),
]