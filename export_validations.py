"""
Script para exportar validações do Google Sheets para CSV.
Útil para análise posterior dos dados de validação.
"""

import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import os
from pathlib import Path

# Configurações do Google Sheets
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

def connect_to_sheets():
    """Conecta ao Google Sheets usando credenciais"""
    try:
        creds_file = Path("credentials.json")
        if not creds_file.exists():
            print("❌ Arquivo credentials.json não encontrado.")
            return None
        
        creds = Credentials.from_service_account_file(
            "credentials.json", 
            scopes=SCOPES
        )
        client = gspread.authorize(creds)
        return client
    except Exception as e:
        print(f"❌ Erro ao conectar ao Google Sheets: {e}")
        return None

def export_validations_to_csv():
    """Exporta validações do Google Sheets para CSV"""
    client = connect_to_sheets()
    if not client:
        return False
    
    try:
        # Abrir planilha
        sheet = client.open("Validações Índice Inovação")
        worksheet = sheet.worksheet("Validações")
        
        # Obter dados
        data = worksheet.get_all_records()
        df = pd.DataFrame(data)
        
        if df.empty:
            print("⚠️ Nenhuma validação encontrada na planilha.")
            return False
        
        # Criar nome do arquivo com timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"validacoes_export_{timestamp}.csv"
        
        # Salvar CSV
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        
        print(f"✅ Validações exportadas para: {filename}")
        print(f"📊 Total de registros: {len(df)}")
        
        # Estatísticas
        print("\n📈 Estatísticas:")
        print(f"- Aprovados: {len(df[df['status'] == 'Aprovar'])}")
        print(f"- Reprovados: {len(df[df['status'] == 'Reprovar'])}")
        print(f"- Sugestões: {len(df[df['status'] == 'Sugerir Redação'])}")
        print(f"- Novos Itens: {len(df[df['status'] == 'Incluir Novo Item'])}")
        
        # Usuários
        usuarios = df['usuario'].unique()
        print(f"\n👥 Avaliadores: {len(usuarios)}")
        for usuario in usuarios:
            count = len(df[df['usuario'] == usuario])
            print(f"  - {usuario}: {count} validações")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao exportar validações: {e}")
        return False

def export_by_user(username):
    """Exporta validações de um usuário específico"""
    client = connect_to_sheets()
    if not client:
        return False
    
    try:
        # Abrir planilha
        sheet = client.open("Validações Índice Inovação")
        worksheet = sheet.worksheet("Validações")
        
        # Obter dados
        data = worksheet.get_all_records()
        df = pd.DataFrame(data)
        
        if df.empty:
            print("⚠️ Nenhuma validação encontrada na planilha.")
            return False
        
        # Filtrar por usuário
        user_df = df[df['usuario'] == username]
        
        if user_df.empty:
            print(f"⚠️ Nenhuma validação encontrada para o usuário: {username}")
            return False
        
        # Criar nome do arquivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"validacoes_{username}_{timestamp}.csv"
        
        # Salvar CSV
        user_df.to_csv(filename, index=False, encoding='utf-8-sig')
        
        print(f"✅ Validações de {username} exportadas para: {filename}")
        print(f"📊 Total de registros: {len(user_df)}")
        
        # Estatísticas do usuário
        print(f"\n📈 Estatísticas de {username}:")
        print(f"- Aprovados: {len(user_df[user_df['status'] == 'Aprovar'])}")
        print(f"- Reprovados: {len(user_df[user_df['status'] == 'Reprovar'])}")
        print(f"- Sugestões: {len(user_df[user_df['status'] == 'Sugerir Redação'])}")
        print(f"- Novos Itens: {len(user_df[user_df['status'] == 'Incluir Novo Item'])}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao exportar validações do usuário: {e}")
        return False

def export_summary():
    """Exporta um resumo das validações"""
    client = connect_to_sheets()
    if not client:
        return False
    
    try:
        # Abrir planilha
        sheet = client.open("Validações Índice Inovação")
        worksheet = sheet.worksheet("Validações")
        
        # Obter dados
        data = worksheet.get_all_records()
        df = pd.DataFrame(data)
        
        if df.empty:
            print("⚠️ Nenhuma validação encontrada na planilha.")
            return False
        
        # Criar resumo
        summary_data = []
        
        # Por usuário
        for usuario in df['usuario'].unique():
            user_df = df[df['usuario'] == usuario]
            summary_data.append({
                'usuario': usuario,
                'total_validacoes': len(user_df),
                'aprovados': len(user_df[user_df['status'] == 'Aprovar']),
                'reprovados': len(user_df[user_df['status'] == 'Reprovar']),
                'sugestoes': len(user_df[user_df['status'] == 'Sugerir Redacao']),
                'novos_itens': len(user_df[user_df['status'] == 'Incluir Novo Item']),
                'primeira_validacao': user_df['timestamp'].min(),
                'ultima_validacao': user_df['timestamp'].max()
            })
        
        # Por dimensão
        for dimensao in df['dimensao_padrao'].unique():
            dim_df = df[df['dimensao_padrao'] == dimensao]
            summary_data.append({
                'categoria': 'dimensao',
                'nome': dimensao,
                'total_validacoes': len(dim_df),
                'aprovados': len(dim_df[dim_df['status'] == 'Aprovar']),
                'reprovados': len(dim_df[dim_df['status'] == 'Reprovar']),
                'sugestoes': len(dim_df[dim_df['status'] == 'Sugerir Redacao']),
                'novos_itens': len(dim_df[dim_df['status'] == 'Incluir Novo Item'])
            })
        
        # Criar DataFrame de resumo
        summary_df = pd.DataFrame(summary_data)
        
        # Salvar resumo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"resumo_validacoes_{timestamp}.csv"
        summary_df.to_csv(filename, index=False, encoding='utf-8-sig')
        
        print(f"✅ Resumo exportado para: {filename}")
        print(f"📊 Total de registros no resumo: {len(summary_df)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao exportar resumo: {e}")
        return False

def main():
    """Função principal"""
    print("📊 EXPORTADOR DE VALIDAÇÕES")
    print("="*40)
    
    print("\nEscolha uma opção:")
    print("1. Exportar todas as validações")
    print("2. Exportar validações de um usuário específico")
    print("3. Exportar resumo das validações")
    print("4. Sair")
    
    opcao = input("\nDigite sua opção (1-4): ").strip()
    
    if opcao == "1":
        export_validations_to_csv()
    elif opcao == "2":
        username = input("Digite o nome do usuário: ").strip()
        if username:
            export_by_user(username)
        else:
            print("❌ Nome de usuário não informado.")
    elif opcao == "3":
        export_summary()
    elif opcao == "4":
        print("👋 Até logo!")
    else:
        print("❌ Opção inválida.")

if __name__ == "__main__":
    main()
