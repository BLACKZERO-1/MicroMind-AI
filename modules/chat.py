import streamlit as st
from utils.api_client import ask_claude_with_history
from utils.helpers import show_header, show_info_card

SYSTEM_PROMPT = """You are MicroMind AI — an expert microbiology and life sciences assistant. 
You were built by Badar Islam, a BS Microbiology graduate with real laboratory experience at 
the National Institute of Health (NIH) Islamabad, Alpha Genomics, and NARC.

Your expertise covers:
- Microbiology — bacteria, fungi, viruses, parasites
- Clinical diagnostics — ELISA, PCR, gram staining, biochemical tests, antimicrobial sensitivity
- Molecular biology — DNA extraction, gel electrophoresis, genomic sequencing
- Biochemistry — metabolic pathways, enzyme activity, biochemical reactions
- Public health — infection control, outbreak management, biosafety
- Laboratory techniques — culture media, microscopy, staining methods

Your communication style:
- Clear, accurate, and educational
- Use proper scientific terminology but explain it when needed
- Give practical, lab-relevant answers
- When explaining tests or results, include what the result means clinically
- Be concise but thorough
- If asked something outside life sciences, politely redirect to your specialty

Always respond as a knowledgeable lab companion — not just a textbook."""

SUGGESTED_QUESTIONS = [
    {"icon": "🦠", "label": "Gram staining?", "full": "What is gram staining and how does it work?"},
    {"icon": "🧪", "label": "How does ELISA work?", "full": "How does ELISA work and what does a positive result mean?"},
    {"icon": "🔬", "label": "What is PCR?", "full": "What is PCR used for in microbiology?"},
    {"icon": "💊", "label": "What is MRSA?", "full": "What is MRSA and why is it dangerous?"},
    {"icon": "🧫", "label": "Culture media types?", "full": "What are the different types of culture media used in microbiology?"},
    {"icon": "⚗️", "label": "Biochemical tests?", "full": "What are the common biochemical tests used to identify bacteria?"},
]

def process_question(question: str):
    st.session_state.messages_display.append({
        "role": "user",
        "content": question
    })
    st.session_state.chat_history.append({
        "role": "user",
        "content": question
    })

    response = ask_claude_with_history(
        system_prompt=SYSTEM_PROMPT,
        conversation_history=st.session_state.chat_history
    )

    st.session_state.messages_display.append({
        "role": "assistant",
        "content": response
    })
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": response
    })

def show_chat_module():
    show_header(
        "Ask Anything — Microbiology Chat",
        "Your intelligent microbiology companion — ask any question about microbes, lab tests, techniques, or life sciences"
    )

    # Initialize session state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "messages_display" not in st.session_state:
        st.session_state.messages_display = []

    # Suggested questions
    st.markdown("### 💡 Quick Questions:")
    cols = st.columns(3)
    for i, q in enumerate(SUGGESTED_QUESTIONS):
        with cols[i % 3]:
            if st.button(f"{q['icon']} {q['label']}", key=f"sq_{i}", use_container_width=True):
                with st.spinner("MicroMind AI is thinking..."):
                    process_question(q["full"])
                st.rerun()

    st.markdown("---")

    # Display chat history
    for msg in st.session_state.messages_display:
        if msg["role"] == "user":
            st.markdown(f"""
                <div class="user-message">
                    <strong>You</strong><br>{msg["content"]}
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class="assistant-message">
                    <strong>🧬 MicroMind AI</strong><br>{msg["content"]}
                </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # Input area
    col_input, col_btn = st.columns([5, 1])
    with col_input:
        user_input = st.text_input(
            "Ask:",
            placeholder="e.g. What is the difference between gram positive and gram negative bacteria?",
            key="chat_input",
            label_visibility="collapsed"
        )
    with col_btn:
        send_clicked = st.button("Send 🚀", use_container_width=True)

    # Process manual input
    if send_clicked and user_input.strip():
        with st.spinner("MicroMind AI is thinking..."):
            process_question(user_input)
        st.rerun()

    # Clear chat
    if st.session_state.messages_display:
        if st.button("🗑️ Clear Chat"):
            st.session_state.chat_history = []
            st.session_state.messages_display = []
            st.rerun()

    # Empty state
    if not st.session_state.messages_display:
        show_info_card(
            "Start by typing any microbiology question above, or click one of the quick question buttons.",
            "👆"
        )