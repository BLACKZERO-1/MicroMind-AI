import plotly.graph_objects as go
import streamlit as st
import numpy as np

def draw_bacterium(fig, cx, cy, shape="cocci", color_fill="#6A0DAD", color_border="#4B0082", size=1.0):
    """Draw a single bacterium cell"""
    if shape == "cocci":
        # Round cell
        theta = np.linspace(0, 2*np.pi, 60)
        x = cx + size * 0.35 * np.cos(theta)
        y = cy + size * 0.35 * np.sin(theta)
        fig.add_trace(go.Scatter(
            x=x, y=y, fill="toself",
            fillcolor=color_fill, opacity=0.85,
            line=dict(color=color_border, width=1.5),
            showlegend=False, hoverinfo="skip", mode="lines"
        ))
        # Shine effect
        x2 = cx - size*0.1 + size*0.1*np.cos(theta)
        y2 = cy + size*0.15 + size*0.08*np.sin(theta)
        fig.add_trace(go.Scatter(
            x=x2, y=y2, fill="toself",
            fillcolor="rgba(255,255,255,0.25)", opacity=0.6,
            line=dict(color="rgba(255,255,255,0)", width=0),
            showlegend=False, hoverinfo="skip", mode="lines"
        ))
    elif shape == "bacilli":
        # Rod shaped cell
        fig.add_shape(type="rect",
            x0=cx-size*0.15, y0=cy-size*0.4,
            x1=cx+size*0.15, y1=cy+size*0.4,
            fillcolor=color_fill, opacity=0.85,
            line=dict(color=color_border, width=1.5))
        # Rounded caps
        for cap_y in [cy-size*0.4, cy+size*0.4]:
            theta = np.linspace(0, np.pi, 30)
            direction = -1 if cap_y < cy else 1
            x = cx + size*0.15*np.cos(theta)
            y = cap_y + direction*size*0.1*np.sin(theta)
            fig.add_trace(go.Scatter(
                x=x, y=y, fill="toself",
                fillcolor=color_fill, opacity=0.85,
                line=dict(color=color_border, width=1.5),
                showlegend=False, hoverinfo="skip", mode="lines"
            ))

def show_gram_stain_visual(result_type: str = "both"):

    fig = go.Figure()

    # ── Background — microscope field ──────────────────────────────────
    # Dark microscope background
    theta = np.linspace(0, 2*np.pi, 100)

    # Left field — Gram Positive (purple field)
    if result_type in ["positive", "both"]:
        x_bg = 2.5 + 2.8*np.cos(theta)
        y_bg = 5.0 + 2.8*np.sin(theta)
        fig.add_trace(go.Scatter(
            x=x_bg, y=y_bg, fill="toself",
            fillcolor="#1a0a2e", opacity=1.0,
            line=dict(color="#0d0016", width=3),
            showlegend=False, hoverinfo="skip", mode="lines"
        ))

        # Gram positive cocci in clusters (Staph pattern)
        gp_positions = [
            (2.1,5.2),(2.5,5.2),(2.9,5.2),
            (2.1,4.85),(2.5,4.85),(2.9,4.85),
            (2.3,4.5),(2.7,4.5),
            (1.8,5.5),(3.2,5.5),
            (2.0,5.55),(2.4,5.6),(2.8,5.55),
            (2.2,6.0),(2.6,6.0),(3.0,5.95),
            (1.9,4.3),(2.5,4.2),(3.1,4.35),
            (3.3,5.0),(1.7,5.0),
        ]
        for (bx, by) in gp_positions:
            draw_bacterium(fig, bx, by, shape="cocci",
                          color_fill="#7B2FBE", color_border="#4B0082", size=0.85)

        # Field label
        fig.add_annotation(x=2.5, y=2.0,
            text="<b>🟣 GRAM POSITIVE</b>",
            showarrow=False,
            font=dict(size=13, color="#C084FC", family="Arial Black"),
            bgcolor="rgba(0,0,0,0.7)",
            bordercolor="#7B2FBE",
            borderwidth=2, borderpad=6)

        fig.add_annotation(x=2.5, y=1.4,
            text="<i>Staphylococcus aureus</i> — cocci in clusters",
            showarrow=False,
            font=dict(size=10, color="#E9D5FF"),
            bgcolor="rgba(0,0,0,0.5)",
            borderpad=4)

    # ── Right field — Gram Negative (pink field) ────────────────────────
    if result_type in ["negative", "both"]:
        offset_x = 5.5 if result_type == "both" else 0

        x_bg2 = (2.5+offset_x) + 2.8*np.cos(theta)
        y_bg2 = 5.0 + 2.8*np.sin(theta)
        fig.add_trace(go.Scatter(
            x=x_bg2, y=y_bg2, fill="toself",
            fillcolor="#1a0a0e", opacity=1.0,
            line=dict(color="#160008", width=3),
            showlegend=False, hoverinfo="skip", mode="lines"
        ))

        # Gram negative bacilli (E. coli pattern)
        gn_positions = [
            (7.5,5.3),(8.1,5.1),(8.7,5.4),
            (7.3,4.7),(7.9,4.6),(8.5,4.8),
            (7.6,5.9),(8.2,5.8),(8.8,5.7),
            (7.2,5.5),(8.9,5.2),
            (7.7,4.2),(8.3,4.3),
            (7.4,6.3),(8.0,6.4),(8.6,6.2),
        ]
        for (bx, by) in gn_positions:
            draw_bacterium(fig, bx, by, shape="bacilli",
                          color_fill="#E91E8C", color_border="#880E4F", size=0.85)

        fig.add_annotation(x=2.5+offset_x, y=2.0,
            text="<b>🩷 GRAM NEGATIVE</b>",
            showarrow=False,
            font=dict(size=13, color="#F9A8D4", family="Arial Black"),
            bgcolor="rgba(0,0,0,0.7)",
            bordercolor="#E91E8C",
            borderwidth=2, borderpad=6)

        fig.add_annotation(x=2.5+offset_x, y=1.4,
            text="<i>Escherichia coli</i> — bacilli (rod-shaped)",
            showarrow=False,
            font=dict(size=10, color="#FBCFE8"),
            bgcolor="rgba(0,0,0,0.5)",
            borderpad=4)

    # ── Staining Steps Timeline ─────────────────────────────────────────
    steps = [
        {"x":1.2, "color":"#5B21B6", "label":"① Crystal Violet", "desc":"Primary stain\nAll cells purple"},
        {"x":3.2, "color":"#78350F", "label":"② Gram's Iodine", "desc":"Mordant\nFixes stain to wall"},
        {"x":5.2, "color":"#D1D5DB", "label":"③ Decolorizer", "desc":"Acetone/Alcohol\nGN loses color"},
        {"x":7.2, "color":"#BE185D", "label":"④ Safranin", "desc":"Counterstain\nGN turns pink"},
    ]

    for i, step in enumerate(steps):
        # Arrow connector
        if i < len(steps)-1:
            fig.add_annotation(
                x=step["x"]+0.85, y=-1.0,
                text="→",
                showarrow=False,
                font=dict(size=20, color="#9CA3AF"))

        # Step box
        fig.add_shape(type="rect",
            x0=step["x"]-0.6, y0=-1.6,
            x1=step["x"]+0.6, y1=-0.4,
            fillcolor=step["color"], opacity=0.9,
            line=dict(color="#1F2937", width=1.5))

        fig.add_annotation(x=step["x"], y=-1.0,
            text=f"<b>{step['label']}</b><br><span style='font-size:9px'>{step['desc']}</span>",
            showarrow=False,
            font=dict(size=10, color="white"),
            align="center")

    # ── Cell wall structure legend ──────────────────────────────────────
    fig.add_annotation(x=2.5, y=8.1,
        text="<b>THICK peptidoglycan</b><br>Traps crystal violet complex",
        showarrow=False,
        font=dict(size=10, color="#C084FC"),
        bgcolor="rgba(20,0,40,0.85)",
        bordercolor="#7B2FBE",
        borderwidth=1, borderpad=5)

    if result_type == "both":
        fig.add_annotation(x=8.0, y=8.1,
            text="<b>THIN peptidoglycan + Outer membrane</b><br>Crystal violet washes out",
            showarrow=False,
            font=dict(size=10, color="#F9A8D4"),
            bgcolor="rgba(40,0,20,0.85)",
            bordercolor="#E91E8C",
            borderwidth=1, borderpad=5)

    # ── Layout ──────────────────────────────────────────────────────────
    fig.update_layout(
        title=dict(
            text="🔬 Gram Staining — Microscopic View & Cell Wall Comparison",
            font=dict(size=15, color="#25B89A"),
            x=0.5
        ),
        xaxis=dict(
            range=[-0.2, 11.5] if result_type == "both" else [-0.2, 5.5],
            showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(
            range=[-2.5, 9.0],
            showgrid=False, zeroline=False, showticklabels=False),
        plot_bgcolor="#0D1B2A",
        paper_bgcolor="#0D1B2A",
        height=550,
        margin=dict(l=10, r=10, t=50, b=10),
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)

    # ── Summary cards ───────────────────────────────────────────────────
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
            <div style="background:linear-gradient(135deg,#2D1B69,#1a0a2e);
                        border-left:4px solid #7B2FBE;
                        padding:14px; border-radius:10px;">
                <h4 style="color:#C084FC; margin:0 0 8px 0;">🟣 Gram Positive</h4>
                <table style="color:#E9D5FF; font-size:12px; width:100%;">
                    <tr><td>Cell wall</td><td><b>Thick peptidoglycan (20-80nm)</b></td></tr>
                    <tr><td>Outer membrane</td><td><b>Absent</b></td></tr>
                    <tr><td>Crystal violet</td><td><b>Retained → Purple</b></td></tr>
                    <tr><td>Safranin</td><td><b>Masked</b></td></tr>
                    <tr><td>Final color</td><td><b style="color:#C084FC;">PURPLE / VIOLET</b></td></tr>
                    <tr><td>Examples</td><td><i>S. aureus, S. pyogenes, B. anthracis</i></td></tr>
                </table>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div style="background:linear-gradient(135deg,#4C0519,#1a0a0e);
                        border-left:4px solid #E91E8C;
                        padding:14px; border-radius:10px;">
                <h4 style="color:#F9A8D4; margin:0 0 8px 0;">🩷 Gram Negative</h4>
                <table style="color:#FBCFE8; font-size:12px; width:100%;">
                    <tr><td>Cell wall</td><td><b>Thin peptidoglycan (2-7nm)</b></td></tr>
                    <tr><td>Outer membrane</td><td><b>Present (LPS layer)</b></td></tr>
                    <tr><td>Crystal violet</td><td><b>Lost during decolorization</b></td></tr>
                    <tr><td>Safranin</td><td><b>Absorbed → Pink</b></td></tr>
                    <tr><td>Final color</td><td><b style="color:#F9A8D4;">PINK / RED</b></td></tr>
                    <tr><td>Examples</td><td><i>E. coli, Klebsiella, Pseudomonas</i></td></tr>
                </table>
            </div>
        """, unsafe_allow_html=True)