import streamlit as st
import pandas as pd
from app.utils import load_data
from app.components.charts import plot_talent_scatter

st.set_page_config(page_title="Talent Hunter", page_icon="👥", layout="wide")

st.title("👥 Talent Hunter")
st.markdown("Find top developers based on influence and community impact.")

# --- Sidebar Filters ---
st.sidebar.subheader("Talent Filters")
all_locations = load_data("SELECT DISTINCT location FROM users WHERE location IS NOT NULL")['location'].tolist()
city = st.sidebar.selectbox("Location Focus", ["All"] + sorted(all_locations))

min_influence = st.sidebar.slider("Minimum Followers", 0, 500, 0)
min_hindex = st.sidebar.slider("Minimum H-Index (High Impact)", 0, 10, 0)

query = """
    SELECT login, name, location, followers, h_index, total_stars_received, repos_per_year 
    FROM users 
    WHERE followers >= ? AND h_index >= ?
"""
params = [min_influence, min_hindex]

if city != "All":
    query += " AND location = ?"
    params.append(city)

df = load_data(query, params=params)

if not df.empty:
    df = df.sort_values(by='total_stars_received', ascending=False)
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Selected Talent pool", f"{len(df)}")
    c2.metric("Avg H-Index", f"{df['h_index'].mean():.1f}")
    c3.metric("Avg Follower Count", f"{int(df['followers'].mean())}")
    
    st.dataframe(
        df,
        column_config={
            "login": "GitHub User",
            "h_index": "Influence (h)",
            "total_stars_received": "⭐ Total Stars",
            "repos_per_year": "🚀 Velocity (repos/yr)"
        },
        hide_index=True,
        use_container_width=True
    )
    
    st.subheader("Influence vs. Output Velocity")
    st.plotly_chart(plot_talent_scatter(df), use_container_width=True)
else:
    st.warning("No developers found with these specific qualities.")
