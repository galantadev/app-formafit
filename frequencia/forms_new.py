"""
Formulários simplificados para frequência.
"""
from django import forms
from .models import AgendaAula
from alunos.models import Aluno


class AgendaAulaForm(forms.ModelForm):
    """
    Formulário simplificado para agendamento de aulas.
    """
    class Meta:
        model = AgendaAula
        fields = ['aluno', 'data_aula', 'horario_inicio', 'horario_fim', 'compareceu', 'observacoes']
        labels = {
            'aluno': 'Aluno',
            'data_aula': 'Data da Aula',
            'horario_inicio': 'Horário de Início',
            'horario_fim': 'Horário de Fim',
            'compareceu': 'Compareceu',
            'observacoes': 'Observações'
        }
        widgets = {
            'aluno': forms.Select(attrs={
                'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500'
            }),
            'data_aula': forms.DateInput(attrs={
                'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'type': 'date'
            }),
            'horario_inicio': forms.TimeInput(attrs={
                'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'type': 'time'
            }),
            'horario_fim': forms.TimeInput(attrs={
                'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'type': 'time'
            }),
            'compareceu': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500'
            }),
            'observacoes': forms.Textarea(attrs={
                'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'rows': 3,
                'placeholder': 'Observações sobre a aula (opcional)'
            })
        }
    
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar apenas alunos do personal trainer logado
        self.fields['aluno'].queryset = Aluno.objects.filter(
            personal_trainer=user,
            ativo=True
        )
    
    def clean(self):
        cleaned_data = super().clean()
        horario_inicio = cleaned_data.get('horario_inicio')
        horario_fim = cleaned_data.get('horario_fim')
        
        if horario_inicio and horario_fim:
            if horario_fim <= horario_inicio:
                raise forms.ValidationError(
                    'O horário de fim deve ser posterior ao horário de início.'
                )
        
        return cleaned_data
