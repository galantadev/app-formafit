import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'formafit.settings')
django.setup()

from django.db import connection
from django.contrib.auth import get_user_model

User = get_user_model()

print("=== STATUS DO BANCO DE DADOS FORMAFIT ===\n")

# Verificar conexão
cursor = connection.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("📁 Tabelas criadas:")
for table in tables:
    print(f"   - {table[0]}")

print(f"\n👥 Total de usuários: {User.objects.count()}")
print(f"🔑 Superusuários: {User.objects.filter(is_superuser=True).count()}")

# Verificar se há alunos
try:
    from alunos.models import Aluno
    print(f"🎓 Total de alunos: {Aluno.objects.count()}")
except:
    print("🎓 Total de alunos: 0")

# Verificar agendamentos
try:
    from frequencia.models import AgendaAula
    print(f"📅 Total de agendamentos: {AgendaAula.objects.count()}")
except:
    print("📅 Total de agendamentos: 0")

print("\n" + "="*50)
