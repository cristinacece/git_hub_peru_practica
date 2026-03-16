import streamlit as st
import os
from PIL import Image

st.set_page_config(page_title="GitHub Peru Analytics", page_icon="🇵🇪", layout="wide")

st.title("🇵🇪 GitHub Peru Analytics")
st.markdown("""
### Welcome to the most comprehensive analysis of the Peruvian developer ecosystem!

This platform provides deep insights into how software development is evolving in Peru, 
leveraging data from thousands of repositories and developers across the country.

**Use the sidebar to explore:**
- **📊 Overview**: High-level KPIs and trends.
- **👥 Talent Hunter**: Discover top-tier developers and influence metrics.
- **📂 Repository Explorer**: Search and filter through thousands of Peruvian projects.
- **🏭 Industry Analysis**: See how AI classifies local software into economic sectors.
- **💻 Languages**: Detailed breakdown of the technologies powering our community.
- **🤖 AI Data Analyst**: Ask natural language questions to our system.

---
Created by **Cristina Cece** as part of the QLAB Prompt Engineering Course.
""")

# Optional feature image
# if os.path.exists("demo/screenshots/overview.png"):
#     st.image("demo/screenshots/overview.png", caption="Dashboard Preview")
