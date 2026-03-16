import streamlit as st
import pandas as pd
import plotly.express as px
from app.utils import load_data
from app.components.charts import plot_growth_trend, plot_language_pie, plot_city_bar

st.set_page_config(page_title="PE GitHub Peru Analytics", page_icon="🇵🇪", layout="wide")

# Custom CSS for premium feel
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stMetric {
        background-color: #161b22;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #30363d;
    }
    div[data-testid="stExpander"] {
        border: none;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🇵🇪 GitHub Peru Analytics")
st.markdown("### El centro de inteligencia del ecosistema dev peruano")

# --- FIRST ROW: KPIs ---
try:
    users_count = load_data("SELECT COUNT(*) as count FROM users")['count'][0]
    repos_count = load_data("SELECT COUNT(*) as count FROM repos WHERE fork=0")['count'][0]
    total_stars = load_data("SELECT SUM(stargazers_count) as total FROM repos WHERE fork=0")['total'][0]
    avg_h = load_data("SELECT AVG(h_index) as avg_h FROM users WHERE h_index > 0")['avg_h'][0]

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("👩‍💻 Desarrolladores", f"{users_count:,}")
    with c2:
        st.metric("📦 Proyectos Propios", f"{repos_count:,}")
    with c3:
        st.metric("⭐ Estrellas Totales", f"{total_stars:,}")
    with c4:
        st.metric("🏆 H-Index Promedio", f"{avg_h:.2f}")

    st.divider()

    # --- SECOND ROW: MAIN ANALYTICS ---
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("📈 Evolución de la Comunidad")
        df_years = load_data("SELECT year, COUNT(*) as count FROM users WHERE year > 2008 GROUP BY year ORDER BY year")
        fig_growth = px.area(df_years, x='year', y='count', 
                            title="Nuevos desarrolladores por año",
                            color_discrete_sequence=['#ff4b4b'])
        fig_growth.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_growth, use_container_width=True)

    with col2:
        st.subheader("🏙️ Top Ciudades")
        df_cities = load_data("SELECT location, COUNT(*) as count FROM users WHERE location IS NOT NULL GROUP BY location ORDER BY count DESC LIMIT 7")
        st.plotly_chart(plot_city_bar(df_cities), use_container_width=True)

    st.divider()

    # --- THIRD ROW: LANGUAGES & CORRELATION ---
    col3, col4 = st.columns(2)

    with col3:
        st.subheader("💻 Dominio Tecnológico")
        df_lang = load_data("SELECT language, COUNT(*) as count FROM repos WHERE fork=0 AND language IS NOT NULL GROUP BY language ORDER BY count DESC LIMIT 8")
        st.plotly_chart(plot_language_pie(df_lang), use_container_width=True)

    with col4:
        st.subheader("🔥 Correlación: Estrellas vs Seguidores")
        df_corr = load_data("SELECT followers, total_stars_received, h_index, login FROM users WHERE followers > 5 AND total_stars_received > 5")
        fig_corr = px.scatter(df_corr, x="followers", y="total_stars_received", 
                             size="h_index", color="h_index",
                             hover_name="login", log_x=True, log_y=True,
                             color_continuous_scale="Viridis",
                             title="Impacto vs Popularidad (Log Scale)")
        st.plotly_chart(fig_corr, use_container_width=True)

except Exception as e:
    st.error(f"Error cargando datos: {e}")
    st.info("Asegúrate de que la base de datos 'data/github_peru.db' existe y tiene datos.")

st.sidebar.success("Navega a las páginas para análisis específicos.")
st.sidebar.markdown("---")
st.sidebar.info("Este dashboard es parte de la Tarea 2 - QLAB Prompt Engineering.")
