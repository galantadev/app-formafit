"""
Modelos simplificados para gestão financeira.
"""
from django.db import models
from django.utils import timezone
from decimal import Decimal
from alunos.models import Aluno


class FaturaSimples(models.Model):
    """
    Modelo simplificado de fatura para alunos.
    """
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('paga', 'Paga'),
        ('atrasada', 'Atrasada'),
    ]
    
    # Dados básicos
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='faturas_simples')
    mes_referencia = models.IntegerField(choices=[(i, i) for i in range(1, 13)])
    ano_referencia = models.IntegerField()
    valor = models.DecimalField(max_digits=8, decimal_places=2)
    data_vencimento = models.DateField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pendente')
    
    # Observações
    observacoes = models.TextField(blank=True, help_text="Observações sobre a fatura")
    
    # Controle
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Fatura'
        verbose_name_plural = 'Faturas'
        ordering = ['-ano_referencia', '-mes_referencia', '-data_vencimento']
        unique_together = ['aluno', 'mes_referencia', 'ano_referencia']
    
    def __str__(self):
        meses = {
            1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril',
            5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
            9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
        }
        return f"{self.aluno.nome} - {meses[self.mes_referencia]}/{self.ano_referencia} - R$ {self.valor}"
    
    def save(self, *args, **kwargs):
        """Verifica se a fatura está atrasada automaticamente."""
        hoje = timezone.now().date()
        if self.data_vencimento < hoje and self.status == 'pendente':
            self.status = 'atrasada'
        super().save(*args, **kwargs)
    
    @property
    def mes_nome(self):
        """Retorna o nome do mês de referência."""
        meses = {
            1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril',
            5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
            9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
        }
        return meses.get(self.mes_referencia, 'Mês inválido')
    
    @property
    def esta_atrasada(self):
        """Verifica se a fatura está atrasada."""
        hoje = timezone.now().date()
        return self.data_vencimento < hoje and self.status != 'paga'
