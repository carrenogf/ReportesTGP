from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.InstructivoListView.as_view(), name='instructivos'),
    path('<int:pk>/', views.InstructivoDetailView.as_view(), name='instructivos-detail')
]