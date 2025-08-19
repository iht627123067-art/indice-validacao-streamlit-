# 📊 Aplicação de Validação - Índice de Inovação Pública

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
