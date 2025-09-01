"""
URLs simplificadas para frequência.
"""
from django.urls import path
from .views_new import (
    AgendaListView, AgendaCreateView, AgendaUpdateView, 
    AgendaDeleteView, agenda_dashboard
)

app_name = 'frequencia'

urlpatterns = [
    # Agenda principal
    path('', AgendaListView.as_view(), name='agenda_lista'),
    path('agenda/', AgendaListView.as_view(), name='agenda'),  # Compatibilidade
    path('dashboard/', agenda_dashboard, name='dashboard'),
    
    # CRUD de aulas
    path('aula/criar/', AgendaCreateView.as_view(), name='criar_aula'),
    path('aula/<int:pk>/editar/', AgendaUpdateView.as_view(), name='editar_aula'),
    path('aula/<int:pk>/excluir/', AgendaDeleteView.as_view(), name='excluir_aula'),
]
