#!/usr/bin/env python
"""
Script para criar usuário administrador no banco de dados
"""

import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'formafit.settings')
django.setup()

from django.contrib.auth import get_user_model

def criar_admin():
    """Cria usuário administrador"""
    
    User = get_user_model()

    print("👤 Criando usuário administrador...")

    # Verificar se já existe um admin
    if not User.objects.filter(username='admin').exists():
        user = User.objects.create_user(
            username='admin',
            email='admin@formafit.com',
            password='admin123',
            first_name='Administrador',
            last_name='FormaFit',
            is_staff=True,
            is_superuser=True
        )
        print(f'✅ Superusuário criado: {user.username}')
        print(f'📧 Email: {user.email}')
        print(f'🔑 Senha: admin123')
        print(f'⚙️  Permissões: Staff e Superuser')
    else:
        print('⚠️  Usuário admin já existe')
        user = User.objects.get(username='admin')
        print(f'📧 Email: {user.email}')

    print("🎉 Processo concluído!")

if __name__ == '__main__':
    criar_admin()
