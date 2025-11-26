import streamlit as st
import pandas as pd
import numpy as np
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
        
        # Filtrar apenas itens de nível 4 (questões)
        df_questoes = df[df['nivel'] == 4].copy()
        
        return df, df_questoes
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        st.error(f"Tentando carregar de: {csv_path}")
        return None, None

# Função para converter tipos numpy/pandas para tipos Python nativos
def convert_to_native_types(obj):
    """Converte tipos numpy/pandas para tipos Python nativos (JSON serializáveis)"""
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

# Função para salvar validação localmente
def save_validation_local(validation_data):
    """Salva a validação em arquivo JSON local"""
    try:
        # Converter tipos numpy/pandas para tipos Python nativos
        validation_data_clean = convert_to_native_types(validation_data)
        
        # Criar pasta para validações se não existir
        validations_dir = Path("validations")
        validations_dir.mkdir(exist_ok=True)
        
        # Nome do arquivo baseado no usuário e timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"validation_{validation_data_clean['usuario']}_{timestamp}.json"
        filepath = validations_dir / filename
        
        # Salvar dados
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(validation_data_clean, f, ensure_ascii=False, indent=2)
        
        return True
    except Exception as e:
        st.error(f"Erro ao salvar validação: {e}")
        return False

# Função para carregar validações existentes
def load_existing_validations():
    """Carrega validações existentes dos arquivos JSON"""
    try:
        validations_dir = Path("validations")
        if not validations_dir.exists():
            return pd.DataFrame()
        
        all_validations = []
        
        # Ler todos os arquivos JSON
        for json_file in validations_dir.glob("*.json"):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    validation = json.load(f)
                    all_validations.append(validation)
            except Exception as e:
                st.warning(f"Erro ao ler arquivo {json_file}: {e}")
        
        if all_validations:
            return pd.DataFrame(all_validations)
        else:
            return pd.DataFrame()
            
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
    col1, col2 = st.columns([1.5, 1.5])
    
    with col1:
        st.markdown("### 📋 Informações do Item")
        
        # Hierarquia
        st.markdown("**Hierarquia:**")
        st.write(f"**Dimensão ID:** {current_item.get('dimensao_id_original', '')}")
        st.write(f"**Dimensão:** {current_item.get('dimensao_padrao', '')}")
        st.write(f"**Subdimensão:** {current_item.get('subdimensao', '')}")
        st.write(f"**Questão:** {current_item.get('questao', '')}")
        st.write(f"**Elemento:** {current_item.get('elemento', '')}")
        
        # Informações adicionais
        if current_item.get('numero_questao'):
            st.write(f"**Número da Questão:** {current_item.get('numero_questao', '')}")
        if current_item.get('nome_variavel'):
            st.write(f"**Nome da Variável:** {current_item.get('nome_variavel', '')}")
        if current_item.get('respuesta'):
            st.write(f"**Tipo de Resposta:** {current_item.get('respuesta', '')}")
        
        # Pontuações
        if pd.notna(current_item.get('pontuacao_maxima_dimensao')):
            st.write(f"**Pontuação Máx. Dimensão:** {current_item.get('pontuacao_maxima_dimensao', '')}")
        if pd.notna(current_item.get('pontuacao_maxima_capacidade_chave')):
            st.write(f"**Pontuação Máx. Capacidade Chave:** {current_item.get('pontuacao_maxima_capacidade_chave', '')}")
        if pd.notna(current_item.get('pontuacao_maxima_questao')):
            st.write(f"**Pontuação Máx. Questão:** {current_item.get('pontuacao_maxima_questao', '')}")
        if current_item.get('pontuacao_item'):
            st.write(f"**Pontuação Item:** {current_item.get('pontuacao_item', '')}")
        
        # Texto completo
        st.markdown("**Texto Completo:**")
        st.text_area("", value=current_item.get('texto_completo', ''), height=150, disabled=True)
    
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
                    # Converter valores do DataFrame para tipos Python nativos
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
                    
                    validation_data = {
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'usuario': str(usuario),
                        'sistema': safe_get(current_item, 'sistema'),
                        'ano': safe_get(current_item, 'ano', None),
                        'dimensao_id_original': safe_get(current_item, 'dimensao_id_original'),
                        'dimensao_padrao': safe_get(current_item, 'dimensao_padrao'),
                        'subdimensao': safe_get(current_item, 'subdimensao'),
                        'questao': safe_get(current_item, 'questao'),
                        'elemento': safe_get(current_item, 'elemento'),
                        'nivel': safe_get(current_item, 'nivel', None),
                        'tipo_elemento': safe_get(current_item, 'tipo_elemento'),
                        'texto_completo': safe_get(current_item, 'texto_completo'),
                        'pontuacao_maxima_dimensao': safe_get(current_item, 'pontuacao_maxima_dimensao', None),
                        'pontuacao_maxima_capacidade_chave': safe_get(current_item, 'pontuacao_maxima_capacidade_chave', None),
                        'nome_variavel': safe_get(current_item, 'nome_variavel'),
                        'numero_questao': safe_get(current_item, 'numero_questao'),
                        'respuesta': safe_get(current_item, 'respuesta'),
                        'pontuacao_maxima_questao': safe_get(current_item, 'pontuacao_maxima_questao', None),
                        'pontuacao_item': safe_get(current_item, 'pontuacao_item'),
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
                    
                    # Salvar localmente
                    if save_validation_local(validation_data):
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
