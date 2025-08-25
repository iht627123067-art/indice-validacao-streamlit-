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
- **Back-end**: Google Sheets (armazenamento em nuvem) ou arquivos JSON locais
- **Hospedagem**: Streamlit Cloud (gratuito)

## 📋 Pré-requisitos

1. Python 3.8+
2. Conta Google Cloud Platform (para versão com Google Sheets)
3. Google Sheets API ativada (opcional)
4. Service Account configurada (opcional)

## 🔧 Instalação

### 1. Clonar o repositório
```bash
git clone <seu-repositorio>
cd indice_validacao
```

### 2. Criar ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

### 3. Instalar dependências
```bash
pip install -r requirements.txt
```

### 4. Executar aplicação

#### Versão Local (JSON)
```bash
streamlit run streamlit_app.py
```

#### Versão Completa (Google Sheets)
```bash
streamlit run app.py
```

## 📊 Estrutura dos Dados

A aplicação utiliza o arquivo `data/chile_iip_2025_preparado.csv` que contém:

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

### Versão Local (JSON)
As validações são salvas em arquivos JSON na pasta `validations/` com:
- Timestamp da avaliação
- Identificação do avaliador
- Dados completos do item
- Status da validação
- Comentários e sugestões
- Novos itens propostos

### Versão Google Sheets
As validações são salvas automaticamente no Google Sheets com os mesmos dados.

## 🔒 Segurança

- Cada usuário só pode ver suas próprias validações
- Dados armazenados de forma segura (Google Sheets ou arquivos locais)
- Controle de acesso via Service Account (Google Sheets)

## 🆘 Suporte

Para problemas ou dúvidas:
1. Verifique se as dependências estão instaladas corretamente
2. Confirme se o arquivo CSV existe em `data/chile_iip_2025_preparado.csv`
3. Para Google Sheets: verifique se as credenciais estão configuradas

## 📝 Licença

Este projeto é de uso interno para validação do Índice de Inovação Pública.
