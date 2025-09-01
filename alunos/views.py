"""
Views para gerenciamento de alunos.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.urls import reverse_lazy, reverse
from django.db.models import Q, Count, Avg
from django.utils import timezone
from datetime import datetime, timedelta
from django.http import JsonResponse

from .models import Aluno, MedidasCorporais, FotoProgresso, HorarioPadraoAluno, AcompanhamentoMensal
from .forms import AlunoForm, MedidasCorporaisForm, FotoProgressoForm, AgendamentoPadraoForm, PlanoFinanceiroForm, AcompanhamentoMensalForm
from frequencia.models import AgendaAula
from financeiro.models import ContratoAluno, Fatura, PlanoMensalidade


class AlunosListView(LoginRequiredMixin, ListView):
    """
    Lista todos os alunos do personal trainer.
    """
    model = Aluno
    template_name = 'alunos/lista.html'
    context_object_name = 'alunos'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Aluno.objects.filter(personal_trainer=self.request.user)
        
        # Filtros
        search = self.request.GET.get('search')
        status = self.request.GET.get('status')
        objetivo = self.request.GET.get('objetivo')
        
        if search:
            queryset = queryset.filter(
                Q(nome__icontains=search) |
                Q(email__icontains=search) |
                Q(telefone__icontains=search)
            )
        
        if status == 'ativo':
            queryset = queryset.filter(ativo=True)
        elif status == 'inativo':
            queryset = queryset.filter(ativo=False)
        
        if objetivo:
            queryset = queryset.filter(objetivo__icontains=objetivo)
        
        return queryset.order_by('-data_criacao')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        context['status'] = self.request.GET.get('status', '')
        context['objetivo'] = self.request.GET.get('objetivo', '')
        
        # Estatísticas
        context['total_alunos'] = Aluno.objects.filter(personal_trainer=self.request.user).count()
        context['alunos_ativos'] = Aluno.objects.filter(personal_trainer=self.request.user, ativo=True).count()
        context['alunos_inativos'] = Aluno.objects.filter(personal_trainer=self.request.user, ativo=False).count()
        
        return context


class AlunoCreateView(LoginRequiredMixin, CreateView):
    """
    Cadastro de novo aluno com agendamento padrão.
    """
    model = Aluno
    form_class = AlunoForm
    template_name = 'alunos/cadastrar.html'
    success_url = reverse_lazy('alunos:lista')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['agendamento_form'] = AgendamentoPadraoForm(self.request.POST)
            context['financeiro_form'] = PlanoFinanceiroForm(self.request.POST)
        else:
            context['agendamento_form'] = AgendamentoPadraoForm()
            context['financeiro_form'] = PlanoFinanceiroForm()
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        agendamento_form = context['agendamento_form']
        financeiro_form = context['financeiro_form']
        
        if agendamento_form.is_valid() and financeiro_form.is_valid():
            # Salvar o aluno
            form.instance.personal_trainer = self.request.user
            aluno = form.save()
            
            # Processar agendamentos padrão se fornecidos
            dias_semana = agendamento_form.cleaned_data.get('dias_semana')
            horario_inicio = agendamento_form.cleaned_data.get('horario_inicio')
            criar_agendamentos = agendamento_form.cleaned_data.get('criar_agendamentos')
            
            if dias_semana and horario_inicio and criar_agendamentos:
                self._criar_agendamentos_padrao(aluno, dias_semana, horario_inicio)
            
            # Processar plano financeiro se fornecido
            plano_mensalidade = financeiro_form.cleaned_data.get('plano_mensalidade')
            criar_contrato = financeiro_form.cleaned_data.get('criar_contrato')
            
            if plano_mensalidade and criar_contrato:
                self._criar_contrato_financeiro(aluno, financeiro_form.cleaned_data)
            
            messages.success(self.request, f'Aluno {aluno.nome} cadastrado com sucesso!')
            return redirect(self.success_url)
        else:
            return self.form_invalid(form)
    
    def _criar_agendamentos_padrao(self, aluno, dias_semana, horario_inicio):
        """
        Cria agendamentos automáticos para as próximas 4 semanas.
        """
        from datetime import timedelta
        
        # Calcular horário de fim (assumindo 1 hora de duração)
        horario_fim = (datetime.combine(timezone.now().date(), horario_inicio) + timedelta(hours=1)).time()
        
        # Obter a data de início da próxima semana
        hoje = timezone.now().date()
        dias_ate_segunda = (7 - hoje.weekday()) % 7
        if dias_ate_segunda == 0:
            dias_ate_segunda = 7
        inicio_proxima_semana = hoje + timedelta(days=dias_ate_segunda)
        
        agendamentos_criados = 0
        
        # Criar agendamentos para as próximas 4 semanas
        for semana in range(4):
            inicio_semana = inicio_proxima_semana + timedelta(weeks=semana)
            
            for dia_semana in dias_semana:
                dia_semana_int = int(dia_semana)
                data_agendamento = inicio_semana + timedelta(days=dia_semana_int)
                
                # Criar o agendamento
                AgendaAula.objects.create(
                    aluno=aluno,
                    data_aula=data_agendamento,
                    horario_inicio=horario_inicio,
                    horario_fim=horario_fim,
                    status='agendado',
                    tipo_treino='Treino Regular',
                    observacoes='Agendamento automático criado no cadastro'
                )
                agendamentos_criados += 1
        
        messages.info(
            self.request, 
            f'{agendamentos_criados} agendamentos criados automaticamente para as próximas 4 semanas.'
        )
    
    def _criar_contrato_financeiro(self, aluno, dados_financeiros):
        """
        Cria contrato financeiro e faturas automáticas.
        """
        from datetime import datetime, timedelta
        from dateutil.relativedelta import relativedelta
        
        plano = dados_financeiros['plano_mensalidade']
        valor_personalizado = dados_financeiros.get('valor_personalizado')
        dia_vencimento = dados_financeiros.get('dia_vencimento', 5)
        meses_antecipados = dados_financeiros.get('meses_antecipados', 3)
        
        # Criar contrato
        contrato = ContratoAluno.objects.create(
            aluno=aluno,
            plano_mensalidade=plano,
            valor_personalizado=valor_personalizado,
            dia_vencimento=dia_vencimento,
            ativo=True,
            data_inicio=timezone.now().date(),
            observacoes='Contrato criado automaticamente no cadastro do aluno'
        )
        
        # Criar faturas para os próximos meses
        valor_fatura = valor_personalizado or plano.valor
        data_atual = timezone.now().date()
        faturas_criadas = 0
        
        for i in range(meses_antecipados):
            # Calcular mês e ano de referência
            data_referencia = data_atual + relativedelta(months=i)
            mes_referencia = data_referencia.month
            ano_referencia = data_referencia.year
            
            # Calcular data de vencimento
            try:
                data_vencimento = data_referencia.replace(day=dia_vencimento)
            except ValueError:
                # Se o dia não existe no mês (ex: 31 em fevereiro), usar o último dia do mês
                import calendar
                ultimo_dia = calendar.monthrange(ano_referencia, mes_referencia)[1]
                data_vencimento = data_referencia.replace(day=min(dia_vencimento, ultimo_dia))
            
            # Verificar se já existe fatura para este período
            if not Fatura.objects.filter(
                aluno=aluno,
                mes_referencia=mes_referencia,
                ano_referencia=ano_referencia
            ).exists():
                Fatura.objects.create(
                    aluno=aluno,
                    contrato=contrato,
                    mes_referencia=mes_referencia,
                    ano_referencia=ano_referencia,
                    valor_original=valor_fatura,
                    valor_final=valor_fatura,
                    data_vencimento=data_vencimento,
                    status='pendente',
                    observacoes='Fatura criada automaticamente no cadastro do aluno'
                )
                faturas_criadas += 1
        
        messages.success(
            self.request,
            f'Contrato criado com sucesso! {faturas_criadas} faturas geradas automaticamente.'
        )


class AlunoUpdateView(LoginRequiredMixin, UpdateView):
    """
    Edição de dados do aluno.
    """
    model = Aluno
    form_class = AlunoForm
    template_name = 'alunos/editar.html'
    
    def get_queryset(self):
        return Aluno.objects.filter(personal_trainer=self.request.user)
    
    def get_success_url(self):
        return reverse('alunos:detalhes', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, f'Dados de {form.instance.nome} atualizados com sucesso!')
        return super().form_valid(form)


class AlunoDetailView(LoginRequiredMixin, DetailView):
    """
    Detalhes completos do aluno com histórico de medidas e treinos.
    """
    model = Aluno
    template_name = 'alunos/detalhes.html'
    context_object_name = 'aluno'
    
    def get_queryset(self):
        return Aluno.objects.filter(personal_trainer=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        aluno = self.object
        
        # Medidas corporais (últimas 10)
        context['medidas'] = MedidasCorporais.objects.filter(aluno=aluno).order_by('-data_medicao')[:10]
        context['ultima_medida'] = context['medidas'].first() if context['medidas'] else None
        
        # Fotos de progresso (últimas 6)
        context['fotos'] = FotoProgresso.objects.filter(aluno=aluno).order_by('-data_foto')[:6]
        
        # Estatísticas de frequência (último mês)
        mes_passado = timezone.now() - timedelta(days=30)
        from frequencia.models import RegistroPresenca
        context['presencas_mes'] = RegistroPresenca.objects.filter(
            aluno=aluno,
            data_aula__gte=mes_passado,
            status='presente'
        ).count()
        
        # Plano de treino atual
        from treinos.models import PlanoTreino
        context['plano_atual'] = PlanoTreino.objects.filter(
            aluno=aluno,
            ativo=True
        ).first()
        
        # Próximas aulas
        from frequencia.models import AgendaAula
        context['proximas_aulas'] = AgendaAula.objects.filter(
            aluno=aluno,
            data_aula__gte=timezone.now().date(),
            status__in=['agendado', 'confirmado']
        ).order_by('data_aula', 'horario_inicio')[:3]
        
        # Faturas pendentes
        from financeiro.models import Fatura
        context['faturas_pendentes'] = Fatura.objects.filter(
            aluno=aluno,
            status__in=['pendente', 'parcial']
        ).order_by('data_vencimento')
        
        # Acompanhamento mensal (ano atual)
        ano_atual = timezone.now().year
        context['ano_atual'] = ano_atual
        context['anos_disponiveis'] = list(range(ano_atual - 2, ano_atual + 2))
        
        # Obter acompanhamentos do ano selecionado
        ano_selecionado = int(self.request.GET.get('ano', ano_atual))
        context['ano_selecionado'] = ano_selecionado
        
        acompanhamentos = AcompanhamentoMensal.objects.filter(
            aluno=aluno,
            ano=ano_selecionado
        ).order_by('mes')
        
        # Criar dicionário de acompanhamentos por mês
        acompanhamentos_dict = {acomp.mes: acomp for acomp in acompanhamentos}
        
        # Lista de meses com dados
        meses = []
        for i in range(1, 13):
            mes_nome = ['', 'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
                       'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'][i]
            meses.append({
                'numero': i,
                'nome': mes_nome,
                'acompanhamento': acompanhamentos_dict.get(i),
                'has_data': i in acompanhamentos_dict
            })
        
        context['meses'] = meses
        
        return context


@login_required
def adicionar_medidas(request, pk):
    """
    Adiciona novas medidas corporais para o aluno.
    """
    aluno = get_object_or_404(Aluno, pk=pk, personal_trainer=request.user)
    
    if request.method == 'POST':
        form = MedidasCorporaisForm(request.POST)
        if form.is_valid():
            medida = form.save(commit=False)
            medida.aluno = aluno
            medida.save()
            messages.success(request, 'Medidas corporais adicionadas com sucesso!')
            return redirect('alunos:detalhes', pk=pk)
    else:
        form = MedidasCorporaisForm()
    
    return render(request, 'alunos/adicionar_medidas.html', {
        'form': form,
        'aluno': aluno
    })


@login_required
def adicionar_foto(request, pk):
    """
    Adiciona foto de progresso para o aluno.
    """
    aluno = get_object_or_404(Aluno, pk=pk, personal_trainer=request.user)
    
    if request.method == 'POST':
        form = FotoProgressoForm(request.POST, request.FILES)
        if form.is_valid():
            foto = form.save(commit=False)
            foto.aluno = aluno
            foto.save()
            messages.success(request, 'Foto de progresso adicionada com sucesso!')
            return redirect('alunos:detalhes', pk=pk)
    else:
        form = FotoProgressoForm()
    
    return render(request, 'alunos/adicionar_foto.html', {
        'form': form,
        'aluno': aluno
    })


@login_required
def historico_medidas(request, pk):
    """
    Exibe histórico completo de medidas corporais do aluno.
    """
    aluno = get_object_or_404(Aluno, pk=pk, personal_trainer=request.user)
    medidas = MedidasCorporais.objects.filter(aluno=aluno).order_by('-data_medicao')
    
    return render(request, 'alunos/historico_medidas.html', {
        'aluno': aluno,
        'medidas': medidas
    })


@login_required
def galeria_fotos(request, pk):
    """
    Galeria com todas as fotos de progresso do aluno.
    """
    aluno = get_object_or_404(Aluno, pk=pk, personal_trainer=request.user)
    fotos = FotoProgresso.objects.filter(aluno=aluno).order_by('-data_foto')
    
    return render(request, 'alunos/galeria_fotos.html', {
        'aluno': aluno,
        'fotos': fotos
    })


@login_required
def toggle_status(request, pk):
    """
    Alterna status ativo/inativo do aluno via AJAX.
    """
    if request.method == 'POST':
        aluno = get_object_or_404(Aluno, pk=pk, personal_trainer=request.user)
        aluno.ativo = not aluno.ativo
        aluno.save()
        
        return JsonResponse({
            'success': True,
            'ativo': aluno.ativo,
            'status_text': 'Ativo' if aluno.ativo else 'Inativo'
        })
    
    return JsonResponse({'success': False})


@login_required
def acompanhamento_mensal(request, pk, ano, mes):
    """
    Gerencia o acompanhamento mensal do aluno (criar/editar).
    """
    aluno = get_object_or_404(Aluno, pk=pk, personal_trainer=request.user)
    
    # Verificar se já existe acompanhamento para este mês/ano
    acompanhamento, created = AcompanhamentoMensal.objects.get_or_create(
        aluno=aluno,
        ano=ano,
        mes=mes,
        defaults={}
    )
    
    if request.method == 'POST':
        form = AcompanhamentoMensalForm(request.POST, instance=acompanhamento)
        if form.is_valid():
            acompanhamento = form.save(commit=False)
            acompanhamento.aluno = aluno
            acompanhamento.ano = ano
            acompanhamento.mes = mes
            acompanhamento.save()
            
            messages.success(request, f'Acompanhamento de {acompanhamento.get_mes_display()}/{ano} salvo com sucesso!')
            return JsonResponse({
                'success': True,
                'message': f'Acompanhamento de {acompanhamento.get_mes_display()}/{ano} salvo com sucesso!',
                'imc': float(acompanhamento.imc) if acompanhamento.imc else None,
                'classificacao_imc': acompanhamento.classificacao_imc
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            })
    
    # GET request - retornar dados do formulário
    form = AcompanhamentoMensalForm(instance=acompanhamento)
    mes_nome = acompanhamento.get_mes_display()
    
    return JsonResponse({
        'success': True,
        'data': {
            'peso': float(acompanhamento.peso) if acompanhamento.peso else '',
            'percentual_gordura': float(acompanhamento.percentual_gordura) if acompanhamento.percentual_gordura else '',
            'ombro': float(acompanhamento.ombro) if acompanhamento.ombro else '',
            'torax': float(acompanhamento.torax) if acompanhamento.torax else '',
            'braco': float(acompanhamento.braco) if acompanhamento.braco else '',
            'quadril': float(acompanhamento.quadril) if acompanhamento.quadril else '',
            'cintura': float(acompanhamento.cintura) if acompanhamento.cintura else '',
            'coxa': float(acompanhamento.coxa) if acompanhamento.coxa else '',
            'panturrilha': float(acompanhamento.panturrilha) if acompanhamento.panturrilha else '',
            'observacoes': acompanhamento.observacoes or '',
            'imc': float(acompanhamento.imc) if acompanhamento.imc else None,
            'classificacao_imc': acompanhamento.classificacao_imc,
            'mes_nome': mes_nome,
            'ano': ano
        }
    })


@login_required
def excluir_acompanhamento_mensal(request, pk, ano, mes):
    """
    Exclui o acompanhamento mensal do aluno.
    """
    if request.method == 'POST':
        aluno = get_object_or_404(Aluno, pk=pk, personal_trainer=request.user)
        
        try:
            acompanhamento = AcompanhamentoMensal.objects.get(
                aluno=aluno,
                ano=ano,
                mes=mes
            )
            mes_nome = acompanhamento.get_mes_display()
            acompanhamento.delete()
            
            return JsonResponse({
                'success': True,
                'message': f'Acompanhamento de {mes_nome}/{ano} excluído com sucesso!'
            })
        except AcompanhamentoMensal.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Acompanhamento não encontrado.'
            })
    
    return JsonResponse({'success': False, 'message': 'Método não permitido.'})


@login_required
def estatisticas_aluno(request, pk):
    """
    Exibe estatísticas detalhadas do aluno.
    """
    aluno = get_object_or_404(Aluno, pk=pk, personal_trainer=request.user)
    
    # Evolução de peso (últimos 6 meses)
    seis_meses_atras = timezone.now() - timedelta(days=180)
    evolucao_peso = MedidasCorporais.objects.filter(
        aluno=aluno,
        data_medicao__gte=seis_meses_atras
    ).order_by('data_medicao').values('data_medicao', 'peso')
    
    # Frequência mensal
    from frequencia.models import RegistroPresenca
    frequencia_mensal = RegistroPresenca.objects.filter(
        aluno=aluno,
        presente=True
    ).extra(
        select={'mes': "DATE_FORMAT(data_presenca, '%%Y-%%m')"}
    ).values('mes').annotate(total=Count('id')).order_by('mes')
    
    context = {
        'aluno': aluno,
        'evolucao_peso': list(evolucao_peso),
        'frequencia_mensal': list(frequencia_mensal),
    }
    
    return render(request, 'alunos/estatisticas.html', context)
