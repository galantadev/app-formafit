"""
URLs simplificadas para financeiro.
"""
from django.urls import path
from .views_new import (
    FinanceiroListView, FaturaCreateView, FaturaUpdateView, 
    FaturaDeleteView, financeiro_dashboard, marcar_como_paga
)

app_name = 'financeiro'

urlpatterns = [
    # Dashboard financeiro
    path('', financeiro_dashboard, name='dashboard'),
    path('dashboard/', financeiro_dashboard, name='dashboard_detalhado'),
    
    # CRUD de faturas
    path('faturas/', FinanceiroListView.as_view(), name='faturas'),
    path('fatura/criar/', FaturaCreateView.as_view(), name='criar_fatura'),
    path('fatura/<int:pk>/editar/', FaturaUpdateView.as_view(), name='editar_fatura'),
    path('fatura/<int:pk>/excluir/', FaturaDeleteView.as_view(), name='excluir_fatura'),
    
    # Ações AJAX
    path('fatura/<int:fatura_id>/marcar-paga/', marcar_como_paga, name='marcar_como_paga'),
]
