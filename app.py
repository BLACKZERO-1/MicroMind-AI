import streamlit as st
from utils.helpers import set_page_config, apply_custom_css
from modules.chat import show_chat_module

# Page config - must be first streamlit command
set_page_config()
apply_custom_css()

# Sidebar navigation
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; padding: 20px 0;">
            <h1 style="color: #25B89A; font-size: 24px; margin: 0;">🧬 MicroMind AI</h1>
            <p style="color: #B0C4CE; font-size: 12px; margin: 4px 0 0 0;">
                Intelligent Microbiology Assistant
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 📚 Modules")
    
    selected_module = st.selectbox(
        "Select Module",
        options=[
            "🧬 Ask Anything Chat",
            "🦠 Organism Identifier (Coming Soon)",
            "🧪 Lab Test Explainer (Coming Soon)",
            "💊 AMR Tracker (Coming Soon)",
            "🔬 PCR Guide (Coming Soon)",
            "🍽️ Culture Media Guide (Coming Soon)",
            "📖 Pathogen Library (Coming Soon)",
            "🏥 Infection Control (Coming Soon)",
            "📊 Learning Dashboard (Coming Soon)",
        ],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    st.markdown("""
        <div style="
            background-color: #1A2B3C;
            border: 1px solid #1B7F7F;
            border-radius: 8px;
            padding: 12px;
            margin-top: 8px;
        ">
            <p style="color: #25B89A; font-size: 12px; margin: 0; font-weight: bold;">
                Built by Badar Islam
            </p>
            <p style="color: #B0C4CE; font-size: 11px; margin: 4px 0 0 0;">
                BS Microbiology | NIH Lab Technician<br>
                Aspiring MS — University of Göttingen
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div style="text-align: center; margin-top: 16px;">
            <p style="color: #B0C4CE; font-size: 10px;">Version 1.0 | May 2026</p>
        </div>
    """, unsafe_allow_html=True)

# Main content routing
if "Ask Anything Chat" in selected_module:
    show_chat_module()
else:
    st.markdown("""
        <div style="
            text-align: center;
            padding: 80px 20px;
            color: #B0C4CE;
        ">
            <h2 style="color: #25B89A;">🚧 Coming Soon</h2>
            <p>This module is currently under development.</p>
            <p>Start with the <strong style="color: #25B89A;">Ask Anything Chat</strong> module while we build the rest.</p>
        </div>
    """, unsafe_allow_html=True)