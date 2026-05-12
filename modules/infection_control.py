import streamlit as st
from utils.api_client import ask_claude
from utils.helpers import show_header, show_info_card

SYSTEM_PROMPT = """You are MicroMind AI — an expert in infection prevention and control, public health, and outbreak management.

You have deep knowledge of:
- WHO infection prevention and control guidelines
- Biosafety levels and laboratory safety
- High consequence pathogens — Ebola, Marburg, SARS-CoV-2, Influenza
- Outbreak investigation methodology
- Healthcare associated infections
- Personal protective equipment
- Antimicrobial stewardship

When given an infection control question:
1. Provide clear, practical, evidence-based guidance
2. Reference WHO or CDC guidelines where relevant
3. Explain the rationale behind each recommendation
4. Give specific, actionable steps
5. Highlight urgent safety concerns
6. Mention relevant regulations or standards

Format your response with these sections:
- KEY RECOMMENDATIONS
- DETAILED GUIDANCE
- RATIONALE AND EVIDENCE BASE
- SPECIFIC ACTION STEPS
- SAFETY CONSIDERATIONS
- RELEVANT GUIDELINES AND STANDARDS

Be practical, safety-focused, and evidence-based.
Think like a senior infection control nurse or public health officer."""

IPC_TOPICS = {
    "🧤 Standard Precautions": [
        "Hand hygiene — WHO 5 moments",
        "Personal protective equipment (PPE) selection",
        "Safe injection practices",
        "Respiratory hygiene and cough etiquette",
        "Safe handling of sharps",
        "Environmental cleaning and disinfection",
        "Waste management in healthcare",
        "Linen and laundry management",
    ],
    "🏥 Transmission Based Precautions": [
        "Contact precautions — when and how",
        "Droplet precautions",
        "Airborne precautions",
        "Combined precautions",
        "Patient placement and room requirements",
        "Visitor management during precautions",
        "Removing precautions safely",
    ],
    "⚠️ High Consequence Pathogens": [
        "Ebola virus disease — IPC measures",
        "Marburg virus — IPC measures",
        "SARS-CoV-2 — IPC in healthcare",
        "Influenza pandemic preparedness",
        "Monkeypox IPC guidance",
        "Lassa fever IPC",
        "Middle East Respiratory Syndrome (MERS)",
        "Managing suspected viral hemorrhagic fever",
    ],
    "🔬 Laboratory Biosafety": [
        "Biosafety levels 1 through 4 explained",
        "Laboratory safety practices BSL-2",
        "Biosafety cabinet usage and classes",
        "Personal protective equipment in the lab",
        "Handling infectious specimens safely",
        "Spill management in the microbiology lab",
        "Sharps and needlestick injury management",
        "Transport of infectious substances",
    ],
    "📊 Outbreak Investigation": [
        "Steps of outbreak investigation",
        "Case definition — how to write one",
        "Epidemic curve — construction and interpretation",
        "Contact tracing methodology",
        "Source identification",
        "Control measures implementation",
        "Communicating outbreak findings",
        "COVID-19 outbreak investigation",
    ],
    "🏨 Healthcare Associated Infections": [
        "Catheter associated urinary tract infections (CAUTI)",
        "Central line associated bloodstream infections (CLABSI)",
        "Surgical site infections (SSI)",
        "Ventilator associated pneumonia (VAP)",
        "Clostridioides difficile infections",
        "MRSA in healthcare settings",
        "Hand hygiene compliance strategies",
        "Antimicrobial stewardship programs",
    ],
    "💉 Vaccination and Prevention": [
        "Healthcare worker vaccination requirements",
        "Post exposure prophylaxis (PEP)",
        "Pre-exposure prophylaxis (PrEP)",
        "Immunocompromised patient protection",
        "Outbreak response vaccination",
    ],
}

BIOSAFETY_LEVELS = {
    "BSL-1": "Basic laboratory — organisms not known to cause disease in healthy adults",
    "BSL-2": "Standard microbiology lab — moderate risk agents — most clinical labs",
    "BSL-3": "Clinical and research — serious or lethal agents — TB, Anthrax",
    "BSL-4": "Maximum containment — dangerous exotic agents — Ebola, Marburg",
}

def show_infection_control_module():
    show_header(
        "Infection Control and Public Health",
        "WHO-aligned guidance on infection prevention, biosafety, outbreak investigation, and public health"
    )

    st.markdown("""
        <div style="background:#1A2B3C; border-left:4px solid #25B89A;
                    padding:12px; border-radius:8px; margin-bottom:16px;">
            <p style="color:#B0C4CE; margin:0; font-size:13px;">
                💡 Based on WHO and CDC infection prevention and control guidelines. 
                Browse by topic, explore biosafety levels, or ask any infection control question.
            </p>
        </div>
    """, unsafe_allow_html=True)

    mode = st.radio(
        "Select Mode",
        ["📚 Browse IPC Topics", "🔬 Biosafety Level Guide", "📊 Outbreak Investigation Tool", "❓ Ask Anything IPC"],
        horizontal=False,
        label_visibility="collapsed"
    )

    st.markdown("---")

    query = ""

    # Mode 1 — Browse Topics
    if "Browse" in mode:
        st.markdown("### 📂 Select Category")
        category = st.selectbox(
            "Category",
            options=list(IPC_TOPICS.keys()),
            label_visibility="collapsed"
        )

        st.markdown("### 📖 Select Topic")
        topic = st.selectbox(
            "Topic",
            options=["-- Select topic --"] + IPC_TOPICS[category],
            label_visibility="collapsed"
        )

        if topic != "-- Select topic --":
            query = f"Provide comprehensive infection prevention and control guidance on: {topic}"

        setting = st.selectbox(
            "Healthcare setting (optional)",
            ["-- All settings --", "Hospital ward", "ICU", "Emergency department", "Outpatient clinic", "Laboratory", "Community setting", "Low resource setting"],
            key="setting"
        )
        if setting != "-- All settings --":
            query += f" in the context of: {setting}"

    # Mode 2 — Biosafety Levels
    elif "Biosafety" in mode:
        st.markdown("### 🔬 Biosafety Level Reference")

        for level, description in BIOSAFETY_LEVELS.items():
            color = {"BSL-1": "#25B89A", "BSL-2": "#F5A623", "BSL-3": "#E05252", "BSL-4": "#8B0000"}[level]
            st.markdown(f"""
                <div style="background:#1A2B3C; border-left:4px solid {color};
                            padding:12px; border-radius:8px; margin-bottom:8px;">
                    <h4 style="color:{color}; margin:0;">{level}</h4>
                    <p style="color:#B0C4CE; margin:4px 0 0 0; font-size:13px;">{description}</p>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### 🔍 Get Detailed Biosafety Information")
        bsl_query = st.selectbox(
            "Select biosafety level for detailed guidance",
            ["-- Select --", "BSL-1 requirements and practices", "BSL-2 requirements and practices",
             "BSL-3 requirements and practices", "BSL-4 requirements and practices",
             "Biosafety cabinet classes and usage", "PPE requirements by biosafety level",
             "Decontamination and disinfection by BSL"],
            key="bsl_query"
        )
        if bsl_query != "-- Select --":
            query = f"Provide detailed guidance on: {bsl_query}"

    # Mode 3 — Outbreak Tool
    elif "Outbreak" in mode:
        st.markdown("### 📊 Outbreak Investigation Tool")
        st.markdown("""
            <div style="background:#1A2B3C; border-left:4px solid #F5A623;
                        padding:12px; border-radius:8px; margin-bottom:16px;">
                <p style="color:#B0C4CE; margin:0; font-size:13px;">
                    💡 Describe your outbreak situation and get step by step investigation guidance.
                </p>
            </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            suspected_disease = st.text_input(
                "Suspected disease or pathogen",
                placeholder="e.g. Salmonella food poisoning, COVID-19, Cholera...",
                key="disease"
            )
            number_of_cases = st.text_input(
                "Approximate number of cases",
                placeholder="e.g. 15 cases, 3 deaths...",
                key="cases"
            )
        with col2:
            setting_outbreak = st.selectbox(
                "Outbreak setting",
                ["-- Select --", "Hospital", "School", "Community", "Food establishment", "Workplace", "Refugee camp", "Prison"],
                key="outbreak_setting"
            )
            time_period = st.text_input(
                "Time period",
                placeholder="e.g. Last 3 days, past 2 weeks...",
                key="time_period"
            )

        symptoms = st.text_area(
            "Main symptoms reported",
            placeholder="e.g. Fever, vomiting, diarrhea, onset 6-12 hours after eating at school cafeteria...",
            height=80,
            key="symptoms"
        )

        if suspected_disease or symptoms:
            query = "Help me investigate this outbreak:\n"
            if suspected_disease:
                query += f"Suspected disease: {suspected_disease}\n"
            if number_of_cases:
                query += f"Number of cases: {number_of_cases}\n"
            if setting_outbreak != "-- Select --":
                query += f"Setting: {setting_outbreak}\n"
            if time_period:
                query += f"Time period: {time_period}\n"
            if symptoms:
                query += f"Symptoms: {symptoms}\n"
            query += "\nProvide step by step outbreak investigation guidance, immediate control measures, and what information to collect."

    # Mode 4 — Ask Anything
    elif "Ask Anything" in mode:
        st.markdown("### ❓ Ask Any Infection Control Question")
        query = st.text_area(
            "Your Question",
            placeholder="""Examples:
- What PPE do I need when collecting samples from a suspected Ebola patient?
- How do I write a case definition for a cholera outbreak?
- What are the WHO hand hygiene 5 moments?
- How do I safely transport infectious specimens?
- What is the difference between disinfection and sterilization?
- How long should healthcare workers isolate after COVID-19 exposure?""",
            height=150,
            key="ipc_question"
        )

    st.markdown("---")

    submit_clicked = st.button("🏥 Get IPC Guidance", use_container_width=True)

    if submit_clicked:
        if not query or not query.strip():
            st.warning("⚠️ Please select a topic or enter your question.")
        else:
            with st.spinner("🏥 Loading infection control guidance..."):
                result = ask_claude(
                    system_prompt=SYSTEM_PROMPT,
                    user_message=query
                )

            st.markdown("---")
            st.markdown("### 🏥 IPC Guidance")
            st.markdown(f"""
                <div style="background:#1A2B3C; border-left:4px solid #25B89A;
                            padding:20px; border-radius:10px;
                            color:#E2E8F0; line-height:1.8; font-size:14px;">
                    {result.replace(chr(10), '<br>')}
                </div>
            """, unsafe_allow_html=True)

            st.markdown("---")
            st.markdown("""
                <div style="background:#0D2B1A; border-left:4px solid #25B89A;
                            padding:12px; border-radius:8px;">
                    <p style="color:#86EFAC; margin:0; font-size:12px;">
                        ⚠️ <b>Note:</b> Always follow your institution's IPC policies and 
                        current WHO/CDC guidelines. During active outbreaks consult 
                        your national public health authority for the latest guidance.
                    </p>
                </div>
            """, unsafe_allow_html=True)

            if "ipc_history" not in st.session_state:
                st.session_state.ipc_history = []
            st.session_state.ipc_history.append({
                "query": query[:80] + "..." if len(query) > 80 else query,
                "result": result
            })

    # History
    if "ipc_history" in st.session_state and len(st.session_state.ipc_history) > 1:
        st.markdown("---")
        st.markdown("### 📋 Previous Queries This Session")
        for item in reversed(st.session_state.ipc_history[:-1]):
            with st.expander(item["query"]):
                st.markdown(item["result"])