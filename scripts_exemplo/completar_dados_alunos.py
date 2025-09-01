#!/usr/bin/env python
"""
Script para adicionar dados complementares aos alunos existentes
"""

import os
import sys
import django
from datetime import date, datetime, time, timedelta
from decimal import Decimal

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'formafit.settings')
django.setup()

from alunos.models import Aluno, HorarioPadraoAluno
from financeiro.models import PlanoMensalidade, ContratoAluno, Fatura
from frequencia.models import RegistroPresenca

def adicionar_dados_complementares():
    """Adiciona horários, contratos e registros aos alunos existentes"""
    
    # Configurações por aluno
    configs = {
        'joao.silva@email.com': {
            'dias_semana': ['segunda', 'quarta', 'sexta'],
            'horario': time(7, 0),
            'plano': 'Plano Intermediário'
        },
        'maria.oliveira@email.com': {
            'dias_semana': ['terca', 'quinta'],
            'horario': time(18, 30),
            'plano': 'Plano Básico'
        },
        'carlos.mendes@email.com': {
            'dias_semana': ['segunda', 'terca', 'quinta', 'sexta'],
            'horario': time(6, 30),
            'plano': 'Plano Premium'
        },
        'ana.ferreira@email.com': {
            'dias_semana': ['segunda', 'quarta', 'sexta', 'sabado'],
            'horario': time(8, 0),
            'plano': 'Plano Premium'
        },
        'pedro.lima@email.com': {
            'dias_semana': ['segunda', 'terca', 'quarta', 'quinta', 'sexta', 'sabado'],
            'horario': time(19, 0),
            'plano': 'Plano VIP'
        }
    }
    
    dias_map = {
        'segunda': 0, 'terca': 1, 'quarta': 2, 'quinta': 3,
        'sexta': 4, 'sabado': 5, 'domingo': 6
    }
    
    print("🔧 Adicionando dados complementares aos alunos...")
    
    for email, config in configs.items():
        try:
            aluno = Aluno.objects.get(email=email)
            print(f"\n📝 Processando: {aluno.nome}")
            
            # 1. Criar horários padrão se não existem
            if not aluno.horarios_padrao.exists():
                for dia_nome in config['dias_semana']:
                    dia_num = dias_map[dia_nome]
                    horario_fim = time(
                        (config['horario'].hour + 1) % 24,
                        config['horario'].minute
                    )
                    
                    HorarioPadraoAluno.objects.create(
                        aluno=aluno,
                        dia_semana=dia_num,
                        horario_inicio=config['horario'],
                        horario_fim=horario_fim
                    )
                print(f"📅 Horários criados para: {', '.join(config['dias_semana'])}")
            else:
                print("📅 Horários já existem")
            
            # 2. Criar contrato financeiro se não existe
            if not hasattr(aluno, 'contrato') or not aluno.contrato:
                try:
                    plano = PlanoMensalidade.objects.get(nome=config['plano'])
                    
                    contrato = ContratoAluno.objects.create(
                        aluno=aluno,
                        plano_mensalidade=plano,
                        data_inicio=date.today(),
                        ativo=True
                    )
                    print(f"💰 Contrato criado com {plano.nome} - R$ {plano.valor}")
                    
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
                    print(f"⚠️  Plano '{config['plano']}' não encontrado")
            else:
                print("💰 Contrato já existe")
            
            # 3. Criar alguns registros de presença das últimas 2 semanas
            hoje = date.today()
            registros_criados = 0
            
            for semana in range(-2, 2):  # 2 semanas passadas e 2 futuras
                for dia_nome in config['dias_semana']:
                    dia_num = dias_map[dia_nome]
                    
                    # Calcular a data
                    dias_ate_dia = (dia_num - hoje.weekday()) % 7
                    if dias_ate_dia == 0 and semana == 0:
                        dias_ate_dia = 7
                    
                    data_registro = hoje + timedelta(days=dias_ate_dia + (semana * 7))
                    
                    # Só criar se não existe
                    if not RegistroPresenca.objects.filter(
                        aluno=aluno,
                        data_aula=data_registro,
                        horario_inicio=config['horario']
                    ).exists():
                        
                        # Status baseado na data (passado = presente, futuro = agendado via status presente para exemplo)
                        status = 'presente' if data_registro <= hoje else 'presente'
                        
                        RegistroPresenca.objects.create(
                            aluno=aluno,
                            data_aula=data_registro,
                            horario_inicio=config['horario'],
                            status=status
                        )
                        registros_criados += 1
            
            print(f"🏋️‍♂️ {registros_criados} registros de presença criados")
            print(f"📊 IMC: {aluno.imc} - {aluno.classificacao_imc}")
            
        except Aluno.DoesNotExist:
            print(f"❌ Aluno com email {email} não encontrado")
        except Exception as e:
            print(f"❌ Erro ao processar {email}: {str(e)}")
    
    print(f"\n🎉 Processo concluído!")
    print(f"📈 Total de alunos: {Aluno.objects.count()}")
    print(f"📅 Total de horários padrão: {HorarioPadraoAluno.objects.count()}")
    print(f"💰 Total de contratos: {ContratoAluno.objects.count()}")
    print(f"📋 Total de registros de presença: {RegistroPresenca.objects.count()}")

if __name__ == '__main__':
    adicionar_dados_complementares()
