"""
Script para configurar o Google Sheets para a aplicação de validação.
Execute este script uma vez para configurar as credenciais e permissões.
"""

import os
import json
from pathlib import Path

def create_credentials_template():
    """Cria um template para o arquivo de credenciais"""
    
    template = {
        "type": "service_account",
        "project_id": "seu-projeto-id",
        "private_key_id": "sua-private-key-id",
        "private_key": "-----BEGIN PRIVATE KEY-----\nSUA_PRIVATE_KEY_AQUI\n-----END PRIVATE KEY-----\n",
        "client_email": "seu-service-account@seu-projeto.iam.gserviceaccount.com",
        "client_id": "seu-client-id",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/seu-service-account%40seu-projeto.iam.gserviceaccount.com"
    }
    
    with open("credentials_template.json", "w") as f:
        json.dump(template, f, indent=2)
    
    print("✅ Template de credenciais criado: credentials_template.json")
    print("📝 Edite este arquivo com suas credenciais reais e renomeie para credentials.json")

def print_setup_instructions():
    """Imprime instruções de configuração"""
    
    print("\n" + "="*60)
    print("🔧 CONFIGURAÇÃO DO GOOGLE SHEETS")
    print("="*60)
    
    print("\n📋 PASSO A PASSO:")
    print("1. Acesse: https://console.cloud.google.com/")
    print("2. Crie um novo projeto ou selecione um existente")
    print("3. Ative a Google Sheets API:")
    print("   - Vá para 'APIs & Services' > 'Library'")
    print("   - Procure por 'Google Sheets API' e ative")
    print("4. Crie uma Service Account:")
    print("   - Vá para 'APIs & Services' > 'Credentials'")
    print("   - Clique em 'Create Credentials' > 'Service Account'")
    print("   - Preencha os dados e clique em 'Create'")
    print("5. Baixe as credenciais:")
    print("   - Clique na Service Account criada")
    print("   - Vá para a aba 'Keys'")
    print("   - Clique em 'Add Key' > 'Create new key'")
    print("   - Selecione 'JSON' e baixe o arquivo")
    print("6. Renomeie o arquivo baixado para 'credentials.json'")
    print("7. Mova o arquivo para a pasta Streamlit/")
    
    print("\n🔐 PERMISSÕES NECESSÁRIAS:")
    print("- https://www.googleapis.com/auth/spreadsheets")
    print("- https://www.googleapis.com/auth/drive")
    
    print("\n📁 ESTRUTURA DE ARQUIVOS:")
    print("Streamlit/")
    print("├── app.py")
    print("├── requirements.txt")
    print("├── credentials.json  ← Coloque aqui")
    print("└── README.md")
    
    print("\n🚀 PARA EXECUTAR:")
    print("cd Streamlit")
    print("pip install -r requirements.txt")
    print("streamlit run app.py")

def create_readme():
    """Cria um README com instruções"""
    
    readme_content = """# 📊 Aplicação de Validação - Índice de Inovação Pública

## 🎯 Objetivo
Aplicação web interativa para validação de itens da planilha do Índice de Inovação Pública do Chile.

## 🚀 Funcionalidades

### ✅ Validação por Linha
- Avaliar cada linha da planilha (aprovar, reprovar, sugerir redação, incluir novo item)
- Controle de avaliações para impedir duplicatas

### 📋 Apresentação Hierárquica
- Mostrar Categoria, Subcategoria, Questão, Subquestão
- Visualização clara da estrutura dos dados

### 🔍 Filtros e Busca
- Filtrar por categoria/subcategoria/questão
- Busca por texto nos itens
- Estatísticas em tempo real

### 📊 Controle de Avaliações
- Impedir avaliações duplicadas/conflitantes por usuário
- Progresso visual do trabalho
- Resumo das validações realizadas

## 🛠️ Tecnologias

- **Front-end**: Streamlit (interface amigável e responsiva)
- **Back-end/SGBD**: Google Sheets (armazenamento em nuvem)
- **Hospedagem**: Streamlit Cloud (gratuito)

## 📋 Pré-requisitos

1. Python 3.8+
2. Conta Google Cloud Platform
3. Google Sheets API ativada
4. Service Account configurada

## 🔧 Instalação

### 1. Configurar Google Sheets
```bash
python setup_google_sheets.py
```

### 2. Instalar dependências
```bash
cd Streamlit
pip install -r requirements.txt
```

### 3. Configurar credenciais
- Baixe o arquivo de credenciais do Google Cloud Console
- Renomeie para `credentials.json`
- Coloque na pasta `Streamlit/`

### 4. Executar aplicação
```bash
streamlit run app.py
```

## 📊 Estrutura dos Dados

A aplicação utiliza o arquivo `chile_iip_2025_preparado.csv` que contém:

- **sistema**: Identificador do sistema (chile)
- **ano**: Ano de referência (2025)
- **dimensao_padrao**: Dimensão padronizada
- **subdimensao**: Subdimensão
- **questao**: Questão específica
- **elemento**: Elemento da questão
- **nivel**: Nível hierárquico (1-4)
- **tipo_elemento**: Tipo do elemento
- **texto_completo**: Texto completo do item

## 🎯 Como Usar

1. **Identificação**: Digite seu nome na barra lateral
2. **Filtros**: Use os filtros para navegar pelos itens
3. **Avaliação**: Para cada item:
   - Leia as informações do item
   - Selecione o status (Aprovar/Reprovar/Sugerir/Novo Item)
   - Adicione comentários se necessário
   - Clique em "Salvar Avaliação"
4. **Progresso**: Acompanhe seu progresso na barra inferior

## 📈 Resultados

As validações são salvas automaticamente no Google Sheets com:
- Timestamp da avaliação
- Identificação do avaliador
- Dados completos do item
- Status da validação
- Comentários e sugestões
- Novos itens propostos

## 🔒 Segurança

- Cada usuário só pode ver suas próprias validações
- Dados armazenados de forma segura no Google Sheets
- Controle de acesso via Service Account

## 🆘 Suporte

Para problemas ou dúvidas:
1. Verifique se as credenciais estão configuradas corretamente
2. Confirme se o arquivo CSV existe no caminho correto
3. Verifique se a Google Sheets API está ativada

## 📝 Licença

Este projeto é de uso interno para validação do Índice de Inovação Pública.
"""
    
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print("✅ README.md criado com instruções completas")

if __name__ == "__main__":
    print("🔧 CONFIGURADOR DO GOOGLE SHEETS")
    print("="*40)
    
    # Criar template de credenciais
    create_credentials_template()
    
    # Criar README
    create_readme()
    
    # Imprimir instruções
    print_setup_instructions()
    
    print("\n✅ Configuração inicial concluída!")
    print("📝 Siga as instruções acima para completar a configuração.")
