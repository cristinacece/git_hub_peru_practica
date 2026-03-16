import streamlit as st
from src.agents.classification_agent import PeruAnalystAgent

st.set_page_config(page_title="AI Data Analyst", page_icon="🤖", layout="wide")

st.title("🤖 AI Data Analyst")
st.write("Ask questions about the Peruvian GitHub ecosystem.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ex: Who are the top Python developers in Lima?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        agent = PeruAnalystAgent()
        response = agent.ask(prompt)
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
