"""
URLs simplificadas para frequência.
"""
from django.urls import path
from . import views

app_name = 'frequencia'

urlpatterns = [
    # Dashboard
    path('', views.agenda_dashboard, name='dashboard'),
    
    # Agenda
    path('agenda/', views.AgendaListView.as_view(), name='agenda_lista'),
    path('agenda/', views.AgendaListView.as_view(), name='agenda'),  # Compatibilidade
    path('aula/criar/', views.AgendaCreateView.as_view(), name='criar_aula'),
    path('aula/criar/', views.AgendaCreateView.as_view(), name='agendar_aula'),  # Compatibilidade
    path('aula/<int:pk>/editar/', views.AgendaUpdateView.as_view(), name='editar_aula'),
    path('aula/<int:pk>/deletar/', views.AgendaDeleteView.as_view(), name='deletar_aula'),
    path('aula/<int:pk>/excluir/', views.AgendaDeleteView.as_view(), name='excluir_aula'),  # Compatibilidade
    path('aula/<int:pk>/alterar-status/', views.alterar_status_aula, name='alterar_status'),
    path('aula/<int:pk>/status/', views.alterar_status_rapido, name='alterar_status_rapido'),
    path('registros/', views.RegistroPresencaListView.as_view(), name='lista'),
    path('registrar-presenca/', views.RegistroPresencaCreateView.as_view(), name='registrar_presenca'),
    path('registrar-presenca-rapido/<int:aula_id>/', views.registrar_presenca_rapido, name='registrar_presenca_rapido'),
    path('calendario/', views.calendario_view, name='calendario'),
]
