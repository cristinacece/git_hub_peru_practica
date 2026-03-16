import streamlit as st
import pandas as pd
import os
from PIL import Image

# Configuración de la página
st.set_page_config(
    page_title="GitHub Peru Dashboard",
    page_icon="📊",
    layout="wide"
)

# Estilo personalizado
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    h1 {
        color: #1e3a8a;
        font-family: 'Inter', sans-serif;
    }
    h2 {
        color: #1e40af;
        border-bottom: 2px solid #e5e7eb;
        padding-bottom: 10px;
    }
    .description-box {
        background-color: #eff6ff;
        padding: 20px;
        border-left: 5px solid #3b82f6;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# Encabezado
st.title("🇵🇪 Dashboard: Ecosistema GitHub en Perú")
st.markdown("Analizando el talento, la tecnología y el impacto de los desarrolladores peruanos.")

# Carga de datos para KPIs
@st.cache_data
def load_data():
    users = pd.read_csv("data/users_peru_full.csv")
    repos = pd.read_csv("data/repos_1200_users.csv")
    return users, repos

try:
    df_users, df_repos = load_data()
    
    # Métricas principales
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Usuarios Identificados", f"{len(df_users):,}")
    with col2:
        st.metric("Muestra de Repos", f"{len(df_repos):,}")
    with col3:
        st.metric("Seguidores Totales", f"{df_users['followers'].sum():,}")
    with col4:
        st.metric("Disponibles para Contratar", f"{(df_users['hireable'] == True).sum():,}")

    # Tabs para organizar el Dashboard
    tab1, tab2, tab3 = st.tabs(["👥 Comunidad de Usuarios", "💻 Ecosistema Técnico", "📈 Análisis Estadístico"])

    with tab1:
        st.header("Análisis de la Comunidad")
        
        # Ciudad y Crecimiento
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Distribución por Ciudad")
            st.image("plots/1_top_cities.png", use_container_width=True)
            st.info("Lima domina el ecosistema con mayor concentración, seguida por Arequipa y Trujillo.")
        
        with c2:
            st.subheader("Crecimiento de Usuarios")
            st.image("plots/2_user_growth.png", use_container_width=True)
            st.info("Se observa un crecimiento exponencial a partir de 2018, con un pico de actividad entre 2020 y 2023.")

    with tab2:
        st.header("Lenguajes y Proyectos")
        
        # Lenguajes
        st.subheader("Lenguajes Dominantes")
        st.image("plots/3_top_languages.png")
        st.markdown("""
        <div class="description-box">
        <b>Dato Clave:</b> JavaScript y TypeScript lideran el ranking, confirmando una fuerte tendencia hacia el desarrollo Web moderno. 
        Python se mantiene sólido en tercer lugar como lenguaje preferido para Ciencia de Datos y Backend.
        </div>
        """, unsafe_allow_html=True)
        
        # Proyectos Top
        st.subheader("Proyectos más Populares")
        st.image("plots/5_top_projects.png")
        st.info("Ranking de los proyectos peruanos con mayor reconocimiento internacional (estrellas).")

    with tab3:
        st.header("Estadísticas Avanzadas")
        
        # Heatmap y Correlación
        st.subheader("Correlación de Métricas")
        col_left, col_right = st.columns([2, 1])
        with col_left:
            st.image("plots/dashboard_heatmap_correlation.png", use_container_width=True)
        with col_right:
            st.write("### Hallazgos:")
            st.write("- **Popularidad:** Existe una correlación lineal perfecta entre seguidores y observadores.")
            st.write("- **Independencia:** El éxito de un repo (estrellas) no depende necesariamente de su tamaño en líneas de código.")
            st.write("- **Engagement:** Los forks están fuertemente ligados a las estrellas recibidas.")

        st.divider()
        
        # Evolución de Lenguajes
        st.subheader("Evolución Temporal de Tecnologías")
        st.image("plots/dashboard_stacked_area_languages.png")
        st.markdown("""
        <div class="description-box">
        <b>Tendencia:</b> Este gráfico de 'Cuota de Voz' muestra la transición tecnológica. 
        Note el crecimiento de <b>TypeScript</b> desplazando gradualmente a lenguajes más antiguos en los últimos 5 años.
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        # Stars vs Forks
        st.subheader("Popularidad vs Colaboración")
        st.image("plots/4_stars_vs_forks.png")
        st.caption("Gráfico de dispersión que muestra el equilibrio entre proyectos estelares y proyectos colaborativos.")

except Exception as e:
    st.error(f"Error al cargar los datos o imágenes: {e}")
    st.info("Asegúrate de haber ejecutado los scripts de extracción y generación de gráficos previos.")

# Footer
st.markdown("---")
st.markdown("Dashboard creado por **Antigravity AI** para análisis de QLAB Peru.")
