import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# Configuração da página do Streamlit
st.set_page_config(
    page_title="Radar - Inteligência de Oportunidades",
    page_icon="📡",
    layout="wide"
)

# --- CSS PERSONALIZADO PARA COPIAR O VISUAL DA PLATAFORMA ---
st.markdown("""
    <style>
    /* Fundo geral da página */
    .main {
        background-color: #ffffff;
        color: #0f172a;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    
    /* Estilização cirúrgica da barra lateral para ficar igual ao print */
    [data-testid="stSidebar"] {
        background-color: #fafafa;
        border-right: 1px solid #eaeaea;
        padding-top: 1rem;
    }
    
    /* Remove espaçamentos indesejados da barra lateral */
    [data-testid="stSidebar"] div.block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }

    /* Caixa de busca / topo da barra lateral */
    .sidebar-search {
        background-color: #f3f4f6;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 6px 12px;
        font-size: 0.85rem;
        color: #9ca3af;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* Estilo dos radio buttons para parecerem o menu lateral da imagem */
    [data-testid="stSidebar"] .stRadio > div {
        gap: 4px;
    }
    [data-testid="stSidebar"] .stRadio label {
        background-color: transparent;
        padding: 8px 12px;
        border-radius: 8px;
        font-size: 0.88rem;
        font-weight: 500;
        color: #374151;
        width: 100%;
        transition: all 0.2s ease;
    }
    [data-testid="stSidebar"] .stRadio label:hover {
        background-color: #f1f5f9;
        color: #0f172a;
    }

    /* Cards principais idênticos ao layout corporativo */
    .app-card {
        background-color: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.02);
        margin-bottom: 16px;
    }
    
    .metric-card {
        background-color: #f9fafb;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 18px;
    }

    /* Botões modernos */
    .stButton>button {
        border-radius: 8px;
        font-weight: 500;
        border: 1px solid #d1d5db;
        background-color: #ffffff;
        color: #374151;
    }
    .stButton>button:hover {
        background-color: #f3f4f6;
        border-color: #9ca3af;
    }
    </style>
""", unsafe_allow_html=True)

# Inicializa o banco e as tabelas caso não existam
def init_db():
    conn = sqlite3.connect("radar_enterprise.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS signals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            url TEXT,
            category TEXT,
            intent TEXT,
            score REAL,
            created_at TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS opportunities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            signal_id INTEGER,
            score REAL,
            status TEXT DEFAULT 'new'
        )
    """)
    conn.commit()
    conn.close()

init_db()

def get_data():
    conn = sqlite3.connect("radar_enterprise.db")
    signals_df = pd.read_sql_query("SELECT * FROM signals", conn)
    opps_df = pd.read_sql_query("SELECT * FROM opportunities", conn)
    conn.close()
    return signals_df, opps_df

# Inicializa sessão
if "selected_opportunity_id" not in st.session_state:
    st.session_state["selected_opportunity_id"] = None

# --- BARRA LATERAL IDÊNTICA AO PRINT ---
with st.sidebar:
    # Barra de Pesquisa simulada no topo do menu
    st.markdown("""
        <div class="sidebar-search">
            <span>🔍</span> Pesquisar...
        </div>
    """, unsafe_allow_html=True)
    
    # Menu idêntico à imagem de referência
    menu = st.radio(
        "Navegação",
        [
            "🏠 Visão geral", 
            "👥 Usuários", 
            "📊 Dados", 
            "📈 Análises", 
            "marketing Marketing", 
            "🌐 Domínios", 
            "🔌 Integrações", 
            "🔒 Segurança", 
            "💻 Código", 
            "🤖 Agentes", 
            "⚡ Flujos de trabalho", 
            "🕒 Registros", 
            "🔌 API", 
            "⚙️ Configurações"
        ],
        label_visibility="collapsed"
    )

# --- CONTEÚDO PRINCIPAL ---
if "Visão geral" in menu:
    # Abas superiores (Pré-visualização / Painel)
    col_tabs, col_actions = st.columns([6, 4])
    with col_tabs:
        st.markdown("""
            <div style="display: flex; gap: 8px; margin-bottom: 20px;">
                <span style="background-color: #f3f4f6; padding: 6px 14px; border-radius: 6px; font-size: 0.85rem; font-weight: 600; border: 1px solid #e5e7eb;">Pré-visualização</span>
                <span style="background-color: #ffffff; padding: 6px 14px; border-radius: 6px; font-size: 0.85rem; font-weight: 500; border: 1px solid #e5e7eb; color: #6b7280;">Painel</span>
            </div>
        """, unsafe_allow_html=True)
        
    with col_actions:
        st.markdown("""
            <div style="display: flex; justify-content: flex-end; gap: 8px;">
                <button style="padding: 6px 12px; border-radius: 6px; border: 1px solid #e5e7eb; background: white; font-size: 0.85rem; font-weight: 500;">Atualizar</button>
                <button style="padding: 6px 12px; border-radius: 6px; border: none; background: #000000; color: white; font-size: 0.85rem; font-weight: 500;">Publicar</button>
            </div>
        """, unsafe_allow_html=True)

    # Card Principal do Aplicativo (Igualzinho ao Print)
    st.markdown("""
        <div class="app-card">
            <div style="display: flex; gap: 20px; align-items: flex-start;">
                <div style="background-color: #0b1329; color: white; width: 64px; height: 64px; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 28px; flex-shrink: 0;">
                    📡
                </div>
                <div style="flex-grow: 1;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <h2 style="margin: 0; font-size: 1.25rem; font-weight: 700; color: #0f172a;">RADAR</h2>
                        <span style="color: #6b7280; font-size: 1.1rem; cursor: pointer;">⭐</span>
                    </div>
                    <p style="margin: 6px 0 12px 0; font-size: 0.88rem; color: #4b5563; line-height: 1.4;">
                        Sistema independente que monitora fontes públicas em tempo real para identificar, qualificar e priorizar oportunidades de negócios com base em intenção e necessidade.
                    </p>
                    <div style="font-size: 0.75rem; color: #9ca3af;">Criado há 2 horas</div>
                </div>
            </div>
            
            <div style="display: flex; gap: 10px; margin-top: 16px; padding-top: 16px; border-top: 1px solid #f3f4f6;">
                <button style="padding: 6px 14px; border-radius: 6px; border: 1px solid #e5e7eb; background: white; font-size: 0.82rem; font-weight: 500;">🔗 Ganhar créditos</button>
                <button style="padding: 6px 14px; border-radius: 6px; border: 1px solid #e5e7eb; background: white; font-size: 0.82rem; font-weight: 500;">⏱️ Ver uso</button>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Linha com Visibilidade do Aplicativo e Convites
    col_vis, col_inv = st.columns(2)
    with col_vis:
        st.markdown("""
            <div class="app-card">
                <div style="font-weight: 600; font-size: 0.95rem; color: #111827;">Visibilidade do aplicativo</div>
                <div style="font-size: 0.8rem; color: #6b7280; margin-bottom: 12px;">Controle quem pode acessar seu aplicativo</div>
                <div style="background-color: #f9fafb; border: 1px solid #e5e7eb; border-radius: 8px; padding: 8px 12px; font-size: 0.85rem; color: #374151; display: flex; justify-content: space-between; align-items: center;">
                    <span>🌍 Público</span>
                    <span>▼</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
    with col_inv:
        st.markdown("""
            <div class="app-card">
                <div style="font-weight: 600; font-size: 0.95rem; color: #111827;">Convidar usuários</div>
                <div style="font-size: 0.8rem; color: #6b7280; margin-bottom: 12px;">Aumente sua base de usuários convidando outras pessoas</div>
                <div style="display: flex; gap: 8px;">
                    <button style="flex: 1; padding: 7px; border-radius: 8px; border: 1px solid #e5e7eb; background: white; font-size: 0.82rem;">📋 Copiar link</button>
                    <button style="flex: 1; padding: 7px; border-radius: 8px; border: 1px solid #e5e7eb; background: white; font-size: 0.82rem;">✉️ Enviar convites</button>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # Selo da plataforma
    st.markdown("""
        <div class="app-card" style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <div style="font-weight: 600; font-size: 0.95rem; color: #111827;">Selo da plataforma</div>
                <div style="font-size: 0.8rem; color: #6b7280;">O selo Base44 está agora visível em seu aplicativo.</div>
            </div>
            <button style="padding: 6px 12px; border-radius: 6px; border: 1px solid #e5e7eb; background: white; font-size: 0.82rem;">👁️ Ocultar selo</button>
        </div>
    """, unsafe_allow_html=True)

else:
    clean_name = menu.split(" ")[1] if " " in menu else menu
    st.markdown(f"## Módulo: {clean_name}")
    st.info(f"Gerenciamento e configurações da seção **{clean_name}** do seu ecossistema.")