#!/usr/bin/env python
"""
Script para criar planos de mensalidade de exemplo no banco de dados
"""

import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'formafit.settings')
django.setup()

from financeiro.models import PlanoMensalidade

def criar_planos_exemplo():
    """Cria planos de mensalidade de exemplo"""
    
    # Criar planos de exemplo se não existirem
    planos_exemplo = [
        {
            'nome': 'Plano Básico',
            'descricao': '8 aulas por mês - Ideal para iniciantes',
            'valor': 120.00,
            'aulas_incluidas': 8
        },
        {
            'nome': 'Plano Intermediário',
            'descricao': '12 aulas por mês - Para quem já tem experiência',
            'valor': 180.00,
            'aulas_incluidas': 12
        },
        {
            'nome': 'Plano Premium',
            'descricao': '20 aulas por mês - Para resultados máximos',
            'valor': 280.00,
            'aulas_incluidas': 20
        },
        {
            'nome': 'Plano VIP',
            'descricao': 'Aulas ilimitadas + acompanhamento nutricional',
            'valor': 400.00,
            'aulas_incluidas': 999
        },
        {
            'nome': 'Plano Avaliação',
            'descricao': '4 aulas experimentais - Para conhecer o serviço',
            'valor': 80.00,
            'aulas_incluidas': 4
        }
    ]

    print("💰 Criando planos de mensalidade de exemplo...")

    for plano_data in planos_exemplo:
        plano, created = PlanoMensalidade.objects.get_or_create(
            nome=plano_data['nome'],
            defaults={
                'descricao': plano_data['descricao'],
                'valor': plano_data['valor'],
                'aulas_incluidas': plano_data['aulas_incluidas'],
                'ativo': True
            }
        )
        
        if created:
            print(f"✅ Plano criado: {plano.nome} - R$ {plano.valor}")
        else:
            print(f"📋 Plano já existe: {plano.nome} - R$ {plano.valor}")

    print(f"\n📊 Total de planos ativos: {PlanoMensalidade.objects.filter(ativo=True).count()}")
    print("🎉 Processo concluído!")

if __name__ == '__main__':
    criar_planos_exemplo()
