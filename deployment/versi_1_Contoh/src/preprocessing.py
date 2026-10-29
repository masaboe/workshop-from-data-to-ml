from __future__ import annotations

import pandas as pd

from .config import (
    RAW_FEATURE_ORDER,
    CATEGORY_MAP,
    EXTENDED_ENCODED_FEATURES,
)


def validate_profile(profile: dict[str, str]) -> None:
    missing = [
        feature
        for feature in RAW_FEATURE_ORDER
        if feature not in profile
        or profile[feature] is None
        or str(profile[feature]).strip() == ""
    ]

    if missing:
        raise ValueError(
            "Input belum lengkap: "
            + ", ".join(missing)
        )

    invalid = []

    for feature in RAW_FEATURE_ORDER:
        value = profile[feature]
        allowed = CATEGORY_MAP[feature]

        if value not in allowed:
            invalid.append(
                f"{feature}={value!r}"
            )

    if invalid:
        raise ValueError(
            "Kategori input tidak sesuai kontrak training: "
            + "; ".join(invalid)
        )


def encode_extended_profile(
    profile: dict[str, str],
) -> pd.DataFrame:
    """
    Reproduce the exact 21-column one-hot contract used by the
    Extended predictor-set training pipeline.

    Training used:
        OneHotEncoder(
            categories=explicit_categories,
            drop=None,
            handle_unknown="ignore"
        )

    For deployment, all UI values are already normalized categories,
    therefore we construct the same one-hot representation directly.
    """
    validate_profile(profile)

    row = {
        col: 0.0
        for col in EXTENDED_ENCODED_FEATURES
    }

    for feature in RAW_FEATURE_ORDER:
        value = profile[feature]
        encoded_name = f"{feature}_{value}"

        if encoded_name not in row:
            raise RuntimeError(
                "Encoded feature tidak ditemukan dalam kontrak model: "
                f"{encoded_name}"
            )

        row[encoded_name] = 1.0

    X = pd.DataFrame(
        [row],
        columns=EXTENDED_ENCODED_FEATURES,
        dtype=float,
    )

    # Every raw categorical variable must activate exactly one column.
    expected_active = len(RAW_FEATURE_ORDER)
    active = int(
        (X.iloc[0] == 1.0).sum()
    )

    if active != expected_active:
        raise RuntimeError(
            f"One-hot QA gagal: expected {expected_active} active columns, "
            f"got {active}."
        )

    return X
