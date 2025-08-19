# 🔑 Resolvendo Problema de Permissão no GitHub

## ❌ **Problema Identificado:**
Você não tem permissão para fazer push diretamente para o repositório `iht627123067-art/indice-validacao-streamlit.git`

## ✅ **Soluções:**

### 🔄 **Opção 1: Fork do Repositório (Recomendado)**

1. **Acesse o repositório original:**
   - Vá para: https://github.com/iht627123067-art/indice-validacao-streamlit/

2. **Faça o Fork:**
   - Clique no botão **"Fork"** (canto superior direito)
   - Escolha sua conta GitHub
   - Aguarde a criação do fork

3. **Clone o seu fork:**
   ```bash
   # Remova a pasta atual
   cd ..
   rm -rf indice_validacao
   
   # Clone o seu fork
   git clone https://github.com/SEU_USUARIO/indice-validacao-streamlit.git
   cd indice-validacao-streamlit
   
   # Configure o ambiente
   ./setup_env.sh  # Linux/Mac
   # ou
   setup_env.bat   # Windows
   ```

4. **Faça as alterações e push:**
   ```bash
   git add .
   git commit -m "Configuração inicial do projeto"
   git push origin main
   ```

### 🆕 **Opção 2: Criar Novo Repositório**

1. **No GitHub:**
   - Vá para: https://github.com/new
   - Nome: `indice-validacao-streamlit`
   - Descrição: `Aplicação de validação do Índice de Inovação Pública do Chile`
   - Público ou Privado (sua escolha)
   - **NÃO** inicialize com README, .gitignore ou licença

2. **Configure o repositório remoto:**
   ```bash
   git remote add origin https://github.com/SEU_USUARIO/indice-validacao-streamlit.git
   git push -u origin main
   ```

### 🔐 **Opção 3: Solicitar Acesso (Se conhecer o dono)**

1. **Entre em contato com o usuário `iht627123067-art`**
2. **Solicite acesso de colaborador ao repositório**
3. **Aguarde a aprovação**

## 🚀 **Após Resolver o Problema:**

### 1. **Deploy no Streamlit Cloud:**
- Acesse: https://share.streamlit.io/
- Faça login com GitHub
- Clique em "New app"
- Selecione seu repositório
- Configure:
  - **Main file path**: `streamlit_app.py`
  - **App URL**: escolha um nome único

### 2. **Configurar Credenciais:**
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

## 📋 **Checklist de Resolução:**

- [ ] Escolher uma das opções acima
- [ ] Configurar o repositório remoto correto
- [ ] Fazer push dos arquivos
- [ ] Configurar no Streamlit Cloud
- [ ] Configurar credenciais do Google Sheets
- [ ] Testar a aplicação

## 🔗 **Links Úteis:**

- **GitHub**: https://github.com/
- **Streamlit Cloud**: https://share.streamlit.io/
- **Google Cloud Console**: https://console.cloud.google.com/

## 💡 **Recomendação:**

**Use a Opção 1 (Fork)** se quiser manter a conexão com o repositório original, ou **Opção 2 (Novo Repositório)** se preferir ter controle total sobre o projeto.

---

**🎯 Escolha uma opção e siga os passos para resolver o problema de permissão!**
