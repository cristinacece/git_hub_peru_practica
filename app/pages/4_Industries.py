import streamlit as st
import pandas as pd
from app.utils import load_data
from app.components.charts import plot_industry_pie

st.set_page_config(page_title="Industry Analysis", page_icon="🏭", layout="wide")

st.title("🏭 Industry Analysis (AI)")

df_industry = load_data("""
    SELECT industry_name, COUNT(*) as count 
    FROM repos 
    WHERE industry_name IS NOT NULL AND industry_name != ''
    GROUP BY industry_name 
    ORDER BY count DESC
""")

if df_industry.empty:
    st.warning("No repositories have been classified yet.")
else:
    st.plotly_chart(plot_industry_pie(df_industry), use_container_width=True)
    
    st.subheader("Repository Details")
    st.dataframe(load_data("SELECT full_name, industry_name, reasoning FROM repos WHERE industry_name IS NOT NULL LIMIT 50"), use_container_width=True)
