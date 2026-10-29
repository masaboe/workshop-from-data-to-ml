# Source alignment

This prototype was built from the uploaded PE-Tab2Conv training source and manuscript.

Training-source contract used for deployment:
- Extended predictor set: 9 raw categorical predictors.
- Explicit OneHotEncoder category order.
- Extended encoded dimension: 21.
- Baseline artifact naming: baseline_original_tabular_extended_XGBoost.joblib.
- XGBoost training objective: binary:logistic.
- Training used gpu_hist / gpu_predictor; deployment forces CPU prediction.
- Primary evaluation threshold: 0.50.

The model binary itself is not included in the uploaded training-source ZIP and must be copied into `models/`.
