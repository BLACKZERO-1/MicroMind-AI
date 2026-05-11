import streamlit as st
from utils.api_client import ask_claude
from utils.helpers import show_header, show_info_card

SYSTEM_PROMPT = """You are MicroMind AI — an expert clinical microbiologist and laboratory scientist with extensive experience in diagnostic testing.

Your task is to explain laboratory tests clearly and practically.

When given a lab test name or result:
1. Explain what the test is and what it detects
2. Explain how the test works mechanistically — step by step
3. Interpret the result if one is provided
4. Explain what a positive, negative, and borderline result means
5. State the clinical significance — what conditions or diseases this test helps diagnose
6. Mention common causes of false positive and false negative results
7. Suggest what follow-up tests are typically recommended

Format your response with these clear sections:
- WHAT IS THIS TEST
- HOW IT WORKS
- RESULT INTERPRETATION
- CLINICAL SIGNIFICANCE
- FALSE POSITIVES AND FALSE NEGATIVES
- FOLLOW-UP TESTS RECOMMENDED

Use clear language suitable for a lab technician or advanced student.
Be practical and lab-focused — not just theoretical."""

TEST_CATEGORIES = {
    "🦠 Microbiology": [
        "Gram Staining",
        "ELISA",
        "PCR (Polymerase Chain Reaction)",
        "Agglutination Test",
        "Immunofluorescence Assay",
        "Widal Test",
        "Blood Culture",
        "Urine Culture",
        "Sensitivity Testing (Kirby-Bauer)",
        "Ziehl-Neelsen Staining",
        "India Ink Preparation",
        "KOH Preparation",
    ],
    "⚗️ Biochemical": [
        "Catalase Test",
        "Oxidase Test",
        "Coagulase Test",
        "Urease Test",
        "Indole Test",
        "Methyl Red Test",
        "Voges-Proskauer Test",
        "Citrate Utilization Test",
        "TSI (Triple Sugar Iron) Test",
        "SIM Medium Test",
        "IMVIC Tests",
        "Bile Esculin Test",
    ],
    "🩸 Clinical Pathology": [
        "Complete Blood Count (CBC)",
        "Liver Function Tests (LFT)",
        "Renal Function Tests (RFT)",
        "Blood Glucose Test",
        "HbA1c Test",
        "Thyroid Stimulating Hormone (TSH)",
        "C-Reactive Protein (CRP)",
        "Erythrocyte Sedimentation Rate (ESR)",
        "Prothrombin Time (PT)",
        "D-Dimer Test",
    ],
    "🧫 Parasitology": [
        "Stool Routine Examination",
        "Occult Blood Test",
        "Combur Strip Urine Test",
        "Thick and Thin Blood Film",
        "Malaria Rapid Diagnostic Test",
        "Kato-Katz Technique",
    ],
    "🔬 Immunology": [
        "ELISA (Antibody Detection)",
        "Western Blot",
        "Complement Fixation Test",
        "Latex Agglutination Test",
        "Rapid Antigen Test",
        "Flow Cytometry",
        "ANA Test",
        "Rheumatoid Factor Test",
    ],
    "🧬 Molecular": [
        "PCR",
        "RT-PCR",
        "Real-Time PCR (qPCR)",
        "DNA Sequencing",
        "Gel Electrophoresis",
        "Southern Blot",
        "FISH (Fluorescence In Situ Hybridization)",
        "Next Generation Sequencing (NGS)",
    ],
}

def show_test_explainer_module():
    show_header(
        "Lab Test Explainer",
        "Select any lab test or enter a result — get a complete explanation instantly"
    )

    st.markdown("""
        <div style="background:#1A2B3C; border-left:4px solid #25B89A;
                    padding:12px; border-radius:8px; margin-bottom:16px;">
            <p style="color:#B0C4CE; margin:0; font-size:13px;">
                💡 You can either browse tests by category, search for a specific test, 
                or enter your own test result for interpretation.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Input Mode Selection
    mode = st.radio(
        "How would you like to use this module?",
        ["Browse by Category", "Search for a Test", "Enter My Own Result"],
        horizontal=True,
        label_visibility="collapsed"
    )

    st.markdown("---")

    selected_test = ""
    user_result = ""

    # Mode 1: Browse by Category
    if mode == "Browse by Category":
        st.markdown("### 📂 Select a Category")
        category = st.selectbox(
            "Category",
            options=list(TEST_CATEGORIES.keys()),
            label_visibility="collapsed"
        )

        st.markdown("### 🧪 Select a Test")
        selected_test = st.selectbox(
            "Test",
            options=["-- Select a test --"] + TEST_CATEGORIES[category],
            label_visibility="collapsed"
        )

        user_result = st.text_input(
            "Your Result (optional)",
            placeholder="e.g. Positive, Negative, 156 U/L, Zone of inhibition 18mm...",
            key="browse_result"
        )

    # Mode 2: Search
    elif mode == "Search for a Test":
        st.markdown("### 🔍 Search for a Test")
        selected_test = st.text_input(
            "Test Name",
            placeholder="e.g. ELISA, TSI, Widal, Combur strip, qPCR...",
            key="search_test"
        )
        user_result = st.text_input(
            "Your Result (optional)",
            placeholder="e.g. Positive, Negative, 156 U/L...",
            key="search_result"
        )

    # Mode 3: Enter Result
    elif mode == "Enter My Own Result":
        st.markdown("### 📋 Enter Your Test and Result")
        selected_test = st.text_input(
            "Test Name",
            placeholder="e.g. Urease Test, Blood Glucose, TSH...",
            key="custom_test"
        )
        user_result = st.text_area(
            "Your Result",
            placeholder="e.g. Urease test positive — pink color developed within 2 minutes...",
            height=100,
            key="custom_result"
        )

    st.markdown("---")

    # Explain Button
    explain_clicked = st.button("🔬 Explain This Test", use_container_width=True)

    if explain_clicked:
        if not selected_test or selected_test == "-- Select a test --":
            st.warning("⚠️ Please select or enter a test name first.")
        else:
            if user_result.strip():
                prompt = f"""Please explain the following laboratory test and interpret the result provided:

Test: {selected_test}
Result: {user_result}

Provide a complete explanation including what the test is, how it works, what this specific result means, clinical significance, and recommended follow-up."""
            else:
                prompt = f"""Please explain the following laboratory test completely:

Test: {selected_test}

Provide a complete explanation including what the test is, how it works, how to interpret results, clinical significance, and common errors."""

            with st.spinner("🔬 Preparing explanation..."):
                result = ask_claude(
                    system_prompt=SYSTEM_PROMPT,
                    user_message=prompt
                )

            st.markdown("---")
            st.markdown(f"### 🧪 {selected_test} — Explanation")
            st.markdown(f"""
                <div style="background:#1A2B3C; border-left:4px solid #25B89A;
                            padding:20px; border-radius:10px;
                            color:#E2E8F0; line-height:1.8; font-size:14px;">
                    {result.replace(chr(10), '<br>')}
                </div>
            """, unsafe_allow_html=True)

            if "test_history" not in st.session_state:
                st.session_state.test_history = []
            st.session_state.test_history.append({
                "test": selected_test,
                "result_input": user_result,
                "explanation": result
            })

            st.markdown("---")
            st.markdown("""
                <div style="background:#0D2B1A; border-left:4px solid #25B89A;
                            padding:12px; border-radius:8px;">
                    <p style="color:#86EFAC; margin:0; font-size:12px;">
                        ⚠️ <b>Disclaimer:</b> This explanation is for educational purposes only. 
                        Always consult a qualified laboratory professional for clinical decisions.
                    </p>
                </div>
            """, unsafe_allow_html=True)

    # History
    if "test_history" in st.session_state and len(st.session_state.test_history) > 1:
        st.markdown("---")
        st.markdown("### 📋 Previous Explanations This Session")
        for item in reversed(st.session_state.test_history[:-1]):
            label = item["test"]
            if item["result_input"]:
                label += f" — Result: {item['result_input']}"
            with st.expander(label):
                st.markdown(item["explanation"])