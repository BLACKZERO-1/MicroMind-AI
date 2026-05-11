import streamlit as st
from utils.api_client import ask_claude
from utils.helpers import show_header, show_info_card

SYSTEM_PROMPT = """You are MicroMind AI — an expert clinical microbiologist with decades of lab experience.

Your task is to identify a microorganism based on the characteristics provided by the user.

When given lab characteristics:
1. Analyze all provided characteristics carefully
2. Identify the most likely organism with a confidence percentage
3. List 2-3 other possible organisms if applicable
4. Explain clearly WHY this organism matches the characteristics
5. State what additional tests would confirm the identification
6. Mention clinical significance — what diseases this organism causes
7. Mention any urgent concerns — like if MRSA or other dangerous organisms are suspected

Format your response clearly with these sections:
- MOST LIKELY ORGANISM (with confidence %)
- WHY THIS IDENTIFICATION
- OTHER POSSIBILITIES
- CONFIRMATORY TESTS RECOMMENDED
- CLINICAL SIGNIFICANCE
- URGENT CONCERNS (if any)

Be precise, educational, and practical. Think like a senior microbiologist guiding a junior technician."""

GRAM_REACTIONS = ["-- Select --", "Gram Positive (Purple)", "Gram Negative (Pink/Red)", "Gram Variable", "Not Tested"]
CELL_SHAPES = ["-- Select --", "Cocci (Round)", "Bacilli (Rod)", "Coccobacilli", "Spirilla (Spiral)", "Vibrio (Comma)", "Filamentous"]
ARRANGEMENTS = ["-- Select --", "Clusters (Staphylo)", "Chains (Strepto)", "Pairs (Diplo)", "Tetrads", "Single", "Palisades"]
OXYGEN_NEEDS = ["-- Select --", "Aerobic", "Anaerobic", "Facultative Anaerobe", "Microaerophilic", "Not Tested"]
CATALASE = ["-- Select --", "Positive", "Negative", "Not Tested"]
OXIDASE = ["-- Select --", "Positive", "Negative", "Not Tested"]
COAGULASE = ["-- Select --", "Positive", "Negative", "Not Tested"]
HEMOLYSIS = ["-- Select --", "Alpha (Partial/Green)", "Beta (Complete/Clear)", "Gamma (None)", "Not Tested"]
MOTILITY = ["-- Select --", "Motile", "Non-Motile", "Not Tested"]
SPORE_FORMATION = ["-- Select --", "Spore Forming", "Non-Spore Forming", "Not Tested"]
SAMPLE_SOURCES = ["-- Select --", "Blood", "Urine", "Stool", "Sputum", "Wound/Pus", "CSF", "Throat Swab", "Nasal Swab", "Genital", "Unknown"]

def show_identifier_module():
    show_header(
        "Organism Identifier",
        "Enter your lab characteristics and MicroMind AI will identify the most likely organism"
    )

    st.markdown("""
        <div style="background:#1A2B3C; border-left:4px solid #25B89A; 
                    padding:12px; border-radius:8px; margin-bottom:16px;">
            <p style="color:#B0C4CE; margin:0; font-size:13px;">
                💡 Fill in as many characteristics as you have. More information = more accurate identification.
                You don't need to fill every field — just what you have from your bench work.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # ── Form ────────────────────────────────────────────────────────────
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🔬 Microscopy")
        gram = st.selectbox("Gram Reaction", GRAM_REACTIONS, key="gram")
        shape = st.selectbox("Cell Shape", CELL_SHAPES, key="shape")
        arrangement = st.selectbox("Cell Arrangement", ARRANGEMENTS, key="arrangement")
        motility = st.selectbox("Motility", MOTILITY, key="motility")
        spore = st.selectbox("Spore Formation", SPORE_FORMATION, key="spore")

        st.markdown("### 🧫 Culture")
        sample_source = st.selectbox("Sample Source", SAMPLE_SOURCES, key="sample")
        hemolysis = st.selectbox("Hemolysis on Blood Agar", HEMOLYSIS, key="hemolysis")
        oxygen = st.selectbox("Oxygen Requirement", OXYGEN_NEEDS, key="oxygen")

    with col2:
        st.markdown("### ⚗️ Biochemical Tests")
        catalase = st.selectbox("Catalase Test", CATALASE, key="catalase")
        oxidase = st.selectbox("Oxidase Test", OXIDASE, key="oxidase")
        coagulase = st.selectbox("Coagulase Test", COAGULASE, key="coagulase")

        st.markdown("### 📝 Additional Information")
        colony_desc = st.text_area(
            "Colony Morphology (optional)",
            placeholder="e.g. Golden yellow colonies, 2-3mm, smooth, convex, opaque...",
            height=80,
            key="colony"
        )
        additional_tests = st.text_area(
            "Other Test Results (optional)",
            placeholder="e.g. TSI: acid slant/acid butt, gas positive, H2S negative. Urease positive...",
            height=80,
            key="other_tests"
        )
        clinical_info = st.text_input(
            "Clinical Information (optional)",
            placeholder="e.g. UTI patient, 45 year old female, recurrent infection...",
            key="clinical"
        )

    st.markdown("---")

    # ── Identify Button ─────────────────────────────────────────────────
    identify_clicked = st.button("🔍 Identify Organism", use_container_width=True)

    if identify_clicked:
        # Build characteristics summary
        characteristics = []

        if gram != "-- Select --":
            characteristics.append(f"Gram reaction: {gram}")
        if shape != "-- Select --":
            characteristics.append(f"Cell shape: {shape}")
        if arrangement != "-- Select --":
            characteristics.append(f"Cell arrangement: {arrangement}")
        if motility != "-- Select --":
            characteristics.append(f"Motility: {motility}")
        if spore != "-- Select --":
            characteristics.append(f"Spore formation: {spore}")
        if sample_source != "-- Select --":
            characteristics.append(f"Sample source: {sample_source}")
        if hemolysis != "-- Select --":
            characteristics.append(f"Hemolysis: {hemolysis}")
        if oxygen != "-- Select --":
            characteristics.append(f"Oxygen requirement: {oxygen}")
        if catalase != "-- Select --":
            characteristics.append(f"Catalase: {catalase}")
        if oxidase != "-- Select --":
            characteristics.append(f"Oxidase: {oxidase}")
        if coagulase != "-- Select --":
            characteristics.append(f"Coagulase: {coagulase}")
        if colony_desc.strip():
            characteristics.append(f"Colony morphology: {colony_desc.strip()}")
        if additional_tests.strip():
            characteristics.append(f"Additional test results: {additional_tests.strip()}")
        if clinical_info.strip():
            characteristics.append(f"Clinical information: {clinical_info.strip()}")

        if len(characteristics) == 0:
            st.warning("⚠️ Please select at least one characteristic before identifying.")
        else:
            # Build prompt
            chars_text = "\n".join([f"- {c}" for c in characteristics])
            prompt = f"""Please identify the most likely microorganism based on these laboratory characteristics:

{chars_text}

Provide a thorough identification with your reasoning."""

            with st.spinner("🔬 Analyzing characteristics..."):
                result = ask_claude(
                    system_prompt=SYSTEM_PROMPT,
                    user_message=prompt
                )

            # Display result
            st.markdown("---")
            st.markdown("### 🧬 Identification Result")
            st.markdown(f"""
                <div style="background:#1A2B3C; border-left:4px solid #25B89A;
                            padding:20px; border-radius:10px; 
                            color:#E2E8F0; line-height:1.8; font-size:14px;">
                    {result.replace(chr(10), '<br>')}
                </div>
            """, unsafe_allow_html=True)

            # Save to session for reference
            if "identification_history" not in st.session_state:
                st.session_state.identification_history = []
            st.session_state.identification_history.append({
                "characteristics": characteristics,
                "result": result
            })

            st.markdown("---")
            st.markdown("""
                <div style="background:#0D2B1A; border-left:4px solid #25B89A;
                            padding:12px; border-radius:8px;">
                    <p style="color:#86EFAC; margin:0; font-size:12px;">
                        ⚠️ <b>Disclaimer:</b> This identification is for educational and reference purposes only. 
                        Always confirm organism identification through standard laboratory procedures 
                        and consult a qualified microbiologist for clinical decisions.
                    </p>
                </div>
            """, unsafe_allow_html=True)

    # ── Previous Identifications ────────────────────────────────────────
    if "identification_history" in st.session_state and st.session_state.identification_history:
        st.markdown("---")
        st.markdown("### 📋 Previous Identifications This Session")
        for i, item in enumerate(reversed(st.session_state.identification_history[:-1]), 1):
            with st.expander(f"Identification #{len(st.session_state.identification_history) - i}"):
                st.markdown("**Characteristics entered:**")
                for char in item["characteristics"]:
                    st.markdown(f"- {char}")
                st.markdown("**Result:**")
                st.markdown(item["result"])