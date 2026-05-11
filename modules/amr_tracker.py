import streamlit as st
from utils.api_client import ask_claude
from utils.helpers import show_header, show_info_card

SYSTEM_PROMPT = """You are MicroMind AI — an expert clinical microbiologist specializing in antimicrobial resistance.

Your task is to provide comprehensive antimicrobial resistance information.

When given an organism or antibiotic:
1. Provide the complete resistance profile
2. Explain the resistance mechanisms in detail
3. List effective treatment options
4. Explain why certain antibiotics fail
5. Mention any urgent resistance concerns — MRSA, ESBL, CRE, etc.
6. Provide WHO priority classification if applicable
7. Suggest susceptibility testing recommendations

Format your response with these sections:
- RESISTANCE PROFILE SUMMARY
- RESISTANCE MECHANISMS EXPLAINED
- EFFECTIVE TREATMENT OPTIONS
- ANTIBIOTICS TO AVOID AND WHY
- URGENT CONCERNS
- SUSCEPTIBILITY TESTING RECOMMENDATIONS
- WHO PRIORITY CLASSIFICATION (if applicable)

Be precise, clinically relevant, and educational.
Think like an infectious disease specialist guiding a clinician."""

ORGANISMS = [
    "-- Select Organism --",
    "Staphylococcus aureus (MRSA)",
    "Staphylococcus aureus (MSSA)",
    "Staphylococcus epidermidis",
    "Streptococcus pneumoniae",
    "Streptococcus pyogenes",
    "Enterococcus faecalis",
    "Enterococcus faecium (VRE)",
    "Escherichia coli",
    "Klebsiella pneumoniae (ESBL)",
    "Klebsiella pneumoniae (CRE)",
    "Pseudomonas aeruginosa",
    "Acinetobacter baumannii",
    "Enterobacter cloacae",
    "Salmonella typhi",
    "Haemophilus influenzae",
    "Neisseria gonorrhoeae",
    "Mycobacterium tuberculosis",
    "Helicobacter pylori",
    "Clostridium difficile",
]

ANTIBIOTICS = [
    "-- Select Antibiotic --",
    "Penicillin",
    "Amoxicillin",
    "Ampicillin",
    "Piperacillin-Tazobactam",
    "Methicillin/Oxacillin",
    "Cloxacillin",
    "Cephalexin (1st Gen)",
    "Cefuroxime (2nd Gen)",
    "Ceftriaxone (3rd Gen)",
    "Cefepime (4th Gen)",
    "Imipenem",
    "Meropenem",
    "Ertapenem",
    "Vancomycin",
    "Teicoplanin",
    "Linezolid",
    "Daptomycin",
    "Ciprofloxacin",
    "Levofloxacin",
    "Gentamicin",
    "Amikacin",
    "Tobramycin",
    "Azithromycin",
    "Clarithromycin",
    "Doxycycline",
    "Tetracycline",
    "Trimethoprim-Sulfamethoxazole",
    "Metronidazole",
    "Colistin",
    "Rifampicin",
]

RESISTANCE_MECHANISMS = [
    "-- Select Mechanism --",
    "Beta-lactamase production",
    "ESBL (Extended Spectrum Beta-lactamase)",
    "Carbapenemase production (KPC, NDM, OXA)",
    "MRSA (mecA gene — altered PBP2a)",
    "Vancomycin resistance (VanA, VanB)",
    "Efflux pumps",
    "Porin loss/modification",
    "Target site modification",
    "Aminoglycoside modifying enzymes",
    "Ribosomal methylation",
    "Fluoroquinolone target mutation (gyrA, parC)",
]

def show_amr_tracker_module():
    show_header(
        "Antimicrobial Resistance Tracker",
        "Explore resistance profiles, mechanisms, and treatment options for any organism or antibiotic"
    )

    st.markdown("""
        <div style="background:#1A2B3C; border-left:4px solid #25B89A;
                    padding:12px; border-radius:8px; margin-bottom:16px;">
            <p style="color:#B0C4CE; margin:0; font-size:13px;">
                💡 Search by organism to see its resistance profile, by antibiotic to see which organisms resist it,
                or by mechanism to understand how resistance works.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Search mode
    mode = st.radio(
        "Search by:",
        ["🦠 By Organism", "💊 By Antibiotic", "⚙️ By Resistance Mechanism", "📝 Custom Query"],
        horizontal=False,
        label_visibility="collapsed"
    )

    st.markdown("---")

    query = ""

    # Mode 1 — By Organism
    if "Organism" in mode:
        st.markdown("### 🦠 Select Organism")
        organism = st.selectbox(
            "Organism",
            options=ORGANISMS,
            label_visibility="collapsed"
        )

        if organism != "-- Select Organism --":
            query = f"organism: {organism}"

        col1, col2 = st.columns(2)
        with col1:
            specific_antibiotic = st.selectbox(
                "Check specific antibiotic (optional)",
                options=["-- All antibiotics --"] + ANTIBIOTICS[1:],
                key="org_antibiotic"
            )
        with col2:
            clinical_setting = st.selectbox(
                "Clinical setting (optional)",
                ["-- Select --", "Community acquired", "Hospital acquired", "ICU", "Immunocompromised patient"],
                key="setting"
            )

        if specific_antibiotic != "-- All antibiotics --":
            query += f" — specific antibiotic: {specific_antibiotic}"
        if clinical_setting != "-- Select --":
            query += f" — clinical setting: {clinical_setting}"

    # Mode 2 — By Antibiotic
    elif "Antibiotic" in mode:
        st.markdown("### 💊 Select Antibiotic")
        antibiotic = st.selectbox(
            "Antibiotic",
            options=ANTIBIOTICS,
            label_visibility="collapsed"
        )

        if antibiotic != "-- Select Antibiotic --":
            query = f"antibiotic: {antibiotic}"

        specific_organism = st.selectbox(
            "Check against specific organism (optional)",
            options=["-- All organisms --"] + ORGANISMS[1:],
            key="ant_organism"
        )

        if specific_organism != "-- All organisms --":
            query += f" — specific organism: {specific_organism}"

    # Mode 3 — By Mechanism
    elif "Mechanism" in mode:
        st.markdown("### ⚙️ Select Resistance Mechanism")
        mechanism = st.selectbox(
            "Mechanism",
            options=RESISTANCE_MECHANISMS,
            label_visibility="collapsed"
        )

        if mechanism != "-- Select Mechanism --":
            query = f"resistance mechanism: {mechanism}"

    # Mode 4 — Custom
    elif "Custom" in mode:
        st.markdown("### 📝 Enter Your Query")
        query = st.text_area(
            "Query",
            placeholder="""Examples:
- What antibiotics work against carbapenem resistant Klebsiella?
- Explain MRSA resistance and treatment options
- What is the mechanism of vancomycin resistance in enterococci?
- Which organisms are naturally resistant to metronidazole?""",
            height=120,
            key="custom_query"
        )

    st.markdown("---")

    # Search button
    search_clicked = st.button("🔍 Get Resistance Information", use_container_width=True)

    if search_clicked:
        if not query or query.strip() == "":
            st.warning("⚠️ Please select an organism, antibiotic, mechanism, or enter a custom query.")
        else:
            if "organism:" in query:
                prompt = f"""Provide a comprehensive antimicrobial resistance profile for:
{query}

Include complete resistance profile, mechanisms, effective treatments, antibiotics to avoid, and clinical guidance."""
            elif "antibiotic:" in query:
                prompt = f"""Provide comprehensive information about antimicrobial resistance related to:
{query}

Include which organisms are resistant, mechanisms of resistance, clinical implications, and alternatives."""
            elif "resistance mechanism:" in query:
                prompt = f"""Explain this antimicrobial resistance mechanism in detail:
{query}

Include how it works molecularly, which organisms carry it, which antibiotics it affects, clinical significance, and detection methods."""
            else:
                prompt = query

            with st.spinner("🔬 Analyzing resistance data..."):
                result = ask_claude(
                    system_prompt=SYSTEM_PROMPT,
                    user_message=prompt
                )

            st.markdown("---")
            st.markdown("### 💊 Resistance Information")
            st.markdown(f"""
                <div style="background:#1A2B3C; border-left:4px solid #E05252;
                            padding:20px; border-radius:10px;
                            color:#E2E8F0; line-height:1.8; font-size:14px;">
                    {result.replace(chr(10), '<br>')}
                </div>
            """, unsafe_allow_html=True)

            st.markdown("---")

            # Warning card
            st.markdown("""
                <div style="background:#2D1515; border-left:4px solid #E05252;
                            padding:12px; border-radius:8px;">
                    <p style="color:#FCA5A5; margin:0; font-size:12px;">
                        ⚠️ <b>Clinical Disclaimer:</b> Resistance patterns vary by region and institution. 
                        Always base treatment decisions on local antibiogram data and confirmed 
                        susceptibility testing results. Consult an infectious disease specialist 
                        for complex cases.
                    </p>
                </div>
            """, unsafe_allow_html=True)

            # Save history
            if "amr_history" not in st.session_state:
                st.session_state.amr_history = []
            st.session_state.amr_history.append({
                "query": query,
                "result": result
            })

    # History
    if "amr_history" in st.session_state and len(st.session_state.amr_history) > 1:
        st.markdown("---")
        st.markdown("### 📋 Previous Searches This Session")
        for item in reversed(st.session_state.amr_history[:-1]):
            with st.expander(item["query"]):
                st.markdown(item["result"])