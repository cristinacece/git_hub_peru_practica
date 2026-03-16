import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from app.utils import load_data
from app.components.charts import plot_growth_trend, plot_language_pie, plot_city_bar, plot_talent_scatter

st.set_page_config(page_title="PE GitHub Peru Analytics", page_icon="🇵🇪", layout="wide")

# Premium CSS
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #161b22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #161b22;
        border-radius: 4px 4px 0px 0px;
        padding: 10px 20px;
        color: #8b949e;
    }
    .stTabs [aria-selected="true"] {
        background-color: #ff4b4b !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🇵🇪 GitHub Peru Analytics")

# --- NAVIGATION TABS ---
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Overview", 
    "👥 Developers", 
    "📂 Repositories", 
    "🏭 Industries", 
    "💻 Languages", 
    "🤖 AI Analyst"
])

# --- TAB 1: OVERVIEW ---
with tab1:
    st.markdown("### El centro de inteligencia del ecosistema dev peruano")
    try:
        users_count = load_data("SELECT COUNT(*) as count FROM users")['count'][0]
        repos_count = load_data("SELECT COUNT(*) as count FROM repos WHERE fork=0")['count'][0]
        total_stars = load_data("SELECT SUM(stargazers_count) as total FROM repos WHERE fork=0")['total'][0]
        avg_h = load_data("SELECT AVG(h_index) as avg_h FROM users WHERE h_index > 0")['avg_h'][0]

        c1, c2, c3, c4 = st.columns(4)
        with c1: st.metric("👩‍💻 Desarrolladores", f"{users_count:,}")
        with c2: st.metric("📦 Proyectos Propios", f"{repos_count:,}")
        with c3: st.metric("⭐ Estrellas Totales", f"{total_stars:,}")
        with c4: st.metric("🏆 H-Index Promedio", f"{avg_h:.2f}")

        col1, col2 = st.columns([2, 1])
        with col1:
            st.subheader("📈 Evolución de la Comunidad")
            df_years = load_data("SELECT year, COUNT(*) as count FROM users WHERE year > 2008 GROUP BY year ORDER BY year")
            st.plotly_chart(px.area(df_years, x='year', y='count', color_discrete_sequence=['#ff4b4b']), use_container_width=True)
        with col2:
            st.subheader("🏙️ Top Ciudades")
            df_cities = load_data("SELECT location, COUNT(*) as count FROM users WHERE location IS NOT NULL AND location != '' GROUP BY location ORDER BY count DESC LIMIT 7")
            st.plotly_chart(plot_city_bar(df_cities), use_container_width=True)
    except Exception as e: st.error(f"Error: {e}")

# --- TAB 2: DEVELOPERS ---
with tab2:
    st.subheader("👥 Explorador de Talento")
    col_f1, col_f2 = st.columns(2)
    with col_f1: min_foll = st.number_input("Mínimo de Seguidores", 0, 5000, 10)
    with col_f2: city_filter = st.text_input("Filtrar por Ciudad (ej. Lima)", "")
    
    query_devs = "SELECT login, name, location, followers, public_repos, h_index, total_stars_received FROM users WHERE followers >= ?"
    params = [min_foll]
    if city_filter:
        query_devs += " AND location LIKE ?"
        params.append(f"%{city_filter}%")
    
    df_devs = load_data(query_devs, params=params).sort_values(by='h_index', ascending=False)
    st.dataframe(df_devs, use_container_width=True, hide_index=True)
    
    st.subheader("🔥 Mapa de Influencia")
    st.plotly_chart(px.scatter(df_devs, x="followers", y="total_stars_received", size="h_index", color="h_index", hover_name="login", log_x=True, log_y=True), use_container_width=True)

# --- TAB 3: REPOSITORIES ---
with tab3:
    st.subheader("📂 Buscador de Proyectos")
    s_query = st.text_input("Buscar por nombre o descripción", "")
    min_s = st.slider("Estrellas mínimas", 0, 5000, 10)
    
    q_repos = "SELECT name, language, stargazers_count, industry_name, description, html_url FROM repos WHERE stargazers_count >= ? AND fork=0"
    p_repos = [min_s]
    if s_query:
        q_repos += " AND (name LIKE ? OR description LIKE ?)"
        p_repos.extend([f"%{s_query}%", f"%{s_query}%"])
    
    df_repos = load_data(q_repos, params=p_repos).sort_values(by='stargazers_count', ascending=False)
    
    if not df_repos.empty:
        # Highlight top 3 cards
        c_top = st.columns(3)
        for i in range(min(3, len(df_repos))):
            r = df_repos.iloc[i]
            with c_top[i]:
                st.markdown(f"""
                <div style="background-color: #161b22; padding: 15px; border-radius: 10px; border: 1px solid #ff4b4b;">
                    <h5><a href='{r['html_url']}' style='color:#ff4b4b; text-decoration:none;'>{r['name']}</a></h5>
                    <p style='font-size:0.8em;'>{r['industry_name'] or 'General'}</p>
                    <b>⭐ {r['stargazers_count']} | {r['language']}</b>
                </div>
                """, unsafe_allow_html=True)
        st.dataframe(df_repos, use_container_width=True, hide_index=True)

# --- TAB 4: INDUSTRIES ---
with tab4:
    st.subheader("🏭 Análisis por Sectores Económicos")
    df_ind = load_data("SELECT industry_name, COUNT(*) as count FROM repos WHERE industry_name IS NOT NULL AND industry_name != '' GROUP BY industry_name ORDER BY count DESC")
    st.plotly_chart(px.pie(df_ind, values='count', names='industry_name', hole=.4, title="Distribución CIIU"), use_container_width=True)

# --- TAB 5: LANGUAGES ---
with tab5:
    st.subheader("💻 Distribución de Tecnologías")
    df_l = load_data("SELECT language, COUNT(*) as count FROM repos WHERE language IS NOT NULL AND fork=0 GROUP BY language ORDER BY count DESC LIMIT 15")
    st.plotly_chart(px.bar(df_l, x='count', y='language', orientation='h', color='count', color_continuous_scale='Reds'), use_container_width=True)

# --- TAB 6: AI ANALYST ---
with tab6:
    st.subheader("🤖 AI Data Analyst")
    user_q = st.text_input("Pregunta algo sobre el ecosistema dev peruano:", placeholder="¿Quién es el desarrollador más influyente en Python?")
    if user_q:
        with st.spinner("Pensando..."):
            try:
                from src.agents.classification_agent import PeruAnalystAgent
                agent = PeruAnalystAgent()
                answer = agent.ask(user_q)
                st.markdown(answer)
            except Exception as e:
                st.error(f"Error en el Agente: {e}")

st.sidebar.info("Dashboard Unificado v2.0")
st.sidebar.markdown("Hecho por Cristina Cece")
