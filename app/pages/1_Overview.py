import streamlit as st
import pandas as pd
from app.utils import get_connection, load_data
from app.components.charts import plot_growth_trend, plot_engagement_scatter, plot_language_pie, plot_city_bar

st.set_page_config(page_title="Ecosystem Overview", page_icon="📊", layout="wide")

st.title("📊 Ecosystem Overview")

# KPIs
users_count = load_data("SELECT COUNT(*) as count FROM users")['count'][0]
repos_count = load_data("SELECT COUNT(*) as count FROM repos")['count'][0]
total_stars = load_data("SELECT SUM(stargazers_count) as total FROM repos WHERE fork=0")['total'][0]

c1, c2, c3 = st.columns(3)
c1.metric("Identified Developers", f"{users_count:,}")
c2.metric("Total Repositories", f"{repos_count:,}")
c3.metric("Total Ecosystem Stars", f"{total_stars:,}")

st.divider()

col1, col2 = st.columns(2)
with col1:
    st.subheader("Community Growth")
    df_years = load_data("SELECT year, COUNT(*) as count FROM users GROUP BY year ORDER BY year")
    st.plotly_chart(plot_growth_trend(df_years), use_container_width=True)

with col2:
    st.subheader("Stars vs Forks Intensity")
    df_scatter = load_data("""
        SELECT stargazers_count, forks_count, language, name 
        FROM repos 
        WHERE stargazers_count > 5 AND fork=0
    """)
    st.plotly_chart(plot_engagement_scatter(df_scatter), use_container_width=True)

st.divider()

c_bot1, c_bot2 = st.columns(2)
with c_bot1:
    st.subheader("Language Market Share")
    df_lang = load_data("SELECT language, COUNT(*) as count FROM repos GROUP BY language ORDER BY count DESC LIMIT 8")
    st.plotly_chart(plot_language_pie(df_lang), use_container_width=True)

with c_bot2:
    st.subheader("Geographic Distribution")
    df_cities = load_data("SELECT location, COUNT(*) as count FROM users WHERE location IS NOT NULL GROUP BY location ORDER BY count DESC LIMIT 8")
    st.plotly_chart(plot_city_bar(df_cities), use_container_width=True)
