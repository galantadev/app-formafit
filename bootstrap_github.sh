#!/usr/bin/env bash
set -euo pipefail

# ============================================================
#  Bootstrap Git + GitHub (primeiro push)
#  - Cria .gitignore e README se não existirem
#  - Inicializa Git e primeiro commit
#  - Cria repo no GitHub (via gh CLI ou via cURL com token)
#  - Seta origin e faz push
# ============================================================

# ---------- helpers ----------
has_cmd() { command -v "$1" >/dev/null 2>&1; }

color() { # usage: color "<code>" "text"
  printf "\033[%sm%s\033[0m" "$1" "$2"
}

hr() { printf "%s\n" "------------------------------------------------------------"; }

prompt() {
  local var="$1" msg="$2" def="${3-}"
  local ans
  if [[ -n "$def" ]]; then
    read -rp "$(color 1 "$msg") [$(color 2 "$def")]: " ans || true
    ans="${ans:-$def}"
  else
    read -rp "$(color 1 "$msg"): " ans || true
  fi
  printf "%s" "$ans"
}

prompt_secret() {
  local var="$1" msg="$2"
  local ans
  read -rs -p "$(color 1 "$msg"): " ans || true
  echo
  printf "%s" "$ans"
}

# ---------- pré-checagens ----------
if ! has_cmd git; then
  echo "❌ Git não encontrado. Instale primeiro: sudo apt-get install -y git"
  exit 1
fi

# ---------- pasta do projeto ----------
PROJECT_DIR="$(pwd)"
PROJECT_NAME_DEFAULT="$(basename "$PROJECT_DIR")"
echo "📂 Projeto: $(color 2 "$PROJECT_DIR")"

# ---------- git init / config ----------
if [[ ! -d .git ]]; then
  echo "🔧 Inicializando repositório Git..."
  git init
fi

# user.name / user.email locais (se não configurados)
if ! git config user.name >/dev/null; then
  GIT_USER_NAME="$(prompt GIT_USER_NAME "Seu nome para commits (git user.name)")"
  git config user.name "$GIT_USER_NAME"
fi

if ! git config user.email >/dev/null; then
  GIT_USER_EMAIL="$(prompt GIT_USER_EMAIL "Seu email para commits (git user.email)")"
  git config user.email "$GIT_USER_EMAIL"
fi

# ---------- .gitignore ----------
if [[ ! -f .gitignore ]]; then
  echo "📝 Criando .gitignore..."
  cat > .gitignore <<'EOF'
# Python
__pycache__/
*.py[cod]
*.pyo
*.pyd
.Python
env/
venv/
ENV/
*.sqlite3

# Django
*.log
*.pot
*.pyc
*.mo
*.db
*.bak
media/

# IDE/Editor
.vscode/
.idea/

# Sistema
.DS_Store
Thumbs.db
EOF
fi

# ---------- README.md ----------
if [[ ! -f README.md ]]; then
  echo "📝 Criando README.md..."
  REPO_TITLE="$(prompt REPO_TITLE "Nome do projeto para o README" "$PROJECT_NAME_DEFAULT")"
  cat > README.md <<EOF
# $REPO_TITLE

Projeto Django do FormaFit.

## Como rodar

\`\`\`bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env  # ajuste as variáveis
python manage.py migrate
python manage.py runserver
\`\`\`
EOF
fi

# ---------- branch main ----------
git checkout -B main >/dev/null 2>&1 || git branch -M main

# ---------- add + primeiro commit (se necessário) ----------
NEEDS_COMMIT=0
if ! git rev-parse --verify HEAD >/dev/null 2>&1; then
  NEEDS_COMMIT=1
else
  # há HEAD, mas pode ter mudanças não commitadas
  if [[ -n "$(git status --porcelain)" ]]; then
    NEEDS_COMMIT=1
  fi
fi

if [[ $NEEDS_COMMIT -eq 1 ]]; then
  echo "➕ Adicionando arquivos e criando commit..."
  git add .
  git commit -m "chore: primeiro commit do projeto"
else
  echo "✅ Nenhuma alteração pendente para commit."
fi

# ---------- criar repo no GitHub ----------
REMOTE_EXISTS=0
if git remote get-url origin >/dev/null 2>&1; then
  REMOTE_EXISTS=1
fi

if [[ $REMOTE_EXISTS -eq 0 ]]; then
  echo
  hr
  echo "🌐 Vamos criar/conectar o repositório no GitHub."
  USE_GH="n"
  if has_cmd gh; then
    USE_GH="$(prompt USE_GH "Usar GitHub CLI 'gh' para criar o repo? (s/n)" "s")"
  fi

  if [[ "$USE_GH" == "s" || "$USE_GH" == "S" ]]; then
    # via gh
    GH_VISIBILITY="$(prompt GH_VISIBILITY "Visibilidade no GitHub (public/private)" "private")"
    GH_VIS_FLAG="--private"
    [[ "$GH_VISIBILITY" == "public" ]] && GH_VIS_FLAG="--public"

    # Nome do repositório
    REPO_NAME="$(prompt REPO_NAME "Nome do repositório no GitHub" "$PROJECT_NAME_DEFAULT")"

    echo "🚀 Criando repositório com gh..."
    gh repo create "$REPO_NAME" --source="." --push $GH_VIS_FLAG
  else
    # via cURL + token
    echo
    echo "🔐 Será usado cURL + Token Pessoal do GitHub."
    echo "   Crie/tenha um token com escopo: repo"
    echo "   Link: https://github.com/settings/tokens (ou use um Fine-Grained com permissões equivalentes)."
    echo

    GH_USER="$(prompt GH_USER "Seu usuário no GitHub (ex: stakonikov)")"
    REPO_NAME="$(prompt REPO_NAME "Nome do repositório no GitHub" "$PROJECT_NAME_DEFAULT")"
    GH_VISIBILITY="$(prompt GH_VISIBILITY "Visibilidade (public/private)" "private")"
    GH_PRIVATE=true
    [[ "$GH_VISIBILITY" == "public" ]] && GH_PRIVATE=false

    GH_TOKEN="$(prompt_secret GH_TOKEN "Cole seu GitHub Personal Access Token (repo)")"

    echo "🌐 Criando repositório via API..."
    CREATE_RES="$(curl -sS -X POST https://api.github.com/user/repos \
      -H "Authorization: token ${GH_TOKEN}" \
      -H "Accept: application/vnd.github+json" \
      -d "{\"name\":\"${REPO_NAME}\", \"private\": ${GH_PRIVATE}}" )" || {
        echo "❌ Falha ao chamar a API do GitHub."
        exit 1
      }

    if echo "$CREATE_RES" | grep -q '"full_name"'; then
      echo "✅ Repositório criado: $(echo "$CREATE_RES" | grep -oE '"full_name":\s*"[^"]+"' | head -1 | cut -d '"' -f4)"
    else
      echo "⚠️ Resposta da API:"
      echo "$CREATE_RES"
      echo "❌ Não foi possível criar o repositório. Verifique o token/permissões e tente novamente."
      exit 1
    fi

    ORIGIN_URL="https://github.com/${GH_USER}/${REPO_NAME}.git"
    echo "🔗 Definindo remoto origin: $ORIGIN_URL"
    git remote add origin "$ORIGIN_URL"
    echo "⬆️ Enviando para o GitHub (main)..."
    git push -u origin main
  fi
else
  echo "🔗 Remoto 'origin' já existe: $(git remote get-url origin)"
  echo "⬆️ Dando push para 'origin main'..."
  git push -u origin main
fi

echo
hr
echo "🎉 Tudo pronto!"
echo "Repo local:  $(color 2 "$PROJECT_DIR")"
if git remote get-url origin >/dev/null 2>&1; then
  echo "Remoto:      $(color 2 "$(git remote get-url origin)")"
fi
echo "Branch:      $(color 2 "$(git rev-parse --abbrev-ref HEAD)")"
hr
    