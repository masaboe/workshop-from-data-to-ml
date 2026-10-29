from __future__ import annotations

import textwrap

import streamlit as st

from .config import (
    DISPLAY_LABELS,
    VALUE_LABELS,
    TEMPORAL_METRICS,
    GLOBAL_IMPORTANCE_ORDER,
)


def inject_css():
    st.markdown(
        textwrap.dedent(
            """
            <style>
                :root {
                    --ink: #18222b;
                    --muted: #6b7a86;
                    --paper: #f5f8fa;
                    --panel: #ffffff;
                    --line: #dce5ea;
                    --brand: #176b73;
                    --brand-dark: #104e55;
                    --brand-soft: #e8f4f4;
                    --navy: #243a4a;
                    --positive: #1e7a61;
                    --warning: #a06b16;
                    --danger: #b54b4b;
                    --danger-soft: #fff0f0;
                    --shadow: rgba(27, 55, 68, 0.08);
                }

                .stApp {
                    background:
                        radial-gradient(circle at 90% 0%, #e9f6f7 0, transparent 26rem),
                        var(--paper);
                }

                .block-container {
                    max-width: 1180px;
                    padding-top: 1.8rem;
                    padding-bottom: 4rem;
                }

                [data-testid="stSidebar"] {
                    background: #eef4f6;
                    border-right: 1px solid var(--line);
                }

                .hero {
                    position: relative;
                    overflow: hidden;
                    border: 1px solid var(--line);
                    border-radius: 24px;
                    padding: 1.7rem 1.8rem;
                    background: linear-gradient(135deg, #ffffff 0%, #eef8f8 100%);
                    box-shadow: 0 16px 42px var(--shadow);
                    margin-bottom: 1.2rem;
                }

                .hero:after {
                    content: "";
                    position: absolute;
                    width: 240px;
                    height: 240px;
                    border: 36px solid rgba(23, 107, 115, .10);
                    border-radius: 50%;
                    right: -90px;
                    top: -125px;
                }

                .hero-kicker {
                    color: var(--brand);
                    font-weight: 800;
                    letter-spacing: .15em;
                    font-size: .7rem;
                    margin-bottom: .35rem;
                }

                .hero-title {
                    color: var(--ink);
                    font-size: 2.35rem;
                    font-weight: 830;
                    line-height: 1.05;
                }

                .hero-subtitle {
                    color: var(--muted);
                    font-size: 1rem;
                    line-height: 1.55;
                    margin-top: .5rem;
                    max-width: 800px;
                }

                .notice {
                    border: 1px solid #d8e8ea;
                    border-left: 4px solid var(--brand);
                    border-radius: 13px;
                    background: #f9fcfc;
                    padding: .9rem 1rem;
                    color: var(--navy);
                    font-size: .88rem;
                    margin-bottom: 1.2rem;
                }

                .section-kicker {
                    color: var(--brand);
                    font-size: .7rem;
                    font-weight: 820;
                    letter-spacing: .13em;
                    text-transform: uppercase;
                    margin-bottom: .15rem;
                }

                .section-title {
                    color: var(--ink);
                    font-size: 1.35rem;
                    font-weight: 800;
                    margin-bottom: .35rem;
                }

                .panel {
                    background: var(--panel);
                    border: 1px solid var(--line);
                    border-radius: 18px;
                    padding: 1rem 1.05rem;
                    box-shadow: 0 8px 22px var(--shadow);
                }

                .result-card {
                    background: linear-gradient(145deg, #ffffff 0%, #f1f8f8 100%);
                    border: 1px solid #d4e7e8;
                    border-radius: 22px;
                    padding: 1.3rem 1.35rem;
                    box-shadow: 0 12px 32px var(--shadow);
                }

                .result-card.result-high {
                    background: linear-gradient(145deg, #ffffff 0%, #fff5f3 100%);
                    border-color: #efcdca;
                }

                .score-label {
                    color: var(--muted);
                    font-size: .75rem;
                    font-weight: 800;
                    letter-spacing: .08em;
                    text-transform: uppercase;
                }

                .score-value {
                    color: var(--brand-dark);
                    font-size: 3rem;
                    font-weight: 850;
                    line-height: 1;
                    margin-top: .45rem;
                }

                .result-high .score-value {
                    color: var(--danger);
                }

                .risk-status {
                    margin-top: .85rem;
                    font-size: 1.06rem;
                    line-height: 1.35;
                    font-weight: 850;
                    color: var(--positive);
                }

                .result-high .risk-status {
                    color: var(--danger);
                }

                .risk-explanation {
                    margin-top: .55rem;
                    color: var(--muted);
                    font-size: .86rem;
                    line-height: 1.55;
                }

                .score-state {
                    display: inline-block;
                    margin-top: .7rem;
                    padding: .38rem .65rem;
                    border-radius: 999px;
                    background: var(--brand-soft);
                    color: var(--brand-dark);
                    font-size: .78rem;
                    font-weight: 800;
                }

                .result-high .score-state {
                    background: var(--danger-soft);
                    color: var(--danger);
                }

                .score-track {
                    position: relative;
                    margin-top: 1.1rem;
                    height: 10px;
                    background: #e5edf0;
                    border-radius: 999px;
                    overflow: visible;
                }

                .score-fill {
                    height: 10px;
                    border-radius: 999px;
                    background: linear-gradient(90deg, #69aeb1 0%, #176b73 100%);
                }

                .result-high .score-fill {
                    background: linear-gradient(90deg, #efb2aa 0%, #b54b4b 100%);
                }

                .threshold-line {
                    position: absolute;
                    top: -5px;
                    width: 2px;
                    height: 20px;
                    background: #a06b16;
                }

                .threshold-caption {
                    display: flex;
                    justify-content: space-between;
                    color: var(--muted);
                    font-size: .72rem;
                    margin-top: .45rem;
                }

                .plain-language-box {
                    margin-top: 1rem;
                    padding: .85rem .95rem;
                    border-radius: 14px;
                    background: rgba(23, 107, 115, .06);
                    border: 1px solid rgba(23, 107, 115, .14);
                    color: var(--navy);
                    font-size: .84rem;
                    line-height: 1.55;
                }

                .result-high .plain-language-box {
                    background: rgba(181, 75, 75, .06);
                    border-color: rgba(181, 75, 75, .16);
                }

                .metric-grid {
                    display: grid;
                    grid-template-columns: repeat(4, minmax(0, 1fr));
                    gap: .7rem;
                }

                .metric-card {
                    background: #fff;
                    border: 1px solid var(--line);
                    border-radius: 15px;
                    padding: .8rem .9rem;
                }

                .metric-name {
                    color: var(--muted);
                    font-size: .72rem;
                    font-weight: 760;
                }

                .metric-value {
                    color: var(--ink);
                    font-size: 1.25rem;
                    font-weight: 820;
                    margin-top: .2rem;
                }

                .stTabs [data-baseweb="tab-list"] {
                    gap: .55rem;
                    padding: .5rem;
                    border: 1px solid var(--line);
                    border-radius: 15px;
                    background: #fff;
                    margin-bottom: 1.1rem;
                }

                .stTabs [data-baseweb="tab"] {
                    padding: .7rem 1rem !important;
                    border-radius: 10px;
                    color: var(--muted);
                }

                .stTabs [data-baseweb="tab"]:hover {
                    background: #f0f6f7;
                    color: var(--ink);
                }

                .stTabs [aria-selected="true"] {
                    color: var(--brand-dark) !important;
                    background: var(--brand-soft) !important;
                    font-weight: 800 !important;
                }

                .stTabs [data-baseweb="tab-highlight"],
                .stTabs [data-baseweb="tab-border"] {
                    display: none;
                }

                @media (max-width: 850px) {
                    .metric-grid {
                        grid-template-columns: repeat(2, minmax(0, 1fr));
                    }
                }
            </style>
            """
        ),
        unsafe_allow_html=True,
    )


def section_header(kicker: str, title: str, subtitle: str | None = None):
    st.markdown(
        textwrap.dedent(
            f"""
            <div class="section-kicker">{kicker}</div>
            <div class="section-title">{title}</div>
            """
        ),
        unsafe_allow_html=True,
    )

    if subtitle:
        st.caption(subtitle)


def render_score(score: float, threshold: float):
    """
    Lay-friendly risk presentation.

    The score is the model output, not a clinical diagnosis.
    Classification shown here is only relative to the research threshold.
    """
    pct = float(score) * 100.0
    thr_pct = float(threshold) * 100.0
    above = score >= threshold

    if above:
        card_class = "result-card result-high"
        headline = "Terindikasi risiko tinggi oleh model"
        state = f"Skor melewati ambang penelitian {thr_pct:.0f}%"
        explanation = (
            f"Skor AI sebesar {pct:.1f}% berada di atas ambang penelitian "
            f"{thr_pct:.0f}%. Dalam simulasi ini, model memasukkan profil "
            "ke kelompok prioritas risiko tinggi."
        )
        plain = (
            "<b>Catatan:</b> hasil AI memberi sinyal yang perlu "
            "mendapat perhatian lebih lanjut. Ini <b>bukan berarti diagnosis "
            "preeklampsia sudah pasti</b>; evaluasi klinis tetap diperlukan."
        )
    else:
        card_class = "result-card"
        headline = "Belum terindikasi risiko tinggi oleh model"
        state = f"Skor berada di bawah ambang penelitian {thr_pct:.0f}%"
        explanation = (
            f"Skor AI sebesar {pct:.1f}% berada di bawah ambang penelitian "
            f"{thr_pct:.0f}%. Dalam simulasi ini, model tidak memasukkan profil "
            "ke kelompok prioritas risiko tinggi."
        )
        plain = (
            "<b>Catatan:</b> model tidak memberi tanda risiko tinggi "
            "pada simulasi ini. Namun hasil ini <b>bukan berarti risiko pasti "
            "tidak ada</b> dan tidak menggantikan pemeriksaan klinis."
        )

    # IMPORTANT:
    # Keep the whole card as a single uninterrupted HTML string.
    # Blank lines / indented HTML inside st.markdown can make Streamlit's
    # Markdown parser render the remaining tags as a code block.
    html = (
        f'<div class="{card_class}">'
        f'<div class="score-label">AI MODEL SCORE</div>'
        f'<div class="score-value">{pct:.1f}%</div>'
        f'<div class="risk-status">{headline}</div>'
        f'<div class="risk-explanation">{explanation}</div>'
        f'<div class="score-state">{state}</div>'
        f'<div class="score-track">'
        f'<div class="score-fill" style="width:{pct:.1f}%"></div>'
        f'<div class="threshold-line" style="left:{thr_pct:.1f}%"></div>'
        f'</div>'
        f'<div class="threshold-caption">'
        f'<span>0%</span>'
        f'<span>Ambang penelitian {thr_pct:.0f}%</span>'
        f'<span>100%</span>'
        f'</div>'
        f'<div class="plain-language-box">{plain}</div>'
        f'</div>'
    )

    st.markdown(
        html,
        unsafe_allow_html=True,
    )

def render_temporal_metrics():
    """
    Render temporal-validation reference metrics.

    HTML is intentionally assembled without blank lines/indentation because
    Streamlit's Markdown parser may otherwise render later <div> blocks as code.
    """
    metric_order = [
        "AUROC",
        "AUPRC",
        "Brier",
        "Sensitivity@0.50",
        "Specificity@0.50",
        "PPV@0.50",
        "F1@0.50",
    ]

    cards = "".join(
        (
            f'<div class="metric-card">'
            f'<div class="metric-name">{key}</div>'
            f'<div class="metric-value">{TEMPORAL_METRICS[key]:.3f}</div>'
            f'</div>'
        )
        for key in metric_order
    )

    html = f'<div class="metric-grid">{cards}</div>'

    st.markdown(
        html,
        unsafe_allow_html=True,
    )

def render_profile_summary(profile: dict[str, str]):
    rows = []

    for feature, value in profile.items():
        rows.append(
            {
                "Variabel": DISPLAY_LABELS.get(
                    feature,
                    feature,
                ),
                "Input": VALUE_LABELS.get(
                    value,
                    value,
                ),
            }
        )

    st.dataframe(
        rows,
        use_container_width=True,
        hide_index=True,
    )


def render_global_importance():
    """
    Render global feature-importance order as compact cards.
    Each card is emitted as one uninterrupted HTML string.
    """
    for idx, item in enumerate(
        GLOBAL_IMPORTANCE_ORDER,
        start=1,
    ):
        html = (
            f'<div class="panel" style="margin-bottom:.55rem;padding:.72rem .9rem;">'
            f'<span style="color:var(--brand);font-weight:850;margin-right:.55rem;">'
            f'{idx:02d}'
            f'</span>'
            f'<span style="color:var(--ink);font-weight:700;">'
            f'{item}'
            f'</span>'
            f'</div>'
        )

        st.markdown(
            html,
            unsafe_allow_html=True,
        )

