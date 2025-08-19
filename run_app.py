#!/usr/bin/env python3
"""
Script principal para executar a aplicação de validação.
Este script facilita o uso da aplicação, oferecendo opções de execução.
"""

import subprocess
import sys
import os
from pathlib import Path

def print_banner():
    """Imprime o banner da aplicação"""
    print("="*60)
    print("📊 APLICAÇÃO DE VALIDAÇÃO - ÍNDICE DE INOVAÇÃO PÚBLICA")
    print("="*60)
    print("🎯 Sistema de validação interativa para itens da planilha")
    print("🚀 Desenvolvido com Streamlit e Google Sheets")
    print("="*60)

def check_environment():
    """Verifica o ambiente de execução"""
    print("🔍 Verificando ambiente...")
    
    # Verificar se está na pasta correta
    if not Path("app.py").exists():
        print("❌ Execute este script dentro da pasta Streamlit/")
        return False
    
    # Verificar se o arquivo CSV existe
    csv_path = Path("../raw_news/dados_preparados/chile_iip_2025_preparado.csv")
    if not csv_path.exists():
        print(f"❌ Arquivo CSV não encontrado: {csv_path}")
        print("Verifique se o arquivo existe no caminho correto.")
        return False
    
    print("✅ Ambiente verificado!")
    return True

def show_menu():
    """Mostra o menu de opções"""
    print("\n📋 OPÇÕES DISPONÍVEIS:")
    print("1. 🚀 Executar aplicação completa (Google Sheets)")
    print("2. 🧪 Executar aplicação local (arquivos JSON)")
    print("3. 🔧 Configurar Google Sheets")
    print("4. 📊 Exportar validações")
    print("5. 🧪 Testar aplicação")
    print("6. 📖 Ver documentação")
    print("7. ❌ Sair")
    
    return input("\nEscolha uma opção (1-7): ").strip()

def run_complete_app():
    """Executa a aplicação completa com Google Sheets"""
    print("\n🚀 Iniciando aplicação completa...")
    print("📱 A aplicação será aberta em: http://localhost:8501")
    print("⏹️  Pressione Ctrl+C para parar")
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", "8501"
        ])
    except KeyboardInterrupt:
        print("\n👋 Aplicação encerrada.")

def run_local_app():
    """Executa a aplicação local com arquivos JSON"""
    print("\n🧪 Iniciando aplicação local...")
    print("📱 A aplicação será aberta em: http://localhost:8501")
    print("💾 Validações serão salvas em arquivos JSON locais")
    print("⏹️  Pressione Ctrl+C para parar")
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
            "--server.port", "8501"
        ])
    except KeyboardInterrupt:
        print("\n👋 Aplicação encerrada.")

def setup_google_sheets():
    """Configura o Google Sheets"""
    print("\n🔧 Configurando Google Sheets...")
    
    try:
        subprocess.run([sys.executable, "setup_google_sheets.py"])
    except Exception as e:
        print(f"❌ Erro ao configurar: {e}")

def export_validations():
    """Exporta validações"""
    print("\n📊 Exportando validações...")
    
    try:
        subprocess.run([sys.executable, "export_validations.py"])
    except Exception as e:
        print(f"❌ Erro ao exportar: {e}")

def test_app():
    """Testa a aplicação"""
    print("\n🧪 Testando aplicação...")
    
    try:
        subprocess.run([sys.executable, "test_app.py"])
    except Exception as e:
        print(f"❌ Erro ao testar: {e}")

def show_documentation():
    """Mostra a documentação"""
    print("\n📖 DOCUMENTAÇÃO:")
    print("="*40)
    
    # Ler e mostrar README
    if Path("README.md").exists():
        with open("README.md", "r", encoding="utf-8") as f:
            content = f.read()
            print(content)
    else:
        print("❌ Arquivo README.md não encontrado.")
    
    # Mostrar troubleshooting
    if Path("TROUBLESHOOTING.md").exists():
        print("\n" + "="*40)
        print("🔧 SOLUÇÃO DE PROBLEMAS:")
        print("="*40)
        with open("TROUBLESHOOTING.md", "r", encoding="utf-8") as f:
            content = f.read()
            print(content)

def main():
    """Função principal"""
    print_banner()
    
    # Verificar ambiente
    if not check_environment():
        return
    
    while True:
        try:
            opcao = show_menu()
            
            if opcao == "1":
                run_complete_app()
            elif opcao == "2":
                run_local_app()
            elif opcao == "3":
                setup_google_sheets()
            elif opcao == "4":
                export_validations()
            elif opcao == "5":
                test_app()
            elif opcao == "6":
                show_documentation()
            elif opcao == "7":
                print("\n👋 Até logo!")
                break
            else:
                print("❌ Opção inválida. Tente novamente.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Aplicação encerrada pelo usuário.")
            break
        except Exception as e:
            print(f"\n❌ Erro inesperado: {e}")
            print("Tente novamente ou escolha a opção 6 para ver a documentação.")

if __name__ == "__main__":
    main()
