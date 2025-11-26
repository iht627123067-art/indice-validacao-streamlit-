import streamlit as st
import pandas as pd
import numpy as np
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import json
import os
from pathlib import Path

# Configuração da página
st.set_page_config(
    page_title="Validação de Itens - Índice de Inovação",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configurações do Google Sheets
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

# Função para obter credenciais do Streamlit Secrets
def get_credentials_from_secrets():
    """Obtém credenciais do Google Sheets a partir do Streamlit Secrets"""
    try:
        creds_dict = dict(st.secrets["gcp_service_account"])
        creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")
        return Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
    except Exception as e:
        st.error(f"Erro ao carregar credenciais do Streamlit Secrets: {e}")
        return None

# Função para carregar dados do CSV
@st.cache_data
def load_data():
    """Carrega os dados do arquivo CSV preparado"""
    try:
        # Caminho para o arquivo CSV
        csv_path = Path("data/chile_iip_2025_preparado.csv")
        df = pd.read_csv(csv_path)
        
        # Limpar dados
        df = df.fillna("")
        
        # Filtrar apenas itens de nível 4 (questões)
        df_questoes = df[df['nivel'] == 4].copy()
        
        return df, df_questoes
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return None, None

# Função para conectar ao Google Sheets
def connect_to_sheets():
    """Conecta ao Google Sheets usando credenciais do Streamlit Secrets"""
    try:
        creds = get_credentials_from_secrets()
        if not creds:
            return None
            
        client = gspread.authorize(creds)
        return client
    except Exception as e:
        st.error(f"Erro ao conectar ao Google Sheets: {e}")
        return None

# Função para testar conexão com Google Sheets
def test_google_sheets_connection():
    """Testa a conexão com o Google Sheets e retorna informações sobre o status"""
    result = {
        'connected': False,
        'message': '',
        'details': {}
    }
    
    try:
        # Verificar se as secrets estão configuradas
        if 'gcp_service_account' not in st.secrets:
            result['message'] = "❌ Secrets do GCP não configuradas"
            result['details'] = {'secrets_configured': False}
            return result
        
        result['details']['secrets_configured'] = True
        
        # Tentar conectar
        client = connect_to_sheets()
        if not client:
            result['message'] = "❌ Falha ao autenticar com Google Sheets"
            return result
        
        result['details']['authentication'] = 'success'
        
        # Tentar listar planilhas (teste de permissão)
        try:
            sheets = client.openall()
            result['details']['sheets_count'] = len(sheets)
            result['details']['can_list_sheets'] = True
            
            # Tentar abrir ou criar planilha de teste
            try:
                sheet = client.open("Validações Índice Inovação")
                result['details']['target_sheet_exists'] = True
                result['details']['sheet_id'] = sheet.id
                result['details']['sheet_url'] = sheet.url
                
                # Tentar acessar worksheet
                try:
                    worksheet = sheet.worksheet("Validações")
                    result['details']['worksheet_exists'] = True
                    result['details']['rows_count'] = len(worksheet.get_all_values())
                except:
                    result['details']['worksheet_exists'] = False
                    result['details']['message'] = "Worksheet 'Validações' não existe, mas será criado automaticamente"
                    
            except gspread.exceptions.SpreadsheetNotFound:
                result['details']['target_sheet_exists'] = False
                result['details']['message'] = "Planilha 'Validações Índice Inovação' não existe, mas será criada automaticamente"
            
            result['connected'] = True
            result['message'] = "✅ Conexão com Google Sheets estabelecida com sucesso!"
            
        except Exception as e:
            result['message'] = f"⚠️ Conectado, mas erro ao acessar planilhas: {e}"
            result['details']['error'] = str(e)
            result['connected'] = True  # Ainda está conectado, só não conseguiu listar
            
    except Exception as e:
        result['message'] = f"❌ Erro ao testar conexão: {e}"
        result['details']['error'] = str(e)
    
    return result

# Função para converter tipos numpy/pandas para tipos Python nativos
def convert_to_native_types(obj):
    """Converte tipos numpy/pandas para tipos Python nativos"""
    if isinstance(obj, (np.integer, np.int64, np.int32, np.int16, np.int8)):
        return int(obj)
    elif isinstance(obj, (np.floating, np.float64, np.float32, np.float16)):
        return float(obj)
    elif isinstance(obj, np.bool_):
        return bool(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {key: convert_to_native_types(value) for key, value in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [convert_to_native_types(item) for item in obj]
    elif pd.isna(obj):
        return None
    else:
        return obj

# Função para salvar validação no Google Sheets
def save_validation_to_sheets(validation_data):
    """Salva a validação no Google Sheets"""
    client = connect_to_sheets()
    if not client:
        return False
    
    try:
        # Abrir ou criar planilha
        try:
            sheet = client.open("Validações Índice Inovação")
        except:
            sheet = client.create("Validações Índice Inovação")
        
        # Selecionar ou criar worksheet
        try:
            worksheet = sheet.worksheet("Validações")
        except:
            worksheet = sheet.add_worksheet("Validações", 1000, 20)
        
        # Converter tipos numpy/pandas para tipos Python nativos
        validation_data_clean = convert_to_native_types(validation_data)
        
        # Preparar dados para inserção
        row_data = [
            validation_data_clean['timestamp'],
            validation_data_clean['usuario'],
            validation_data_clean['sistema'],
            validation_data_clean['ano'],
            validation_data_clean['dimensao_padrao'],
            validation_data_clean['subdimensao'],
            validation_data_clean['questao'],
            validation_data_clean['elemento'],
            validation_data_clean['nivel'],
            validation_data_clean['tipo_elemento'],
            validation_data_clean['texto_completo'],
            validation_data_clean['status'],
            validation_data_clean['comentario'],
            validation_data_clean['novo_item'],
            validation_data_clean['texto_novo_item']
        ]
        
        # Inserir dados
        worksheet.append_row(row_data)
        return True
        
    except Exception as e:
        st.error(f"Erro ao salvar no Google Sheets: {e}")
        return False

# Função para carregar validações existentes
def load_existing_validations():
    """Carrega validações existentes do Google Sheets"""
    client = connect_to_sheets()
    if not client:
        return pd.DataFrame()
    
    try:
        sheet = client.open("Validações Índice Inovação")
        worksheet = sheet.worksheet("Validações")
        
        # Obter dados
        data = worksheet.get_all_records()
        return pd.DataFrame(data)
        
    except Exception as e:
        st.warning(f"Não foi possível carregar validações existentes: {e}")
        return pd.DataFrame()

# Função para verificar se item já foi validado
def check_existing_validation(validations_df, item_data):
    """Verifica se um item já foi validado pelo usuário atual"""
    if validations_df.empty:
        return None
    
    # Filtrar por usuário e dados do item
    mask = (
        (validations_df['usuario'] == st.session_state.get('usuario', '')) &
        (validations_df['sistema'] == item_data['sistema']) &
        (validations_df['ano'] == item_data['ano']) &
        (validations_df['dimensao_padrao'] == item_data['dimensao_padrao']) &
        (validations_df['subdimensao'] == item_data['subdimensao']) &
        (validations_df['questao'] == item_data['questao']) &
        (validations_df['elemento'] == item_data['elemento'])
    )
    
    existing = validations_df[mask]
    return existing.iloc[0] if not existing.empty else None

# Interface principal
def main():
    st.title("📊 Validação de Itens - Índice de Inovação Pública")
    st.markdown("---")
    
    # Sidebar para configurações
    with st.sidebar:
        st.header("⚙️ Configurações")
        
        # Teste de conexão Google Sheets
        st.subheader("🔗 Google Sheets")
        if st.button("🧪 Testar Conexão", key="test_connection"):
            with st.spinner("Testando conexão..."):
                test_result = test_google_sheets_connection()
                
                if test_result['connected']:
                    st.success(test_result['message'])
                    
                    # Mostrar detalhes
                    with st.expander("📋 Detalhes da Conexão"):
                        details = test_result['details']
                        if 'secrets_configured' in details:
                            st.write(f"**Secrets configuradas:** {'✅ Sim' if details['secrets_configured'] else '❌ Não'}")
                        
                        if 'authentication' in details:
                            st.write(f"**Autenticação:** ✅ Sucesso")
                        
                        if 'sheets_count' in details:
                            st.write(f"**Planilhas acessíveis:** {details['sheets_count']}")
                        
                        if 'target_sheet_exists' in details:
                            if details['target_sheet_exists']:
                                st.write(f"**Planilha 'Validações Índice Inovação':** ✅ Existe")
                                if 'sheet_url' in details:
                                    st.write(f"**URL:** {details['sheet_url']}")
                                if 'worksheet_exists' in details:
                                    if details['worksheet_exists']:
                                        st.write(f"**Worksheet 'Validações':** ✅ Existe")
                                        if 'rows_count' in details:
                                            st.write(f"**Linhas existentes:** {details['rows_count']}")
                                    else:
                                        st.write(f"**Worksheet 'Validações':** ⚠️ Será criado automaticamente")
                            else:
                                st.write(f"**Planilha 'Validações Índice Inovação':** ⚠️ Será criada automaticamente")
                        
                        if 'error' in details:
                            st.error(f"**Erro:** {details['error']}")
                else:
                    st.error(test_result['message'])
                    if 'details' in test_result and 'error' in test_result['details']:
                        st.error(f"**Detalhes:** {test_result['details']['error']}")
        
        st.markdown("---")
        
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
            dimensoes = [''] + sorted(df_questoes['dimensao_padrao'].unique().tolist())
            dimensao_filtro = st.selectbox("Dimensão:", dimensoes)
            
            # Filtro por subdimensão
            if dimensao_filtro:
                subdimensoes = [''] + sorted(df_questoes[df_questoes['dimensao_padrao'] == dimensao_filtro]['subdimensao'].unique().tolist())
            else:
                subdimensoes = [''] + sorted(df_questoes['subdimensao'].unique().tolist())
            subdimensao_filtro = st.selectbox("Subdimensão:", subdimensoes)
            
            # Busca por texto
            busca = st.text_input("Buscar por texto:")
            
            # Aplicar filtros
            df_filtrado = df_questoes.copy()
            
            if dimensao_filtro:
                df_filtrado = df_filtrado[df_filtrado['dimensao_padrao'] == dimensao_filtro]
            
            if subdimensao_filtro:
                df_filtrado = df_filtrado[df_filtrado['subdimensao'] == subdimensao_filtro]
            
            if busca:
                mask = df_filtrado['texto_completo'].str.contains(busca, case=False, na=False)
                df_filtrado = df_filtrado[mask]
            
            st.info(f"📈 Total de itens: {len(df_filtrado)}")
            
            # Estatísticas
            if not df_filtrado.empty:
                st.subheader("📊 Estatísticas")
                st.write(f"**Dimensões:** {df_filtrado['dimensao_padrao'].nunique()}")
                st.write(f"**Subdimensões:** {df_filtrado['subdimensao'].nunique()}")
    
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
    
    # Exibir informações do item
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📋 Informações do Item")
        
        # Hierarquia
        st.markdown("**Hierarquia:**")
        st.write(f"**Dimensão:** {current_item['dimensao_padrao']}")
        st.write(f"**Subdimensão:** {current_item['subdimensao']}")
        st.write(f"**Questão:** {current_item['questao']}")
        st.write(f"**Elemento:** {current_item['elemento']}")
        
        # Texto completo
        st.markdown("**Texto Completo:**")
        st.text_area("", value=current_item['texto_completo'], height=150, disabled=True)
    
    with col2:
        st.markdown("### ✅ Avaliação")
        
        # Status da validação
        status = st.selectbox(
            "Status:",
            ["", "Aprovar", "Reprovar", "Sugerir Redação", "Incluir Novo Item"],
            key=f"status_{current_idx}"
        )
        
        # Comentário
        comentario = st.text_area(
            "Comentário/Sugestão:",
            key=f"comentario_{current_idx}",
            height=100
        )
        
        # Novo item (se aplicável)
        novo_item = False
        texto_novo_item = ""
        
        if status == "Incluir Novo Item":
            novo_item = True
            texto_novo_item = st.text_area(
                "Texto do Novo Item:",
                key=f"novo_item_{current_idx}",
                height=100
            )
        
        # Botões de ação
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            if st.button("💾 Salvar Avaliação", key=f"save_{current_idx}"):
                if status:
                    # Preparar dados da validação
                    # Converter valores do DataFrame para tipos Python nativos
                    validation_data = {
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'usuario': str(usuario),
                        'sistema': str(current_item['sistema']) if pd.notna(current_item['sistema']) else '',
                        'ano': int(current_item['ano']) if pd.notna(current_item['ano']) else None,
                        'dimensao_padrao': str(current_item['dimensao_padrao']) if pd.notna(current_item['dimensao_padrao']) else '',
                        'subdimensao': str(current_item['subdimensao']) if pd.notna(current_item['subdimensao']) else '',
                        'questao': str(current_item['questao']) if pd.notna(current_item['questao']) else '',
                        'elemento': str(current_item['elemento']) if pd.notna(current_item['elemento']) else '',
                        'nivel': int(current_item['nivel']) if pd.notna(current_item['nivel']) else None,
                        'tipo_elemento': str(current_item['tipo_elemento']) if pd.notna(current_item['tipo_elemento']) else '',
                        'texto_completo': str(current_item['texto_completo']) if pd.notna(current_item['texto_completo']) else '',
                        'status': str(status),
                        'comentario': str(comentario) if comentario else '',
                        'novo_item': bool(novo_item),
                        'texto_novo_item': str(texto_novo_item) if texto_novo_item else ''
                    }
                    
                    # Salvar no Google Sheets
                    if save_validation_to_sheets(validation_data):
                        st.success("✅ Avaliação salva com sucesso!")
                        st.session_state['current_item_index'] += 1
                        st.rerun()
                    else:
                        st.error("❌ Erro ao salvar avaliação.")
                else:
                    st.warning("⚠️ Selecione um status para continuar.")
        
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
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                aprovados = len(user_validations[user_validations['status'] == 'Aprovar'])
                st.metric("✅ Aprovados", aprovados)
            
            with col2:
                reprovados = len(user_validations[user_validations['status'] == 'Reprovar'])
                st.metric("❌ Reprovados", reprovados)
            
            with col3:
                sugestoes = len(user_validations[user_validations['status'] == 'Sugerir Redação'])
                st.metric("✏️ Sugestões", sugestoes)
            
            with col4:
                novos = len(user_validations[user_validations['status'] == 'Incluir Novo Item'])
                st.metric("🆕 Novos Itens", novos)

if __name__ == "__main__":
    main()
