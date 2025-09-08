#!/usr/bin/env python
"""
Script para criar tipos de relatórios padrão no banco de dados.
"""
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'formafit.settings')
django.setup()

from relatorios.models import TipoRelatorio

def criar_tipos_relatorios():
    """Cria tipos de relatórios padrão."""
    
    tipos_relatorios = [
        {
            'nome': 'Relatório de Progresso Semanal',
            'descricao': 'Relatório detalhado do progresso semanal do aluno',
            'template_filename': 'relatorio_semanal.html',
            'ativo': True,
            'incluir_graficos': True,
            'incluir_fotos': True,
            'incluir_medidas': True,
            'incluir_frequencia': True,
        },
        {
            'nome': 'Relatório de Progresso Mensal',
            'descricao': 'Relatório completo do progresso mensal do aluno',
            'template_filename': 'relatorio_mensal.html',
            'ativo': True,
            'incluir_graficos': True,
            'incluir_fotos': True,
            'incluir_medidas': True,
            'incluir_frequencia': True,
        },
        {
            'nome': 'Relatório de Progresso Trimestral',
            'descricao': 'Relatório detalhado do progresso trimestral do aluno',
            'template_filename': 'relatorio_trimestral.html',
            'ativo': True,
            'incluir_graficos': True,
            'incluir_fotos': True,
            'incluir_medidas': True,
            'incluir_frequencia': True,
        },
        {
            'nome': 'Relatório de Frequência',
            'descricao': 'Relatório focado na frequência e presença do aluno',
            'template_filename': 'relatorio_frequencia.html',
            'ativo': True,
            'incluir_graficos': True,
            'incluir_fotos': False,
            'incluir_medidas': False,
            'incluir_frequencia': True,
        },
        {
            'nome': 'Relatório de Medidas Corporais',
            'descricao': 'Relatório focado nas medidas corporais e evolução física',
            'template_filename': 'relatorio_medidas.html',
            'ativo': True,
            'incluir_graficos': True,
            'incluir_fotos': True,
            'incluir_medidas': True,
            'incluir_frequencia': False,
        },
    ]
    
    for tipo_data in tipos_relatorios:
        tipo, created = TipoRelatorio.objects.get_or_create(
            nome=tipo_data['nome'],
            defaults=tipo_data
        )
        
        if created:
            print(f"✅ Tipo de relatório criado: {tipo.nome}")
        else:
            print(f"⚠️  Tipo de relatório já existe: {tipo.nome}")
    
    print(f"\n🎉 Processo concluído! Total de tipos de relatórios: {TipoRelatorio.objects.count()}")

if __name__ == '__main__':
    criar_tipos_relatorios()
