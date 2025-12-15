import streamlit as st
import os
from router import get_router_engine

# --- Page Config ---
st.set_page_config(
    page_title="Enterprise Conversational Analyst",
    page_icon="📊",
    layout="centered"
)

# --- Header ---
st.title("📊 Enterprise Analyst Agent")
st.markdown("ask me about **Financial Data** (SQL) or **Strategic Documents** (Vector).")

# --- Initialize Session State ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I have access to your database and PDF reports. How can I help?"}
    ]

# --- Cache the Engine ---
# We cache this so we don't reload the database connection on every message
@st.cache_resource
def load_engine():
    return get_router_engine()

try:
    engine = load_engine()
except Exception as e:
    st.error(f"Failed to load engine: {e}")
    st.stop()

# --- Chat Interface ---
# 1. Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 2. Handle User Input
if prompt := st.chat_input("Ex: 'Total AWS spend?' or 'What is the Q3 strategy?'"):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Response
    with st.chat_message("assistant"):
        with st.spinner("Analyzing..."):
            try:
                # The Router decides SQL vs Vector here
                response = engine.query(prompt)
                st.markdown(str(response))
                
                # Add assistant message to history
                st.session_state.messages.append({"role": "assistant", "content": str(response)})
            except Exception as e:
                st.error(f"An error occurred: {e}")