from django.contrib import admin
from .models import TipoRelatorio

@admin.register(TipoRelatorio)
class TipoRelatorioAdmin(admin.ModelAdmin):
    list_display = ['nome', 'incluir_graficos', 'incluir_fotos', 'incluir_medidas', 'incluir_frequencia', 'ativo']
    list_filter = ['ativo', 'incluir_graficos', 'incluir_fotos', 'incluir_medidas', 'incluir_frequencia']
    search_fields = ['nome', 'descricao']
    list_editable = ['ativo']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'descricao', 'template_filename', 'ativo')
        }),
        ('Configurações do Relatório', {
            'fields': ('incluir_graficos', 'incluir_fotos', 'incluir_medidas', 'incluir_frequencia')
        })
    )
