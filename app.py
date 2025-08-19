import streamlit as st
import pandas as pd
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

# Função para carregar dados do CSV
@st.cache_data
def load_data():
    """Carrega os dados do arquivo CSV preparado"""
    try:
        # Caminho para o arquivo CSV
        csv_path = Path("../raw_news/dados_preparados/chile_iip_2025_preparado.csv")
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
    """Conecta ao Google Sheets usando credenciais"""
    try:
        # Verificar se existe arquivo de credenciais
        creds_file = Path("credentials.json")
        if not creds_file.exists():
            st.error("Arquivo credentials.json não encontrado. Por favor, configure as credenciais do Google Sheets.")
            return None
        
        creds = Credentials.from_service_account_file(
            "credentials.json", 
            scopes=SCOPES
        )
        client = gspread.authorize(creds)
        return client
    except Exception as e:
        st.error(f"Erro ao conectar ao Google Sheets: {e}")
        return None

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
        
        # Preparar dados para inserção
        row_data = [
            validation_data['timestamp'],
            validation_data['usuario'],
            validation_data['sistema'],
            validation_data['ano'],
            validation_data['dimensao_padrao'],
            validation_data['subdimensao'],
            validation_data['questao'],
            validation_data['elemento'],
            validation_data['nivel'],
            validation_data['tipo_elemento'],
            validation_data['texto_completo'],
            validation_data['status'],
            validation_data['comentario'],
            validation_data['novo_item'],
            validation_data['texto_novo_item']
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
                    validation_data = {
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'usuario': usuario,
                        'sistema': current_item['sistema'],
                        'ano': current_item['ano'],
                        'dimensao_padrao': current_item['dimensao_padrao'],
                        'subdimensao': current_item['subdimensao'],
                        'questao': current_item['questao'],
                        'elemento': current_item['elemento'],
                        'nivel': current_item['nivel'],
                        'tipo_elemento': current_item['tipo_elemento'],
                        'texto_completo': current_item['texto_completo'],
                        'status': status,
                        'comentario': comentario,
                        'novo_item': novo_item,
                        'texto_novo_item': texto_novo_item
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
