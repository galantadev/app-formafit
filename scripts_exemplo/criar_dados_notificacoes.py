#!/usr/bin/env python
"""
Script para criar dados iniciais do módulo de notificações.
"""
import os
import sys
import django
from datetime import time

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'formafit.settings')
django.setup()

from notificacoes.models import TipoNotificacao, NotificacaoAutomatica

def criar_tipos_notificacao():
    """Criar tipos básicos de notificação."""
    
    print("📝 Criando tipos de notificação...")
    
    tipos = [
        {
            'nome': 'Lembrete de Treino',
            'descricao': 'Lembretes automáticos sobre agendamentos de treino',
            'cor': '#10B981'  # Verde
        },
        {
            'nome': 'Cobrança de Mensalidade',
            'descricao': 'Avisos sobre vencimento de mensalidades',
            'cor': '#F59E0B'  # Amarelo
        },
        {
            'nome': 'Mensagem Motivacional',
            'descricao': 'Mensagens de motivação e incentivo',
            'cor': '#8B5CF6'  # Roxo
        },
        {
            'nome': 'Resultado de Avaliação',
            'descricao': 'Envio de relatórios de progresso e evolução',
            'cor': '#3B82F6'  # Azul
        },
        {
            'nome': 'Aniversário',
            'descricao': 'Parabenização automática em aniversários',
            'cor': '#EC4899'  # Rosa
        },
        {
            'nome': 'Geral',
            'descricao': 'Notificações gerais e comunicados',
            'cor': '#6B7280'  # Cinza
        }
    ]
    
    for tipo_data in tipos:
        tipo, created = TipoNotificacao.objects.get_or_create(
            nome=tipo_data['nome'],
            defaults={
                'descricao': tipo_data['descricao'],
                'cor': tipo_data['cor'],
                'ativo': True
            }
        )
        if created:
            print(f'✅ Tipo criado: {tipo.nome}')
        else:
            print(f'⚠️  Tipo já existe: {tipo.nome}')

def criar_notificacoes_automaticas():
    """Criar configurações de notificações automáticas."""
    
    print("\n🔄 Criando notificações automáticas...")
    
    # Buscar tipos de notificação
    tipo_cobranca = TipoNotificacao.objects.get(nome='Cobrança de Mensalidade')
    tipo_treino = TipoNotificacao.objects.get(nome='Lembrete de Treino')
    tipo_aniversario = TipoNotificacao.objects.get(nome='Aniversário')
    
    automaticas = [
        {
            'nome': 'Lembrete de Vencimento - 3 dias',
            'trigger': 'pagamento_vence_3_dias',
            'tipo_notificacao': tipo_cobranca,
            'antecedencia_dias': 3,
            'horario_envio': time(9, 0),  # 09:00
            'ativa': True,
            'apenas_alunos_ativos': True
        },
        {
            'nome': 'Lembrete de Vencimento - Hoje',
            'trigger': 'pagamento_vence_hoje',
            'tipo_notificacao': tipo_cobranca,
            'antecedencia_dias': 0,
            'horario_envio': time(10, 0),  # 10:00
            'ativa': True,
            'apenas_alunos_ativos': True
        },
        {
            'nome': 'Cobrança de Pagamento Vencido',
            'trigger': 'pagamento_vencido',
            'tipo_notificacao': tipo_cobranca,
            'antecedencia_dias': 3,  # 3 dias após vencimento
            'horario_envio': time(10, 0),  # 10:00
            'ativa': True,
            'apenas_alunos_ativos': True
        },
        {
            'nome': 'Lembrete de Treino Agendado',
            'trigger': 'treino_agendado',
            'tipo_notificacao': tipo_treino,
            'antecedencia_dias': 1,
            'horario_envio': time(20, 0),  # 20:00
            'ativa': True,
            'apenas_alunos_ativos': True
        },
        {
            'nome': 'Parabéns pelo Aniversário',
            'trigger': 'aniversario_aluno',
            'tipo_notificacao': tipo_aniversario,
            'antecedencia_dias': 0,
            'horario_envio': time(9, 0),  # 09:00
            'ativa': True,
            'apenas_alunos_ativos': False
        }
    ]
    
    for auto_data in automaticas:
        auto, created = NotificacaoAutomatica.objects.get_or_create(
            trigger=auto_data['trigger'],
            defaults=auto_data
        )
        if created:
            print(f'✅ Notificação automática criada: {auto.nome}')
        else:
            print(f'⚠️  Notificação automática já existe: {auto.nome}')

def criar_dados_notificacoes():
    """Função principal para criar todos os dados"""
    
    print('📢 Criando dados iniciais para o módulo de notificações...\n')
    
    criar_tipos_notificacao()
    criar_notificacoes_automaticas()
    
    print('\n🎉 Dados iniciais criados com sucesso!')
    print('\n📱 Agora você pode:')
    print('• Acessar /notificacoes/ para ver o dashboard')
    print('• Criar notificações manuais')
    print('• Configurar notificações por aluno')
    print('• Testar envio via WhatsApp')

if __name__ == '__main__':
    criar_dados_notificacoes()
