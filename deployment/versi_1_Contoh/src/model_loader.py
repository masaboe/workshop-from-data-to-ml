from __future__ import annotations

from pathlib import Path

import joblib

from .config import EXTENDED_ENCODED_FEATURES


class ModelContractError(RuntimeError):
    pass


def _normalize_feature_names(names):
    if names is None:
        return None
    return [str(x) for x in list(names)]


def validate_model_contract(model) -> dict:
    """
    Validate the loaded XGBoost artifact against the exact feature contract
    reconstructed from the training notebooks.
    """
    expected = list(EXTENDED_ENCODED_FEATURES)

    sklearn_names = _normalize_feature_names(
        getattr(model, "feature_names_in_", None)
    )

    booster_names = None

    if hasattr(model, "get_booster"):
        try:
            booster_names = _normalize_feature_names(
                model.get_booster().feature_names
            )
        except Exception:
            booster_names = None

    checked = False

    if sklearn_names:
        checked = True
        if sklearn_names != expected:
            raise ModelContractError(
                "feature_names_in_ pada artifact tidak sama dengan "
                "21 fitur Extended yang diharapkan."
            )

    if booster_names:
        checked = True
        if booster_names != expected:
            raise ModelContractError(
                "Feature names pada XGBoost Booster tidak sama dengan "
                "kontrak 21 fitur Extended."
            )

    n_features = getattr(
        model,
        "n_features_in_",
        None,
    )

    if n_features is not None:
        checked = True
        if int(n_features) != len(expected):
            raise ModelContractError(
                f"Artifact mengharapkan {n_features} fitur, "
                f"deployment menyediakan {len(expected)}."
            )

    return {
        "feature_contract_checked": checked,
        "expected_feature_count": len(expected),
        "sklearn_feature_names_available": bool(sklearn_names),
        "booster_feature_names_available": bool(booster_names),
    }


def force_cpu_predictor(model):
    """
    Training used gpu_hist / gpu_predictor.
    For local Streamlit deployment (including macOS), force prediction
    onto CPU without modifying learned tree weights.
    """
    try:
        model.set_params(
            predictor="cpu_predictor",
            tree_method="hist",
            gpu_id=-1,
        )
    except Exception:
        pass

    if hasattr(model, "get_booster"):
        try:
            model.get_booster().set_param(
                {
                    "predictor": "cpu_predictor",
                    "gpu_id": -1,
                }
            )
        except Exception:
            pass

    return model


def load_model(
    model_path: str | Path,
):
    model_path = Path(model_path)

    if not model_path.exists():
        raise FileNotFoundError(
            f"Model tidak ditemukan: {model_path}"
        )

    model = joblib.load(model_path)
    model = force_cpu_predictor(model)
    contract = validate_model_contract(model)

    return model, contract
