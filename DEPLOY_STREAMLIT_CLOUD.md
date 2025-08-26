# 🚀 Deploy no Streamlit Cloud - Guia Completo

## 📋 Pré-requisitos

1. ✅ Conta GitHub ativa
2. ✅ Fork do repositório [indice-validacao-streamlit](https://github.com/iht627123067-art/indice-validacao-streamlit)
3. ✅ Conta Streamlit Cloud (gratuita)

## 🔄 Passo 1: Fork do Repositório

1. Acesse: [https://github.com/iht627123067-art/indice-validacao-streamlit](https://github.com/iht627123067-art/indice-validacao-streamlit)
2. Clique no botão **"Fork"** no canto superior direito
3. Escolha sua conta GitHub
4. Aguarde a criação do fork


    echo "# indice-validacao-streamlit-" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/iht627123067-art/indice-validacao-streamlit-.git
git push -u origin main

## 🌐 Passo 2: Deploy no Streamlit Cloud

1. Acesse: [https://share.streamlit.io/](https://share.streamlit.io/)
2. Faça login com sua conta GitHub
3. Clique em **"New app"**
4. Configure a aplicação:

### Configurações Básicas
- **Repository**: `seu-usuario/indice-validacao-streamlit`
- **Branch**: `main`
- **Main file path**: `streamlit_app.py`

### Configurações Avançadas (Opcional)
- **App URL**: Deixe em branco para URL automática
- **Advanced settings**: Clique para expandir

## ⚙️ Passo 3: Configurar Secrets (Google Sheets)

Se quiser usar a versão com Google Sheets:

1. No painel do Streamlit Cloud, vá em **"Settings"** → **"Secrets"**
2. Cole o conteúdo do arquivo `.streamlit/secrets.toml`
3. Substitua os valores placeholder pelos seus dados reais:

```toml
[gcp_service_account]
type = "service_account"
project_id = "SEU_PROJECT_ID"
private_key_id = "SUA_PRIVATE_KEY_ID"
private_key = "-----BEGIN PRIVATE KEY-----\nSUA_CHAVE_PRIVADA\n-----END PRIVATE KEY-----\n"
client_email = "sua-service-account@seu-projeto.iam.gserviceaccount.com"
client_id = "SEU_CLIENT_ID"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/sua-service-account%40seu-projeto.iam.gserviceaccount.com"

google_sheets_id = "ID_DA_SUA_PLANILHA"
```

## 🔧 Passo 4: Configurar Google Cloud (Opcional)

Para usar Google Sheets:

1. Acesse [Google Cloud Console](https://console.cloud.google.com/)
2. Crie um novo projeto ou selecione existente
3. Ative a **Google Sheets API**
4. Crie uma **Service Account**
5. Baixe o arquivo JSON de credenciais
6. Configure as credenciais no Streamlit Cloud

## 📱 Passo 5: Testar a Aplicação

1. Clique em **"Deploy!"**
2. Aguarde o build (pode levar alguns minutos)
3. Acesse a URL fornecida
4. Teste a funcionalidade básica

## 🆘 Solução de Problemas

### Erro de Build
- Verifique se o arquivo `requirements.txt` está correto
- Confirme se o arquivo principal existe (`streamlit_app.py`)
- Verifique se não há erros de sintaxe

### Erro de Dependências
- O Streamlit Cloud instala automaticamente as dependências do `requirements.txt`
- Se houver problemas, verifique a compatibilidade das versões

### Erro de Secrets
- Verifique se o arquivo `.streamlit/secrets.toml` está correto
- Confirme se as credenciais do Google Cloud estão válidas

## 🔄 Atualizações

Para atualizar sua aplicação:

1. Faça push das mudanças para seu fork
2. O Streamlit Cloud detecta automaticamente as mudanças
3. A aplicação é redeployada automaticamente

## 📊 Monitoramento

- **Logs**: Acesse "Settings" → "Logs" para ver logs em tempo real
- **Status**: Monitore o status da aplicação no dashboard
- **Uso**: Acompanhe o uso de recursos (gratuito até 1GB RAM)

## 🎯 Próximos Passos

1. ✅ Fork do repositório
2. ✅ Deploy no Streamlit Cloud
3. ✅ Configurar secrets (se necessário)
4. ✅ Testar a aplicação
5. 🚀 Compartilhar a URL com sua equipe!

## 📞 Suporte

- **Streamlit Cloud**: [Documentação oficial](https://docs.streamlit.io/streamlit-community-cloud)
- **GitHub**: [Issues do repositório](https://github.com/iht627123067-art/indice-validacao-streamlit/issues)
- **Google Cloud**: [Documentação da API](https://developers.google.com/sheets/api)
