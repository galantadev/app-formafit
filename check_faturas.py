from django.core.wsgi import get_wsgi_application
import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'formafit.settings')
application = get_wsgi_application()

from financeiro.models import FaturaSimples
from django.db.models import Sum

print('Verificando faturas por mês:')
for mes in [6, 8, 10]:
    faturas = FaturaSimples.objects.filter(mes_referencia=mes, status='paga')
    total = faturas.aggregate(total=Sum('valor'))['total'] or 0
    print(f'Mês {mes}: {faturas.count()} faturas, Total: R$ {total}')

print('\nVerificando faturas por mês e ano (2025):')
for mes in [6, 8, 10]:
    faturas = FaturaSimples.objects.filter(mes_referencia=mes, ano_referencia=2025, status='paga')
    total = faturas.aggregate(total=Sum('valor'))['total'] or 0
    print(f'Mês {mes}/2025: {faturas.count()} faturas, Total: R$ {total}')