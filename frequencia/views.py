"""
Views simplificadas para controle de frequência dos alunos.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.db.models import Q
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime, timedelta

from .models import AgendaAula, RegistroPresenca
from .forms import AgendaAulaForm, RegistroPresencaForm
from alunos.models import Aluno


class AgendaListView(LoginRequiredMixin, ListView):
    """
    Lista todas as aulas agendadas com filtros.
    """
    model = AgendaAula
    template_name = 'frequencia/agenda_lista.html'
    context_object_name = 'aulas'
    paginate_by = 50
    
    def get_queryset(self):
        queryset = AgendaAula.objects.filter(
            aluno__personal_trainer=self.request.user
        ).select_related('aluno').order_by('data_aula', 'horario_inicio')
        
        # Filtros de busca
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(aluno__nome__icontains=search) |
                Q(tipo_treino__icontains=search) |
                Q(observacoes__icontains=search)
            )
        
        # Filtro por status
        status_filter = self.request.GET.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filtro por data
        data_inicio = self.request.GET.get('data_inicio')
        data_fim = self.request.GET.get('data_fim')
        
        if data_inicio:
            queryset = queryset.filter(data_aula__gte=data_inicio)
        if data_fim:
            queryset = queryset.filter(data_aula__lte=data_fim)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Estatísticas básicas
        hoje = timezone.now().date()
        context['aulas_hoje'] = self.get_queryset().filter(data_aula=hoje).count()
        context['aulas_semana'] = self.get_queryset().filter(
            data_aula__range=[hoje, hoje + timedelta(days=7)]
        ).count()
        
        # Valores dos filtros para manter estado
        context['search'] = self.request.GET.get('search', '')
        context['status_filter'] = self.request.GET.get('status', '')
        context['data_inicio'] = self.request.GET.get('data_inicio', '')
        context['data_fim'] = self.request.GET.get('data_fim', '')
        
        # Choices de status para filtro
        context['status_choices'] = AgendaAula.STATUS_CHOICES
        
        return context


class AgendaCreateView(LoginRequiredMixin, CreateView):
    """
    Criar nova aula.
    """
    model = AgendaAula
    form_class = AgendaAulaForm
    template_name = 'frequencia/aula_form.html'
    success_url = reverse_lazy('frequencia:agenda_lista')
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Filtrar apenas alunos do personal trainer logado
        form.fields['aluno'].queryset = Aluno.objects.filter(
            personal_trainer=self.request.user
        ).order_by('nome')
        return form
    
    def form_valid(self, form):
        messages.success(self.request, 'Aula agendada com sucesso!')
        return super().form_valid(form)


class AgendaUpdateView(LoginRequiredMixin, UpdateView):
    """
    Editar aula existente.
    """
    model = AgendaAula
    form_class = AgendaAulaForm
    template_name = 'frequencia/aula_form.html'
    success_url = reverse_lazy('frequencia:agenda_lista')
    
    def get_queryset(self):
        return AgendaAula.objects.filter(aluno__personal_trainer=self.request.user)
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Filtrar apenas alunos do personal trainer logado
        form.fields['aluno'].queryset = Aluno.objects.filter(
            personal_trainer=self.request.user
        ).order_by('nome')
        return form
    
    def form_valid(self, form):
        messages.success(self.request, 'Aula atualizada com sucesso!')
        return super().form_valid(form)


class AgendaDeleteView(LoginRequiredMixin, DeleteView):
    """
    Excluir aula.
    """
    model = AgendaAula
    template_name = 'frequencia/aula_confirm_delete.html'
    success_url = reverse_lazy('frequencia:agenda_lista')
    
    def get_queryset(self):
        return AgendaAula.objects.filter(aluno__personal_trainer=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Aula excluída com sucesso!')
        return super().delete(request, *args, **kwargs)


# View função para agilizar o desenvolvimento
@login_required
def agenda_dashboard(request):
    """
    Dashboard simplificado da agenda.
    """
    hoje = timezone.now().date()
    primeiro_dia_mes = hoje.replace(day=1)
    
    # Aulas de hoje
    aulas_hoje = AgendaAula.objects.filter(
        aluno__personal_trainer=request.user,
        data_aula=hoje
    ).select_related('aluno').order_by('horario_inicio')
    
    # Próximas aulas (próximos 7 dias)
    proximas_aulas = AgendaAula.objects.filter(
        aluno__personal_trainer=request.user,
        data_aula__range=[hoje + timedelta(days=1), hoje + timedelta(days=7)]
    ).select_related('aluno').order_by('data_aula', 'horario_inicio')[:10]
    
    # Estatísticas básicas
    total_aulas_semana = AgendaAula.objects.filter(
        aluno__personal_trainer=request.user,
        data_aula__range=[hoje, hoje + timedelta(days=7)]
    ).count()
    
    # Estatísticas de frequência dos alunos (este mês)
    alunos_stats = []
    alunos = Aluno.objects.filter(personal_trainer=request.user)
    
    for aluno in alunos:
        total_aulas_mes = AgendaAula.objects.filter(
            aluno=aluno,
            data_aula__gte=primeiro_dia_mes,
            data_aula__lte=hoje,
            status='realizado'
        ).count()
        
        presencas = RegistroPresenca.objects.filter(
            aluno=aluno,
            data_aula__gte=primeiro_dia_mes,
            data_aula__lte=hoje,
            status='presente'
        ).count()
        
        if total_aulas_mes > 0:
            percentual = (presencas / total_aulas_mes) * 100
            alunos_stats.append({
                'aluno': aluno,
                'total_aulas': total_aulas_mes,
                'presencas': presencas,
                'percentual': round(percentual, 1)
            })
    
    # Ordenar por percentual de frequência
    alunos_stats.sort(key=lambda x: x['percentual'], reverse=True)
    alunos_stats = alunos_stats[:5]  # Top 5
    
    context = {
        'aulas_hoje': aulas_hoje,
        'proximas_aulas': proximas_aulas,
        'total_aulas_semana': total_aulas_semana,
        'hoje': hoje,
        'alunos_stats': alunos_stats,
    }
    
    return render(request, 'frequencia/dashboard.html', context)


@login_required
def alterar_status_aula(request, pk):
    """
    Altera o status de uma aula agendada.
    """
    aula = get_object_or_404(AgendaAula, pk=pk, aluno__personal_trainer=request.user)
    
    if request.method == 'POST':
        novo_status = request.POST.get('status')
        if novo_status in dict(AgendaAula.STATUS_CHOICES):
            aula.status = novo_status
            aula.save()
            messages.success(request, f'Status da aula alterado para {aula.get_status_display()}')
        else:
            messages.error(request, 'Status inválido')
        
        return redirect('frequencia:dashboard')
    
    context = {
        'aula': aula,
        'status_choices': AgendaAula.STATUS_CHOICES,
    }
    
    return render(request, 'frequencia/alterar_status.html', context)


@login_required
def alterar_status_rapido(request, pk):
    """
    Altera rapidamente o status de uma aula via AJAX ou POST.
    """
    if request.method == 'POST':
        aula = get_object_or_404(AgendaAula, pk=pk, aluno__personal_trainer=request.user)
        novo_status = request.POST.get('status')
        
        if novo_status in dict(AgendaAula.STATUS_CHOICES):
            aula.status = novo_status
            aula.save()
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': f'Status alterado para {aula.get_status_display()}',
                    'novo_status': aula.get_status_display()
                })
            else:
                messages.success(request, f'Status da aula alterado para {aula.get_status_display()}')
                return redirect('frequencia:dashboard')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': 'Status inválido'})
            else:
                messages.error(request, 'Status inválido')
                return redirect('frequencia:dashboard')
    
    return redirect('frequencia:dashboard')


class RegistroPresencaListView(LoginRequiredMixin, ListView):
    """
    Lista todos os registros de presença com filtros.
    """
    model = RegistroPresenca
    template_name = 'frequencia/registros_lista.html'
    context_object_name = 'registros'
    paginate_by = 50
    
    def get_queryset(self):
        queryset = RegistroPresenca.objects.filter(
            aluno__personal_trainer=self.request.user
        ).select_related('aluno').order_by('-data_aula', 'horario_inicio')
        
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
        
        # Filtro por data
        data_inicio = self.request.GET.get('data_inicio')
        data_fim = self.request.GET.get('data_fim')
        if data_inicio:
            queryset = queryset.filter(data_aula__gte=data_inicio)
        if data_fim:
            queryset = queryset.filter(data_aula__lte=data_fim)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = RegistroPresenca.STATUS_CHOICES
        return context


class RegistroPresencaCreateView(LoginRequiredMixin, CreateView):
    """
    Criar novo registro de presença.
    """
    model = RegistroPresenca
    form_class = RegistroPresencaForm
    template_name = 'frequencia/registrar_presenca_form.html'
    success_url = reverse_lazy('frequencia:lista')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_initial(self):
        initial = super().get_initial()
        
        # Se veio de uma aula agendada, pré-preencher os dados
        aula_id = self.request.GET.get('aula_id')
        if aula_id:
            try:
                aula = AgendaAula.objects.get(
                    id=aula_id, 
                    aluno__personal_trainer=self.request.user
                )
                initial.update({
                    'aluno': aula.aluno,
                    'data_aula': aula.data_aula,
                    'horario_inicio': aula.horario_inicio,
                    'horario_fim': aula.horario_fim,
                    'status': 'presente',  # Status padrão
                })
            except AgendaAula.DoesNotExist:
                pass
        
        return initial
    
    def form_valid(self, form):
        messages.success(self.request, 'Presença registrada com sucesso!')
        return super().form_valid(form)


@login_required
def calendario_view(request):
    """
    View do calendário de aulas.
    """
    import calendar
    from datetime import datetime, date, timedelta
    
    # Obter mês e ano dos parâmetros GET ou usar atual
    hoje = date.today()
    ano = int(request.GET.get('ano', hoje.year))
    mes = int(request.GET.get('mes', hoje.month))
    
    # Validação básica
    if mes < 1 or mes > 12:
        mes = hoje.month
    if ano < 2020 or ano > 2030:
        ano = hoje.year
    
    # Criar calendário
    cal = calendar.Calendar(firstweekday=6)  # Domingo como primeiro dia
    dias_mes = cal.monthdayscalendar(ano, mes)
    
    # Buscar aulas do mês
    primeiro_dia = date(ano, mes, 1)
    if mes == 12:
        ultimo_dia = date(ano + 1, 1, 1) - timedelta(days=1)
    else:
        ultimo_dia = date(ano, mes + 1, 1) - timedelta(days=1)
    
    aulas_mes = AgendaAula.objects.filter(
        aluno__personal_trainer=request.user,
        data_aula__gte=primeiro_dia,
        data_aula__lte=ultimo_dia
    ).select_related('aluno').order_by('data_aula', 'horario_inicio')
    
    # Organizar aulas por dia
    aulas_por_dia = {}
    for aula in aulas_mes:
        dia = aula.data_aula.day
        if dia not in aulas_por_dia:
            aulas_por_dia[dia] = []
        aulas_por_dia[dia].append(aula)
    
    # Navegação (mês anterior/próximo)
    if mes == 1:
        mes_anterior = 12
        ano_anterior = ano - 1
    else:
        mes_anterior = mes - 1
        ano_anterior = ano
    
    if mes == 12:
        mes_proximo = 1
        ano_proximo = ano + 1
    else:
        mes_proximo = mes + 1
        ano_proximo = ano
    
    context = {
        'ano': ano,
        'mes': mes,
        'nome_mes': calendar.month_name[mes],
        'dias_mes': dias_mes,
        'aulas_por_dia': aulas_por_dia,
        'hoje': hoje,
        'mes_anterior': mes_anterior,
        'ano_anterior': ano_anterior,
        'mes_proximo': mes_proximo,
        'ano_proximo': ano_proximo,
        'dias_semana': ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb'],
    }
    
    return render(request, 'frequencia/calendario.html', context)


@login_required
def registrar_presenca_rapido(request, aula_id):
    """
    Registra presença rapidamente com um clique.
    """
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Método não permitido'})
    
    try:
        # Buscar a aula
        aula = get_object_or_404(AgendaAula, pk=aula_id, aluno__personal_trainer=request.user)
        
        # Verificar se já existe registro de presença
        registro_existente = RegistroPresenca.objects.filter(
            aluno=aula.aluno,
            data_aula=aula.data_aula,
            horario_inicio=aula.horario_inicio
        ).first()
        
        if registro_existente:
            return JsonResponse({
                'success': False, 
                'message': f'Presença já registrada para {aula.aluno.nome} em {aula.data_aula.strftime("%d/%m/%Y")}'
            })
        
        # Criar registro de presença
        registro = RegistroPresenca.objects.create(
            aluno=aula.aluno,
            data_aula=aula.data_aula,
            horario_inicio=aula.horario_inicio,
            horario_fim=aula.horario_fim,
            status='presente',
            observacoes=f'Aula realizada - {aula.tipo_treino}'
        )
        
        # Atualizar status da aula para 'realizado'
        aula.status = 'realizado'
        aula.save()
        
        return JsonResponse({
            'success': True,
            'message': f'Presença registrada com sucesso para {aula.aluno.nome}!',
            'registro_id': registro.id,
            'status': 'presente'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Erro ao registrar presença: {str(e)}'
        })
