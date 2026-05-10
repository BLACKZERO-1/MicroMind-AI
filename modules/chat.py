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

def show_chat_module():
    show_header(
        "Ask Anything — Microbiology Chat",
        "Your intelligent microbiology companion — ask any question about microbes, lab tests, techniques, or life sciences"
    )

    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "messages_display" not in st.session_state:
        st.session_state.messages_display = []

    # Suggested questions
    st.markdown("### 💡 Try asking:")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🦠 What is gram staining?"):
            st.session_state.quick_question = "What is gram staining and how does it work?"
    with col2:
        if st.button("🧪 How does ELISA work?"):
            st.session_state.quick_question = "How does ELISA work and what does a positive result mean?"
    with col3:
        if st.button("🔬 What is PCR used for?"):
            st.session_state.quick_question = "What is PCR used for in microbiology?"

    st.markdown("---")

    # Display chat history
    chat_container = st.container()
    with chat_container:
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
            "Ask your microbiology question:",
            value=st.session_state.get("quick_question", ""),
            placeholder="e.g. What is the difference between gram positive and gram negative bacteria?",
            key="chat_input",
            label_visibility="collapsed"
        )
    
    with col_btn:
        send_clicked = st.button("Send 🚀", use_container_width=True)

    # Clear quick question after use
    if "quick_question" in st.session_state:
        del st.session_state.quick_question

    # Process input
    if send_clicked and user_input.strip():
        # Add to display history
        st.session_state.messages_display.append({
            "role": "user",
            "content": user_input
        })

        # Add to API history
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_input
        })

        # Get response
        with st.spinner("MicroMind AI is thinking..."):
            response = ask_claude_with_history(
                system_prompt=SYSTEM_PROMPT,
                conversation_history=st.session_state.chat_history
            )

        # Add response to histories
        st.session_state.messages_display.append({
            "role": "assistant",
            "content": response
        })
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": response
        })

        st.rerun()

    # Clear chat button
    if st.session_state.messages_display:
        if st.button("🗑️ Clear Chat"):
            st.session_state.chat_history = []
            st.session_state.messages_display = []
            st.rerun()

    # Empty state
    if not st.session_state.messages_display:
        show_info_card(
            "Start by typing any microbiology question above, or click one of the suggested questions.",
            "👆"
        )