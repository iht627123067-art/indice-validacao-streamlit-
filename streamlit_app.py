import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import os
from pathlib import Path
import gspread
from google.oauth2.service_account import Credentials
import json

# Configuração da página
st.set_page_config(
    page_title="Validação de Itens - Índice de Inovação",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Função para carregar dados do CSV
@st.cache_data
def load_data():
    """Carrega os dados do arquivo CSV preparado"""
    try:
        # Caminho para o arquivo CSV - ajustado para Streamlit Cloud
        csv_path = Path("data/chile_iip_2025_preparado.csv")
        
        # Se não encontrar no caminho local, tentar caminho relativo
        if not csv_path.exists():
            csv_path = Path("data/chile_iip_2025_preparado.csv")
        
        df = pd.read_csv(csv_path)
        
        # Limpar dados
        df = df.fillna("")
        
        # Remover linhas completamente vazias
        df = df.dropna(how='all')
        
        # Filtrar apenas linhas que têm Texto_Questao (questões)
        df_questoes = df[df['Texto_Questao'].notna() & (df['Texto_Questao'] != '')].copy()
        
        return df, df_questoes
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        st.error(f"Tentando carregar de: {csv_path}")
        return None, None

# Função para converter tipos numpy/pandas para tipos Python nativos
def convert_to_native_types(obj):
    """Converte tipos numpy/pandas para tipos Python nativos (JSON serializáveis)"""
    try:
        if obj is None:
            return None
        elif isinstance(obj, (np.integer, np.int64, np.int32, np.int16, np.int8)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float64, np.float32, np.float16)):
            # Verificar se não é NaN
            if pd.isna(obj) or np.isnan(obj):
                return None
            return float(obj)
        elif isinstance(obj, np.bool_):
            return bool(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, dict):
            return {str(key): convert_to_native_types(value) for key, value in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [convert_to_native_types(item) for item in obj]
        elif pd.isna(obj):
            return None
        elif isinstance(obj, str):
            # Garantir que strings não contenham caracteres problemáticos
            return str(obj)
        else:
            # Tentar converter para string como último recurso
            return str(obj) if obj else None
    except Exception as e:
        # Em caso de erro, retornar None ou string vazia
        return None
# Google Sheets scopes
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]


def connect_to_sheets():
    """Conecta ao Google Sheets usando `credentials.json` localizado na raiz do projeto."""
    try:
        # Procurar por possíveis arquivos de credenciais no workspace
        candidates = [Path("credentials.json"), Path(".streamlit/credentials.json")]
        # também buscar por outros arquivos que contenham 'credentials' no nome
        for p in Path('.').glob('*credentials*.json'):
            if p not in candidates:
                candidates.append(p)

        for candidate in candidates:
            try:
                if candidate.exists():
                    creds = Credentials.from_service_account_file(str(candidate), scopes=SCOPES)
                    client = gspread.authorize(creds)
                    st.info(f"Usando credenciais do arquivo: {candidate}")
                    return client
            except Exception:
                # tentar próximo candidato
                continue

        # 2) Fallback: carregar credenciais do Streamlit secrets (útil no Streamlit Cloud)
        try:
            svc = st.secrets.get('gcp_service_account') if hasattr(st, 'secrets') else None
            if svc:
                creds = Credentials.from_service_account_info(svc, scopes=SCOPES)
                client = gspread.authorize(creds)
                st.info("Usando credenciais a partir de st.secrets['gcp_service_account']")
                return client
        except Exception as e:
            st.warning(f"Falha ao carregar credenciais do st.secrets: {e}")

        # Se chegar aqui, nenhuma credencial disponível
        st.error("Nenhum arquivo de credenciais válido encontrado (procurados: credentials.json, .streamlit/credentials.json e '*credentials*.json') e `st.secrets['gcp_service_account']` não está configurado.")
        return None
    except Exception as e:
        st.error(f"Erro ao conectar ao Google Sheets: {e}")
        return None


def save_validation_to_sheets_streamlit(validation_data, sheet_name="Validações Índice Inovação", worksheet_name="Validações_Streamlit"):
    """Salva a validação (dicionário) em uma worksheet específica no Google Sheets.

    - Cria a planilha/worksheet se não existir.
    - Garante que o cabeçalho corresponda às chaves do dicionário ao criar a worksheet.
    """
    client = connect_to_sheets()
    if not client:
        return False

    try:
        try:
            sheet = client.open(sheet_name)
        except gspread.exceptions.SpreadsheetNotFound:
            sheet = client.create(sheet_name)

        # Selecionar ou criar worksheet
        try:
            worksheet = sheet.worksheet(worksheet_name)
        except gspread.exceptions.WorksheetNotFound:
            # Criar worksheet com cabeçalho baseado nas chaves do validation_data
            headers = list(validation_data.keys())
            worksheet = sheet.add_worksheet(title=worksheet_name, rows=1000, cols=max(20, len(headers)))
            worksheet.append_row(headers)

        # Garantir headers
        existing = worksheet.get_all_values()
        if not existing or len(existing) == 0:
            headers = list(validation_data.keys())
            worksheet.append_row(headers)
        else:
            headers = existing[0]

        # Preparar linha de dados na ordem dos headers
        row = []
        for h in headers:
            v = validation_data.get(h, "")
            # Converter tipos básicos
            if v is None:
                row.append("")
            elif isinstance(v, (int, float, bool, str)):
                row.append(str(v))
            else:
                try:
                    row.append(str(v))
                except:
                    row.append("")

        worksheet.append_row(row)
        return True

    except Exception as e:
        st.error(f"Erro ao salvar no Google Sheets: {e}")
        return False


def load_existing_validations():
    """Carrega validações existentes da worksheet `Validações_Streamlit` no Google Sheets."""
    client = connect_to_sheets()
    if not client:
        return pd.DataFrame()

    try:
        sheet = client.open("Validações Índice Inovação")
        worksheet = sheet.worksheet("Validações_Streamlit")
        data = worksheet.get_all_records()
        return pd.DataFrame(data)
    except Exception:
        # Se planilha ou worksheet não existir, retornar DataFrame vazio
        return pd.DataFrame()

# Função para verificar se item já foi validado
def check_existing_validation(validations_df, item_data):
    """Verifica se um item já foi validado pelo usuário atual"""
    if validations_df.empty:
        return None
    
    # Extrair valores do item_data (Series do pandas)
    try:
        numero_questao = str(item_data.get('Numero_Questao', '')) if 'Numero_Questao' in item_data.index else ''
        sistema = str(item_data.get('sistema', '')) if 'sistema' in item_data.index else ''
        ano = item_data.get('ano', None) if 'ano' in item_data.index else None
    except (KeyError, AttributeError):
        return None
    
    # Filtrar por usuário e dados do item (usando Numero_Questao como identificador principal)
    # Verificar se a coluna existe no DataFrame de validações
    if 'numero_questao' in validations_df.columns:
        mask = (
            (validations_df['usuario'] == st.session_state.get('usuario', '')) &
            (validations_df['sistema'] == sistema) &
            (validations_df['ano'] == ano) &
            (validations_df['numero_questao'] == numero_questao)
        )
    else:
        # Fallback: usar texto_questao se numero_questao não existir
        try:
            texto_questao = str(item_data.get('Texto_Questao', '')) if 'Texto_Questao' in item_data.index else ''
        except (KeyError, AttributeError):
            texto_questao = ''
        
        if 'texto_questao' in validations_df.columns:
            mask = (
                (validations_df['usuario'] == st.session_state.get('usuario', '')) &
                (validations_df['sistema'] == sistema) &
                (validations_df['texto_questao'] == texto_questao)
            )
        else:
            return None
    
    existing = validations_df[mask]
    return existing.iloc[0] if not existing.empty else None

# Interface principal
def main():
    st.title("📊 Validação de Itens - Índice de Inovação Pública")
    st.markdown("---")
    
    # Sidebar para configurações
    with st.sidebar:
        st.header("⚙️ Configurações")
        
        # Identificação do usuário
        usuario = st.text_input("Nome do Avaliador:", key="usuario_input")
        if usuario:
            st.session_state['usuario'] = usuario
        
        # Filtros
        st.subheader("🔍 Filtros")
        
        # Carregar dados
        df, df_questoes = load_data()
        
        if df is not None:
            # Filtro por dimensão
            dimensoes = [''] + sorted(df_questoes['Dimensao'].dropna().unique().tolist())
            dimensao_filtro = st.selectbox("Dimensão:", dimensoes)
            
            # Filtro por capacidade chave (subdimensão)
            if dimensao_filtro:
                capacidades = [''] + sorted(df_questoes[df_questoes['Dimensao'] == dimensao_filtro]['Capacidade_Chave'].dropna().unique().tolist())
            else:
                capacidades = [''] + sorted(df_questoes['Capacidade_Chave'].dropna().unique().tolist())
            capacidade_filtro = st.selectbox("Capacidade Chave:", capacidades)
            
            # Busca por texto
            busca = st.text_input("Buscar por texto:")
            
            # Aplicar filtros
            df_filtrado = df_questoes.copy()
            
            if dimensao_filtro:
                df_filtrado = df_filtrado[df_filtrado['Dimensao'] == dimensao_filtro]
            
            if capacidade_filtro:
                df_filtrado = df_filtrado[df_filtrado['Capacidade_Chave'] == capacidade_filtro]
            
            if busca:
                mask = df_filtrado['Texto_Questao'].str.contains(busca, case=False, na=False)
                df_filtrado = df_filtrado[mask]
            
            st.info(f"📈 Total de itens: {len(df_filtrado)}")
            
            # Estatísticas
            if not df_filtrado.empty:
                st.subheader("📊 Estatísticas")
                st.write(f"**Dimensões:** {df_filtrado['Dimensao'].nunique()}")
                st.write(f"**Capacidades Chave:** {df_filtrado['Capacidade_Chave'].nunique()}")
    
    # Área principal
    if df is None:
        st.error("❌ Erro ao carregar dados. Verifique se o arquivo CSV existe.")
        return
    
    if not usuario:
        st.warning("⚠️ Por favor, identifique-se na barra lateral para começar a avaliação.")
        return
    
    # Carregar validações existentes
    validations_df = load_existing_validations()
    
    # Seleção de item para avaliação
    st.subheader("🎯 Avaliação de Item")
    
    if df_filtrado.empty:
        st.warning("Nenhum item encontrado com os filtros aplicados.")
        return
    
    # Selecionar item aleatório não validado
    if 'current_item_index' not in st.session_state:
        st.session_state['current_item_index'] = 0
    
    # Encontrar próximo item não validado
    items_nao_validados = []
    for idx, row in df_filtrado.iterrows():
        existing = check_existing_validation(validations_df, row)
        if existing is None:
            items_nao_validados.append(idx)
    
    if not items_nao_validados:
        st.success("🎉 Todos os itens foram validados!")
        return
    
    # Selecionar item atual
    current_idx = items_nao_validados[st.session_state['current_item_index'] % len(items_nao_validados)]
    current_item = df_filtrado.loc[current_idx]
    
    # Função auxiliar para extrair valores de forma segura
    def safe_get(item, key, default=''):
        """Extrai valor do item de forma segura, convertendo para tipo nativo"""
        try:
            # Tentar acessar como Series do pandas primeiro
            if hasattr(item, 'get'):
                value = item.get(key, default)
            elif hasattr(item, '__getitem__'):
                if hasattr(item, 'index') and key in item.index:
                    value = item[key]
                elif key in item:
                    value = item[key]
                else:
                    value = default
            else:
                value = default
            
            # Verificar se é NaN
            if pd.isna(value):
                return default if default != None else None
            
            # Converter tipos numpy para Python nativo
            if isinstance(value, (np.integer, np.int64, np.int32, np.int16, np.int8)):
                return int(value)
            elif isinstance(value, (np.floating, np.float64, np.float32, np.float16)):
                return float(value)
            elif isinstance(value, np.bool_):
                return bool(value)
            else:
                return str(value) if value else default
        except (KeyError, IndexError, AttributeError, TypeError):
            return default
    
    # Exibir informações do item
    col1, col2 = st.columns([1.5, 1.5])
    
    with col1:
        st.markdown("### 📋 Informações do Item")
        
        # Informações iniciais (obrigatórias)
        st.markdown("#### 📌 Informações Principais")
        
        # 1. Número da Questão
        numero_questao = safe_get(current_item, 'Numero_Questao', '')
        if numero_questao:
            st.write(f"**Número da Questão:** {numero_questao}")
        
        # 2. Questão
        questao = safe_get(current_item, 'Texto_Questao', '')
        if questao:
            st.markdown(f"**Questão:**")
            st.text_area("", value=questao, height=100, disabled=True, key=f"questao_display_{current_idx}")
        
        # 3. Respuesta
        respuesta = safe_get(current_item, 'Respuesta', '')
        if respuesta:
            st.write(f"**Respuesta:** {respuesta}")
        
        st.markdown("---")
        
        # Informações adicionais
        st.markdown("#### ℹ️ Informações Adicionais")
        
        # Dimensão
        dimensao = safe_get(current_item, 'Dimensao', '')
        if dimensao:
            st.write(f"**Dimensão:** {dimensao}")
        
        # Capacidade Chave
        capacidade_chave = safe_get(current_item, 'Capacidade_Chave', '')
        if capacidade_chave:
            st.write(f"**Capacidade Chave:** {capacidade_chave}")
        
        # Pontuação Máx. Dimensão
        pont_max_dimensao = safe_get(current_item, 'Pontuacao_Maxima_Dimensao', None)
        if pont_max_dimensao is not None and pont_max_dimensao != '':
            st.write(f"**Pontuação Máx. Dimensão:** {pont_max_dimensao}")
        
        # Pontuação Máx. Capacidade Chave
        pont_max_capacidade = safe_get(current_item, 'Pontuacao_Maxima_Capacidadclave', None)
        if pont_max_capacidade is not None and pont_max_capacidade != '':
            st.write(f"**Pontuação Máx. Capacidade Chave:** {pont_max_capacidade}")
        
        # Pontuação Máx. Questão
        pont_max_questao = safe_get(current_item, 'Pontuacao_Maxima_Questao', None)
        if pont_max_questao is not None and pont_max_questao != '':
            st.write(f"**Pontuação Máx. Questão:** {pont_max_questao}")
        
        # Pontuação Item
        pont_item = safe_get(current_item, 'Pontuação_item', '')
        if pont_item:
            st.write(f"**Pontuação Item:** {pont_item}")
        
        # Nome da Variável
        nome_variavel = safe_get(current_item, 'Nomble de la variable', '')
        if nome_variavel:
            st.write(f"**Nome da Variável:** {nome_variavel}")
        
        # Sistema e Ano
        sistema = safe_get(current_item, 'sistema', '')
        if sistema:
            st.write(f"**Sistema:** {sistema}")
        
        ano = safe_get(current_item, 'ano', None)
        if ano is not None:
            st.write(f"**Ano:** {ano}")
    
    with col2:
        st.markdown("### ✅ Avaliação")
        
        # Questão 1: Adequação à realidade brasileira (OBRIGATÓRIA)
        st.markdown("**1. Você considera o item adequado à realidade da administração pública brasileira?** ⚠️ *Obrigatório*")
        adequacao = st.radio(
            "",
            ["", "Sim", "Não", "Em partes"],
            key=f"adequacao_{current_idx}",
            horizontal=True
        )
        
        justificativa_adequacao = ""
        if adequacao == "Em partes":
            justificativa_adequacao = st.text_area(
                "Justificativa:",
                key=f"justificativa_adequacao_{current_idx}",
                height=80
            )
        
        st.markdown("---")
        
        # Questão 2: Grau de relevância (OBRIGATÓRIA)
        st.markdown("**2. Considerando a premissa de que o índice será implementado em etapas, avalie o item conforme o grau de relevância do item para medir quão inovadora pode ser a administração pública brasileira.** ⚠️ *Obrigatório*")
        st.markdown("*Escala de 1 a 5, onde 1 representa baixa relevância e 5, alta relevância.*")
        relevancia = st.selectbox(
            "Grau de relevância:",
            ["", "1 - Baixa relevância", "2", "3", "4", "5 - Alta relevância"],
            key=f"relevancia_{current_idx}"
        )
        
        st.markdown("---")
        
        # Questão 3: Norma que exige o item
        st.markdown("**3. Considerando que muitos itens podem ser exigidos por alguma norma (Constituição, instrução normativa, portaria, decreto), avalie se há alguma norma que exija iniciativas por parte do órgão público.**")
        tem_norma = st.radio(
            "",
            ["", "Não", "Sim"],
            key=f"tem_norma_{current_idx}",
            horizontal=True
        )
        
        detalhes_norma = ""
        if tem_norma == "Sim":
            detalhes_norma = st.text_area(
                "Qual normativo? Qual inciso? É obrigatório ou facultativo?",
                key=f"detalhes_norma_{current_idx}",
                height=80
            )
        
        st.markdown("---")
        
        # Questão 4: Base de dados pública
        st.markdown("**4. A resposta ao item pode ser encontrada em bases de dados públicas do Brasil por meio de coleta ativa de dados?**")
        tem_base_dados = st.radio(
            "",
            ["", "Não", "Sim"],
            key=f"tem_base_dados_{current_idx}",
            horizontal=True
        )
        
        link_base_dados = ""
        if tem_base_dados == "Sim":
            link_base_dados = st.text_input(
                "Qual link para acessar a base?",
                key=f"link_base_dados_{current_idx}"
            )
        
        st.markdown("---")
        
        # Questão 5: Exigência por outros organismos
        st.markdown("**5. Você tem conhecimento de que o item é exigido ou solicitado por outros organismos da administração pública (por exemplo: SIORG), órgãos de controle como CGU e TCU, ou organismos internacionais como ONU e OCDE em razão de relatórios, rankings ou monitoramentos?**")
        tem_organismo = st.radio(
            "",
            ["", "Não", "Sim"],
            key=f"tem_organismo_{current_idx}",
            horizontal=True
        )
        
        qual_organismo = ""
        if tem_organismo == "Sim":
            qual_organismo = st.text_input(
                "Qual?",
                key=f"qual_organismo_{current_idx}"
            )
        
        st.markdown("---")
        
        # Comentário geral (opcional)
        comentario = st.text_area(
            "Comentário adicional (opcional):",
            key=f"comentario_{current_idx}",
            height=80
        )
        
        # Botões de ação
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            if st.button("💾 Salvar Avaliação", key=f"save_{current_idx}"):
                # Validar campos obrigatórios
                erros_validacao = []
                
                if not adequacao or adequacao == "":
                    erros_validacao.append("⚠️ A questão 1 (Adequação à realidade brasileira) é obrigatória.")
                
                if not relevancia or relevancia == "":
                    erros_validacao.append("⚠️ A questão 2 (Grau de relevância) é obrigatória.")
                
                if adequacao == "Em partes" and not justificativa_adequacao:
                    erros_validacao.append("⚠️ É necessário fornecer justificativa quando selecionar 'Em partes' na questão 1.")
                
                if erros_validacao:
                    for erro in erros_validacao:
                        st.error(erro)
                else:
                    # Preparar dados da validação
                    validation_data = {
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'usuario': str(usuario),
                        'sistema': safe_get(current_item, 'sistema'),
                        'ano': safe_get(current_item, 'ano', None),
                        'dimensao': safe_get(current_item, 'Dimensao'),
                        'pontuacao_maxima_dimensao': safe_get(current_item, 'Pontuacao_Maxima_Dimensao', None),
                        'capacidade_chave': safe_get(current_item, 'Capacidade_Chave'),
                        'pontuacao_maxima_capacidade_chave': safe_get(current_item, 'Pontuacao_Maxima_Capacidadclave', None),
                        'nome_variavel': safe_get(current_item, 'Nomble de la variable'),
                        'numero_questao': safe_get(current_item, 'Numero_Questao'),
                        'texto_questao': safe_get(current_item, 'Texto_Questao'),
                        'respuesta': safe_get(current_item, 'Respuesta'),
                        'pontuacao_maxima_questao': safe_get(current_item, 'Pontuacao_Maxima_Questao', None),
                        'pontuacao_item': safe_get(current_item, 'Pontuação_item'),
                        # Novas questões de avaliação
                        'adequacao_realidade_brasileira': str(adequacao),
                        'justificativa_adequacao': str(justificativa_adequacao) if justificativa_adequacao else '',
                        'grau_relevancia': str(relevancia),
                        'tem_norma_exigente': str(tem_norma),
                        'detalhes_norma': str(detalhes_norma) if detalhes_norma else '',
                        'tem_base_dados_publica': str(tem_base_dados),
                        'link_base_dados': str(link_base_dados) if link_base_dados else '',
                        'tem_organismo_exigente': str(tem_organismo),
                        'qual_organismo': str(qual_organismo) if qual_organismo else '',
                        'comentario': str(comentario) if comentario else ''
                    }
                    
                    # Salvar no Google Sheets
                    if save_validation_to_sheets_streamlit(validation_data):
                        st.success("✅ Avaliação salva com sucesso!")
                        st.session_state['current_item_index'] += 1
                        st.rerun()
                    else:
                        st.error("❌ Erro ao salvar avaliação.")
        
        with col_btn2:
            if st.button("⏭️ Próximo Item", key=f"next_{current_idx}"):
                st.session_state['current_item_index'] += 1
                st.rerun()
    
    # Progresso
    st.markdown("---")
    st.subheader("📈 Progresso")
    
    total_items = len(df_filtrado)
    items_validados = len(validations_df[validations_df['usuario'] == usuario]) if not validations_df.empty else 0
    
    progress = items_validados / total_items if total_items > 0 else 0
    st.progress(progress)
    st.write(f"**Progresso:** {items_validados}/{total_items} itens validados ({progress:.1%})")
    
    # Resumo das validações
    if not validations_df.empty:
        user_validations = validations_df[validations_df['usuario'] == usuario]
        if not user_validations.empty:
            st.subheader("📊 Resumo das Suas Validações")
            
            # Verificar quais colunas existem no DataFrame
            colunas_disponiveis = user_validations.columns.tolist()
            
            # Resumo baseado nas novas questões de avaliação
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                # Adequação à realidade brasileira
                if 'adequacao_realidade_brasileira' in colunas_disponiveis:
                    adequados = len(user_validations[user_validations['adequacao_realidade_brasileira'] == 'Sim'])
                    st.metric("✅ Adequados", adequados)
                else:
                    st.metric("✅ Total", len(user_validations))
            
            with col2:
                # Em partes
                if 'adequacao_realidade_brasileira' in colunas_disponiveis:
                    em_partes = len(user_validations[user_validations['adequacao_realidade_brasileira'] == 'Em partes'])
                    st.metric("⚠️ Em Partes", em_partes)
                else:
                    st.metric("📝 Validações", len(user_validations))
            
            with col3:
                # Não adequados
                if 'adequacao_realidade_brasileira' in colunas_disponiveis:
                    nao_adequados = len(user_validations[user_validations['adequacao_realidade_brasileira'] == 'Não'])
                    st.metric("❌ Não Adequados", nao_adequados)
                else:
                    st.metric("📊 Itens", len(user_validations))
            
            with col4:
                # Alta relevância (5)
                if 'grau_relevancia' in colunas_disponiveis:
                    alta_relevancia = len(user_validations[user_validations['grau_relevancia'].str.contains('5', na=False)])
                    st.metric("⭐ Alta Relevância", alta_relevancia)
                else:
                    st.metric("📈 Total", len(user_validations))
            
            # Estatísticas adicionais
            st.markdown("---")
            st.markdown("#### 📈 Estatísticas Detalhadas")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if 'grau_relevancia' in colunas_disponiveis:
                    st.markdown("**Distribuição de Relevância:**")
                    relevancia_counts = user_validations['grau_relevancia'].value_counts().sort_index()
                    for nivel, count in relevancia_counts.items():
                        if nivel and str(nivel).strip():
                            st.write(f"  {nivel}: {count}")
            
            with col2:
                if 'tem_norma_exigente' in colunas_disponiveis:
                    st.markdown("**Normas Exigentes:**")
                    com_norma = len(user_validations[user_validations['tem_norma_exigente'] == 'Sim'])
                    sem_norma = len(user_validations[user_validations['tem_norma_exigente'] == 'Não'])
                    st.write(f"  Com norma: {com_norma}")
                    st.write(f"  Sem norma: {sem_norma}")
            
            with col3:
                if 'tem_base_dados_publica' in colunas_disponiveis:
                    st.markdown("**Bases de Dados:**")
                    com_base = len(user_validations[user_validations['tem_base_dados_publica'] == 'Sim'])
                    sem_base = len(user_validations[user_validations['tem_base_dados_publica'] == 'Não'])
                    st.write(f"  Com base: {com_base}")
                    st.write(f"  Sem base: {sem_base}")

if __name__ == "__main__":
    main()

