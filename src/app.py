import streamlit as st
import os
from router import get_router_engine

# --- Page Config ---
st.set_page_config(
    page_title="Enterprise Analyst",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for "Pro" UI ---
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background-color: #0E1117;
    }
    
    /* Chat Message Bubbles */
    .stChatMessage {
        background-color: transparent;
        border: none;
    }
    
    /* User Message Style */
    div[data-testid="stChatMessage"]:nth-child(odd) {
        background-color: #1E2329;
        border-left: 5px solid #00ADB5;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
    }
    
    /* Assistant Message Style */
    div[data-testid="stChatMessage"]:nth-child(even) {
        background-color: #262730;
        border-left: 5px solid #FF2B2B;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
    }
    
    /* Input Box styling */
    .stTextInput input {
        color: white;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #161B22;
    }
</style>
""", unsafe_allow_html=True)

# --- Initialize Engine (Cached) ---
@st.cache_resource(show_spinner="Booting up Neural Engines...")
def load_engine():
    return get_router_engine()

# --- Sidebar ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/bot.png", width=80)
    st.title("Enterprise Analyst")
    st.markdown("---")
    st.markdown("### 🟢 System Status")
    st.success("SQL Engine: **Online**")
    st.success("Vector Database: **Online**")
    st.markdown("---")
    st.markdown("### 💡 Example Queries")
    st.code("Total spend on AWS?", language=None)
    st.code("Why is Q3 marketing high?", language=None)
    st.code("List all vendors in IT.", language=None)
    st.markdown("---")
    st.markdown("v1.0.0 | Built with LlamaIndex")

# --- Main Interface ---
st.title("⚡ Conversational BI Agent")
st.markdown("##### *Hybrid Retrieval: SQL (Structured) + Vector (Unstructured)*")
st.divider()

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Ready. Accessing secure financial data and strategic reports."}
    ]

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="👤" if message["role"] == "user" else "🤖"):
        st.markdown(message["content"])

# Handle User Input
if prompt := st.chat_input("Enter your query here..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # Generate Response
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Processing query..."):
            try:
                engine = load_engine()
                response = engine.query(prompt)
                st.markdown(str(response))
                st.session_state.messages.append({"role": "assistant", "content": str(response)})
            except Exception as e:
                error_msg = f"⚠️ System Error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})