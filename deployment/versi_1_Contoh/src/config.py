from pathlib import Path

APP_NAME = "PE-Tab2Conv"
APP_SUBTITLE = "Preeclampsia Risk Prioritization Prototype"
APP_TAGLINE = "Research interface for routine maternal-data risk prioritization"

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "baseline_original_tabular_extended_XGBoost.joblib"
MODEL_CARD_PATH = BASE_DIR / "metadata" / "model_card.json"

PRIMARY_THRESHOLD = 0.50

RAW_FEATURE_ORDER = [
    "maternal_age_group_norm",
    "parity_norm",
    "birth_interval_norm",
    "history_hypertension_norm",
    "obesity_norm",
    "history_diabetes_mellitus_norm",
    "low_socioeconomic_status_norm",
    "prior_pe_history_norm",
    "family_history_ht_pe_norm",
]

CATEGORY_MAP = {
    "maternal_age_group_norm": [
        "reproductive_healthy",
        "reproductive_unhealthy",
    ],
    "parity_norm": [
        "grandemultipara",
        "multipara",
        "nullipara",
        "primipara",
    ],
    "birth_interval_norm": [
        "first_child",
        "gt_2_years",
        "lt_2_years",
    ],
    "history_hypertension_norm": ["no", "yes"],
    "obesity_norm": ["no", "yes"],
    "history_diabetes_mellitus_norm": ["no", "yes"],
    "low_socioeconomic_status_norm": [
        "above_umr",
        "below_umr",
    ],
    "prior_pe_history_norm": ["no", "yes"],
    "family_history_ht_pe_norm": ["no", "yes"],
}

EXTENDED_ENCODED_FEATURES = [
    "maternal_age_group_norm_reproductive_healthy",
    "maternal_age_group_norm_reproductive_unhealthy",
    "parity_norm_grandemultipara",
    "parity_norm_multipara",
    "parity_norm_nullipara",
    "parity_norm_primipara",
    "birth_interval_norm_first_child",
    "birth_interval_norm_gt_2_years",
    "birth_interval_norm_lt_2_years",
    "history_hypertension_norm_no",
    "history_hypertension_norm_yes",
    "obesity_norm_no",
    "obesity_norm_yes",
    "history_diabetes_mellitus_norm_no",
    "history_diabetes_mellitus_norm_yes",
    "low_socioeconomic_status_norm_above_umr",
    "low_socioeconomic_status_norm_below_umr",
    "prior_pe_history_norm_no",
    "prior_pe_history_norm_yes",
    "family_history_ht_pe_norm_no",
    "family_history_ht_pe_norm_yes",
]

DISPLAY_LABELS = {
    "maternal_age_group_norm": "Kelompok usia maternal",
    "parity_norm": "Paritas",
    "birth_interval_norm": "Jarak kelahiran",
    "history_hypertension_norm": "Riwayat hipertensi",
    "obesity_norm": "Obesitas",
    "history_diabetes_mellitus_norm": "Riwayat diabetes mellitus",
    "low_socioeconomic_status_norm": "Status sosial ekonomi",
    "prior_pe_history_norm": "Riwayat preeklampsia sebelumnya",
    "family_history_ht_pe_norm": "Riwayat keluarga hipertensi / preeklampsia",
}

VALUE_LABELS = {
    "reproductive_healthy": "Reproductive healthy",
    "reproductive_unhealthy": "Reproductive unhealthy",
    "grandemultipara": "Grandemultipara",
    "multipara": "Multipara",
    "nullipara": "Nullipara",
    "primipara": "Primipara",
    "first_child": "Anak pertama",
    "gt_2_years": "> 2 tahun",
    "lt_2_years": "< 2 tahun",
    "yes": "Ya",
    "no": "Tidak",
    "above_umr": "Di atas UMR",
    "below_umr": "Di bawah UMR",
}

TEMPORAL_METRICS = {
    "AUROC": 0.881,
    "AUPRC": 0.761,
    "Brier": 0.036,
    "Sensitivity@0.50": 0.587,
    "Specificity@0.50": 0.9959,
    "PPV@0.50": 0.931,
    "NPV@0.50": 0.9622,
    "F1@0.50": 0.720,
}

GLOBAL_IMPORTANCE_ORDER = [
    "Riwayat preeklampsia sebelumnya",
    "Riwayat keluarga hipertensi / preeklampsia",
    "Riwayat hipertensi",
    "Riwayat diabetes mellitus",
    "Jarak kelahiran",
    "Paritas",
    "Kelompok usia maternal",
]
