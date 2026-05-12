import streamlit as st
from utils.api_client import ask_claude
from utils.helpers import show_header, show_info_card

SYSTEM_PROMPT = """You are MicroMind AI — an expert clinical microbiologist specializing in culture media and microbial cultivation.

Your task is to guide users on culture media selection, preparation, and interpretation.

When given a media question:
1. Explain what the media is and its purpose
2. Describe its composition and key ingredients
3. Explain what organisms grow on it and why
4. Describe expected colony morphology and appearance
5. Explain how to interpret growth results
6. Mention incubation conditions — temperature, atmosphere, duration
7. Describe quality control requirements

Format your response with these sections:
- MEDIA OVERVIEW
- COMPOSITION AND KEY INGREDIENTS
- ORGANISMS AND GROWTH PATTERNS
- EXPECTED COLONY APPEARANCE
- RESULT INTERPRETATION
- INCUBATION CONDITIONS
- QUALITY CONTROL
- CLINICAL APPLICATION

Be practical, detailed, and educational.
Think like an experienced lab scientist teaching proper media usage."""

MEDIA_CATEGORIES = {
    "🟥 Blood Based Media": [
        "Blood Agar (BA)",
        "Chocolate Agar",
        "Heated Blood Agar",
        "Lysed Blood Agar",
    ],
    "🟨 Selective Media": [
        "MacConkey Agar",
        "Eosin Methylene Blue (EMB) Agar",
        "Mannitol Salt Agar (MSA)",
        "TCBS Agar",
        "XLD Agar",
        "Hektoen Enteric Agar",
        "CLED Agar",
        "Cetrimide Agar",
        "Thiosulfate Citrate Bile Salt Agar",
    ],
    "🟩 Differential Media": [
        "MacConkey Agar",
        "Blood Agar — Hemolysis types",
        "Triple Sugar Iron Agar (TSI)",
        "Phenylethyl Alcohol Agar",
        "Bismuth Sulfite Agar",
    ],
    "🟦 Enrichment Media": [
        "Selenite Broth",
        "Tetrathionate Broth",
        "Alkaline Peptone Water",
        "Thioglycollate Broth",
        "Brain Heart Infusion Broth (BHI)",
        "Nutrient Broth",
    ],
    "🟪 Fungal Media": [
        "Sabouraud Dextrose Agar (SDA)",
        "CHROMagar Candida",
        "Cornmeal Agar",
        "Potato Dextrose Agar",
        "Dermatophyte Test Medium (DTM)",
    ],
    "⬛ Anaerobic Media": [
        "Brucella Blood Agar",
        "Kanamycin Vancomycin Blood Agar",
        "Phenylethyl Alcohol Blood Agar",
        "Cooked Meat Medium",
        "Thioglycollate Broth",
    ],
    "🔵 Special Purpose Media": [
        "Lowenstein-Jensen Medium (TB)",
        "Thayer-Martin Agar (Neisseria)",
        "Bordet-Gengou Agar (Bordetella)",
        "BCYE Agar (Legionella)",
        "Campylobacter Selective Agar",
        "Buffered Charcoal Yeast Extract",
    ],
}

ORGANISMS_LIST = [
    "-- Select Organism --",
    "Escherichia coli",
    "Klebsiella pneumoniae",
    "Salmonella typhi",
    "Shigella species",
    "Staphylococcus aureus",
    "Streptococcus pyogenes",
    "Streptococcus pneumoniae",
    "Pseudomonas aeruginosa",
    "Vibrio cholerae",
    "Mycobacterium tuberculosis",
    "Candida albicans",
    "Aspergillus species",
    "Neisseria gonorrhoeae",
    "Haemophilus influenzae",
    "Clostridium difficile",
    "Campylobacter jejuni",
    "Legionella pneumophila",
    "Bordetella pertussis",
]

SAMPLE_TYPES = [
    "-- Select Sample --",
    "Urine",
    "Blood",
    "Stool / Feces",
    "Sputum",
    "Wound / Pus",
    "CSF (Cerebrospinal Fluid)",
    "Throat Swab",
    "Nasal Swab",
    "Vaginal Swab",
    "Eye Swab",
    "Ear Swab",
    "Tissue Biopsy",
]

def show_media_guide_module():
    show_header(
        "Culture Media Guide",
        "Find the right media for any organism or sample — with expected results and interpretation"
    )

    st.markdown("""
        <div style="background:#1A2B3C; border-left:4px solid #25B89A;
                    padding:12px; border-radius:8px; margin-bottom:16px;">
            <p style="color:#B0C4CE; margin:0; font-size:13px;">
                💡 Browse media by category, find the right media for a specific organism,
                or get a complete media panel recommendation for your sample type.
            </p>
        </div>
    """, unsafe_allow_html=True)

    mode = st.radio(
        "Select Mode",
        ["📂 Browse Media by Category", "🦠 Find Media for Organism", "🧪 Media Panel for Sample Type", "❓ Ask Anything About Media"],
        horizontal=False,
        label_visibility="collapsed"
    )

    st.markdown("---")

    query = ""

    # Mode 1 — Browse by Category
    if "Browse" in mode:
        st.markdown("### 📂 Select Media Category")
        category = st.selectbox(
            "Category",
            options=list(MEDIA_CATEGORIES.keys()),
            label_visibility="collapsed"
        )

        st.markdown("### 🧫 Select Media")
        media = st.selectbox(
            "Media",
            options=["-- Select media --"] + MEDIA_CATEGORIES[category],
            label_visibility="collapsed"
        )

        if media != "-- Select media --":
            query = f"Explain this culture media in detail: {media}"

        specific_organism = st.text_input(
            "Looking for a specific organism on this media? (optional)",
            placeholder="e.g. E. coli, Salmonella, Staphylococcus...",
            key="browse_organism"
        )
        if specific_organism:
            query += f" — specifically for growing and identifying {specific_organism}"

    # Mode 2 — By Organism
    elif "Organism" in mode:
        st.markdown("### 🦠 Select Organism")
        organism = st.selectbox(
            "Organism",
            options=ORGANISMS_LIST,
            label_visibility="collapsed"
        )

        if organism != "-- Select Organism --":
            query = f"What culture media should I use to grow and identify {organism}?"

        purpose = st.selectbox(
            "Purpose",
            ["-- Select --", "Primary isolation", "Identification", "Subculture", "Susceptibility testing", "Storage"],
            key="purpose"
        )
        if purpose != "-- Select --":
            query += f" Purpose: {purpose}"

    # Mode 3 — By Sample Type
    elif "Sample" in mode:
        st.markdown("### 🧪 Select Sample Type")
        sample = st.selectbox(
            "Sample Type",
            options=SAMPLE_TYPES,
            label_visibility="collapsed"
        )

        if sample != "-- Select Sample --":
            query = f"What is the complete culture media panel I should use for processing a {sample} sample? Include primary, selective, differential, and enrichment media as appropriate."

        suspected_organism = st.text_input(
            "Suspected organism (optional)",
            placeholder="e.g. Suspected UTI — E. coli, or suspected TB...",
            key="suspected"
        )
        if suspected_organism:
            query += f" Suspected organism: {suspected_organism}"

    # Mode 4 — Ask Anything
    elif "Ask Anything" in mode:
        st.markdown("### ❓ Ask Any Media Question")
        query = st.text_area(
            "Your Question",
            placeholder="""Examples:
- What is the difference between MacConkey and EMB agar?
- Why does Pseudomonas produce a green pigment on certain media?
- What does beta hemolysis look like on blood agar?
- How do I prepare Lowenstein-Jensen medium for TB culture?
- What media do I use for fungal cultures from skin scrapings?""",
            height=150,
            key="media_question"
        )

    st.markdown("---")

    submit_clicked = st.button("🧫 Get Media Information", use_container_width=True)

    if submit_clicked:
        if not query or not query.strip():
            st.warning("⚠️ Please select a media, organism, sample type, or enter your question.")
        else:
            with st.spinner("🧫 Preparing media information..."):
                result = ask_claude(
                    system_prompt=SYSTEM_PROMPT,
                    user_message=query
                )

            st.markdown("---")
            st.markdown("### 🧫 Media Information")
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
                        ⚠️ <b>Note:</b> Always follow your laboratory's standard operating procedures 
                        for media preparation, quality control, and result interpretation. 
                        Media performance should be verified with known control organisms.
                    </p>
                </div>
            """, unsafe_allow_html=True)

            if "media_history" not in st.session_state:
                st.session_state.media_history = []
            st.session_state.media_history.append({
                "query": query[:80] + "..." if len(query) > 80 else query,
                "result": result
            })

    # History
    if "media_history" in st.session_state and len(st.session_state.media_history) > 1:
        st.markdown("---")
        st.markdown("### 📋 Previous Queries This Session")
        for item in reversed(st.session_state.media_history[:-1]):
            with st.expander(item["query"]):
                st.markdown(item["result"])