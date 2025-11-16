# ext_dashboard.py
"""
Dashboard extensor para Análise de Partidas Anotadas.

Este dashboard usa o `lance_analysis_v2.csv` gerado pelo `ext_pipeline`
para responder perguntas analíticas sobre o desempenho no x_xadrez.

Módulo 2-Ext: Análise de EDA
Módulo 5 (Conceito): Agente de IA para Análise de Dados
"""

# --- Importações Principais ---
import streamlit as st
import pandas as pd
import altair as alt
import os
from typing import Dict

# --- Importações do Agente de IA (Seção 4) ---
# Estas são importadas aqui para verificar a instalação
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
    AGENT_LIBS_INSTALLED = True
except ImportError:
    AGENT_LIBS_INSTALLED = False
# ----------------------------------------------


# --- Configuração ---
DATA_FILE = "data/processed/lance_analysis_v2.csv"

# --- Funções de Carregamento (Seção 1) ---

@st.cache_data
def load_data(filepath: str) -> pd.DataFrame:
    """Carrega os dados do CSV e faz um leve pré-processamento."""
    if not os.path.exists(filepath):
        st.error(f"Arquivo de dados não encontrado: {filepath}")
        st.info("Por favor, execute `python ext_pipeline.py` primeiro.")
        return pd.DataFrame()
        
    try:
        df = pd.read_csv(filepath)
        
        # Converte colunas numéricas (algumas podem ser lidas como 'object')
        df['eval_cp_pov_white'] = pd.to_numeric(df['eval_cp_pov_white'], errors='coerce')
        df['cent_pawn_loss'] = pd.to_numeric(df['centipawn_loss'], errors='coerce')
        
        # Garante que 'classification' seja uma categoria e preenche NAs
        df['classification'] = df['classification'].fillna('Normal')
        
        return df
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo de dados: {e}")
        return pd.DataFrame()

# --- Funções de Análise (Seção 1) ---

def get_first_error_stats(df: pd.DataFrame) -> Dict[str, float]:
    """
    Calcula o lance (ply) médio para a primeira Inaccuracy, Mistake, e Blunder.
    Espera um DataFrame JÁ FILTRADO para um único jogador.
    """
    stats = {}
    
    for error_type in ["Inaccuracy", "Mistake", "Blunder"]:
        # Encontra o primeiro ply (lance) de cada tipo de erro, por jogo
        first_errors = df[
            df['classification'] == error_type
        ].groupby('GameId')['ply'].min()
        
        # Calcula a média desses "primeiros erros"
        if not first_errors.empty:
            stats[error_type] = first_errors.mean()
        else:
            stats[error_type] = 0 # Nenhum erro desse tipo encontrado
            
    return stats

# --- Interface Principal do Dashboard ---

st.set_page_config(layout="wide", page_title="DCA - Análise de PGNs")
st.title("♟️ Dashboard de Análise de Partidas Anotadas")

# 1. Carregar Dados
df = load_data(DATA_FILE)

if df.empty:
    st.stop()

# 2. Sidebar de Filtros
st.sidebar.header("Filtros de Análise")

# Filtro de Jogador
player_names = pd.concat([df['White'], df['Black']]).unique()
selected_player = st.sidebar.selectbox(
    "Selecione o Jogador para Análise:",
    options=player_names,
    index=0
)

# Filtro de Jogo Específico
game_ids = df['GameId'].unique()
selected_games = st.sidebar.multiselect(
    "Selecione os Jogos (deixe em branco para todos):",
    options=game_ids
)

# 3. Aplicar Filtros
if selected_games:
    filtered_df = df[df['GameId'].isin(selected_games)].copy()
else:
    filtered_df = df.copy()


# Lógica de filtragem principal (CORRIGIDA)
player_moves_df = filtered_df[
    ((filtered_df['White'] == selected_player) & (filtered_df['player'] == 'White')) |
    ((filtered_df['Black'] == selected_player) & (filtered_df['player'] == 'Black'))
].copy()


# --- Seção 1: Linguagem Natural (Métricas Chave) ---
st.header(f"Resumo do Desempenho: {selected_player}")

if player_moves_df.empty:
    st.warning("Nenhum lance encontrado para este jogador com os filtros atuais.")
else:
    # Pergunta 1: Média de lances para o primeiro erro
    st.subheader("Q1: Média de Lances para o Primeiro Erro")
    
    # Chamada da função (CORRIGIDA)
    error_stats = get_first_error_stats(player_moves_df)
    
    col1, col2, col3 = st.columns(3)
    col1.metric(
        "Primeira Imprecisão (média)",
        f"{error_stats['Inaccuracy']:.1f}º lance (ply)"
    )
    col2.metric(
        "Primeiro Erro (média)",
        f"{error_stats['Mistake']:.1f}º lance (ply)"
    )
    col3.metric(
        "Primeira GAFE (média)",
        f"{error_stats['Blunder']:.1f}º lance (ply)"
    )
    
    # Outras métricas
    avg_cp_loss = player_moves_df['centipawn_loss'].mean()
    total_blunders = player_moves_df[player_moves_df['classification'] == 'Blunder'].shape[0]
    
    st.markdown("---")
    col1, col2 = st.columns(2)
    col1.metric("CP Loss Médio por Lance", f"{avg_cp_loss:.2f}")
    col2.metric("Total de GAFES (Blunders) nos jogos filtrados", total_blunders)


# --- Seção 2: Análise Gráfica ---
st.header("Análise Gráfica")

if player_moves_df.empty and not st.session_state.get('warning_shown', False):
    st.warning("Nenhum dado para exibir nos gráficos.")
    st.session_state['warning_shown'] = True # Evita repetição da mensagem
elif not player_moves_df.empty:
    # Pergunta 2: Onde os erros acontecem?
    st.subheader("Q2: CP Loss Médio por Fase do Jogo (pelo nº de lance)")
    
    # Agrupa por ply e calcula o CP Loss médio
    cp_loss_by_ply = player_moves_df.groupby('ply')['centipawn_loss'].mean().reset_index()
    
    chart_ply = alt.Chart(cp_loss_by_ply).mark_line(point=True).encode(
        x=alt.X('ply', title='Nº do Lance (Ply)'),
        y=alt.Y('centipawn_loss', title='CP Loss Médio'),
        tooltip=['ply', 'centipawn_loss']
    ).properties(
        title=f"CP Loss Médio de '{selected_player}' por Lance"
    ).interactive()
    
    st.altair_chart(chart_ply, use_container_width=True)

    # Gráficos Adicionais
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Tipos de Lances")
        # Gráfico de barras das classificações
        chart_class = alt.Chart(player_moves_df).mark_bar().encode(
            x=alt.X('classification', title='Classificação'),
            y=alt.Y('count()', title='Contagem'),
            color='classification',
            tooltip=['classification', 'count()']
        ).properties(
            title=f"Contagem de Tipos de Lances ({selected_player})"
        )
        st.altair_chart(chart_class, use_container_width=True)

    with col2:
        st.subheader("CP Loss Médio por Abertura")
        # CP Loss médio por abertura
        cp_loss_by_opening = player_moves_df.groupby('Opening')['centipawn_loss'].mean().reset_index()
        
        chart_opening = alt.Chart(cp_loss_by_opening).mark_bar().encode(
            x=alt.X('centipawn_loss', title='CP Loss Médio'),
            y=alt.Y('Opening', sort='-x', title='Abertura'),
            color=alt.Color('centipawn_loss', title='CP Loss Médio'),
            tooltip=['Opening', 'centipawn_loss']
        ).properties(
            title=f"Aberturas Mais Problemáticas ({selected_player})"
        )
        st.altair_chart(chart_opening, use_container_width=True)


# --- Seção 3: Dados Brutos ---
st.header("Explorador de Dados Brutos")

st.dataframe(player_moves_df.sort_values(by='centipawn_loss', ascending=False))

st.caption("Exibindo lances para o jogador selecionado. Desmarque os filtros para ver todos os dados.")

st.markdown("---")

# --- Seção 4: Assistente de Análise com IA (Google Gemini) ---
st.header("🤖 Assistente de Análise (IA)")

if not AGENT_LIBS_INSTALLED:
    st.error("Bibliotecas do Agente de IA não instaladas.")
    st.info("Por favor, ative seu 'venv' e execute:")
    st.code("pip install langchain langchain-google-genai google-generativeai langchain_experimental")
else:
    st.info("Faça uma pergunta em linguagem natural sobre seus dados, usando o Google Gemini.")

    # Verifica se a API Key está nos secrets
    if "GOOGLE_API_KEY" in st.secrets:
        
        # Configura o LLM do Google (Gemini)
        try:
            # Configura a chave de API como uma variável de ambiente
            os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
            
            # Inicializa o modelo. 
            # Garantindo o gemini-1.5-flash para controle de custos.
            llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", 
                                         temperature=0,
                                         convert_system_message_to_human=True)

            # Cria o "Agente Pandas"
            # Ele recebe o LLM e o DataFrame 'df' (com todos os dados)
            # Damos a ele o 'filtered_df' para respeitar os filtros da sidebar
            @st.cache_resource
            def get_pandas_agent(df_to_use):
                return create_pandas_dataframe_agent(
                    llm,
                    df_to_use,
                    verbose=True, 
                    allow_dangerous_code=True
                )

            # Usamos o 'filtered_df' para que o agente respeite os filtros de Jogo
            # Se nenhum jogo for selecionado, ele usa o 'df' completo
            agent_df = filtered_df if not filtered_df.empty else df
            pandas_agent = get_pandas_agent(agent_df)

            user_question = st.text_input("Sua pergunta sobre os dados filtrados:")

            if user_question:
                with st.spinner("Gemini está 'raciocinando' e executando o código..."):
                    try:
                        # O Agente executa os 4 passos (NL -> Código -> Dados -> NL)
                        response = pandas_agent.invoke(user_question)
                        st.write(response["output"])
                        
                        # Mostra o "pensamento" (código gerado) se estiver em modo de debug
                        if "intermediate_steps" in response:
                            st.subheader("Raciocínio do Agente (Debug):")
                            st.code(response["intermediate_steps"][0][0].tool_input["query"])
                            
                    except Exception as e:
                        st.error(f"Erro ao executar a consulta: {e}")
                        st.warning("Tente ser mais específico. O agente funciona melhor com perguntas sobre colunas (ex: 'CP Loss', 'Opening', 'GameId').")

        except Exception as e:
            st.error(f"Não foi possível inicializar o agente Gemini: {e}")
            st.info("Verifique se a API Key do Google está correta em '.streamlit/secrets.toml'.")

    else:
        st.error("Chave de API do Google não encontrada.")
        st.info("Por favor, crie o arquivo .streamlit/secrets.toml e adicione sua GOOGLE_API_KEY.")


# --- Explicação sobre Perguntas Futuras (Módulo 4) ---
st.markdown("---")
st.header("Próximos Passos (Módulo 4: Feature Engineering)")
st.info("""
**Por que não consigo responder (ainda) a todas as perguntas?**

As perguntas que você listou (como "par de bispos vs. par de cavalos", "gasto de tempo" ou "objetivos da abertura") exigem mais do que este dashboard. Elas exigem **Feature Engineering**.

1.  **Gasto de Tempo por Lance:** O PGN nos dá o `time_on_clock`. Para calcular o `time_spent`, precisaríamos modificar o `ext_parser.py` para subtrair o tempo do lance $N$ do tempo do lance $N-2$ (pois os lances são alternados).
2.  **Par de Bispos vs. Cavalos:** Precisaríamos modificar o `ext_parser.py` para analisar a coluna `fen_before_move` (usando a biblioteca `python-chess`) e adicionar colunas booleanas como `player_has_bishop_pair` ou `opponent_has_knight_pair`.
3.  **Objetivos da Abertura:** Similarmente, o parser precisaria analisar o FEN para determinar "quantas peças menores estão desenvolvidas" ou "o rei rocou".

Este dashboard (Módulo 2) está pronto. O próximo passo lógico seria implementar essas lógicas no `ext_parser.py` (Módulo 4).
""")
