# 🚀 Deploy no Streamlit Cloud

## Pré-requisitos

1. **Conta no GitHub**: Crie uma conta em [github.com](https://github.com)
2. **Conta no Streamlit Cloud**: Acesse [share.streamlit.io](https://share.streamlit.io)

## Passos para Deploy

### 1. Criar Repositório no GitHub

1. Acesse [github.com](https://github.com)
2. Clique em "New repository"
3. Nome: `indice-validacao-streamlit`
4. Descrição: `Aplicação Streamlit para validação de itens do índice de inovação`
5. Deixe público (Public)
6. **NÃO** inicialize com README, .gitignore ou license
7. Clique em "Create repository"

### 2. Conectar Repositório Local ao GitHub

```bash
# No terminal, dentro da pasta Streamlit
git remote add origin https://github.com/SEU_USUARIO/indice-validacao-streamlit.git
git branch -M main
git push -u origin main
```

### 3. Deploy no Streamlit Cloud

1. Acesse [share.streamlit.io](https://share.streamlit.io)
2. Faça login com sua conta GitHub
3. Clique em "New app"
4. Configure:
   - **Repository**: `SEU_USUARIO/indice-validacao-streamlit`
   - **Branch**: `main`
   - **Main file path**: `streamlit_app.py`
5. Clique em "Deploy!"

## Estrutura do Projeto

```
Streamlit/
├── streamlit_app.py          # Aplicação principal
├── requirements.txt          # Dependências Python
├── packages.txt             # Dependências do sistema
├── .streamlit/
│   └── config.toml         # Configuração do Streamlit
├── data/
│   └── chile_iip_2025_preparado.csv  # Dados da aplicação
└── README.md               # Documentação
```

## Configurações Importantes

### requirements.txt
```
streamlit>=1.28.0
pandas>=2.0.0
pathlib
```

### packages.txt
```
requests
```

### .streamlit/config.toml
```toml
[global]
developmentMode = false

[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"
```

## Troubleshooting

### Erro: "Repository not found"
- Verifique se o repositório foi criado corretamente no GitHub
- Confirme se o nome do usuário está correto no URL

### Erro: "Module not found"
- Verifique se todas as dependências estão no `requirements.txt`
- Certifique-se de que o `packages.txt` está presente se necessário

### Erro: "File not found"
- Verifique se o arquivo CSV está na pasta `data/`
- Confirme se o caminho no código está correto

## URLs Importantes

- **GitHub**: https://github.com
- **Streamlit Cloud**: https://share.streamlit.io
- **Documentação Streamlit**: https://docs.streamlit.io
