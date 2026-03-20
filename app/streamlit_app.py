import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.retriever_pipeline.rag_chain import invoke_agent
import uuid
import time
import streamlit as st # type: ignore


st.set_page_config(page_title="AAFAPHI", page_icon="🦜")
st.title("🦜 Chat with AAFAPHI ")


with st.sidebar:

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("data/images/AAFAPHI.png", width=120)   

    st.markdown("<h2 style='text-align: center;'>AAFAPHI</h2>", unsafe_allow_html=True)
    st.caption(" Assistant IA pour la Santé Publique au Maroc")


    with st.expander("ℹ️ À propos", expanded=False):
        st.markdown("""
        **AAFAPHI** est un assistant intelligent spécialisé
        dans la santé publique au Maroc.

        Il répond à vos questions sur :
        -  Les vaccins et calendrier vaccinal
        -  L'assurance maladie (AMO / RAMED)
        -  Les maladies infectieuses
        -  Les textes législatifs
        """)


    
    if st.button(" Réinitialiser la conversation", use_container_width=True):
        st.session_state.messages  = []
        st.session_state.thread_id = str(uuid.uuid4())
        st.rerun()

    
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())  # one per session

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Posez votre question..."):

    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Recherche en cours..."):
            result = invoke_agent(
                question=prompt,
                thread_id=st.session_state.thread_id )
        st.markdown(result['messages'][-1].content)

    st.session_state.messages.append({
        "role":    "assistant",
        "content": result['messages'][-1].content})
