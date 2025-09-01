#!/usr/bin/env python
"""
Script para criar tipos de relatórios no banco de dados
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'formafit.settings')
django.setup()

from relatorios.models import TipoRelatorio

def criar_tipos_relatorios():
    """Cria os tipos de relatórios padrão do sistema"""
    
    tipos_data = [
        {
            'nome': 'Relatório de Progresso Completo',
            'descricao': 'Relatório completo com todas as informações do aluno: medidas, frequência, evolução de peso, fotos e gráficos.',
            'template_filename': 'relatorios/progresso_completo.html',
            'incluir_graficos': True,
            'incluir_fotos': True,
            'incluir_medidas': True,
            'incluir_frequencia': True,
            'ativo': True
        },
        {
            'nome': 'Relatório de Medidas Corporais',
            'descricao': 'Relatório focado na evolução das medidas corporais, peso, IMC e percentual de gordura.',
            'template_filename': 'relatorios/medidas_corporais.html',
            'incluir_graficos': True,
            'incluir_fotos': False,
            'incluir_medidas': True,
            'incluir_frequencia': False,
            'ativo': True
        },
        {
            'nome': 'Relatório de Frequência',
            'descricao': 'Relatório de frequência e assiduidade do aluno aos treinos.',
            'template_filename': 'relatorios/frequencia.html',
            'incluir_graficos': True,
            'incluir_fotos': False,
            'incluir_medidas': False,
            'incluir_frequencia': True,
            'ativo': True
        },
        {
            'nome': 'Relatório Simples',
            'descricao': 'Relatório básico com informações essenciais sem gráficos complexos.',
            'template_filename': 'relatorios/simples.html',
            'incluir_graficos': False,
            'incluir_fotos': False,
            'incluir_medidas': True,
            'incluir_frequencia': True,
            'ativo': True
        },
        {
            'nome': 'Relatório Fotográfico',
            'descricao': 'Relatório com foco na evolução fotográfica do aluno (antes e depois).',
            'template_filename': 'relatorios/fotografico.html',
            'incluir_graficos': False,
            'incluir_fotos': True,
            'incluir_medidas': True,
            'incluir_frequencia': False,
            'ativo': True
        },
        {
            'nome': 'Relatório Mensal Executive',
            'descricao': 'Relatório executivo mensal com os principais indicadores e resultados.',
            'template_filename': 'relatorios/executive.html',
            'incluir_graficos': True,
            'incluir_fotos': False,
            'incluir_medidas': True,
            'incluir_frequencia': True,
            'ativo': True
        }
    ]
    
    print("📊 Criando tipos de relatórios...")
    
    for i, dados in enumerate(tipos_data, 1):
        print(f"\n📝 Criando tipo {i}: {dados['nome']}")
        
        # Verificar se já existe
        if TipoRelatorio.objects.filter(nome=dados['nome']).exists():
            print(f"⚠️  Tipo {dados['nome']} já existe, pulando...")
            continue
        
        try:
            tipo = TipoRelatorio.objects.create(**dados)
            print(f"✅ Tipo criado: {tipo.nome}")
            print(f"   📋 Descrição: {tipo.descricao}")
            print(f"   📄 Template: {tipo.template_filename}")
            
            configuracoes = []
            if tipo.incluir_graficos:
                configuracoes.append("Gráficos")
            if tipo.incluir_fotos:
                configuracoes.append("Fotos")
            if tipo.incluir_medidas:
                configuracoes.append("Medidas")
            if tipo.incluir_frequencia:
                configuracoes.append("Frequência")
            
            print(f"   ⚙️  Inclui: {', '.join(configuracoes)}")
            
        except Exception as e:
            print(f"❌ Erro ao criar tipo {dados['nome']}: {str(e)}")
    
    print(f"\n🎉 Processo concluído!")
    print(f"📈 Total de tipos de relatórios: {TipoRelatorio.objects.count()}")
    
    # Listar todos os tipos criados
    print(f"\n📋 Tipos de relatórios disponíveis:")
    for tipo in TipoRelatorio.objects.all():
        status = "✅ Ativo" if tipo.ativo else "❌ Inativo"
        print(f"   - {tipo.nome} ({status})")

if __name__ == '__main__':
    criar_tipos_relatorios()
