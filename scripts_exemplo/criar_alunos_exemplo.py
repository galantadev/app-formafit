#!/usr/bin/env python
"""
Script para criar 5 alunos de exemplo no banco de dados FormaFit
"""

import os
import sys
import django
from datetime import date, datetime, time
from decimal import Decimal

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'formafit.settings')
django.setup()

from alunos.models import Aluno, HorarioPadraoAluno
from financeiro.models import PlanoMensalidade, ContratoAluno, Fatura
from frequencia.models import RegistroPresenca
from django.contrib.auth import get_user_model

User = get_user_model()

def criar_alunos_exemplo():
    """Cria 5 alunos de exemplo com dados realistas"""
    
    # Dados dos alunos de exemplo
    alunos_data = [
        {
            'nome': 'João Silva Santos',
            'email': 'joao.silva@email.com',
            'telefone': '(11) 98765-4321',
            'data_nascimento': date(1990, 3, 15),
            'altura': Decimal('1.75'),
            'peso': Decimal('75.5'),
            'dias_semana': ['segunda', 'quarta', 'sexta'],
            'horario': time(7, 0),
            'plano': 'Plano Intermediário'
        },
        {
            'nome': 'Maria Oliveira Costa',
            'email': 'maria.oliveira@email.com',
            'telefone': '(11) 97654-3210',
            'data_nascimento': date(1985, 7, 22),
            'altura': Decimal('1.65'),
            'peso': Decimal('62.0'),
            'dias_semana': ['terca', 'quinta'],
            'horario': time(18, 30),
            'plano': 'Plano Básico'
        },
        {
            'nome': 'Carlos Roberto Mendes',
            'email': 'carlos.mendes@email.com',
            'telefone': '(11) 96543-2109',
            'data_nascimento': date(1982, 11, 8),
            'altura': Decimal('1.80'),
            'peso': Decimal('85.3'),
            'dias_semana': ['segunda', 'terca', 'quinta', 'sexta'],
            'horario': time(6, 30),
            'plano': 'Plano Premium'
        },
        {
            'nome': 'Ana Paula Ferreira',
            'email': 'ana.ferreira@email.com',
            'telefone': '(11) 95432-1098',
            'data_nascimento': date(1995, 2, 14),
            'altura': Decimal('1.68'),
            'peso': Decimal('58.7'),
            'dias_semana': ['segunda', 'quarta', 'sexta', 'sabado'],
            'horario': time(8, 0),
            'plano': 'Plano Premium'
        },
        {
            'nome': 'Pedro Henrique Lima',
            'email': 'pedro.lima@email.com',
            'telefone': '(11) 94321-0987',
            'data_nascimento': date(1988, 9, 30),
            'altura': Decimal('1.78'),
            'peso': Decimal('82.1'),
            'dias_semana': ['segunda', 'terca', 'quarta', 'quinta', 'sexta', 'sabado'],
            'horario': time(19, 0),
            'plano': 'Plano VIP'
        }
    ]
    
    print("🏃‍♂️ Criando alunos de exemplo...")
    
    for i, dados in enumerate(alunos_data, 1):
        print(f"\n📝 Criando aluno {i}: {dados['nome']}")
        
        # Verificar se o aluno já existe
        if Aluno.objects.filter(email=dados['email']).exists():
            print(f"⚠️  Aluno {dados['nome']} já existe, pulando...")
            continue
        
        try:
            # Criar o aluno
            # Primeiro, vamos buscar um personal trainer (vamos usar o admin)
            try:
                personal_trainer = User.objects.get(username='admin')
            except User.DoesNotExist:
                personal_trainer = User.objects.first()
                if not personal_trainer:
                    print("❌ Nenhum usuário encontrado para ser personal trainer")
                    continue
            
            aluno = Aluno.objects.create(
                nome=dados['nome'],
                email=dados['email'],
                telefone=dados['telefone'],
                data_nascimento=dados['data_nascimento'],
                altura=dados['altura'],
                peso_inicial=dados['peso'],
                sexo='M' if 'João' in dados['nome'] or 'Carlos' in dados['nome'] or 'Pedro' in dados['nome'] else 'F',
                objetivo='condicionamento',
                personal_trainer=personal_trainer
            )
            print(f"✅ Aluno criado: {aluno.nome}")
            
            # Criar horários padrão
            dias_map = {
                'segunda': 0, 'terca': 1, 'quarta': 2, 'quinta': 3,
                'sexta': 4, 'sabado': 5, 'domingo': 6
            }
            
            for dia in dados['dias_semana']:
                from datetime import time as time_func, timedelta
                horario_fim = time_func(
                    (dados['horario'].hour + 1) % 24,
                    dados['horario'].minute
                )
                
                HorarioPadraoAluno.objects.create(
                    aluno=aluno,
                    dia_semana=dias_map[dia],
                    horario_inicio=dados['horario'],
                    horario_fim=horario_fim
                )
            print(f"📅 Horários criados para: {', '.join(dados['dias_semana'])}")
            
            # Buscar ou criar plano financeiro
            try:
                plano = PlanoMensalidade.objects.get(nome=dados['plano'])
                
                # Criar contrato financeiro
                contrato = ContratoAluno.objects.create(
                    aluno=aluno,
                    plano_mensalidade=plano,
                    data_inicio=date.today(),
                    ativo=True
                )
                print(f"💰 Contrato criado com plano {plano.nome} - R$ {plano.valor}")
                
                # Criar primeira fatura
                fatura = Fatura.objects.create(
                    aluno=aluno,
                    contrato=contrato,
                    mes_referencia=date.today().month,
                    ano_referencia=date.today().year,
                    valor_original=plano.valor,
                    valor_final=plano.valor,
                    data_vencimento=date.today().replace(day=10),
                    status='pendente'
                )
                print(f"🧾 Fatura criada para {fatura.mes_referencia:02d}/{fatura.ano_referencia}")
                
            except PlanoMensalidade.DoesNotExist:
                print(f"⚠️  Plano '{dados['plano']}' não encontrado")
            
            # Criar algumas aulas para as próximas 4 semanas
            from datetime import timedelta
            hoje = date.today()
            
            aulas_criadas = 0
            for semana in range(4):  # 4 semanas
                for dia_nome in dados['dias_semana']:
                    dia_num = dias_map[dia_nome]
                    
                    # Calcular a data da aula
                    dias_ate_dia = (dia_num - hoje.weekday()) % 7
                    if dias_ate_dia == 0 and semana == 0:
                        dias_ate_dia = 7  # Próxima semana se for hoje
                    
                    data_aula = hoje + timedelta(days=dias_ate_dia + (semana * 7))
                    
                    # Criar registro de presença agendado
                    RegistroPresenca.objects.create(
                        aluno=aluno,
                        data_aula=data_aula,
                        horario_inicio=dados['horario'],
                        status='presente'  # Vou marcar como presente para exemplo
                    )
                    aulas_criadas += 1
            
            print(f"🏋️‍♂️ {aulas_criadas} registros de presença criados para as próximas 4 semanas")
            print(f"📊 IMC calculado: {aluno.imc} - {aluno.classificacao_imc}")
            
        except Exception as e:
            print(f"❌ Erro ao criar aluno {dados['nome']}: {str(e)}")
    
    print(f"\n🎉 Processo concluído!")
    print(f"📈 Total de alunos no sistema: {Aluno.objects.count()}")

if __name__ == '__main__':
    criar_alunos_exemplo()
