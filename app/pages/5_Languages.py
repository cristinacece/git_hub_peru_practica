import streamlit as st
import pandas as pd
from app.utils import load_data
from app.components.charts import plot_language_pie

st.set_page_config(page_title="Language Distribution", page_icon="💻", layout="wide")

st.title("💻 Language Distribution")

df_lang = load_data("SELECT language, COUNT(*) as count FROM repos WHERE language IS NOT NULL GROUP BY language ORDER BY count DESC")

if df_lang.empty:
    st.warning("No data found.")
else:
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Market share")
        st.plotly_chart(plot_language_pie(df_lang), use_container_width=True)
    with col2:
        st.subheader("Data Table")
        st.dataframe(df_lang, use_container_width=True, hide_index=True)

    st.subheader("Top Projects by Language")
    selected_lang = st.selectbox("Select a language to see top repos", df_lang['language'].tolist())
    df_top = load_data("SELECT full_name, stargazers_count, forks_count, description FROM repos WHERE language = ? ORDER BY stargazers_count DESC LIMIT 10", (selected_lang,))
    st.table(df_top)
