# 📁 Estrutura da Aplicação Streamlit

## 🎯 Visão Geral
Aplicação web interativa para validação de itens da planilha do Índice de Inovação Pública do Chile.

## 📂 Estrutura de Arquivos

```
Streamlit/
├── 📄 app.py                    # Aplicação principal com Google Sheets
├── 📄 streamlit_app.py          # Aplicação local (arquivos JSON)
├── 📄 run_app.py               # Script principal de execução
├── 📄 requirements.txt          # Dependências Python
├── 📄 packages.txt             # Dependências do sistema (Streamlit Cloud)
├── 📄 README.md                # Documentação principal
├── 📄 TROUBLESHOOTING.md       # Guia de solução de problemas
├── 📄 ESTRUTURA.md             # Este arquivo
├── 📄 credentials_template.json # Template para credenciais Google
├── 📄 setup_google_sheets.py   # Configurador do Google Sheets
├── 📄 export_validations.py    # Exportador de validações
├── 📄 test_app.py              # Testador da aplicação
├── 📁 .streamlit/              # Configurações do Streamlit
│   └── 📄 config.toml          # Configuração da aplicação
└── 📁 validations/             # Pasta para validações locais (criada automaticamente)
    └── 📄 *.json               # Arquivos de validação
```

## 🚀 Como Usar

### Opção 1: Script Principal (Recomendado)
```bash
cd Streamlit
python run_app.py
```

### Opção 2: Execução Direta
```bash
cd Streamlit
pip install -r requirements.txt
streamlit run streamlit_app.py  # Versão local
# ou
streamlit run app.py            # Versão com Google Sheets
```

## 📊 Funcionalidades

### ✅ Validação por Linha
- **Aprovar**: Item aprovado sem modificações
- **Reprovar**: Item rejeitado
- **Sugerir Redação**: Sugestão de modificação no texto
- **Incluir Novo Item**: Proposta de novo item

### 📋 Apresentação Hierárquica
- **Dimensão**: Categoria principal (ex: recursos_institucionais)
- **Subdimensão**: Subcategoria (ex: Talento humano)
- **Questão**: Questão específica
- **Elemento**: Elemento da questão

### 🔍 Filtros e Busca
- Filtro por dimensão
- Filtro por subdimensão
- Busca por texto
- Estatísticas em tempo real

### 📊 Controle de Avaliações
- Impedir avaliações duplicadas
- Progresso visual
- Resumo das validações
- Histórico por usuário

## 🛠️ Tecnologias

### Front-end
- **Streamlit**: Interface web responsiva
- **Pandas**: Manipulação de dados
- **Pathlib**: Gerenciamento de arquivos

### Back-end
- **Google Sheets**: Armazenamento em nuvem (versão completa)
- **JSON**: Armazenamento local (versão local)
- **Google Cloud**: Autenticação e APIs

### Hospedagem
- **Streamlit Cloud**: Deploy gratuito
- **Local**: Desenvolvimento e testes

## 🔧 Configuração

### 1. Dependências
```bash
pip install -r requirements.txt
```

### 2. Google Sheets (Opcional)
```bash
python setup_google_sheets.py
# Siga as instruções para configurar credenciais
```

### 3. Dados
- Arquivo CSV deve estar em: `../raw_news/dados_preparados/chile_iip_2025_preparado.csv`
- Estrutura esperada: sistema, ano, dimensao_padrao, subdimensao, questao, elemento, nivel, tipo_elemento, texto_completo

## 📈 Fluxo de Trabalho

1. **Identificação**: Usuário se identifica na barra lateral
2. **Filtros**: Aplica filtros para navegar pelos itens
3. **Avaliação**: Para cada item:
   - Lê as informações
   - Seleciona status
   - Adiciona comentários
   - Salva avaliação
4. **Progresso**: Acompanha progresso e estatísticas
5. **Exportação**: Exporta resultados para análise

## 🔒 Segurança

### Versão Local
- Dados salvos em arquivos JSON locais
- Sem dependência externa
- Controle total dos dados

### Versão Google Sheets
- Autenticação via Service Account
- Dados armazenados na nuvem
- Backup automático
- Compartilhamento controlado

## 📊 Estrutura dos Dados

### Entrada (CSV)
```csv
sistema,ano,dimensao_padrao,subdimensao,questao,elemento,nivel,tipo_elemento,texto_completo
chile,2025,recursos_institucionais,Talento humano,Questão específica,Elemento,4,Questão,Texto completo
```

### Saída (Validações)
```json
{
  "timestamp": "2025-01-15 10:30:00",
  "usuario": "Nome do Avaliador",
  "sistema": "chile",
  "ano": "2025",
  "dimensao_padrao": "recursos_institucionais",
  "subdimensao": "Talento humano",
  "questao": "Questão específica",
  "elemento": "Elemento",
  "nivel": 4,
  "tipo_elemento": "Questão",
  "texto_completo": "Texto completo",
  "status": "Aprovar",
  "comentario": "Comentário opcional",
  "novo_item": false,
  "texto_novo_item": ""
}
```

## 🆘 Suporte

### Problemas Comuns
1. **Arquivo CSV não encontrado**: Verifique o caminho
2. **Dependências faltando**: Execute `pip install -r requirements.txt`
3. **Google Sheets não conecta**: Configure credenciais
4. **Aplicação não inicia**: Execute `python test_app.py`

### Logs e Debug
```bash
streamlit run app.py --logger.level debug
```

### Teste Completo
```bash
python test_app.py
```

## 🚀 Deploy

### Streamlit Cloud
1. Conecte seu repositório GitHub
2. Configure as variáveis de ambiente
3. Deploy automático

### Local
1. Instale dependências
2. Configure credenciais (se necessário)
3. Execute `python run_app.py`

## 📝 Licença
Uso interno para validação do Índice de Inovação Pública.




