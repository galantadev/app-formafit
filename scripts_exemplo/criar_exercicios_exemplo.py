#!/usr/bin/env python
"""
Script para criar exercícios de exemplo no banco de dados
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'formafit.settings')
django.setup()

from treinos.models import Exercicio

def criar_exercicios_exemplo():
    """Cria exercícios de exemplo para testar o CRUD"""
    
    exercicios_data = [
        {
            'nome': 'Supino Reto com Barra',
            'descricao': 'Exercício fundamental para desenvolvimento do peitoral, tríceps e deltoides anterior.',
            'grupo_muscular': 'peito',
            'categoria': 'forca',
            'equipamento': 'livre',
            'instrucoes': '1. Deite no banco com os pés firmes no chão\n2. Posicione as mãos na barra com pegada média\n3. Desça a barra controladamente até o peito\n4. Empurre a barra de volta à posição inicial'
        },
        {
            'nome': 'Puxada Frontal',
            'descricao': 'Exercício para fortalecimento dos músculos das costas, especialmente latíssimo do dorso.',
            'grupo_muscular': 'costas',
            'categoria': 'forca',
            'equipamento': 'cabo',
            'instrucoes': '1. Sente-se no aparelho com as coxas presas\n2. Segure a barra com pegada aberta\n3. Puxe a barra até a altura do peito\n4. Retorne controladamente à posição inicial'
        },
        {
            'nome': 'Agachamento Livre',
            'descricao': 'Exercício completo para membros inferiores, trabalhando quadríceps, glúteos e posteriores.',
            'grupo_muscular': 'quadriceps',
            'categoria': 'forca',
            'equipamento': 'livre',
            'instrucoes': '1. Posicione a barra nos ombros\n2. Pés na largura dos ombros\n3. Desça flexionando joelhos e quadril\n4. Suba mantendo o tronco ereto'
        },
        {
            'nome': 'Flexão de Braços',
            'descricao': 'Exercício com peso corporal para peito, tríceps e deltoides anterior.',
            'grupo_muscular': 'peito',
            'categoria': 'forca',
            'equipamento': 'corporal',
            'instrucoes': '1. Posição de prancha com mãos no chão\n2. Desça o corpo flexionando os braços\n3. Empurre de volta até estender os braços\n4. Mantenha o corpo alinhado durante todo movimento'
        },
        {
            'nome': 'Remada Curvada',
            'descricao': 'Exercício para fortalecimento das costas e músculos posturais.',
            'grupo_muscular': 'costas',
            'categoria': 'forca',
            'equipamento': 'livre',
            'instrucoes': '1. Segure a barra com pegada pronada\n2. Flexione o tronco para frente\n3. Puxe a barra em direção ao abdômen\n4. Retorne controladamente'
        },
        {
            'nome': 'Desenvolvimento com Halteres',
            'descricao': 'Exercício para desenvolvimento dos ombros e estabilização.',
            'grupo_muscular': 'ombros',
            'categoria': 'forca',
            'equipamento': 'livre',
            'instrucoes': '1. Sente-se com halteres nas mãos\n2. Posicione os halteres na altura dos ombros\n3. Empurre para cima até estender os braços\n4. Retorne controladamente'
        },
        {
            'nome': 'Esteira - Caminhada',
            'descricao': 'Exercício cardiovascular de baixo impacto para condicionamento.',
            'grupo_muscular': 'cardio',
            'categoria': 'cardio',
            'equipamento': 'cardio',
            'instrucoes': '1. Ajuste a velocidade conforme seu condicionamento\n2. Mantenha postura ereta\n3. Braços em movimento natural\n4. Respire de forma constante'
        },
        {
            'nome': 'Prancha Abdominal',
            'descricao': 'Exercício isométrico para fortalecimento do core.',
            'grupo_muscular': 'abdomen',
            'categoria': 'funcional',
            'equipamento': 'corporal',
            'instrucoes': '1. Posição de prancha com antebraços no chão\n2. Mantenha o corpo em linha reta\n3. Contraia o abdômen\n4. Mantenha a posição pelo tempo determinado'
        }
    ]
    
    print("🏋️‍♂️ Criando exercícios de exemplo...")
    
    for i, dados in enumerate(exercicios_data, 1):
        print(f"\n📝 Criando exercício {i}: {dados['nome']}")
        
        # Verificar se o exercício já existe
        if Exercicio.objects.filter(nome=dados['nome']).exists():
            print(f"⚠️  Exercício {dados['nome']} já existe, pulando...")
            continue
        
        try:
            exercicio = Exercicio.objects.create(**dados)
            print(f"✅ Exercício criado: {exercicio.nome}")
            
        except Exception as e:
            print(f"❌ Erro ao criar exercício {dados['nome']}: {str(e)}")
    
    print(f"\n🎉 Processo concluído!")
    print(f"📈 Total de exercícios no sistema: {Exercicio.objects.count()}")

if __name__ == '__main__':
    criar_exercicios_exemplo()
