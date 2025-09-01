"""
Formulários simplificados para frequência.
"""
from django import forms
from .models import AgendaAula, RegistroPresenca
from alunos.models import Aluno


class AgendaAulaForm(forms.ModelForm):
    """
    Formulário para criar/editar aulas.
    """
    
    class Meta:
        model = AgendaAula
        fields = [
            'aluno', 'data_aula', 'horario_inicio', 'horario_fim',
            'status', 'tipo_treino', 'observacoes'
        ]
        widgets = {
            'aluno': forms.Select(attrs={
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
            }),
            'data_aula': forms.DateInput(attrs={
                'type': 'date',
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
            'status': forms.Select(attrs={
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
            }),
            'tipo_treino': forms.TextInput(attrs={
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Ex: Treino A, Avaliação, Cardio...'
            }),
            'observacoes': forms.Textarea(attrs={
                'rows': 3,
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Observações sobre a aula...'
            }),
        }
        labels = {
            'aluno': 'Aluno *',
            'data_aula': 'Data da Aula *',
            'horario_inicio': 'Horário de Início *',
            'horario_fim': 'Horário de Fim *',
            'status': 'Status',
            'tipo_treino': 'Tipo de Treino',
            'observacoes': 'Observações',
        }
    
    def clean(self):
        cleaned_data = super().clean()
        horario_inicio = cleaned_data.get('horario_inicio')
        horario_fim = cleaned_data.get('horario_fim')
        
        if horario_inicio and horario_fim:
            if horario_fim <= horario_inicio:
                raise forms.ValidationError('O horário de fim deve ser posterior ao horário de início.')
        
        return cleaned_data


class RegistroPresencaForm(forms.ModelForm):
    """
    Formulário para registrar presença.
    """
    
    class Meta:
        model = RegistroPresenca
        fields = [
            'aluno', 'data_aula', 'horario_inicio', 'horario_fim',
            'status', 'observacoes'
        ]
        widgets = {
            'aluno': forms.Select(attrs={
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
            }),
            'data_aula': forms.DateInput(attrs={
                'type': 'date',
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
            'status': forms.Select(attrs={
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
            }),
            'observacoes': forms.Textarea(attrs={
                'rows': 3,
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Observações sobre a presença...'
            }),
        }
        labels = {
            'aluno': 'Aluno *',
            'data_aula': 'Data da Aula *',
            'horario_inicio': 'Horário de Início *',
            'horario_fim': 'Horário de Fim',
            'status': 'Status *',
            'observacoes': 'Observações',
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            # Filtrar apenas alunos do personal trainer logado
            self.fields['aluno'].queryset = Aluno.objects.filter(
                personal_trainer=user
            ).order_by('nome')

    def clean(self):
        cleaned_data = super().clean()
        horario_inicio = cleaned_data.get('horario_inicio')
        horario_fim = cleaned_data.get('horario_fim')
        
        if horario_inicio and horario_fim:
            if horario_fim <= horario_inicio:
                raise forms.ValidationError('O horário de fim deve ser posterior ao horário de início.')
        
        return cleaned_data
