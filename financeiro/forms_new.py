"""
Formulários simplificados para financeiro.
"""
from django import forms
from .models import FaturaSimples
from alunos.models import Aluno


class FaturaForm(forms.ModelForm):
    """
    Formulário para criar/editar faturas.
    """
    
    class Meta:
        model = FaturaSimples
        fields = [
            'aluno', 'mes_referencia', 'ano_referencia', 'valor', 
            'data_vencimento', 'status', 'observacoes'
        ]
        widgets = {
            'aluno': forms.Select(attrs={
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
            }),
            'mes_referencia': forms.Select(attrs={
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
            }),
            'ano_referencia': forms.NumberInput(attrs={
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'min': '2020',
                'max': '2030'
            }),
            'valor': forms.NumberInput(attrs={
                'step': '0.01',
                'min': '0',
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Ex: 150.00'
            }),
            'data_vencimento': forms.DateInput(attrs={
                'type': 'date',
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
            }),
            'status': forms.Select(attrs={
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
            }),
            'observacoes': forms.Textarea(attrs={
                'rows': 3,
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Observações sobre a fatura...'
            }),
        }
        labels = {
            'aluno': 'Aluno *',
            'mes_referencia': 'Mês de Referência *',
            'ano_referencia': 'Ano de Referência *',
            'valor': 'Valor *',
            'data_vencimento': 'Data de Vencimento *',
            'status': 'Status',
            'observacoes': 'Observações',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Choices para mês de referência
        meses = [
            (1, 'Janeiro'), (2, 'Fevereiro'), (3, 'Março'), (4, 'Abril'),
            (5, 'Maio'), (6, 'Junho'), (7, 'Julho'), (8, 'Agosto'),
            (9, 'Setembro'), (10, 'Outubro'), (11, 'Novembro'), (12, 'Dezembro')
        ]
        self.fields['mes_referencia'].choices = meses
    
    def clean(self):
        cleaned_data = super().clean()
        aluno = cleaned_data.get('aluno')
        mes = cleaned_data.get('mes_referencia')
        ano = cleaned_data.get('ano_referencia')
        
        # Verificar se já existe fatura para este aluno no mesmo mês/ano
        if aluno and mes and ano:
            # Se estamos editando, excluir a instância atual da verificação
            queryset = FaturaSimples.objects.filter(
                aluno=aluno, 
                mes_referencia=mes, 
                ano_referencia=ano
            )
            
            if self.instance.pk:
                queryset = queryset.exclude(pk=self.instance.pk)
            
            if queryset.exists():
                raise forms.ValidationError(
                    f'Já existe uma fatura para {aluno.nome} em {mes:02d}/{ano}.'
                )
        
        return cleaned_data
