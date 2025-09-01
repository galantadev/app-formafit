"""
Views simplificadas para gestão financeira.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.db.models import Q, Sum
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal

from .models import FaturaSimples
from .forms import FaturaForm
from alunos.models import Aluno


class FinanceiroListView(LoginRequiredMixin, ListView):
    """
    Lista todas as faturas com filtros.
    """
    model = FaturaSimples
    template_name = 'financeiro/faturas_lista.html'
    context_object_name = 'faturas'
    paginate_by = 50
    
    def get_queryset(self):
        queryset = FaturaSimples.objects.filter(
            aluno__personal_trainer=self.request.user
        ).select_related('aluno').order_by('-ano_referencia', '-mes_referencia', '-data_vencimento')
        
        # Filtros de busca
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(aluno__nome__icontains=search) |
                Q(observacoes__icontains=search)
            )
        
        # Filtro por status
        status_filter = self.request.GET.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filtro por mês/ano
        mes_filter = self.request.GET.get('mes')
        ano_filter = self.request.GET.get('ano')
        
        if mes_filter:
            queryset = queryset.filter(mes_referencia=mes_filter)
        if ano_filter:
            queryset = queryset.filter(ano_referencia=ano_filter)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Estatísticas básicas
        todas_faturas = FaturaSimples.objects.filter(aluno__personal_trainer=self.request.user)
        
        context['total_faturas'] = todas_faturas.count()
        context['faturas_pendentes'] = todas_faturas.filter(status='pendente').count()
        context['faturas_atrasadas'] = todas_faturas.filter(status='atrasada').count()
        context['faturas_pagas'] = todas_faturas.filter(status='paga').count()
        
        # Valores financeiros
        context['valor_total'] = todas_faturas.aggregate(total=Sum('valor'))['total'] or Decimal('0.00')
        context['valor_recebido'] = todas_faturas.filter(status='paga').aggregate(total=Sum('valor'))['total'] or Decimal('0.00')
        context['valor_pendente'] = todas_faturas.filter(status__in=['pendente', 'atrasada']).aggregate(total=Sum('valor'))['total'] or Decimal('0.00')
        
        # Valores dos filtros para manter estado
        context['search'] = self.request.GET.get('search', '')
        context['status_filter'] = self.request.GET.get('status', '')
        context['mes_filter'] = self.request.GET.get('mes', '')
        context['ano_filter'] = self.request.GET.get('ano', '')
        
        # Choices para filtros
        context['status_choices'] = FaturaSimples.STATUS_CHOICES
        context['meses_choices'] = [(i, i) for i in range(1, 13)]
        
        # Anos disponíveis
        anos = todas_faturas.values_list('ano_referencia', flat=True).distinct().order_by('-ano_referencia')
        context['anos_choices'] = [(ano, ano) for ano in anos]
        
        return context


class FaturaCreateView(LoginRequiredMixin, CreateView):
    """
    Criar nova fatura.
    """
    model = FaturaSimples
    form_class = FaturaForm
    template_name = 'financeiro/fatura_form.html'
    success_url = reverse_lazy('financeiro:faturas')
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Filtrar apenas alunos do personal trainer logado
        form.fields['aluno'].queryset = Aluno.objects.filter(
            personal_trainer=self.request.user
        ).order_by('nome')
        return form
    
    def form_valid(self, form):
        messages.success(self.request, 'Fatura criada com sucesso!')
        return super().form_valid(form)


class FaturaUpdateView(LoginRequiredMixin, UpdateView):
    """
    Editar fatura existente.
    """
    model = FaturaSimples
    form_class = FaturaForm
    template_name = 'financeiro/fatura_form.html'
    success_url = reverse_lazy('financeiro:faturas')
    
    def get_queryset(self):
        return FaturaSimples.objects.filter(aluno__personal_trainer=self.request.user)
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Filtrar apenas alunos do personal trainer logado
        form.fields['aluno'].queryset = Aluno.objects.filter(
            personal_trainer=self.request.user
        ).order_by('nome')
        return form
    
    def form_valid(self, form):
        messages.success(self.request, 'Fatura atualizada com sucesso!')
        return super().form_valid(form)


class FaturaDeleteView(LoginRequiredMixin, DeleteView):
    """
    Excluir fatura.
    """
    model = FaturaSimples
    template_name = 'financeiro/fatura_confirm_delete.html'
    success_url = reverse_lazy('financeiro:faturas')
    
    def get_queryset(self):
        return FaturaSimples.objects.filter(aluno__personal_trainer=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Fatura excluída com sucesso!')
        return super().delete(request, *args, **kwargs)


@login_required
def financeiro_dashboard(request):
    """
    Dashboard financeiro simplificado.
    """
    hoje = timezone.now().date()
    mes_atual = hoje.month
    ano_atual = hoje.year
    
    # Faturas do mês atual
    faturas_mes = FaturaSimples.objects.filter(
        aluno__personal_trainer=request.user,
        mes_referencia=mes_atual,
        ano_referencia=ano_atual
    )
    
    # Estatísticas do mês
    total_mes = faturas_mes.aggregate(total=Sum('valor'))['total'] or Decimal('0.00')
    recebido_mes = faturas_mes.filter(status='paga').aggregate(total=Sum('valor'))['total'] or Decimal('0.00')
    pendente_mes = faturas_mes.filter(status__in=['pendente', 'atrasada']).aggregate(total=Sum('valor'))['total'] or Decimal('0.00')
    
    # Faturas que vencem hoje
    vencem_hoje = FaturaSimples.objects.filter(
        aluno__personal_trainer=request.user,
        data_vencimento=hoje,
        status__in=['pendente', 'atrasada']
    )
    
    # Faturas atrasadas
    atrasadas = FaturaSimples.objects.filter(
        aluno__personal_trainer=request.user,
        data_vencimento__lt=hoje,
        status__in=['pendente', 'atrasada']
    )
    
    # Próximos vencimentos (próximos 7 dias)
    proximos_vencimentos = FaturaSimples.objects.filter(
        aluno__personal_trainer=request.user,
        data_vencimento__range=[hoje + timedelta(days=1), hoje + timedelta(days=7)],
        status__in=['pendente', 'atrasada']
    ).order_by('data_vencimento')
    
    context = {
        'total_mes': total_mes,
        'recebido_mes': recebido_mes,
        'pendente_mes': pendente_mes,
        'vencem_hoje': vencem_hoje,
        'atrasadas': atrasadas,
        'proximos_vencimentos': proximos_vencimentos,
        'mes_atual': mes_atual,
        'ano_atual': ano_atual,
    }
    
    return render(request, 'financeiro/dashboard.html', context)


@login_required
def marcar_como_paga(request, fatura_id):
    """
    Marcar fatura como paga via AJAX.
    """
    if request.method == 'POST':
        fatura = get_object_or_404(
            FaturaSimples, 
            id=fatura_id, 
            aluno__personal_trainer=request.user
        )
        fatura.status = 'paga'
        fatura.save()
        
        messages.success(request, f'Fatura de {fatura.aluno.nome} marcada como paga!')
        
        if request.headers.get('Content-Type') == 'application/json':
            return JsonResponse({'success': True})
        else:
            return redirect('financeiro:faturas')
    
    return JsonResponse({'success': False})
