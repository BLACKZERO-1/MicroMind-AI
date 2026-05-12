import streamlit as st
from utils.api_client import ask_claude
from utils.helpers import show_header, show_info_card

SYSTEM_PROMPT = """You are MicroMind AI — an expert microbiologist and infectious disease specialist with comprehensive knowledge of pathogenic microorganisms.

Your task is to provide detailed, accurate profiles of pathogenic microorganisms.

When given a pathogen name or disease:
1. Provide complete taxonomic classification
2. Describe morphology and key characteristics
3. Explain pathogenesis and virulence factors
4. Describe diseases caused and clinical presentation
5. Explain transmission routes and epidemiology
6. Describe laboratory diagnosis methods
7. Explain treatment options and antimicrobial therapy
8. Mention prevention and control measures
9. Provide global burden and public health significance

Format your response with these sections:
- PATHOGEN PROFILE
- MORPHOLOGY AND CHARACTERISTICS
- PATHOGENESIS AND VIRULENCE FACTORS
- DISEASES AND CLINICAL PRESENTATION
- TRANSMISSION AND EPIDEMIOLOGY
- LABORATORY DIAGNOSIS
- TREATMENT OPTIONS
- PREVENTION AND CONTROL
- PUBLIC HEALTH SIGNIFICANCE

Be comprehensive, accurate, and educational.
Think like an infectious disease textbook but written clearly for students and clinicians."""

PATHOGEN_CATEGORIES = {
    "🦠 Gram Positive Bacteria": [
        "Staphylococcus aureus",
        "Staphylococcus epidermidis",
        "Streptococcus pyogenes",
        "Streptococcus pneumoniae",
        "Streptococcus agalactiae",
        "Enterococcus faecalis",
        "Enterococcus faecium",
        "Bacillus anthracis",
        "Bacillus cereus",
        "Clostridium tetani",
        "Clostridium botulinum",
        "Clostridium difficile",
        "Clostridium perfringens",
        "Listeria monocytogenes",
        "Corynebacterium diphtheriae",
    ],
    "🔴 Gram Negative Bacteria": [
        "Escherichia coli",
        "Klebsiella pneumoniae",
        "Pseudomonas aeruginosa",
        "Acinetobacter baumannii",
        "Salmonella typhi",
        "Salmonella typhimurium",
        "Shigella dysenteriae",
        "Vibrio cholerae",
        "Haemophilus influenzae",
        "Neisseria meningitidis",
        "Neisseria gonorrhoeae",
        "Helicobacter pylori",
        "Campylobacter jejuni",
        "Yersinia pestis",
        "Brucella species",
        "Legionella pneumophila",
        "Bordetella pertussis",
    ],
    "🟡 Mycobacteria": [
        "Mycobacterium tuberculosis",
        "Mycobacterium leprae",
        "Mycobacterium avium complex",
        "Non-tuberculous Mycobacteria (NTM)",
    ],
    "🟠 Spirochetes": [
        "Treponema pallidum (Syphilis)",
        "Borrelia burgdorferi (Lyme disease)",
        "Leptospira interrogans",
    ],
    "🟣 Fungi": [
        "Candida albicans",
        "Candida auris",
        "Aspergillus fumigatus",
        "Cryptococcus neoformans",
        "Histoplasma capsulatum",
        "Coccidioides immitis",
        "Pneumocystis jirovecii",
        "Dermatophytes (Tinea infections)",
    ],
    "🔵 Viruses": [
        "SARS-CoV-2 (COVID-19)",
        "Influenza A and B",
        "Hepatitis B Virus",
        "Hepatitis C Virus",
        "HIV (Human Immunodeficiency Virus)",
        "Dengue Virus",
        "Ebola Virus",
        "Marburg Virus",
        "Rabies Virus",
        "Measles Virus",
        "Norovirus",
        "Rotavirus",
    ],
    "🟤 Parasites": [
        "Plasmodium falciparum (Malaria)",
        "Plasmodium vivax (Malaria)",
        "Entamoeba histolytica",
        "Giardia lamblia",
        "Cryptosporidium parvum",
        "Toxoplasma gondii",
        "Leishmania species",
        "Trypanosoma cruzi (Chagas disease)",
        "Schistosoma species",
        "Ascaris lumbricoides",
        "Taenia solium (Tapeworm)",
    ],
}

BODY_SYSTEMS = [
    "-- Select System --",
    "Respiratory System",
    "Gastrointestinal System",
    "Urinary Tract",
    "Central Nervous System",
    "Cardiovascular System",
    "Skin and Soft Tissue",
    "Bone and Joint",
    "Reproductive System",
    "Eye (Ocular)",
    "Ear (Otologic)",
    "Bloodstream (Sepsis)",
    "Liver and Hepatic",
]

def show_pathogen_library_module():
    show_header(
        "Pathogen Library",
        "Complete profiles of bacteria, fungi, viruses, and parasites — searchable by pathogen, disease, or body system"
    )

    st.markdown("""
        <div style="background:#1A2B3C; border-left:4px solid #25B89A;
                    padding:12px; border-radius:8px; margin-bottom:16px;">
            <p style="color:#B0C4CE; margin:0; font-size:13px;">
                💡 Browse pathogens by category, search by disease name, 
                or explore pathogens by the body system they affect.
            </p>
        </div>
    """, unsafe_allow_html=True)

    mode = st.radio(
        "Search by:",
        ["📂 Browse by Pathogen Category", "🔍 Search by Disease or Pathogen Name", "🫁 Browse by Body System", "⚖️ Compare Two Pathogens"],
        horizontal=False,
        label_visibility="collapsed"
    )

    st.markdown("---")

    query = ""

    # Mode 1 — Browse by Category
    if "Category" in mode:
        st.markdown("### 📂 Select Pathogen Category")
        category = st.selectbox(
            "Category",
            options=list(PATHOGEN_CATEGORIES.keys()),
            label_visibility="collapsed"
        )

        st.markdown("### 🦠 Select Pathogen")
        pathogen = st.selectbox(
            "Pathogen",
            options=["-- Select pathogen --"] + PATHOGEN_CATEGORIES[category],
            label_visibility="collapsed"
        )

        if pathogen != "-- Select pathogen --":
            query = f"Provide a complete pathogen profile for: {pathogen}"

        focus_area = st.selectbox(
            "Focus on specific aspect (optional)",
            ["-- Full profile --", "Diagnosis only", "Treatment only", "Epidemiology only", "Virulence factors only", "Lab diagnosis only"],
            key="focus"
        )
        if focus_area != "-- Full profile --":
            query += f" — focus specifically on: {focus_area}"

    # Mode 2 — Search by Name
    elif "Search" in mode:
        st.markdown("### 🔍 Search for Pathogen or Disease")
        search_term = st.text_input(
            "Enter pathogen name or disease",
            placeholder="e.g. Tuberculosis, E. coli, Malaria, Dengue fever, MRSA, Candidiasis...",
            key="search_term"
        )

        if search_term.strip():
            query = f"Provide a complete profile for this pathogen or disease: {search_term}"

    # Mode 3 — By Body System
    elif "Body System" in mode:
        st.markdown("### 🫁 Select Body System")
        system = st.selectbox(
            "Body System",
            options=BODY_SYSTEMS,
            label_visibility="collapsed"
        )

        if system != "-- Select System --":
            query = f"List and describe the most important pathogens that cause infections in the {system}. For each pathogen include key characteristics, how it causes infection, diagnosis, and treatment."

        severity = st.selectbox(
            "Filter by severity (optional)",
            ["-- All severities --", "Life threatening", "Serious", "Common/mild", "Opportunistic"],
            key="severity"
        )
        if severity != "-- All severities --":
            query += f" Focus on {severity} infections."

    # Mode 4 — Compare
    elif "Compare" in mode:
        st.markdown("### ⚖️ Compare Two Pathogens")
        col1, col2 = st.columns(2)

        with col1:
            pathogen1 = st.text_input(
                "First Pathogen",
                placeholder="e.g. Staphylococcus aureus",
                key="pathogen1"
            )

        with col2:
            pathogen2 = st.text_input(
                "Second Pathogen",
                placeholder="e.g. Streptococcus pyogenes",
                key="pathogen2"
            )

        compare_aspect = st.selectbox(
            "What to compare",
            ["-- Select --", "Everything", "Morphology and characteristics", "Diseases caused", "Diagnosis methods", "Treatment options", "Virulence factors", "Epidemiology"],
            key="compare_aspect"
        )

        if pathogen1.strip() and pathogen2.strip():
            query = f"Compare and contrast {pathogen1} and {pathogen2}"
            if compare_aspect != "-- Select --":
                query += f" focusing on: {compare_aspect}"
            query += ". Present in a clear structured format highlighting key similarities and differences."

    st.markdown("---")

    search_clicked = st.button("🔍 Get Pathogen Information", use_container_width=True)

    if search_clicked:
        if not query or not query.strip():
            st.warning("⚠️ Please select a pathogen, disease, body system, or enter your search term.")
        else:
            with st.spinner("📖 Loading pathogen information..."):
                result = ask_claude(
                    system_prompt=SYSTEM_PROMPT,
                    user_message=query
                )

            st.markdown("---")
            st.markdown("### 📖 Pathogen Profile")
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
                        ⚠️ <b>Note:</b> This information is for educational purposes. 
                        Clinical decisions should be based on current guidelines, 
                        local resistance patterns, and patient-specific factors.
                    </p>
                </div>
            """, unsafe_allow_html=True)

            if "pathogen_history" not in st.session_state:
                st.session_state.pathogen_history = []
            st.session_state.pathogen_history.append({
                "query": query[:80] + "..." if len(query) > 80 else query,
                "result": result
            })

    # History
    if "pathogen_history" in st.session_state and len(st.session_state.pathogen_history) > 1:
        st.markdown("---")
        st.markdown("### 📋 Previous Searches This Session")
        for item in reversed(st.session_state.pathogen_history[:-1]):
            with st.expander(item["query"]):
                st.markdown(item["result"])