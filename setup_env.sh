#!/bin/bash

# Script para configurar o ambiente de desenvolvimento
# Índice de Validação - Streamlit

echo "🚀 Configurando ambiente de desenvolvimento..."

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado. Por favor, instale o Python 3.8+"
    exit 1
fi

# Verificar versão do Python
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✅ Python $python_version encontrado"

# Criar ambiente virtual
echo "📦 Criando ambiente virtual..."
python3 -m venv venv

# Ativar ambiente virtual
echo "🔧 Ativando ambiente virtual..."
source venv/bin/activate

# Atualizar pip
echo "⬆️ Atualizando pip..."
pip install --upgrade pip

# Instalar dependências
echo "📚 Instalando dependências..."
pip install -r requirements.txt

# Instalar dependências de desenvolvimento (opcional)
read -p "🤔 Deseja instalar dependências de desenvolvimento? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🔧 Instalando dependências de desenvolvimento..."
    pip install pytest pytest-cov flake8 black isort
fi

echo "✅ Ambiente configurado com sucesso!"
echo ""
echo "📋 Próximos passos:"
echo "1. Ative o ambiente virtual: source venv/bin/activate"
echo "2. Configure as credenciais do Google Sheets"
echo "3. Execute a aplicação: streamlit run streamlit_app.py"
echo ""
echo "🔗 Para mais informações, consulte o README.md"
