from __future__ import annotations

import sys

import sklearn
import xgboost

from src.config import MODEL_PATH
from src.inference import run_inference
from src.model_loader import load_model


print("=" * 78)
print("PE-TAB2CONV / EXTENDED XGBOOST DIAGNOSTIC")
print("=" * 78)
print("Python       :", sys.version.split()[0])
print("scikit-learn :", sklearn.__version__)
print("xgboost      :", xgboost.__version__)
print("Model path   :", MODEL_PATH)

model, contract = load_model(MODEL_PATH)

print("\nMODEL LOAD: OK")
print("Model class:", type(model).__name__)
print("Contract   :", contract)

profile = {
    "maternal_age_group_norm": "reproductive_healthy",
    "parity_norm": "nullipara",
    "birth_interval_norm": "first_child",
    "history_hypertension_norm": "no",
    "obesity_norm": "no",
    "history_diabetes_mellitus_norm": "no",
    "low_socioeconomic_status_norm": "above_umr",
    "prior_pe_history_norm": "no",
    "family_history_ht_pe_norm": "no",
}

result = run_inference(model, profile)

print("\nSMOKE INFERENCE: OK")
print("Score      :", result["score"])
print("Threshold  :", result["threshold"])
print("Above thr. :", result["above_threshold"])
print("Encoded dim:", result["encoded_input"].shape[1])
print("\nFINAL STATUS: READY")
