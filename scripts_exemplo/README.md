# Scripts de Exemplo - FormaFit

Este diretório contém scripts para popular o banco de dados com dados de exemplo e teste do sistema FormaFit.

## 📋 Scripts Disponíveis

### 1. `criar_admin.py`
**Objetivo:** Criar usuário administrador do sistema

**Função:** Cria um superusuário com as credenciais:
- **Usuário:** admin
- **Senha:** admin123
- **Email:** admin@formafit.com

**Como executar:**
```bash
python scripts_exemplo/criar_admin.py
```

### 2. `criar_planos_exemplo.py`
**Objetivo:** Criar planos de mensalidade de exemplo

**Função:** Cria 5 planos financeiros padrão:
- Plano Avaliação (4 aulas - R$ 80,00)
- Plano Básico (8 aulas - R$ 120,00)
- Plano Intermediário (12 aulas - R$ 180,00)
- Plano Premium (20 aulas - R$ 280,00)
- Plano VIP (ilimitado - R$ 400,00)

**Como executar:**
```bash
python scripts_exemplo/criar_planos_exemplo.py
```

### 3. `criar_exercicios_exemplo.py`
**Objetivo:** Criar exercícios de exemplo para os treinos

**Função:** Cria 8 exercícios variados:
- Supino Reto com Barra
- Puxada Frontal
- Agachamento Livre
- Flexão de Braços
- Remada Curvada
- Desenvolvimento com Halteres
- Esteira - Caminhada
- Prancha Abdominal

**Como executar:**
```bash
python scripts_exemplo/criar_exercicios_exemplo.py
```

### 4. `criar_alunos_exemplo.py`
**Objetivo:** Criar 5 alunos de exemplo com dados completos

**Função:** Cria alunos com:
- Dados pessoais completos
- Horários de treino configurados
- Contratos financeiros
- Registros de presença das próximas 4 semanas
- Cálculo automático de IMC

**Alunos criados:**
- João Silva Santos
- Maria Oliveira Costa
- Carlos Roberto Mendes
- Ana Paula Ferreira
- Pedro Henrique Lima

**Como executar:**
```bash
python scripts_exemplo/criar_alunos_exemplo.py
```

### 5. `criar_dados_notificacoes.py`
**Objetivo:** Criar tipos de notificação e configurações automáticas

**Função:** Cria:
- 6 tipos de notificação com cores específicas
- 5 configurações de notificações automáticas
- Triggers para cobrança, lembretes e aniversários

**Como executar:**
```bash
python scripts_exemplo/criar_dados_notificacoes.py
```

### 6. `criar_notificacoes_exemplo.py`
**Objetivo:** Criar notificações de exemplo para teste

**Função:** Cria 4 notificações de exemplo:
- Lembrete de treino
- Cobrança de mensalidade
- Mensagem motivacional
- Relatório disponível

**Como executar:**
```bash
python scripts_exemplo/criar_notificacoes_exemplo.py
```

### 7. `criar_tipos_relatorios.py`
**Objetivo:** Criar tipos de relatórios do sistema

**Função:** Cria 6 tipos de relatórios:
- Relatório de Progresso Completo
- Relatório de Medidas Corporais
- Relatório de Frequência
- Relatório Simples
- Relatório Fotográfico
- Relatório Mensal Executive

**Como executar:**
```bash
python scripts_exemplo/criar_tipos_relatorios.py
```

## 🚀 Setup Completo do Sistema

Para configurar o sistema completo com todos os dados de exemplo, execute os scripts na seguinte ordem:

```bash
# 1. Criar usuário administrador
python scripts_exemplo/criar_admin.py

# 2. Criar planos financeiros
python scripts_exemplo/criar_planos_exemplo.py

# 3. Criar exercícios
python scripts_exemplo/criar_exercicios_exemplo.py

# 4. Criar tipos e dados de notificações
python scripts_exemplo/criar_dados_notificacoes.py

# 5. Criar tipos de relatórios
python scripts_exemplo/criar_tipos_relatorios.py

# 6. Criar alunos de exemplo (após os planos)
python scripts_exemplo/criar_alunos_exemplo.py

# 7. Criar notificações de exemplo (após alunos)
python scripts_exemplo/criar_notificacoes_exemplo.py
```

## ⚠️ Importante

- **Execute apenas uma vez:** Todos os scripts verificam se os dados já existem antes de criar
- **Ordem de execução:** Respeite a ordem sugerida devido às dependências entre os dados
- **Ambiente:** Execute sempre a partir do diretório raiz do projeto
- **Configuração:** Certifique-se de que o Django está configurado corretamente

## 📊 Dados Criados

Após executar todos os scripts, você terá:
- ✅ 1 usuário administrador
- ✅ 5 planos de mensalidade
- ✅ 8 exercícios variados
- ✅ 6 tipos de notificação
- ✅ 5 notificações automáticas
- ✅ 6 tipos de relatórios
- ✅ 5 alunos completos com contratos e agendamentos
- ✅ 4 notificações de exemplo

## 🔧 Troubleshooting

**Erro de import do Django:**
```bash
# Certifique-se de estar no diretório correto
cd /caminho/para/formafit

# Execute com o Python do ambiente virtual
python scripts_exemplo/nome_do_script.py
```

**Erro de dependências:**
```bash
# Execute os scripts na ordem correta
# Exemplo: criar_planos_exemplo.py antes de criar_alunos_exemplo.py
```

## 📝 Personalização

Você pode modificar os dados nos scripts para adequar às suas necessidades:
- Alterar valores dos planos
- Adicionar/remover exercícios
- Modificar dados dos alunos
- Customizar tipos de notificação

## 🧹 Limpeza dos Dados

Para remover todos os dados de exemplo, use o Django Admin ou execute comandos de limpeza específicos conforme necessário.
