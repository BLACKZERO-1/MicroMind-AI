import streamlit as st

def set_page_config():
    st.set_page_config(
        page_title="MicroMind AI",
        page_icon="🧬",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def apply_custom_css():
    st.markdown("""
        <style>
        /* Main background */
        .stApp {
            background-color: #0D1B2A;
            color: #FFFFFF;
        }
        
        /* Sidebar */
        [data-testid="stSidebar"] {
            background-color: #1A2B3C;
            border-right: 1px solid #1B7F7F;
        }
        
        /* Headers */
        h1, h2, h3 {
            color: #25B89A;
        }
        
        /* Input boxes */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea {
            background-color: #1A2B3C;
            color: #FFFFFF;
            border: 1px solid #1B7F7F;
            border-radius: 8px;
        }
        
        /* Buttons */
        .stButton > button {
            background-color: #1B7F7F;
            color: #FFFFFF;
            border: none;
            border-radius: 8px;
            padding: 0.5rem 1.5rem;
            font-weight: bold;
            transition: background-color 0.3s;
        }
        
        .stButton > button:hover {
            background-color: #25B89A;
            color: #0D1B2A;
        }
        
        /* Chat messages */
        .user-message {
            background-color: #1B7F7F;
            padding: 12px 16px;
            border-radius: 12px 12px 4px 12px;
            margin: 8px 0;
            color: white;
            max-width: 80%;
            margin-left: auto;
        }
        
        .assistant-message {
            background-color: #1A2B3C;
            padding: 12px 16px;
            border-radius: 12px 12px 12px 4px;
            margin: 8px 0;
            color: white;
            max-width: 80%;
            border-left: 3px solid #25B89A;
        }
        
        /* Cards */
        .info-card {
            background-color: #1A2B3C;
            border: 1px solid #1B7F7F;
            border-radius: 12px;
            padding: 16px;
            margin: 8px 0;
        }
        
        /* Selectbox */
        .stSelectbox > div > div {
            background-color: #1A2B3C;
            color: #FFFFFF;
            border: 1px solid #1B7F7F;
        }

        /* Hide streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)

def show_header(title: str, subtitle: str = ""):
    st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #0D1B2A, #1B7F7F);
            padding: 24px;
            border-radius: 12px;
            margin-bottom: 24px;
            border-left: 4px solid #25B89A;
        ">
            <h1 style="color: #25B89A; margin: 0; font-size: 28px;">🧬 {title}</h1>
            <p style="color: #B0C4CE; margin: 8px 0 0 0; font-size: 14px;">{subtitle}</p>
        </div>
    """, unsafe_allow_html=True)

def show_info_card(content: str, icon: str = "ℹ️"):
    st.markdown(f"""
        <div class="info-card">
            {icon} {content}
        </div>
    """, unsafe_allow_html=True)