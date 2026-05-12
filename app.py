import streamlit as st
from utils.helpers import set_page_config, apply_custom_css
from modules.chat import show_chat_module
from modules.identifier import show_identifier_module
from modules.test_explainer import show_test_explainer_module
from modules.panel_simulator import show_panel_simulator_module
from modules.amr_tracker import show_amr_tracker_module
from modules.pcr_guide import show_pcr_guide_module
from modules.media_guide import show_media_guide_module
from modules.pathogen_library import show_pathogen_library_module
from modules.infection_control import show_infection_control_module

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
            "🦠 Organism Identifier",
            "🧪 Lab Test Explainer",
            "⚗️ Biochemical Panel Simulator",
            "💊 AMR Tracker",
            "🔬 PCR Guide",
            "🧫 Culture Media Guide",
            "📖 Pathogen Library",
            "🏥 Infection Control",
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
elif "Organism Identifier" in selected_module:
    show_identifier_module()
elif "Lab Test Explainer" in selected_module:
    show_test_explainer_module()
elif "Biochemical Panel Simulator" in selected_module:
    show_panel_simulator_module()
elif "AMR Tracker" in selected_module:
    show_amr_tracker_module()
elif "PCR Guide" in selected_module:
    show_pcr_guide_module()
elif "Culture Media Guide" in selected_module:
    show_media_guide_module()
elif "Pathogen Library" in selected_module:
    show_pathogen_library_module()
elif "Infection Control" in selected_module:
    show_infection_control_module()
else:
    st.markdown("""
        <div style="
            text-align: center;
            padding: 80px 20px;
            color: #B0C4CE;
        ">
            <h2 style="color: #25B89A;">🚧 Coming Soon</h2>
            <p>This module is currently under development.</p>
            <p>All other modules are available in the sidebar.</p>
        </div>
    """, unsafe_allow_html=True)