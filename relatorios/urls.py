"""
URLs para geração de relatórios.
"""
from django.urls import path
from . import views

app_name = 'relatorios'

urlpatterns = [
    # Lista e dashboard
    path('', views.lista_relatorios, name='lista'),
    path('dashboard/', views.dashboard_relatorios_view, name='dashboard'),
    
    # Gerar relatórios
    path('gerar/', views.gerar_relatorio_view, name='gerar'),
    path('gerar-multiplos/', views.GerarRelatoriosMultiplosView.as_view(), name='gerar_multiplos'),
    
    # Visualizar e gerenciar
    path('<uuid:pk>/', views.relatorio_detail_view, name='detalhe'),
    path('<uuid:pk>/download/', views.download_relatorio_view, name='download'),
    path('<uuid:pk>/regenerar/', views.regenerar_relatorio_view, name='regenerar'),
    path('<uuid:pk>/enviar-email/', views.enviar_relatorio_email_view, name='enviar_email'),
    
    # AJAX
    path('ajax/<uuid:pk>/status/', views.ajax_status_relatorio, name='ajax_status'),
    
    # Administração de Tipos de Relatórios
    path('admin/tipos/', views.admin_tipos_relatorios, name='admin_tipos_relatorios'),
    path('admin/tipos/criar/', views.admin_criar_tipo_relatorio, name='admin_criar_tipo_relatorio'),
    path('admin/tipos/<int:pk>/editar/', views.admin_editar_tipo_relatorio, name='admin_editar_tipo_relatorio'),
    path('admin/tipos/<int:pk>/excluir/', views.admin_excluir_tipo_relatorio, name='admin_excluir_tipo_relatorio'),
]
