# 🚀 Guia de Deploy - Índice de Validação

## 📋 Pré-requisitos

### 1. Conta Google Cloud Platform
- Acesse [Google Cloud Console](https://console.cloud.google.com/)
- Crie um novo projeto ou use um existente
- Ative a Google Sheets API

### 2. Service Account
- No Google Cloud Console, vá para "IAM & Admin" > "Service Accounts"
- Crie uma nova Service Account
- Baixe o arquivo JSON de credenciais
- Compartilhe a planilha do Google Sheets com o email da Service Account

### 3. Google Sheets
- Crie uma nova planilha no Google Sheets
- Anote o ID da planilha (está na URL)
- Crie uma aba chamada "Validacoes"

## 🌐 Deploy no Streamlit Cloud

### 1. Preparar o Repositório
```bash
# Clone o repositório
git clone https://github.com/iht627123067-art/indice-validacao-streamlit.git
cd indice-validacao-streamlit

# Configure o ambiente local
./setup_env.sh  # Linux/Mac
# ou
setup_env.bat   # Windows
```

### 2. Configurar no Streamlit Cloud
1. Acesse [share.streamlit.io](https://share.streamlit.io/)
2. Faça login com sua conta GitHub
3. Clique em "New app"
4. Selecione o repositório: `iht627123067-art/indice-validacao-streamlit`
5. Configure:
   - **Main file path**: `streamlit_app.py`
   - **App URL**: escolha um nome único

### 3. Configurar Secrets
No painel do Streamlit Cloud, vá em "Settings" > "Secrets" e adicione:

```toml
[gcp_service_account]
type = "service_account"
project_id = "seu-projeto-id"
private_key_id = "sua-private-key-id"
private_key = "-----BEGIN PRIVATE KEY-----\nsua-chave-privada-aqui\n-----END PRIVATE KEY-----\n"
client_email = "sua-service-account@seu-projeto.iam.gserviceaccount.com"
client_id = "seu-client-id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/sua-service-account%40seu-projeto.iam.gserviceaccount.com"

[sheets]
spreadsheet_id = "seu-spreadsheet-id"
worksheet_name = "Validacoes"
```

### 4. Deploy
1. Clique em "Deploy!"
2. Aguarde o build completar
3. Acesse a URL da aplicação

## 🔧 Configuração Local

### 1. Ambiente Virtual
```bash
# Criar ambiente virtual
python3 -m venv venv

# Ativar (Linux/Mac)
source venv/bin/activate

# Ativar (Windows)
venv\Scripts\activate.bat
```

### 2. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 3. Configurar Credenciais
- Renomeie o arquivo de credenciais para `credentials.json`
- Coloque na pasta raiz do projeto

### 4. Executar Localmente
```bash
streamlit run streamlit_app.py
```

## 🔍 Troubleshooting

### Erro de Autenticação
- Verifique se o arquivo `credentials.json` está correto
- Confirme se a Service Account tem permissão na planilha
- Verifique se a Google Sheets API está ativada

### Erro de Dependências
- Atualize o pip: `pip install --upgrade pip`
- Reinstale as dependências: `pip install -r requirements.txt --force-reinstall`

### Erro no Streamlit Cloud
- Verifique os logs no painel do Streamlit Cloud
- Confirme se os secrets estão configurados corretamente
- Verifique se o arquivo principal está correto (`streamlit_app.py`)

## 📊 Monitoramento

### Logs do Streamlit Cloud
- Acesse o painel do Streamlit Cloud
- Vá em "Settings" > "Logs"
- Monitore erros e performance

### Google Sheets
- Verifique a aba "Validacoes" regularmente
- Monitore o volume de dados
- Faça backup dos dados importantes

## 🔄 Atualizações

### Deploy de Novas Versões
1. Faça commit das mudanças no GitHub
2. O Streamlit Cloud fará deploy automático
3. Monitore os logs para verificar se tudo está funcionando

### Rollback
- No Streamlit Cloud, vá em "Settings" > "Deploy"
- Selecione uma versão anterior
- Clique em "Redeploy"

## 📞 Suporte

Para problemas ou dúvidas:
1. Verifique a documentação no README.md
2. Consulte os logs do Streamlit Cloud
3. Abra uma issue no GitHub
4. Entre em contato com a equipe de desenvolvimento
