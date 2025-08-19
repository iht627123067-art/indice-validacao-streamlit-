@echo off
REM Script para configurar o ambiente de desenvolvimento no Windows
REM Índice de Validação - Streamlit

echo 🚀 Configurando ambiente de desenvolvimento...

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python não encontrado. Por favor, instale o Python 3.8+
    pause
    exit /b 1
)

REM Verificar versão do Python
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set python_version=%%i
echo ✅ Python %python_version% encontrado

REM Criar ambiente virtual
echo 📦 Criando ambiente virtual...
python -m venv venv

REM Ativar ambiente virtual
echo 🔧 Ativando ambiente virtual...
call venv\Scripts\activate.bat

REM Atualizar pip
echo ⬆️ Atualizando pip...
python -m pip install --upgrade pip

REM Instalar dependências
echo 📚 Instalando dependências...
pip install -r requirements.txt

REM Perguntar sobre dependências de desenvolvimento
set /p install_dev="🤔 Deseja instalar dependências de desenvolvimento? (y/n): "
if /i "%install_dev%"=="y" (
    echo 🔧 Instalando dependências de desenvolvimento...
    pip install pytest pytest-cov flake8 black isort
)

echo ✅ Ambiente configurado com sucesso!
echo.
echo 📋 Próximos passos:
echo 1. Ative o ambiente virtual: venv\Scripts\activate.bat
echo 2. Configure as credenciais do Google Sheets
echo 3. Execute a aplicação: streamlit run streamlit_app.py
echo.
echo 🔗 Para mais informações, consulte o README.md
pause
