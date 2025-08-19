"""
Script para testar a aplicação Streamlit localmente.
Execute este script para verificar se tudo está funcionando corretamente.
"""

import subprocess
import sys
import os
from pathlib import Path

def check_dependencies():
    """Verifica se as dependências estão instaladas"""
    print("🔍 Verificando dependências...")
    
    required_packages = [
        'streamlit',
        'pandas',
        'pathlib'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package}")
    
    if missing_packages:
        print(f"\n⚠️ Pacotes faltando: {', '.join(missing_packages)}")
        print("Execute: pip install -r requirements.txt")
        return False
    
    print("✅ Todas as dependências estão instaladas!")
    return True

def check_data_file():
    """Verifica se o arquivo de dados existe"""
    print("\n📁 Verificando arquivo de dados...")
    
    csv_path = Path("../raw_news/dados_preparados/chile_iip_2025_preparado.csv")
    
    if csv_path.exists():
        print(f"✅ Arquivo encontrado: {csv_path}")
        
        # Verificar tamanho do arquivo
        size_mb = csv_path.stat().st_size / (1024 * 1024)
        print(f"📊 Tamanho: {size_mb:.2f} MB")
        
        return True
    else:
        print(f"❌ Arquivo não encontrado: {csv_path}")
        print("Verifique se o arquivo CSV existe no caminho correto.")
        return False

def check_structure():
    """Verifica a estrutura de arquivos"""
    print("\n📂 Verificando estrutura de arquivos...")
    
    required_files = [
        "app.py",
        "streamlit_app.py", 
        "requirements.txt",
        "setup_google_sheets.py",
        "export_validations.py",
        "README.md"
    ]
    
    missing_files = []
    
    for file in required_files:
        if Path(file).exists():
            print(f"✅ {file}")
        else:
            missing_files.append(file)
            print(f"❌ {file}")
    
    if missing_files:
        print(f"\n⚠️ Arquivos faltando: {', '.join(missing_files)}")
        return False
    
    print("✅ Todos os arquivos estão presentes!")
    return True

def run_streamlit():
    """Executa a aplicação Streamlit"""
    print("\n🚀 Iniciando aplicação Streamlit...")
    print("📱 A aplicação será aberta em: http://localhost:8501")
    print("⏹️  Pressione Ctrl+C para parar")
    
    try:
        # Executar streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
            "--server.port", "8501",
            "--server.headless", "false"
        ])
    except KeyboardInterrupt:
        print("\n👋 Aplicação encerrada pelo usuário.")
    except Exception as e:
        print(f"❌ Erro ao executar Streamlit: {e}")

def main():
    """Função principal"""
    print("🧪 TESTADOR DA APLICAÇÃO STREAMLIT")
    print("="*50)
    
    # Verificar dependências
    if not check_dependencies():
        return
    
    # Verificar estrutura
    if not check_structure():
        return
    
    # Verificar arquivo de dados
    if not check_data_file():
        return
    
    print("\n✅ Todas as verificações passaram!")
    print("🎯 A aplicação está pronta para ser executada.")
    
    # Perguntar se quer executar
    response = input("\n🚀 Deseja executar a aplicação agora? (s/n): ").strip().lower()
    
    if response in ['s', 'sim', 'y', 'yes']:
        run_streamlit()
    else:
        print("👋 Para executar manualmente, use: streamlit run streamlit_app.py")

if __name__ == "__main__":
    main()


