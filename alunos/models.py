"""
Modelos para gerenciamento de alunos.
"""
from django.db import models
from django.conf import settings
from django.utils import timezone


class Aluno(models.Model):
    """
    Modelo para representar um aluno do personal trainer.
    """
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'),
    ]
    
    # Dados pessoais
    nome = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20)
    data_nascimento = models.DateField()
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    endereco = models.TextField(blank=True)
    
    # Dados físicos iniciais
    peso_inicial = models.DecimalField(max_digits=5, decimal_places=2, help_text="Peso em kg")
    altura = models.DecimalField(max_digits=4, decimal_places=2, help_text="Altura em metros")
    
    # Objetivos e observações
    objetivo = models.TextField(blank=True, help_text="Descreva os objetivos do aluno...")
    observacoes = models.TextField(blank=True, help_text="Observações gerais, histórico médico, etc.")
    
    # Relacionamento com personal trainer
    personal_trainer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='alunos')
    
    # Dados de controle
    ativo = models.BooleanField(default=True)
    data_inicio = models.DateField(default=timezone.now)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Aluno'
        verbose_name_plural = 'Alunos'
        ordering = ['nome']
    
    def __str__(self):
        return self.nome
    
    @property
    def idade(self):
        """Calcula a idade do aluno."""
        hoje = timezone.now().date()
        idade = hoje.year - self.data_nascimento.year
        if hoje.month < self.data_nascimento.month or (hoje.month == self.data_nascimento.month and hoje.day < self.data_nascimento.day):
            idade -= 1
        return idade
    
    @property
    def imc_inicial(self):
        """Calcula o IMC inicial do aluno."""
        if self.peso_inicial and self.altura:
            return float(self.peso_inicial) / (float(self.altura) ** 2)
        return None
    
    @property
    def classificacao_imc(self):
        """Retorna a classificação do IMC inicial."""
        imc = self.imc_inicial
        if imc is None:
            return "Não calculado"
        
        if imc < 18.5:
            return "Abaixo do peso"
        elif 18.5 <= imc < 25:
            return "Peso normal"
        elif 25 <= imc < 30:
            return "Sobrepeso"
        elif 30 <= imc < 35:
            return "Obesidade grau I"
        elif 35 <= imc < 40:
            return "Obesidade grau II"
        else:
            return "Obesidade grau III"
    
    @property
    def cor_imc(self):
        """Retorna a cor para exibição do IMC baseado na classificação."""
        imc = self.imc_inicial
        if imc is None:
            return "gray"
        
        if imc < 18.5:
            return "blue"  # Abaixo do peso
        elif 18.5 <= imc < 25:
            return "green"  # Normal
        elif 25 <= imc < 30:
            return "yellow"  # Sobrepeso
        else:
            return "red"  # Obesidade


class MedidasCorporais(models.Model):
    """
    Modelo para armazenar medidas corporais do aluno ao longo do tempo.
    """
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='medidas')
    data_medicao = models.DateField(default=timezone.now)
    
    # Medidas básicas
    peso = models.DecimalField(max_digits=5, decimal_places=2, help_text="Peso em kg")
    percentual_gordura = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    
    # Medidas específicas (em cm)
    pescoco = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    torax = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    cintura = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    quadril = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    braco_direito = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    braco_esquerdo = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    coxa_direita = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    coxa_esquerda = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    
    # Observações
    observacoes = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Medidas Corporais'
        verbose_name_plural = 'Medidas Corporais'
        ordering = ['-data_medicao']
        unique_together = ['aluno', 'data_medicao']
    
    def __str__(self):
        return f"{self.aluno.nome} - {self.data_medicao.strftime('%d/%m/%Y')}"
    
    @property
    def imc(self):
        """Calcula o IMC para esta medição."""
        if self.peso and self.aluno.altura:
            return float(self.peso) / (float(self.aluno.altura) ** 2)
        return None


class FotoProgresso(models.Model):
    """
    Modelo para armazenar fotos de progresso do aluno.
    """
    TIPO_FOTO_CHOICES = [
        ('frente', 'Frente'),
        ('lado', 'Lado'),
        ('costas', 'Costas'),
        ('outro', 'Outro'),
    ]
    
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='fotos_progresso')
    data_foto = models.DateField(default=timezone.now)
    tipo_foto = models.CharField(max_length=10, choices=TIPO_FOTO_CHOICES)
    foto = models.ImageField(upload_to='progresso/')
    descricao = models.CharField(max_length=200, blank=True)
    
    class Meta:
        verbose_name = 'Foto de Progresso'
        verbose_name_plural = 'Fotos de Progresso'
        ordering = ['-data_foto']
    
    def __str__(self):
        return f"{self.aluno.nome} - {self.tipo_foto} - {self.data_foto.strftime('%d/%m/%Y')}"


class AcompanhamentoMensal(models.Model):
    """
    Modelo para armazenar acompanhamento mensal detalhado do aluno.
    """
    MESES_CHOICES = [
        (1, 'Janeiro'),
        (2, 'Fevereiro'),
        (3, 'Março'),
        (4, 'Abril'),
        (5, 'Maio'),
        (6, 'Junho'),
        (7, 'Julho'),
        (8, 'Agosto'),
        (9, 'Setembro'),
        (10, 'Outubro'),
        (11, 'Novembro'),
        (12, 'Dezembro'),
    ]
    
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='acompanhamentos_mensais')
    ano = models.PositiveIntegerField()
    mes = models.PositiveIntegerField(choices=MESES_CHOICES)
    
    # Medidas obrigatórias
    peso = models.DecimalField(max_digits=5, decimal_places=2, help_text="Peso em kg")
    percentual_gordura = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True, help_text="Percentual de gordura corporal")
    
    # Medidas corporais em cm
    ombro = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True, help_text="Medida do ombro em cm")
    torax = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True, help_text="Medida do tórax em cm")
    braco = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True, help_text="Medida do braço em cm")
    quadril = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True, help_text="Medida do quadril em cm")
    cintura = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True, help_text="Medida da cintura em cm")
    coxa = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True, help_text="Medida da coxa em cm")
    panturrilha = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True, help_text="Medida da panturrilha em cm")
    
    # Dados calculados
    imc = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True, help_text="IMC calculado automaticamente")
    
    # Observações e controle
    observacoes = models.TextField(blank=True, help_text="Observações sobre as medidas do mês")
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Acompanhamento Mensal'
        verbose_name_plural = 'Acompanhamentos Mensais'
        unique_together = ['aluno', 'ano', 'mes']
        ordering = ['-ano', '-mes']
    
    def __str__(self):
        return f"{self.aluno.nome} - {self.get_mes_display()}/{self.ano}"
    
    def save(self, *args, **kwargs):
        """Calcula automaticamente o IMC antes de salvar."""
        if self.peso and self.aluno.altura:
            self.imc = float(self.peso) / (float(self.aluno.altura) ** 2)
        super().save(*args, **kwargs)
    
    @property
    def classificacao_imc(self):
        """Retorna a classificação do IMC."""
        if self.imc is None:
            return "Não calculado"
        
        imc = float(self.imc)
        if imc < 18.5:
            return "Abaixo do peso"
        elif 18.5 <= imc < 25:
            return "Peso normal"
        elif 25 <= imc < 30:
            return "Sobrepeso"
        elif 30 <= imc < 35:
            return "Obesidade grau I"
        elif 35 <= imc < 40:
            return "Obesidade grau II"
        else:
            return "Obesidade grau III"


class HorarioPadraoAluno(models.Model):
    """
    Modelo para armazenar horários padrão de treino do aluno.
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
    
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='horarios_padrao')
    dia_semana = models.IntegerField(choices=DIAS_SEMANA_CHOICES)
    horario_inicio = models.TimeField()
    horario_fim = models.TimeField()
    ativo = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Horário Padrão'
        verbose_name_plural = 'Horários Padrão'
        unique_together = ['aluno', 'dia_semana', 'horario_inicio']
        ordering = ['dia_semana', 'horario_inicio']
    
    def __str__(self):
        return f"{self.aluno.nome} - {self.get_dia_semana_display()} às {self.horario_inicio.strftime('%H:%M')}"