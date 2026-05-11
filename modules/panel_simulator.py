import streamlit as st
from utils.api_client import ask_claude
from utils.helpers import show_header, show_info_card

SYSTEM_PROMPT = """You are MicroMind AI — an expert clinical microbiologist specializing in biochemical identification of bacteria.

Your task is to analyze biochemical test results and identify the most likely organism.

When given a set of biochemical test results:
1. Analyze the complete pattern of results
2. Identify the most likely organism with confidence percentage
3. Explain why each test result points toward or away from certain organisms
4. List 2-3 alternative possibilities
5. Recommend confirmatory tests
6. State clinical significance

Format your response with these sections:
- MOST LIKELY ORGANISM (confidence %)
- RESULT PATTERN ANALYSIS (explain each test result)
- ALTERNATIVE POSSIBILITIES
- CONFIRMATORY TESTS
- CLINICAL SIGNIFICANCE
- URGENT CONCERNS (if any)

Think like a senior microbiologist teaching a junior technician.
Be thorough, educational, and practical."""

def show_panel_simulator_module():
    show_header(
        "Biochemical Panel Simulator",
        "Enter your biochemical test results — get real-time organism identification"
    )

    st.markdown("""
        <div style="background:#1A2B3C; border-left:4px solid #25B89A;
                    padding:12px; border-radius:8px; margin-bottom:16px;">
            <p style="color:#B0C4CE; margin:0; font-size:13px;">
                💡 Enter your biochemical test results one by one. 
                The more results you enter, the more accurate the identification.
                Leave tests as Not Tested if you haven't run them.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Mode selection
    mode = st.radio(
        "Select Mode",
        ["🔬 Enterobacteriaceae Panel (IMViC + TSI)", "⚗️ Full Biochemical Panel", "🧫 Custom Tests"],
        horizontal=False,
        label_visibility="collapsed"
    )

    st.markdown("---")

    results = {}

    # Mode 1 — IMViC + TSI
    if "Enterobacteriaceae" in mode:
        st.markdown("### 🧪 IMViC Panel")
        col1, col2 = st.columns(2)

        with col1:
            results["Indole"] = st.selectbox("Indole Test", ["Not Tested", "Positive", "Negative"], key="indole")
            results["Methyl Red"] = st.selectbox("Methyl Red Test", ["Not Tested", "Positive", "Negative"], key="mr")
            results["Voges-Proskauer"] = st.selectbox("Voges-Proskauer Test", ["Not Tested", "Positive", "Negative"], key="vp")
            results["Citrate"] = st.selectbox("Citrate Utilization", ["Not Tested", "Positive", "Negative"], key="citrate")

        with col2:
            st.markdown("### 🧫 TSI Agar Results")
            results["TSI Slant"] = st.selectbox("TSI Slant", ["Not Tested", "Acid (Yellow)", "Alkaline (Red/Pink)", "No Change"], key="tsi_slant")
            results["TSI Butt"] = st.selectbox("TSI Butt", ["Not Tested", "Acid (Yellow)", "Alkaline (Red/Pink)", "No Change"], key="tsi_butt")
            results["TSI Gas"] = st.selectbox("Gas Production", ["Not Tested", "Positive (Cracks/Displacement)", "Negative"], key="tsi_gas")
            results["TSI H2S"] = st.selectbox("H2S Production", ["Not Tested", "Positive (Black precipitate)", "Negative"], key="tsi_h2s")

        st.markdown("### ⚗️ Additional Tests")
        col3, col4 = st.columns(2)
        with col3:
            results["Urease"] = st.selectbox("Urease Test", ["Not Tested", "Positive", "Negative", "Weakly Positive"], key="urease")
            results["Motility"] = st.selectbox("Motility", ["Not Tested", "Motile", "Non-Motile"], key="motility")
        with col4:
            results["Oxidase"] = st.selectbox("Oxidase Test", ["Not Tested", "Positive", "Negative"], key="oxidase")
            results["Catalase"] = st.selectbox("Catalase Test", ["Not Tested", "Positive", "Negative"], key="catalase")

    # Mode 2 — Full Panel
    elif "Full" in mode:
        st.markdown("### 🔬 Gram Stain & Morphology")
        col1, col2 = st.columns(2)
        with col1:
            results["Gram Reaction"] = st.selectbox("Gram Reaction", ["Not Tested", "Gram Positive", "Gram Negative", "Gram Variable"], key="gram")
            results["Cell Shape"] = st.selectbox("Cell Shape", ["Not Tested", "Cocci", "Bacilli", "Coccobacilli", "Spirilla"], key="shape")
        with col2:
            results["Arrangement"] = st.selectbox("Arrangement", ["Not Tested", "Clusters", "Chains", "Pairs", "Single"], key="arrangement")
            results["Spore Formation"] = st.selectbox("Spore Formation", ["Not Tested", "Positive", "Negative"], key="spore")

        st.markdown("### ⚗️ Key Biochemical Tests")
        col3, col4 = st.columns(2)
        with col3:
            results["Catalase"] = st.selectbox("Catalase", ["Not Tested", "Positive", "Negative"], key="catalase2")
            results["Oxidase"] = st.selectbox("Oxidase", ["Not Tested", "Positive", "Negative"], key="oxidase2")
            results["Coagulase"] = st.selectbox("Coagulase", ["Not Tested", "Positive", "Negative"], key="coagulase")
            results["Urease"] = st.selectbox("Urease", ["Not Tested", "Positive", "Negative", "Weakly Positive"], key="urease2")
            results["Indole"] = st.selectbox("Indole", ["Not Tested", "Positive", "Negative"], key="indole2")
        with col4:
            results["Methyl Red"] = st.selectbox("Methyl Red", ["Not Tested", "Positive", "Negative"], key="mr2")
            results["Voges-Proskauer"] = st.selectbox("Voges-Proskauer", ["Not Tested", "Positive", "Negative"], key="vp2")
            results["Citrate"] = st.selectbox("Citrate", ["Not Tested", "Positive", "Negative"], key="citrate2")
            results["Hemolysis"] = st.selectbox("Hemolysis", ["Not Tested", "Alpha", "Beta", "Gamma"], key="hemolysis")
            results["Motility"] = st.selectbox("Motility", ["Not Tested", "Motile", "Non-Motile"], key="motility2")

        st.markdown("### 🧫 TSI Results")
        col5, col6 = st.columns(2)
        with col5:
            results["TSI Slant"] = st.selectbox("TSI Slant", ["Not Tested", "Acid (Yellow)", "Alkaline (Red/Pink)"], key="tsi_slant2")
            results["TSI Butt"] = st.selectbox("TSI Butt", ["Not Tested", "Acid (Yellow)", "Alkaline (Red/Pink)"], key="tsi_butt2")
        with col6:
            results["TSI Gas"] = st.selectbox("Gas Production", ["Not Tested", "Positive", "Negative"], key="tsi_gas2")
            results["TSI H2S"] = st.selectbox("H2S Production", ["Not Tested", "Positive (Black)", "Negative"], key="tsi_h2s2")

    # Mode 3 — Custom
    elif "Custom" in mode:
        st.markdown("### 📝 Enter Your Custom Test Results")
        st.markdown("""
            <p style="color:#B0C4CE; font-size:13px;">
            Enter each test and its result below. Add as many tests as you have.
            </p>
        """, unsafe_allow_html=True)

        custom_results = st.text_area(
            "Test Results",
            placeholder="""Enter your results like this:
Gram stain: Positive
Cell shape: Cocci
Catalase: Positive
Coagulase: Negative
Novobiocin sensitivity: Resistant
Urease: Positive""",
            height=200,
            key="custom_results"
        )
        results["custom"] = custom_results

    st.markdown("---")

    # Sample source
    sample_source = st.text_input(
        "Sample Source (optional)",
        placeholder="e.g. Urine, Blood, Wound swab, Stool...",
        key="sample_source"
    )

    additional_info = st.text_area(
        "Any Additional Information (optional)",
        placeholder="e.g. Colony morphology, patient information, special staining results...",
        height=80,
        key="additional_info"
    )

    st.markdown("---")

    # Identify button
    identify_clicked = st.button("🔬 Identify Organism", use_container_width=True)

    if identify_clicked:
        # Build results summary
        if "custom" in results:
            if not results["custom"].strip():
                st.warning("⚠️ Please enter your test results.")
                return
            results_text = results["custom"]
        else:
            tested_results = {k: v for k, v in results.items() if v != "Not Tested"}
            if not tested_results:
                st.warning("⚠️ Please enter at least one test result.")
                return
            results_text = "\n".join([f"- {k}: {v}" for k, v in tested_results.items()])

        prompt = f"""Please identify the organism based on these biochemical test results:

{results_text}
{f'Sample source: {sample_source}' if sample_source else ''}
{f'Additional information: {additional_info}' if additional_info else ''}

Analyze the complete pattern and identify the most likely organism."""

        with st.spinner("🔬 Analyzing biochemical pattern..."):
            result = ask_claude(
                system_prompt=SYSTEM_PROMPT,
                user_message=prompt
            )

        st.markdown("---")
        st.markdown("### 🧬 Identification Result")
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
                    ⚠️ <b>Disclaimer:</b> For educational purposes only. 
                    Always confirm through standard laboratory procedures.
                </p>
            </div>
        """, unsafe_allow_html=True)