"""
Formulários para gerenciamento de alunos.
"""
from django import forms
from django.core.validators import RegexValidator
from .models import Aluno, MedidasCorporais, FotoProgresso, HorarioPadraoAluno, AcompanhamentoMensal
from financeiro.models import PlanoMensalidade


class AlunoForm(forms.ModelForm):
    """
    Formulário para cadastro e edição de alunos.
    """
    telefone = forms.CharField(
        validators=[RegexValidator(
            regex=r'^\(\d{2}\)\s\d{4,5}-\d{4}$',
            message='Digite o telefone no formato: (11) 99999-9999'
        )],
        widget=forms.TextInput(attrs={
            'placeholder': '(11) 99999-9999',
            'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
        })
    )
    
    class Meta:
        model = Aluno
        fields = [
            'nome', 'email', 'telefone', 'data_nascimento',
            'sexo', 'altura', 'peso_inicial', 'objetivo',
            'observacoes', 'endereco', 'ativo'
        ]
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Nome completo do aluno'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'email@exemplo.com'
            }),
            'data_nascimento': forms.DateInput(attrs={
                'type': 'date',
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
            }),
            'sexo': forms.Select(attrs={
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
            }),
            'altura': forms.NumberInput(attrs={
                'step': '0.01',
                'min': '0.5',
                'max': '2.5',
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Ex: 1.75'
            }),
            'peso_inicial': forms.NumberInput(attrs={
                'step': '0.1',
                'min': '20',
                'max': '300',
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Ex: 70.5'
            }),
            'objetivo': forms.Textarea(attrs={
                'rows': 3,
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Descreva os objetivos do aluno...'
            }),
            'nivel_atividade': forms.Select(attrs={
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
            }),
            'endereco': forms.Textarea(attrs={
                'rows': 2,
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Endereço completo...'
            }),
            'observacoes': forms.Textarea(attrs={
                'rows': 3,
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Observações gerais, histórico médico, restrições...'
            }),
            'ativo': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded'
            })
        }


class MedidasCorporaisForm(forms.ModelForm):
    """
    Formulário para registro de medidas corporais.
    """
    class Meta:
        model = MedidasCorporais
        fields = [
            'peso', 'percentual_gordura', 'pescoco', 'torax', 
            'cintura', 'quadril', 'braco_direito', 'braco_esquerdo',
            'coxa_direita', 'coxa_esquerda', 'observacoes'
        ]
        widgets = {
            'peso': forms.NumberInput(attrs={
                'step': '0.1',
                'min': '20',
                'max': '300',
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Ex: 70.5'
            }),
            'percentual_gordura': forms.NumberInput(attrs={
                'step': '0.1',
                'min': '0',
                'max': '100',
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Ex: 15.2'
            }),
            'pescoco': forms.NumberInput(attrs={
                'step': '0.1',
                'min': '20',
                'max': '80',
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Em centímetros'
            }),
            'torax': forms.NumberInput(attrs={
                'step': '0.1',
                'min': '50',
                'max': '200',
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Em centímetros'
            }),
            'cintura': forms.NumberInput(attrs={
                'step': '0.1',
                'min': '40',
                'max': '200',
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Em centímetros'
            }),
            'quadril': forms.NumberInput(attrs={
                'step': '0.1',
                'min': '40',
                'max': '200',
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Em centímetros'
            }),
            'braco_direito': forms.NumberInput(attrs={
                'step': '0.1',
                'min': '15',
                'max': '60',
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Em centímetros'
            }),
            'braco_esquerdo': forms.NumberInput(attrs={
                'step': '0.1',
                'min': '15',
                'max': '60',
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Em centímetros'
            }),
            'coxa_direita': forms.NumberInput(attrs={
                'step': '0.1',
                'min': '30',
                'max': '100',
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Em centímetros'
            }),
            'coxa_esquerda': forms.NumberInput(attrs={
                'step': '0.1',
                'min': '30',
                'max': '100',
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Em centímetros'
            }),
            'observacoes': forms.Textarea(attrs={
                'rows': 3,
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Observações sobre as medidas...'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove o auto-cálculo de IMC já que não temos altura nas medidas
        pass


class FotoProgressoForm(forms.ModelForm):
    """
    Formulário para upload de fotos de progresso.
    """
    class Meta:
        model = FotoProgresso
        fields = ['foto', 'tipo_foto', 'descricao']
        widgets = {
            'foto': forms.FileInput(attrs={
                'accept': 'image/*',
                'class': 'mt-1 block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100'
            }),
            'tipo_foto': forms.Select(attrs={
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
            }),
            'descricao': forms.Textarea(attrs={
                'rows': 3,
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Descrição da foto...'
            })
        }


class AlunoSearchForm(forms.Form):
    """
    Formulário para busca e filtro de alunos.
    """
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Buscar por nome, email ou telefone...',
            'class': 'block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
        })
    )
    
    status = forms.ChoiceField(
        choices=[
            ('', 'Todos'),
            ('ativo', 'Ativos'),
            ('inativo', 'Inativos')
        ],
        required=False,
        widget=forms.Select(attrs={
            'class': 'block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
        })
    )
    
    objetivo = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
            'placeholder': 'Buscar por objetivo...'
        })
    )


class HorarioPadraoForm(forms.ModelForm):
    """
    Formulário para configuração de horários padrão do aluno.
    """
    class Meta:
        model = HorarioPadraoAluno
        fields = ['dia_semana', 'horario_inicio', 'horario_fim']
        widgets = {
            'dia_semana': forms.Select(attrs={
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
            }),
            'horario_inicio': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
            }),
            'horario_fim': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
            }),
        }


class AgendamentoPadraoForm(forms.Form):
    """
    Formulário para configurar agendamentos padrão durante o cadastro do aluno.
    """
    DIAS_SEMANA_CHOICES = [
        (0, 'Segunda-feira'),
        (1, 'Terça-feira'),
        (2, 'Quarta-feira'),
        (3, 'Quinta-feira'),
        (4, 'Sexta-feira'),
        (5, 'Sábado'),
        (6, 'Domingo'),
    ]
    
    dias_semana = forms.MultipleChoiceField(
        choices=DIAS_SEMANA_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded'
        }),
        required=False,
        label="Dias da Semana do Treino"
    )
    
    horario_inicio = forms.TimeField(
        widget=forms.TimeInput(attrs={
            'type': 'time',
            'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
        }),
        required=False,
        label="Horário do Treino"
    )
    
    criar_agendamentos = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'h-4 w-4 text-red-600 focus:ring-red-500 border-gray-300 rounded'
        }),
        label="Criar agendamentos automáticos das próximas 4 semanas"
    )


class PlanoFinanceiroForm(forms.Form):
    """
    Formulário para configurar plano financeiro durante o cadastro do aluno.
    """
    plano_mensalidade = forms.ModelChoiceField(
        queryset=PlanoMensalidade.objects.filter(ativo=True),
        empty_label="Selecione um plano...",
        widget=forms.Select(attrs={
            'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
        }),
        required=False,
        label="Plano de Mensalidade"
    )
    
    valor_personalizado = forms.DecimalField(
        max_digits=8,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'step': '0.01',
            'min': '0',
            'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
            'placeholder': 'Ex: 150.00'
        }),
        required=False,
        label="Valor Personalizado (opcional)",
        help_text="Deixe em branco para usar o valor do plano selecionado"
    )
    
    dia_vencimento = forms.IntegerField(
        min_value=1,
        max_value=28,
        initial=5,
        widget=forms.NumberInput(attrs={
            'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
            'placeholder': '5'
        }),
        required=False,
        label="Dia do Vencimento",
        help_text="Dia do mês para vencimento das faturas (1-28)"
    )
    
    criar_contrato = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300 rounded'
        }),
        label="Criar contrato e gerar faturas automaticamente"
    )
    
    meses_antecipados = forms.IntegerField(
        min_value=1,
        max_value=12,
        initial=3,
        widget=forms.NumberInput(attrs={
            'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
        }),
        required=False,
        label="Quantidade de meses para gerar faturas",
        help_text="Quantos meses de faturas serão criados antecipadamente"
    )


class AcompanhamentoMensalForm(forms.ModelForm):
    """
    Formulário para acompanhamento mensal do aluno.
    """
    
    class Meta:
        model = AcompanhamentoMensal
        fields = [
            'peso', 'percentual_gordura', 'ombro', 'torax', 'braco',
            'quadril', 'cintura', 'coxa', 'panturrilha', 'observacoes'
        ]
        widgets = {
            'peso': forms.NumberInput(attrs={
                'step': '0.1',
                'min': '0',
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Ex: 70.5'
            }),
            'percentual_gordura': forms.NumberInput(attrs={
                'step': '0.1',
                'min': '0',
                'max': '100',
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Ex: 15.2'
            }),
            'ombro': forms.NumberInput(attrs={
                'step': '0.1',
                'min': '0',
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Em cm'
            }),
            'torax': forms.NumberInput(attrs={
                'step': '0.1',
                'min': '0',
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Em cm'
            }),
            'braco': forms.NumberInput(attrs={
                'step': '0.1',
                'min': '0',
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Em cm'
            }),
            'quadril': forms.NumberInput(attrs={
                'step': '0.1',
                'min': '0',
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Em cm'
            }),
            'cintura': forms.NumberInput(attrs={
                'step': '0.1',
                'min': '0',
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Em cm'
            }),
            'coxa': forms.NumberInput(attrs={
                'step': '0.1',
                'min': '0',
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Em cm'
            }),
            'panturrilha': forms.NumberInput(attrs={
                'step': '0.1',
                'min': '0',
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Em cm'
            }),
            'observacoes': forms.Textarea(attrs={
                'rows': 3,
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Observações sobre as medidas deste mês...'
            }),
        }
        labels = {
            'peso': 'Peso (kg)',
            'percentual_gordura': 'Percentual de Gordura (%)',
            'ombro': 'Ombro (cm)',
            'torax': 'Tórax (cm)',
            'braco': 'Braço (cm)',
            'quadril': 'Quadril (cm)',
            'cintura': 'Cintura (cm)',
            'coxa': 'Coxa (cm)',
            'panturrilha': 'Panturrilha (cm)',
            'observacoes': 'Observações',
        }
