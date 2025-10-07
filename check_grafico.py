from django.core.wsgi import get_wsgi_application
import os
import sys
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'formafit.settings')
application = get_wsgi_application()

from financeiro.models import FaturaSimples
from django.db.models import Sum

# Simular a lógica do gráfico financeiro
hoje = datetime.now()
meses_abreviados = {
    1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Abr', 5: 'Mai', 6: 'Jun',
    7: 'Jul', 8: 'Ago', 9: 'Set', 10: 'Out', 11: 'Nov', 12: 'Dez'
}

print('Simulando o gráfico financeiro (usando ano 2025):')
receitas_ultimos_meses = []
nomes_meses = []

for i in range(5, -1, -1):  # 6 meses atrás até o mês atual
    mes_calc = hoje.month - i
    ano_calc = 2025  # Usando o ano fixo 2025 onde existem as faturas
    
    # Ajustar ano se o mês for menor que 1
    if mes_calc <= 0:
        mes_calc += 12
        ano_calc -= 1
    
    # Calcular receita baseada no mês de referência
    receita_mes = FaturaSimples.objects.filter(
        status='paga',
        mes_referencia=mes_calc,
        ano_referencia=ano_calc
    ).aggregate(total=Sum('valor'))['total'] or 0
    
    receitas_ultimos_meses.append(float(receita_mes))
    nomes_meses.append(meses_abreviados[mes_calc])
    
    print(f'Mês {meses_abreviados[mes_calc]} ({mes_calc}/{ano_calc}): R$ {receita_mes}')

print('\nArray de receitas para o gráfico:')
print(receitas_ultimos_meses)
print('\nArray de nomes de meses para o gráfico:')
print(nomes_meses)