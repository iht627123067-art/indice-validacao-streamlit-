# 🔧 Guia de Solução de Problemas

## ❓ Por que o .env não está funcionando?

### Problema Comum: Arquivo .env não encontrado

Se você está enfrentando problemas com variáveis de ambiente (.env), aqui estão as soluções:

### 🔍 Verificação do Problema

1. **Verificar se o arquivo .env existe:**
```bash
ls -la | grep .env
```

2. **Verificar se o arquivo está no local correto:**
   - O arquivo `.env` deve estar na **raiz do projeto**
   - Não dentro de subpastas

3. **Verificar o conteúdo do arquivo:**
```bash
cat .env
```

### 🛠️ Soluções

#### Solução 1: Criar arquivo .env
Se o arquivo não existe, crie-o na raiz do projeto:

```bash
# Na raiz do projeto (não dentro de Streamlit/)
touch .env
```

#### Solução 2: Configurar variáveis de ambiente
Adicione suas variáveis ao arquivo `.env`:

```env
# Exemplo de configuração
GOOGLE_SHEETS_CREDENTIALS_PATH=./Streamlit/credentials.json
CSV_DATA_PATH=./raw_news/dados_preparados/chile_iip_2025_preparado.csv
```

#### Solução 3: Usar python-dotenv
Instale e configure o python-dotenv:

```bash
pip install python-dotenv
```

No seu código Python:
```python
from dotenv import load_dotenv
import os

# Carregar variáveis do .env
load_dotenv()

# Usar as variáveis
credentials_path = os.getenv('GOOGLE_SHEETS_CREDENTIALS_PATH')
```

#### Solução 4: Configurar no Streamlit Cloud
Para deploy no Streamlit Cloud, configure as variáveis de ambiente na interface web:

1. Acesse seu app no Streamlit Cloud
2. Vá em "Settings" > "Secrets"
3. Adicione suas variáveis de ambiente

### 🚀 Para esta aplicação específica

Esta aplicação **NÃO usa arquivo .env** por padrão. Ela usa:

1. **Google Sheets**: Arquivo `credentials.json` na pasta Streamlit/
2. **Dados CSV**: Caminho relativo para o arquivo CSV

### 📁 Estrutura Correta

```
indice_report/
├── .env                    ← Se necessário
├── Streamlit/
│   ├── app.py
│   ├── streamlit_app.py
│   ├── credentials.json    ← Credenciais do Google Sheets
│   └── requirements.txt
└── raw_news/
    └── dados_preparados/
        └── chile_iip_2025_preparado.csv
```

### 🔧 Problemas Específicos

#### Problema: "ModuleNotFoundError: No module named 'dotenv'"
**Solução:**
```bash
pip install python-dotenv
```

#### Problema: "FileNotFoundError: .env"
**Solução:**
- Verifique se o arquivo está na raiz do projeto
- Verifique se o nome está correto (`.env`, não `env`)

#### Problema: Variáveis não carregadas
**Solução:**
```python
import os
from dotenv import load_dotenv

# Carregar .env
load_dotenv()

# Verificar se carregou
print(os.getenv('SUA_VARIAVEL'))
```

### 🆘 Ainda com problemas?

1. **Verifique os logs:**
```bash
streamlit run app.py --logger.level debug
```

2. **Teste a aplicação:**
```bash
cd Streamlit
python test_app.py
```

3. **Verifique dependências:**
```bash
pip list | grep -E "(streamlit|pandas|dotenv)"
```

### 📞 Suporte

Se ainda tiver problemas:
1. Verifique se está na pasta correta
2. Execute `python test_app.py` para diagnóstico
3. Verifique se todas as dependências estão instaladas
4. Confirme se o arquivo CSV existe no caminho correto

