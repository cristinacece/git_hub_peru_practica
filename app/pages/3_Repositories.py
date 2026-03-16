import streamlit as st
import pandas as pd
from app.utils import load_data

st.set_page_config(page_title="Repository Explorer", page_icon="📂", layout="wide")

st.title("📂 Repository Explorer")
st.markdown("Search and discover impactful projects from the Peruvian ecosystem.")

# --- Sidebar Filters ---
st.sidebar.subheader("Filters")
search_query = st.sidebar.text_input("🔍 Search by name or description", "")

langs_df = load_data("SELECT DISTINCT language FROM repos WHERE language IS NOT NULL AND language != ''")
selected_langs = st.sidebar.multiselect("Select Languages", langs_df['language'].tolist())

industries_df = load_data("SELECT DISTINCT industry_name FROM repos WHERE industry_name IS NOT NULL AND industry_name != ''")
selected_industries = st.sidebar.multiselect("Select Industries", industries_df['industry_name'].tolist())

min_stars = st.sidebar.slider("Minimum Stars", 0, 1000, 0)

# --- Data Querying ---
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

if df.empty:
    st.info("No repositories found matching those criteria.")
else:
    st.subheader(f"Found {len(df)} repositories")
    df_display = df.sort_values(by='stargazers_count', ascending=False)
    
    st.dataframe(
        df_display[['full_name', 'language', 'stargazers_count', 'forks_count', 'industry_name', 'description']],
        column_config={
            "full_name": st.column_config.TextColumn("Repository"),
            "stargazers_count": st.column_config.NumberColumn("⭐ Stars"),
            "forks_count": st.column_config.NumberColumn("🍴 Forks"),
            "industry_name": st.column_config.TextColumn("Industry (AI Classified)"),
        },
        use_container_width=True,
        hide_index=True
    )
    
    c1, c2 = st.columns(2)
    with c1:
        top_lang = df['language'].value_counts().idxmax() if not df['language'].empty else "N/A"
        st.metric("Primary Language in Selection", top_lang)
    with c2:
        avg_stars = round(df['stargazers_count'].mean(), 1)
        st.metric("Average Stars", avg_stars)
