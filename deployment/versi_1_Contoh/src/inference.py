from __future__ import annotations

import numpy as np

from .config import PRIMARY_THRESHOLD
from .preprocessing import encode_extended_profile


def positive_probability(model, X) -> float:
    if hasattr(model, "predict_proba"):
        proba = model.predict_proba(X)
        arr = np.asarray(proba)

        if arr.ndim == 2 and arr.shape[1] >= 2:
            return float(arr[0, 1])

        return float(arr.reshape(-1)[0])

    raise TypeError(
        "Artifact model tidak menyediakan predict_proba()."
    )


def run_inference(
    model,
    profile: dict[str, str],
    threshold: float = PRIMARY_THRESHOLD,
) -> dict:
    X = encode_extended_profile(profile)
    score = positive_probability(model, X)

    if not np.isfinite(score):
        raise RuntimeError(
            "Model menghasilkan probabilitas non-finite."
        )

    score = float(
        np.clip(score, 0.0, 1.0)
    )

    return {
        "score": score,
        "threshold": float(threshold),
        "above_threshold": bool(
            score >= threshold
        ),
        "encoded_input": X,
    }
