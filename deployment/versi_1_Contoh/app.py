from __future__ import annotations

import json

import streamlit as st

from src.config import (
    APP_NAME,
    APP_SUBTITLE,
    APP_TAGLINE,
    MODEL_PATH,
    MODEL_CARD_PATH,
    PRIMARY_THRESHOLD,
)
from src.inference import run_inference
from src.model_loader import load_model
from src.ui import (
    inject_css,
    render_global_importance,
    render_profile_summary,
    render_score,
    render_temporal_metrics,
    section_header,
)


st.set_page_config(
    page_title=f"{APP_NAME} | {APP_SUBTITLE}",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()

st.markdown(
    f"""
    <div class="hero">
        <div class="hero-kicker">CLINICAL INFORMATICS • RESEARCH PROTOTYPE</div>
        <div class="hero-title">{APP_NAME}</div>
        <div class="hero-subtitle">
            <b>{APP_SUBTITLE}</b><br>
            {APP_TAGLINE}. Antarmuka ini mensimulasikan penggunaan
            <b>Extended XGBoost baseline</b> dari studi PE-Tab2Conv untuk
            memprioritaskan sinyal risiko berdasarkan data maternal rutin.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="notice">
        <b>Prototype penelitian.</b>
        Output aplikasi adalah <i>model risk score</i> untuk simulasi
        risk prioritization, bukan diagnosis, keputusan terapi, atau estimasi
        probabilitas klinis individual yang telah tervalidasi untuk penggunaan rutin.
    </div>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource(show_spinner="Memuat Extended XGBoost...")
def get_model():
    return load_model(MODEL_PATH)


if not MODEL_PATH.exists():
    st.error(
        "Artifact model belum ditemukan. "
        "Salin file berikut ke folder `models/`:"
    )
    st.code(
        "baseline_original_tabular_extended_XGBoost.joblib",
        language="text",
    )
    st.caption(
        "Setelah file model tersedia, restart Streamlit."
    )
    st.stop()


try:
    model, model_contract = get_model()
except Exception as exc:
    st.error("Model gagal dimuat atau kontrak fitur tidak cocok.")
    st.exception(exc)
    st.stop()


with st.sidebar:
    st.markdown("## PE-Tab2Conv")
    st.caption("Preeclampsia Risk Prioritization Prototype")

    st.markdown("---")
    st.markdown("### Model aktif")
    st.success("Extended XGBoost")
    st.caption("9 predictor klinis → 21 one-hot features")

    st.markdown("---")
    st.markdown("### Research threshold")
    st.metric(
        "Primary operating point",
        f"{PRIMARY_THRESHOLD:.2f}",
    )

    st.caption(
        "Threshold 0.50 digunakan sebagai operating point utama "
        "pada locked temporal validation."
    )

    st.markdown("---")
    st.caption(
        "Tidak ada identitas pasien yang diperlukan pada prototype ini."
    )


section_header(
    "SIMULATION INPUT",
    "Data maternal rutin",
    "Lengkapi sembilan predictor sesuai struktur variabel Extended pada studi.",
)

with st.form("pe_input_form"):
    c1, c2, c3 = st.columns(3, gap="large")

    with c1:
        st.markdown("#### Profil maternal")

        age = st.selectbox(
            "Kelompok usia maternal",
            [
                "— pilih —",
                "Reproductive healthy",
                "Reproductive unhealthy",
            ],
        )

        obesity = st.selectbox(
            "Obesitas",
            [
                "— pilih —",
                "Tidak",
                "Ya",
            ],
        )

        ses = st.selectbox(
            "Status sosial ekonomi",
            [
                "— pilih —",
                "Di atas UMR",
                "Di bawah UMR",
            ],
        )

    with c2:
        st.markdown("#### Riwayat obstetri")

        parity = st.selectbox(
            "Paritas",
            [
                "— pilih —",
                "Nullipara",
                "Primipara",
                "Multipara",
                "Grandemultipara",
            ],
        )

        interval = st.selectbox(
            "Jarak kelahiran",
            [
                "— pilih —",
                "Anak pertama",
                "< 2 tahun",
                "> 2 tahun",
            ],
        )

        prior_pe = st.selectbox(
            "Riwayat preeklampsia sebelumnya",
            [
                "— pilih —",
                "Tidak",
                "Ya",
            ],
        )

        family = st.selectbox(
            "Riwayat keluarga hipertensi / preeklampsia",
            [
                "— pilih —",
                "Tidak",
                "Ya",
            ],
        )

    with c3:
        st.markdown("#### Komorbid")

        hypertension = st.selectbox(
            "Riwayat hipertensi",
            [
                "— pilih —",
                "Tidak",
                "Ya",
            ],
        )

        diabetes = st.selectbox(
            "Riwayat diabetes mellitus",
            [
                "— pilih —",
                "Tidak",
                "Ya",
            ],
        )

        st.markdown(
            """
            <div class="panel" style="margin-top:1rem;">
                <b>Input contract</b><br>
                <span style="color:var(--muted);font-size:.82rem;">
                    Semua variabel dikonversi ke kategori training,
                    lalu di-encode menjadi 21 fitur dengan urutan tetap.
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    submitted = st.form_submit_button(
        "Analisis Model",
        use_container_width=True,
        type="primary",
    )


ui_to_model = {
    "age": {
        "Reproductive healthy": "reproductive_healthy",
        "Reproductive unhealthy": "reproductive_unhealthy",
    },
    "obesity": {
        "Tidak": "no",
        "Ya": "yes",
    },
    "ses": {
        "Di atas UMR": "above_umr",
        "Di bawah UMR": "below_umr",
    },
    "parity": {
        "Nullipara": "nullipara",
        "Primipara": "primipara",
        "Multipara": "multipara",
        "Grandemultipara": "grandemultipara",
    },
    "interval": {
        "Anak pertama": "first_child",
        "< 2 tahun": "lt_2_years",
        "> 2 tahun": "gt_2_years",
    },
    "prior_pe": {
        "Tidak": "no",
        "Ya": "yes",
    },
    "family": {
        "Tidak": "no",
        "Ya": "yes",
    },
    "hypertension": {
        "Tidak": "no",
        "Ya": "yes",
    },
    "diabetes": {
        "Tidak": "no",
        "Ya": "yes",
    },
}


if submitted:
    selections = {
        "age": age,
        "obesity": obesity,
        "ses": ses,
        "parity": parity,
        "interval": interval,
        "prior_pe": prior_pe,
        "family": family,
        "hypertension": hypertension,
        "diabetes": diabetes,
    }

    incomplete = [
        key
        for key, value in selections.items()
        if value == "— pilih —"
    ]

    if incomplete:
        st.warning(
            "Lengkapi seluruh sembilan predictor sebelum menjalankan model."
        )
    else:
        profile = {
            "maternal_age_group_norm": ui_to_model["age"][age],
            "parity_norm": ui_to_model["parity"][parity],
            "birth_interval_norm": ui_to_model["interval"][interval],
            "history_hypertension_norm": ui_to_model["hypertension"][hypertension],
            "obesity_norm": ui_to_model["obesity"][obesity],
            "history_diabetes_mellitus_norm": ui_to_model["diabetes"][diabetes],
            "low_socioeconomic_status_norm": ui_to_model["ses"][ses],
            "prior_pe_history_norm": ui_to_model["prior_pe"][prior_pe],
            "family_history_ht_pe_norm": ui_to_model["family"][family],
        }

        try:
            result = run_inference(
                model,
                profile,
                threshold=PRIMARY_THRESHOLD,
            )

            st.session_state["pe_result"] = result
            st.session_state["pe_profile"] = profile

        except Exception as exc:
            st.error("Inference tidak dapat diselesaikan.")
            st.exception(exc)


if "pe_result" not in st.session_state:
    st.markdown("---")
    st.info(
        "Isi form dan pilih **Analisis Model** untuk menampilkan simulasi hasil penelitian."
    )
    st.stop()


result = st.session_state["pe_result"]
profile = st.session_state["pe_profile"]

st.markdown("---")

tab_result, tab_factors, tab_model = st.tabs(
    [
        "Hasil Skrining",
        "Ringkasan Faktor",
        "Tentang Model AI",
    ]
)


with tab_result:
    section_header(
        "MODEL OUTPUT",
        "Simulasi hasil risk prioritization",
        "Skor berasal dari predict_proba() Extended XGBoost dan dibandingkan dengan research threshold 0.50.",
    )

    left, right = st.columns([1.05, 1.0], gap="large")

    with left:
        render_score(
            result["score"],
            result["threshold"],
        )

    with right:
        st.markdown(
            """
            <div class="panel">
                <div class="section-kicker">MEMBACA NILAI AI</div>
                <b>Model score bukan kepastian diagnosis.</b>
                <div style="color:var(--muted);font-size:.88rem;line-height:1.55;margin-top:.55rem;">
                    Nilai ini adalah probabilitas keluaran model untuk kelas preeklampsia
                    berdasarkan pola yang dipelajari dari cohort pengembangan.
                    Threshold 0.50 hanya merupakan operating point penelitian.
                    Karena studi menemukan underprediction pada tingkat cohort,
                    skor tidak boleh dianggap sebagai probabilitas klinis absolut
                    individual tanpa recalibration dan validasi prospektif.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<div style='height:.7rem'></div>", unsafe_allow_html=True)

        st.markdown(
            f"""
            <div class="panel">
                <div class="section-kicker">INFERENCE STATUS</div>
                <b>Feature contract:</b>
                {'terverifikasi' if model_contract['feature_contract_checked'] else 'jumlah fitur diverifikasi'}<br>
                <span style="color:var(--muted);font-size:.82rem;">
                    Input: 9 predictor • Encoded: 21 features • Model: Extended XGBoost
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("### Referensi performa temporal model")
    render_temporal_metrics()

    st.caption(
        "Metrik di atas merupakan performa model pada locked temporal validation RS Adhyatma 2023, "
        "bukan confidence interval untuk individu yang sedang disimulasikan."
    )


with tab_factors:
    section_header(
        "INPUT TRACE",
        "Ringkasan faktor yang masuk ke model",
        "Tabel ini hanya merangkum input simulasi; bukan penilaian kausal terhadap faktor pasien.",
    )

    render_profile_summary(profile)

    st.markdown("### Faktor dengan importance global tertinggi pada studi")
    render_global_importance()

    st.caption(
        "Urutan tersebut merupakan ringkasan global feature importance dari model penelitian, "
        "bukan penjelasan individual seperti SHAP dan bukan hubungan sebab-akibat."
    )


with tab_model:
    section_header(
        "MODEL CARD",
        "Extended XGBoost baseline",
        "Mesin prediksi prototype berasal dari baseline tabular Extended pada studi PE-Tab2Conv.",
    )

    a, b, c = st.columns(3, gap="medium")

    with a:
        st.markdown(
            """
            <div class="panel">
                <div class="section-kicker">REPRESENTATION</div>
                <b>Original tabular</b><br>
                <span style="color:var(--muted);font-size:.84rem;">
                    9 predictor kategorikal → 21 fitur one-hot.
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with b:
        st.markdown(
            """
            <div class="panel">
                <div class="section-kicker">MODEL</div>
                <b>XGBoost Extended</b><br>
                <span style="color:var(--muted);font-size:.84rem;">
                    Binary logistic objective; model dipilih dengan kriteria multi-metrik.
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c:
        st.markdown(
            """
            <div class="panel">
                <div class="section-kicker">VALIDATION</div>
                <b>Locked temporal</b><br>
                <span style="color:var(--muted);font-size:.84rem;">
                    Development 2021–2022; temporal validation 2023.
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("### Batas interpretasi")
    st.markdown(
        """
        - Prototype ini merepresentasikan **within-site Extended model**, bukan model portable lintas rumah sakit.
        - Dua predictor Extended—riwayat preeklampsia dan riwayat keluarga hipertensi/preeklampsia—tidak tersedia secara struktural pada cohort eksternal RSW dalam studi.
        - Model belum dimaksudkan untuk diagnosis, terapi, atau keputusan klinis otomatis.
        - Recalibration, balanced external validation, dan prospective workflow evaluation masih diperlukan sebelum implementasi klinis.
        """
    )

    with st.expander("Lihat kontrak fitur encoded"):
        st.dataframe(
            result["encoded_input"].T.rename(
                columns={0: "value"}
            ),
            use_container_width=True,
        )

    if MODEL_CARD_PATH.exists():
        with st.expander("Metadata model card"):
            card = json.loads(
                MODEL_CARD_PATH.read_text(
                    encoding="utf-8"
                )
            )
            st.json(card)
