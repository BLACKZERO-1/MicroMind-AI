import streamlit as st
from utils.api_client import ask_claude
from utils.helpers import show_header, show_info_card

SYSTEM_PROMPT = """You are MicroMind AI — an expert molecular biologist specializing in PCR and molecular diagnostic techniques.

Your task is to guide users through PCR protocols, troubleshooting, and result interpretation.

When given a PCR question or problem:
1. Provide clear, practical, step-by-step guidance
2. Explain the molecular basis behind each step
3. For troubleshooting — identify the most likely causes and solutions
4. For protocol questions — give specific conditions and concentrations
5. For result interpretation — explain what each band pattern means
6. Mention quality control considerations
7. Suggest optimization strategies when relevant

Format your response with these sections:
- ANSWER / DIAGNOSIS
- STEP BY STEP GUIDANCE
- MOLECULAR BASIS (why this works)
- TROUBLESHOOTING TIPS
- QUALITY CONTROL CONSIDERATIONS
- OPTIMIZATION SUGGESTIONS

Be practical, specific, and educational.
Think like an experienced molecular biology lab instructor."""

PCR_TOPICS = {
    "🔬 PCR Basics": [
        "What is PCR and how does it work?",
        "PCR components and their roles",
        "Thermal cycling conditions explained",
        "Denaturation, annealing, extension steps",
        "How to set up a PCR master mix",
        "Positive and negative controls in PCR",
        "Different types of PCR — conventional, RT-PCR, qPCR, nested",
    ],
    "⚗️ Protocol Guide": [
        "Standard PCR protocol step by step",
        "RT-PCR protocol for RNA samples",
        "Real-time qPCR protocol",
        "Multiplex PCR setup",
        "Hot start PCR protocol",
        "Colony PCR protocol",
        "Primer design guidelines",
        "Annealing temperature optimization",
    ],
    "🧫 DNA Extraction": [
        "DNA extraction from bacterial culture",
        "DNA extraction from blood sample",
        "DNA extraction from tissue",
        "DNA extraction from swab samples",
        "RNA extraction protocol",
        "Assessing DNA quality and quantity",
        "Common DNA extraction problems",
    ],
    "🔍 Troubleshooting": [
        "No bands on gel — causes and solutions",
        "Faint or weak bands",
        "Multiple non-specific bands",
        "Smearing on gel",
        "Wrong band size",
        "Primer dimer formation",
        "High background signal in qPCR",
        "Inconsistent results between runs",
    ],
    "📊 Result Interpretation": [
        "How to read a gel electrophoresis result",
        "Interpreting band size and intensity",
        "Positive vs negative result interpretation",
        "qPCR Ct value interpretation",
        "Melting curve analysis",
        "What to do with unexpected results",
    ],
    "🧬 Advanced Topics": [
        "SARS-CoV-2 PCR testing explained",
        "Influenza PCR detection",
        "Tuberculosis molecular diagnosis",
        "MRSA molecular detection (mecA gene)",
        "Next Generation Sequencing basics",
        "CRISPR-based diagnostics",
    ],
}

def show_pcr_guide_module():
    show_header(
        "PCR and Molecular Techniques Guide",
        "Complete guide for PCR protocols, troubleshooting, DNA extraction, and result interpretation"
    )

    st.markdown("""
        <div style="background:#1A2B3C; border-left:4px solid #25B89A;
                    padding:12px; border-radius:8px; margin-bottom:16px;">
            <p style="color:#B0C4CE; margin:0; font-size:13px;">
                💡 Browse by topic category, describe your PCR problem for troubleshooting,
                or ask any molecular biology question directly.
            </p>
        </div>
    """, unsafe_allow_html=True)

    mode = st.radio(
        "Select Mode",
        ["📚 Browse Topics", "🔧 Troubleshoot My PCR", "❓ Ask Anything Molecular"],
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
            options=list(PCR_TOPICS.keys()),
            label_visibility="collapsed"
        )

        st.markdown("### 📖 Select Topic")
        topic = st.selectbox(
            "Topic",
            options=["-- Select a topic --"] + PCR_TOPICS[category],
            label_visibility="collapsed"
        )

        if topic != "-- Select a topic --":
            query = topic

        additional = st.text_input(
            "Any specific details? (optional)",
            placeholder="e.g. Using Taq polymerase, target gene is 16S rRNA, sample is clinical blood...",
            key="browse_additional"
        )
        if additional:
            query += f" — specific context: {additional}"

    # Mode 2 — Troubleshoot
    elif "Troubleshoot" in mode:
        st.markdown("### 🔧 Describe Your PCR Problem")

        col1, col2 = st.columns(2)
        with col1:
            problem_type = st.selectbox(
                "What is the problem?",
                [
                    "-- Select problem --",
                    "No bands at all",
                    "Faint/weak bands",
                    "Multiple extra bands",
                    "Smearing",
                    "Wrong band size",
                    "Primer dimers only",
                    "Inconsistent results",
                    "High Ct value in qPCR",
                    "No amplification in positive control",
                    "Amplification in negative control",
                ],
                key="problem_type"
            )
            pcr_type = st.selectbox(
                "PCR type",
                ["-- Select --", "Conventional PCR", "RT-PCR", "qPCR/Real-time", "Multiplex PCR", "Nested PCR"],
                key="pcr_type"
            )

        with col2:
            template_source = st.selectbox(
                "Template source",
                ["-- Select --", "Bacterial DNA", "Human DNA", "RNA/cDNA", "Plasmid", "Environmental sample", "Clinical sample"],
                key="template"
            )
            polymerase = st.selectbox(
                "Polymerase used",
                ["-- Select --", "Taq polymerase", "Phusion", "Q5", "Hot start Taq", "One-step RT-PCR kit", "Other"],
                key="polymerase"
            )

        problem_description = st.text_area(
            "Describe the problem in detail",
            placeholder="""e.g. I am running PCR for 16S rRNA gene detection from bacterial colonies. 
Using Taq polymerase, annealing at 55°C, 35 cycles. 
Positive control works but patient samples show no bands. 
DNA was extracted using boiling method...""",
            height=120,
            key="problem_desc"
        )

        if problem_type != "-- Select problem --":
            query = f"PCR troubleshooting problem: {problem_type}"
            if pcr_type != "-- Select --":
                query += f", PCR type: {pcr_type}"
            if template_source != "-- Select --":
                query += f", template: {template_source}"
            if polymerase != "-- Select --":
                query += f", polymerase: {polymerase}"
            if problem_description.strip():
                query += f"\n\nDetailed description: {problem_description}"

    # Mode 3 — Ask Anything
    elif "Ask Anything" in mode:
        st.markdown("### ❓ Ask Any Molecular Biology Question")
        query = st.text_area(
            "Your Question",
            placeholder="""Examples:
- How do I design primers for detecting MRSA mecA gene?
- What is the difference between one-step and two-step RT-PCR?
- How do I interpret a Ct value of 32 in COVID-19 testing?
- What causes primer dimer formation and how to prevent it?
- Explain the difference between SYBR Green and TaqMan probes""",
            height=150,
            key="molecular_question"
        )

    st.markdown("---")

    # Submit button
    submit_clicked = st.button("🔬 Get Guidance", use_container_width=True)

    if submit_clicked:
        if not query or not query.strip():
            st.warning("⚠️ Please select a topic or enter your question.")
        else:
            if "troubleshooting" in query.lower() or "Troubleshoot" in mode:
                prompt = f"""Please help troubleshoot this PCR problem:

{query}

Provide systematic troubleshooting guidance, most likely causes, and step by step solutions."""
            else:
                prompt = f"""Please provide comprehensive guidance on this molecular biology topic:

{query}

Be practical, specific, and educational."""

            with st.spinner("🔬 Preparing molecular guidance..."):
                result = ask_claude(
                    system_prompt=SYSTEM_PROMPT,
                    user_message=prompt
                )

            st.markdown("---")
            st.markdown("### 🧬 Molecular Guidance")
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
                        ⚠️ <b>Note:</b> Always validate protocols in your specific lab conditions. 
                        Reagent quality, equipment calibration, and sample quality 
                        significantly affect PCR results.
                    </p>
                </div>
            """, unsafe_allow_html=True)

            if "pcr_history" not in st.session_state:
                st.session_state.pcr_history = []
            st.session_state.pcr_history.append({
                "query": query[:80] + "..." if len(query) > 80 else query,
                "result": result
            })

    # History
    if "pcr_history" in st.session_state and len(st.session_state.pcr_history) > 1:
        st.markdown("---")
        st.markdown("### 📋 Previous Queries This Session")
        for item in reversed(st.session_state.pcr_history[:-1]):
            with st.expander(item["query"]):
                st.markdown(item["result"])