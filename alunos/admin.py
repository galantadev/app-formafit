from django.contrib import admin
from .models import Aluno, MedidasCorporais, FotoProgresso, HorarioPadraoAluno, AcompanhamentoMensal


@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'email', 'telefone', 'personal_trainer', 'ativo', 'data_inicio']
    list_filter = ['ativo', 'sexo', 'personal_trainer', 'data_inicio']
    search_fields = ['nome', 'email', 'telefone']
    date_hierarchy = 'data_inicio'


@admin.register(MedidasCorporais)
class MedidasCorporaisAdmin(admin.ModelAdmin):
    list_display = ['aluno', 'data_medicao', 'peso', 'percentual_gordura', 'imc']
    list_filter = ['data_medicao', 'aluno__personal_trainer']
    search_fields = ['aluno__nome']
    date_hierarchy = 'data_medicao'


@admin.register(AcompanhamentoMensal)
class AcompanhamentoMensalAdmin(admin.ModelAdmin):
    list_display = ['aluno', 'ano', 'mes', 'peso', 'imc', 'data_criacao']
    list_filter = ['ano', 'mes', 'aluno__personal_trainer']
    search_fields = ['aluno__nome']
    ordering = ['-ano', '-mes', 'aluno__nome']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(aluno__personal_trainer=request.user)


@admin.register(FotoProgresso)
class FotoProgressoAdmin(admin.ModelAdmin):
    list_display = ['aluno', 'data_foto', 'tipo_foto', 'descricao']
    list_filter = ['tipo_foto', 'data_foto', 'aluno__personal_trainer']
    search_fields = ['aluno__nome', 'descricao']
    date_hierarchy = 'data_foto'


@admin.register(HorarioPadraoAluno)
class HorarioPadraoAlunoAdmin(admin.ModelAdmin):
    list_display = ['aluno', 'dia_semana', 'horario_inicio', 'horario_fim', 'ativo']
    list_filter = ['dia_semana', 'ativo', 'aluno__personal_trainer']
    search_fields = ['aluno__nome']
