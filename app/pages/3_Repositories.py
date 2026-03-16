import streamlit as st
import pandas as pd
from app.utils import load_data

st.set_page_config(page_title="Repository Explorer", page_icon="📂", layout="wide")

st.title("📂 Explorador de Proyectos")
st.markdown("Busca y descubre los proyectos más impactantes del ecosistema peruano.")

# --- SIDEBAR FILTERS ---
st.sidebar.header("🔍 Filtros de Búsqueda")
search_query = st.sidebar.text_input("Palabra clave (nombre o desc.)", "")

# Languages multi-select with search
langs_df = load_data("SELECT DISTINCT language FROM repos WHERE language IS NOT NULL AND language != ''")
selected_langs = st.sidebar.multiselect("Lenguajes", sorted(langs_df['language'].tolist()))

# Industries
industries_df = load_data("SELECT DISTINCT industry_name FROM repos WHERE industry_name IS NOT NULL AND industry_name != ''")
selected_industries = st.sidebar.multiselect("Sectores (Clasificados por AI)", sorted(industries_df['industry_name'].tolist()))

min_stars = st.sidebar.select_slider("Mínimo de Estrellas ⭐", options=[0, 10, 50, 100, 500, 1000], value=0)

# --- DATA QUERYING ---
query = "SELECT name, full_name, language, stargazers_count, forks_count, industry_name, description, html_url FROM repos WHERE stargazers_count >= ?"
params = [min_stars]

if search_query:
    query += " AND (name LIKE ? OR description LIKE ?)"
    params.extend([f"%{search_query}%", f"%{search_query}%"])

if selected_langs:
    placeholders = ', '.join(['?'] * len(selected_langs))
    query += f" AND language IN ({placeholders})"
    params.extend(selected_langs)
    
if selected_industries:
    placeholders = ', '.join(['?'] * len(selected_industries))
    query += f" AND industry_name IN ({placeholders})"
    params.extend(selected_industries)

df = load_data(query, params=params)

# --- DISPLAY ---
if df.empty:
    st.warning("No se encontraron proyectos con esos criterios. Prueba quitando filtros.")
else:
    df = df.sort_values(by='stargazers_count', ascending=False)
    
    st.subheader(f"Encontrados: {len(df)} repositorios")
    
    # --- HIGHLIGHT CARDS (Top 3) ---
    if not search_query and not selected_langs and len(df) >= 3:
        st.write("### 🏆 Proyectos Destacados")
        top_cols = st.columns(3)
        for i in range(3):
            repo = df.iloc[i]
            with top_cols[i]:
                st.markdown(f"""
                <div style="background-color: #161b22; padding: 20px; border-radius: 10px; border: 1px solid #ff4b4b; height: 200px">
                    <h4 style="margin-top: 0;"><a href="{repo['html_url']}" target="_blank" style="text-decoration: none; color: #ff4b4b;">{repo['name']}</a></h4>
                    <p style="font-size: 0.8em; color: #8b949e;">{repo['description'][:100] if repo['description'] else 'Sin descripción'}...</p>
                    <div style="margin-top: 10px;">
                        <span style="background-color: #21262d; padding: 4px 8px; border-radius: 12px; font-size: 0.7em;">⭐ {repo['stargazers_count']}</span>
                        <span style="background-color: #21262d; padding: 4px 8px; border-radius: 12px; font-size: 0.7em;">🍴 {repo['forks_count']}</span>
                        <span style="background-color: #21262d; padding: 4px 8px; border-radius: 12px; font-size: 0.7em;">💻 {repo['language']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        st.divider()

    # --- FULL DATA TABLE ---
    st.dataframe(
        df,
        column_config={
            "html_url": st.column_config.LinkColumn("GitHub Link"),
            "full_name": "Repositorio",
            "stargazers_count": "⭐",
            "forks_count": "🍴",
            "industry_name": "Sector Económico",
            "description": "Descripción"
        },
        use_container_width=True,
        hide_index=True
    )
