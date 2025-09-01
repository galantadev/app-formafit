# FormaFit - Sistema de Gestão para Personal Trainers 💪

Sistema web completo desenvolvido em Django para gestão de personal trainers, incluindo cadastro de alunos, controle financeiro, agendamento de aulas e relatórios.

## 🚀 Funcionalidades Principais

### 👥 **Gestão de Alunos**
- ✅ Cadastro completo de alunos
- ✅ Histórico de acompanhamento mensal  
- ✅ Controle de status (ativo/inativo)
- ✅ Sistema de objetivos e metas
- ✅ Interface responsiva para visualização

### 📅 **Sistema de Frequência e Agendamento**
- ✅ Dashboard com estatísticas de aulas
- ✅ Agendamento de aulas individuais
- ✅ Calendário visual mensal interativo
- ✅ Controle de status das aulas (agendado, confirmado, realizado, cancelado, remarcado)
- ✅ Registro de presença dos alunos
- ✅ Navegação mensal no calendário
- ✅ Cores diferenciadas por status

### 💰 **Gestão Financeira**
- ✅ Criação e gestão de faturas
- ✅ Controle de contratos de alunos
- ✅ Dashboard financeiro com estatísticas
- ✅ Planos de mensalidade personalizáveis
- ✅ Relatórios de receitas e pagamentos
- ✅ Sistema de status (pendente, paga, atrasada)

### 📊 **Relatórios e Dashboard**
- ✅ Dashboard principal integrado
- ✅ Estatísticas de aulas e frequência
- ✅ Indicadores financeiros
- ✅ Visualizações gráficas
- ✅ Filtros por período

### 🔐 **Sistema de Autenticação**
- ✅ Login seguro para personal trainers
- ✅ Perfis de usuário
- ✅ Controle de acesso por usuário
- ✅ Configurações personalizadas

## 🛠️ **Tecnologias Utilizadas**

- **Backend**: Django 4.2.23
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Tailwind CSS
- **Database**: SQLite (desenvolvimento)
- **Icons**: Font Awesome
- **Calendar**: Python calendar module
- **Forms**: Django ModelForms com validação

## 📋 **Pré-requisitos**

- Python 3.8+
- Django 4.2+
- Git

## ⚡ **Instalação e Configuração**

### 1. Clone o repositório
```bash
git clone https://github.com/g-paiva/#
cd formafit_min
```

### 2. Instale as dependências
```bash
pip install -r requirements.txt
```

### 3. Configure o banco de dados
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Crie um superusuário
```bash
python manage.py createsuperuser
```

### 5. Execute o servidor
```bash
python manage.py runserver
```

### 6. Acesse o sistema
- **URL**: http://127.0.0.1:8000/
- **Admin**: http://127.0.0.1:8000/admin/

## 🐛 **Correções Realizadas Hoje**

- ✅ Resolvidos erros NoReverseMatch no módulo frequência
- ✅ Corrigido formulário de criação de faturas  
- ✅ Removida duplicação de modelos
- ✅ Implementado sistema de templates filters
- ✅ Ajustadas views e URLs para consistência
- ✅ Sistema de calendário visual funcional

## 👨‍💻 **Desenvolvedor**

**Gabriel Paiva**
- GitHub: [@g-paiva](https://github.com/g-paiva)

---

**FormaFit** - Transformando a gestão de personal trainers com tecnologia! 💪🚀
- ✅ **Filtros Avançados**: Busca por período, status, valor e aluno
- ✅ **Dashboard Executivo**: Visão geral das finanças em tempo real

### 📈 **Relatórios e Análises**
- ✅ **6 Tipos de Relatórios**: Progresso completo, medidas corporais, frequência, simples, fotográfico e executivo
- ✅ **Interface Administrativa**: Gestão completa de tipos de relatórios (apenas staff)
- ✅ **Gráficos de Evolução**: Peso, medidas corporais e progressão temporal
- ✅ **Exportação Profissional**: PDF otimizado para impressão e apresentação
- ✅ **Relatórios de Frequência**: Análises detalhadas de presença e performance
- ✅ **Análises Financeiras**: Métricas de negócio e dashboard executivo
- ✅ **Personalização**: Configuração flexível de conteúdo e layout

### 🔔 **Sistema de Notificações Completo**
- ✅ **Dashboard de Notificações**: Visão geral com métricas e ações rápidas
- ✅ **Notificações Manuais**: Criação e envio de mensagens personalizadas
- ✅ **Notificações Automáticas**: Triggers baseados em eventos (vencimento, pagamento)
- ✅ **Configurações Personalizáveis**: Horários preferenciais e canais por aluno
- ✅ **Tipos de Notificação**: Categorização com cores e ícones
- ✅ **WhatsApp Integration**: API ChatPro para envio automático
- ✅ **Templates Inteligentes**: Mensagens personalizáveis com variáveis dinâmicas
- ✅ **Logs Detalhados**: Histórico completo de envios e status
- ✅ **Teste de Conectividade**: Validação de configurações WhatsApp
- ✅ **Configuração por Aluno**: Preferências individuais de comunicação
- ✅ **Sistema de Triggers**: Automação baseada em vencimentos e eventos
- ✅ **Interface Moderna**: Design responsivo com Tailwind CSS

### 🎨 **Interface e Experiência**
- ✅ **Design Moderno**: Interface responsiva com Tailwind CSS e componentes otimizados
- ✅ **Dashboard Intuitivo**: Métricas em tempo real com visualizações interativas
- ✅ **Navegação Fluida**: Experiência otimizada com breadcrumbs e contexto
- ✅ **Interface Administrativa**: Área específica para staff com controle total
- ✅ **Filtros Avançados**: Busca e filtros inteligentes em todas as listagens
- ✅ **Paginação Inteligente**: Otimizada para grandes volumes de dados
- ✅ **Responsividade**: Design adaptativo para desktop, tablet e mobile
- ✅ **Acessibilidade**: Componentes otimizados para diferentes dispositivos

## �️ Tecnologias e Arquitetura

### **Backend**
- **Python 3.9+** - Linguagem principal
- **Django 4.2** - Framework web robusto e escalável
- **PostgreSQL** - Banco de dados (produção)
- **SQLite** - Banco de dados (desenvolvimento)
- **Django Rest Framework** - APIs RESTful (futuro)

### **Frontend**
- **HTML5 & CSS3** - Estrutura e estilização semântica
- **JavaScript ES6+** - Interatividade e dinamismo
- **Tailwind CSS** - Framework CSS utilitário e responsivo
- **Django Templates** - Sistema de templates robusto

### **Integrações e APIs**
- **API ChatPro** - Envio de mensagens WhatsApp automáticas
- **SMTP Email** - Sistema de notificações por email
- **Pillow** - Processamento e otimização de imagens
- **Python-decouple** - Gerenciamento seguro de configurações
- **Django CORS** - Controle de Cross-Origin Resource Sharing
- **Requests** - Integração com APIs externas

### **Ferramentas de Desenvolvimento**
- **Git** - Controle de versão
- **Virtual Environment** - Isolamento de dependências
- **Django Debug Toolbar** - Debugging avançado
- **pytest** - Testes automatizados (futuro)

## � Instalação e Configuração

### **Pré-requisitos**
- Python 3.9 ou superior
- pip (gerenciador de pacotes Python)
- Git
- PostgreSQL (para produção)

### **🛠️ Instalação Local (Desenvolvimento)**

#### **1. Clone o Repositório**
```bash
git clone https://github.com/g-paiva/#
cd FormaFit
```

#### **2. Crie e Ative o Ambiente Virtual**
```bash
# Criar ambiente virtual
python -m venv venv

# Ativar no Linux/Mac
source venv/bin/activate

# Ativar no Windows
venv\Scripts\activate
```

#### **3. Instale as Dependências**
```bash
pip install -r requirements.txt
```

#### **4. Configure as Variáveis de Ambiente**
Crie um arquivo `.env` na raiz do projeto:
```env
# Configurações Básicas
SECRET_KEY=sua-chave-secreta-muito-segura-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Banco de Dados (desenvolvimento com SQLite)
DATABASE_URL=sqlite:///db.sqlite3

# API ChatPro (opcional para desenvolvimento)
CHATPRO_API_KEY=sua-chave-api-chatpro
CHATPRO_API_URL=https://api.chatpro.com.br

# Email (opcional para desenvolvimento)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

#### **5. Execute as Migrações**
```bash
python manage.py migrate
```

#### **6. Crie um Superusuário**
```bash
python manage.py createsuperuser
```

#### **7. Execute o Servidor de Desenvolvimento**
```bash
python manage.py runserver
```

Acesse: `http://localhost:8000`

## 🔑 **Dados de Acesso para Teste**

Para facilitar os testes, você pode usar os seguintes dados de acesso:

### **👨‍💼 Usuário Administrador (Superuser)**
```
Usuário: admin
Email: admin@formafit.com
Senha: admin123
```

### **� Scripts de Setup Automatizado**
O sistema inclui scripts organizados em `scripts_exemplo/` para configuração completa:

#### **📋 Setup Rápido - Execute na Ordem:**
```bash
# 1. Criar usuário administrador
python scripts_exemplo/criar_admin.py

# 2. Criar planos de mensalidade (5 planos)
python scripts_exemplo/criar_planos_exemplo.py

# 3. Criar exercícios (8 exercícios variados)
python scripts_exemplo/criar_exercicios_exemplo.py

# 4. Configurar sistema de notificações
python scripts_exemplo/criar_dados_notificacoes.py

# 5. Criar tipos de relatórios (6 tipos)
python scripts_exemplo/criar_tipos_relatorios.py

# 6. Criar alunos de exemplo (5 alunos completos)
python scripts_exemplo/criar_alunos_exemplo.py

# 7. Criar notificações de teste
python scripts_exemplo/criar_notificacoes_exemplo.py
```

### **� Dados Inclusos Após Setup:**
- ✅ **5 Alunos Completos**: João Silva, Maria Santos, Carlos Mendes, Ana Paula, Pedro Lima
- ✅ **5 Planos Financeiros**: Avaliação, Básico, Intermediário, Premium, VIP
- ✅ **8 Exercícios Variados**: Supino, puxada, agachamento, flexão, etc.
- ✅ **6 Tipos de Relatórios**: Progresso, medidas, frequência, simples, fotográfico, executivo
- ✅ **Sistema de Notificações**: Configurado com tipos e triggers automáticos
- ✅ **Contratos e Agendamentos**: Dados completos para 4 semanas de teste

> **💡 Dica**: Após o primeiro login, explore o dashboard para ver todas as funcionalidades e dados de demonstração.

## 🎯 **Como Usar o Sistema**

### **🚀 Primeiros Passos**
1. **Login**: Use os dados de acesso fornecidos acima
2. **Dashboard**: Explore o painel principal com métricas em tempo real
3. **Alunos**: Navegue para "Alunos" e veja os dados de demonstração
4. **Financeiro**: Acesse o módulo financeiro para ver contratos e faturas
5. **Notificações**: Configure as notificações automáticas
6. **Relatórios**: Gere relatórios de progresso e evolução

### **📋 Fluxo de Trabalho Recomendado**
1. **Cadastre seus alunos** com dados completos
2. **Crie contratos** definindo valores e vencimentos
3. **Configure notificações** para lembretes automáticos
4. **Registre presença** e acompanhe frequência
5. **Gere relatórios** mensais de progresso
6. **Monitore finanças** através do dashboard executivo

### **🔧 Configurações Iniciais**
- **Interface Administrativa**: Acesse `/relatorios/admin/tipos/` para gerenciar tipos de relatórios (apenas staff)
- **Notificações WhatsApp**: Configure sua API key do ChatPro nas configurações
- **Email SMTP**: Configure servidor de email para envio de relatórios
- **Scripts de Setup**: Use os scripts em `scripts_exemplo/` para dados iniciais
- **Tipos de Relatório**: Configure através da interface administrativa
- **Dados da Academia**: Atualize informações no perfil do usuário

### **🌐 Configuração para Produção**

#### **1. Servidor e Dependências**
```bash
# Instalar dependências do sistema (Ubuntu/Debian)
sudo apt update
sudo apt install python3 python3-pip python3-venv postgresql postgresql-contrib nginx

# Instalar dependências do sistema (CentOS/RHEL)
sudo yum install python3 python3-pip postgresql postgresql-server nginx
```

#### **2. Configuração do PostgreSQL**
```bash
# Acessar PostgreSQL
sudo -u postgres psql

# Criar banco e usuário
CREATE DATABASE formafit_db;
CREATE USER formafit_user WITH PASSWORD 'senha_segura_aqui';
ALTER ROLE formafit_user SET client_encoding TO 'utf8';
ALTER ROLE formafit_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE formafit_user SET timezone TO 'America/Sao_Paulo';
GRANT ALL PRIVILEGES ON DATABASE formafit_db TO formafit_user;
\q
```

#### **3. Clone e Configure o Projeto**
```bash
# Clone para diretório de produção
cd /var/www
sudo git clone clone https://github.com/g-paiva/#
sudo chown -R www-data:www-data FormaFit
cd FormaFit

# Crie ambiente virtual
sudo -u www-data python3 -m venv venv
sudo -u www-data venv/bin/pip install -r requirements.txt
```

#### **4. Configuração de Produção (.env)**
```env
# Configurações de Produção
SECRET_KEY=chave-super-secreta-de-producao-256-bits
DEBUG=False
ALLOWED_HOSTS=seudominio.com,www.seudominio.com

# Banco PostgreSQL
DATABASE_URL=postgresql://formafit_user:senha_segura_aqui@localhost:5432/formafit_db

# APIs de Produção
CHATPRO_API_KEY=sua-chave-api-chatpro-producao
CHATPRO_API_URL=https://api.chatpro.com.br

# Email SMTP
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=seu-email@gmail.com
EMAIL_HOST_PASSWORD=sua-senha-app

# Configurações de Segurança
SECURE_SSL_REDIRECT=True
SECURE_BROWSER_XSS_FILTER=True
SECURE_CONTENT_TYPE_NOSNIFF=True
```

#### **5. Migrações e Arquivos Estáticos**
```bash
# Executar migrações
sudo -u www-data venv/bin/python manage.py migrate

# Coletar arquivos estáticos
sudo -u www-data venv/bin/python manage.py collectstatic --noinput

# Criar superusuário
sudo -u www-data venv/bin/python manage.py createsuperuser
```

#### **6. Configuração do Gunicorn**
Crie `/etc/systemd/system/formafit.service`:
```ini
[Unit]
Description=FormaFit Django App
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/FormaFit
Environment="PATH=/var/www/FormaFit/venv/bin"
ExecStart=/var/www/FormaFit/venv/bin/gunicorn --workers 3 --bind unix:/var/www/FormaFit/formafit.sock formafit.wsgi:application

[Install]
WantedBy=multi-user.target
```

```bash
# Habilitar e iniciar serviço
sudo systemctl daemon-reload
sudo systemctl start formafit
sudo systemctl enable formafit
```

#### **7. Configuração do Nginx**
Crie `/etc/nginx/sites-available/formafit`:
```nginx
server {
    listen 80;
    server_name seudominio.com www.seudominio.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /var/www/FormaFit;
    }
    
    location /media/ {
        root /var/www/FormaFit;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/FormaFit/formafit.sock;
    }
}
```

```bash
# Habilitar site
sudo ln -s /etc/nginx/sites-available/formafit /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

#### **8. SSL com Let's Encrypt (Opcional)**
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d seudominio.com -d www.seudominio.com
```

## 📁 Estrutura do Projeto
```
FormaFit/
├── 📁 accounts/                 # Autenticação e usuários
│   ├── migrations/
│   ├── models.py               # Modelo de usuário customizado
│   ├── views.py                # Views de auth e dashboard
│   ├── forms.py                # Formulários de registro/login
│   └── urls.py                 # URLs de autenticação
├── 📁 alunos/                  # Gestão de alunos
│   ├── migrations/
│   ├── models.py               # Modelo de aluno e medidas
│   ├── views.py                # CRUD de alunos
│   ├── forms.py                # Formulários de aluno
│   └── urls.py                 # URLs de alunos
├── 📁 treinos/                 # Sistema de treinos
│   ├── migrations/
│   ├── models.py               # Modelos de plano e exercício
│   ├── views.py                # Gestão de treinos
│   └── urls.py                 # URLs de treinos
├── 📁 frequencia/              # Controle de frequência
│   ├── migrations/
│   ├── models.py               # Modelo de agenda e presença
│   ├── views.py                # Controle de presença
│   └── urls.py                 # URLs de frequência
├── 📁 financeiro/              # Gestão financeira
│   ├── migrations/
│   ├── models.py               # Contratos, faturas, planos
│   ├── views.py                # Dashboard e gestão financeira
│   ├── forms.py                # Formulários financeiros
│   ├── services.py             # Serviços de negócio
│   └── urls.py                 # URLs financeiras
├── 📁 relatorios/              # Sistema de relatórios
│   ├── migrations/
│   ├── models.py               # Tipos e configurações de relatório
│   ├── views.py                # Geração e administração de relatórios
│   ├── forms.py                # Formulários administrativos
│   ├── services.py             # Serviços de geração PDF
│   └── management/commands/    # Comandos customizados
├── 📁 notificacoes/            # Sistema de notificações
│   ├── migrations/
│   ├── models.py               # Configurações, tipos e logs
│   ├── views.py                # Dashboard e gestão completa
│   ├── forms.py                # Formulários de notificação
│   ├── services.py             # Integração WhatsApp/Email
│   └── urls.py                 # URLs de notificações
├── 📁 scripts_exemplo/         # Scripts de configuração e teste
│   ├── README.md               # Documentação dos scripts
│   ├── criar_admin.py          # Criação de usuário administrador
│   ├── criar_planos_exemplo.py # Planos de mensalidade
│   ├── criar_exercicios_exemplo.py # Exercícios para treinos
│   ├── criar_alunos_exemplo.py # 5 alunos completos
│   ├── criar_dados_notificacoes.py # Sistema de notificações
│   ├── criar_notificacoes_exemplo.py # Notificações de teste
│   └── criar_tipos_relatorios.py # Tipos de relatórios
├── 📁 templates/               # Templates HTML
│   ├── base.html               # Template base
│   ├── 📁 accounts/            # Templates de autenticação
│   ├── 📁 alunos/              # Templates de alunos
│   ├── 📁 financeiro/          # Templates financeiros
│   ├── 📁 relatorios/          # Templates de relatórios
│   │   └── 📁 admin/           # Interface administrativa
│   └── ...
├── 📁 static/                  # Arquivos estáticos
├── 📁 media/                   # Uploads de usuário
├── 📁 formafit/                # Configurações Django
│   ├── settings.py             # Configurações principais
│   ├── urls.py                 # URLs principais
│   └── wsgi.py                 # WSGI para produção
├── 📄 manage.py                # Comando Django
├── 📄 requirements.txt         # Dependências Python
├── 📄 .env.example             # Exemplo de configuração
└── 📄 README.md                # Este arquivo
```

## 🎯 Módulos e Funcionalidades Detalhadas

### **🏋️‍♂️ Módulo de Alunos**
- **Cadastro Completo**: Dados pessoais, físicos, contato e objetivos
- **Medidas Corporais**: Histórico de peso, altura, % de gordura, etc.
- **Fotos de Progresso**: Upload e organização de fotos por data
- **Gestão de Status**: Controle de alunos ativos/inativos
- **Busca Avançada**: Filtros por nome, status, data de cadastro

### **💪 Módulo de Treinos**
- **Planos Personalizados**: Criação por dias da semana
- **Catálogo de Exercícios**: Organizados por grupo muscular
- **Especificações Técnicas**: Séries, repetições, carga, descanso
- **Cópia de Planos**: Reutilização e personalização
- **Histórico de Execução**: Acompanhamento de progresso

### **📊 Módulo de Frequência**
- **Registro de Presença**: Check-in/check-out com horários
- **Agendamento**: Sistema de reserva de horários
- **Relatórios de Frequência**: Análises mensais e semanais
- **Dashboard de Presença**: Visão geral em tempo real

### **💰 Módulo Financeiro (Completo)**
- **Dashboard Executivo**: Métricas financeiras em tempo real
- **Gestão de Contratos**: Criação e acompanhamento de contratos
- **Planos de Mensalidade**: Definição de valores e condições
- **Faturas Automáticas**: Geração automática baseada nos contratos
- **Controle de Pagamentos**: Registro e acompanhamento
- **Inadimplência**: Dashboard específico para controle de atrasos
- **Relatórios Financeiros**: Análises de receita e performance
- **Filtros Avançados**: Busca por múltiplos critérios

### **📈 Módulo de Relatórios (Completo)**
- **6 Tipos de Relatórios**: Progresso completo, medidas corporais, frequência, simples, fotográfico e executivo
- **Interface Administrativa**: Gestão completa de tipos de relatórios com controle de acesso staff
- **CRUD Administrativo**: Criar, editar, listar e excluir tipos de relatórios
- **Personalização Avançada**: Configuração de conteúdo, layout e estrutura
- **Gráficos de Evolução**: Visualização de medidas e peso com progressão temporal
- **Exportação Profissional**: PDF otimizado para impressão e apresentação
- **Relatórios de Frequência**: Análises detalhadas de presença e performance
- **Segurança**: Acesso restrito apenas para usuários staff

### **🔔 Módulo de Notificações (Completo)**
- **Dashboard Inteligente**: Métricas de notificações e ações rápidas
- **Notificações Manuais**: Criação e envio de mensagens personalizadas
- **Notificações Automáticas**: Sistema de triggers baseado em eventos
- **Configurações Avançadas**: Horários preferenciais e canais por aluno
- **Tipos Personalizáveis**: Categorização com cores, ícones e templates
- **WhatsApp Integration**: API ChatPro para envio automático de mensagens
- **Templates Dinâmicos**: Mensagens com variáveis personalizáveis
- **Logs Detalhados**: Histórico completo de envios com status e timestamps
- **Teste de Conectividade**: Validação e teste das configurações WhatsApp
- **Configuração Individual**: Preferências específicas por aluno
- **Triggers de Eventos**: Automação baseada em vencimentos e pagamentos

## 🔧 Comandos Úteis

### **Desenvolvimento**
```bash
# Executar servidor de desenvolvimento
python manage.py runserver

# Criar migrações
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Coletar arquivos estáticos
python manage.py collectstatic

# Shell interativo
python manage.py shell

# Executar setup completo do sistema (na ordem)
python scripts_exemplo/criar_admin.py               # Usuário administrador
python scripts_exemplo/criar_planos_exemplo.py      # 5 planos de mensalidade
python scripts_exemplo/criar_exercicios_exemplo.py  # 8 exercícios variados
python scripts_exemplo/criar_dados_notificacoes.py  # Sistema de notificações
python scripts_exemplo/criar_tipos_relatorios.py    # 6 tipos de relatórios
python scripts_exemplo/criar_alunos_exemplo.py      # 5 alunos completos
python scripts_exemplo/criar_notificacoes_exemplo.py # Notificações de teste
```

### **Manutenção**
```bash
# Backup do banco de dados
python manage.py dumpdata > backup.json

# Restaurar backup
python manage.py loaddata backup.json

# Limpar sessões expiradas
python manage.py clearsessions

# Verificar configurações
python manage.py check
```

## 🚀 Deploy e Monitoramento

### **Checklist de Deploy**
- [ ] Configurar variáveis de ambiente de produção
- [ ] Configurar banco PostgreSQL
- [ ] Executar migrações
- [ ] Coletar arquivos estáticos
- [ ] Configurar servidor web (Nginx)
- [ ] Configurar SSL/HTTPS
- [ ] Configurar backups automáticos
- [ ] Configurar monitoramento

### **Monitoramento**
```bash
# Status do serviço
sudo systemctl status formafit

# Logs do aplicação
sudo journalctl -u formafit -f

# Logs do Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Monitorar recursos
htop
df -h
```

## 📊 Performance e Otimizações

### **Otimizações Implementadas**
- ✅ **Queries Otimizadas**: select_related e prefetch_related
- ✅ **Paginação**: Listagens paginadas para performance
- ✅ **Índices de Banco**: Campos frequentemente consultados
- ✅ **Cache de Template**: Templates compilados
- ✅ **Compressão de Imagens**: Otimização automática
- ✅ **Lazy Loading**: Carregamento sob demanda

### **Métricas Recomendadas**
- Tempo de resposta < 200ms (páginas simples)
- Tempo de resposta < 500ms (páginas com gráficos)
- Uso de memória < 512MB por worker
- Tempo de query < 100ms (95% das queries)

## 🛡️ Segurança

### **Implementações de Segurança**
- ✅ **Autenticação Robusta**: Sistema de login seguro
- ✅ **Autorização**: Controle de acesso por usuário
- ✅ **CSRF Protection**: Proteção contra ataques CSRF
- ✅ **SQL Injection**: Prevenção via ORM Django
- ✅ **XSS Protection**: Sanitização de inputs
- ✅ **HTTPS**: Configuração de SSL/TLS
- ✅ **Headers de Segurança**: Configurações adequadas

### **Boas Práticas de Segurança**
- Use senhas fortes para banco de dados
- Mantenha SECRET_KEY segura e única
- Configure ALLOWED_HOSTS adequadamente
- Use HTTPS em produção
- Mantenha dependências atualizadas
- Configure backups regulares

## 🤝 Contribuindo

### **Como Contribuir**
1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

### **Padrões de Desenvolvimento**
- Siga PEP 8 para código Python
- Use nomes descritivos em português para models e views
- Documente funções e classes importantes
- Escreva testes para novas funcionalidades
- Mantenha templates responsivos

## 📄 Licença

Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 📞 Suporte e Contato

- **Documentação**: [Wiki do Projeto](https://github.com/g-paiva/#/wiki)
- **Issues**: [GitHub Issues](https://github.com/g-paiva/#/issues)
- **Discussões**: [GitHub Discussions](https://github.com/g-paiva/#/formafit/discussions)

## 🎉 Agradecimentos

- Comunidade Django pela excelente documentação
- Tailwind CSS pelo framework CSS intuitivo
- ChatPro pela API de WhatsApp
- Todos os personal trainers que contribuíram com feedback

---

**FormaFit** - Transformando a gestão de personal trainers através da tecnologia! 🏋️‍♂️💪

*Desenvolvido com ❤️ para a comunidade fitness*
