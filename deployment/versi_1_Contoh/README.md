# PE-Tab2Conv — Preeclampsia Risk Prioritization Prototype

A Streamlit research prototype for simulating the **Extended XGBoost baseline**
from the PE-Tab2Conv preeclampsia study.

> This is a research interface, not a diagnostic device.

## Why this model

The manuscript retains **Extended XGBoost** as the primary temporal model
because it achieved the strongest combined profile across AUPRC, Brier score,
threshold-based performance, and false-positive burden.

The product brand is **PE-Tab2Conv**, while the active prediction engine in this
prototype is transparently identified as the **Original-tabular Extended XGBoost
baseline**.

## Required model artifact

Copy:

```text
baseline_original_tabular_extended_XGBoost.joblib
```

into:

```text
models/
```

Final structure:

```text
PE_Tab2Conv_Preeclampsia_Prototype/
├── app.py
├── diagnose_model.py
├── environment.yml
├── requirements.txt
├── models/
│   └── baseline_original_tabular_extended_XGBoost.joblib
├── metadata/
│   └── model_card.json
├── src/
│   ├── config.py
│   ├── preprocessing.py
│   ├── model_loader.py
│   ├── inference.py
│   └── ui.py
└── .streamlit/
    └── config.toml
```

## Recommended conda setup

### Option A — environment.yml

```bash
conda env create -f environment.yml
conda activate petab2conv
```

### Option B — create manually

```bash
conda create -n petab2conv python=3.10 -y
conda activate petab2conv
conda install -c conda-forge libomp -y
pip install -r requirements.txt
```

The training manuscript reports Python 3.10.6, scikit-learn 1.2.0, and XGBoost
1.7.5. The deployment environment therefore pins the same scikit-learn and
XGBoost versions.

## Verify the artifact

Before running Streamlit:

```bash
python diagnose_model.py
```

Expected final line:

```text
FINAL STATUS: READY
```

The diagnostic checks:
- artifact loading;
- CPU prediction compatibility;
- 21-feature contract;
- one-hot encoding;
- `predict_proba()` smoke inference.

## Run

```bash
streamlit run app.py
```

Streamlit will print a local address, normally:

```text
http://localhost:8501
```

## Feature contract

The UI collects 9 categorical predictors and recreates the exact Extended
one-hot layout used in training:

1. maternal age group
2. parity
3. birth interval
4. history of hypertension
5. obesity
6. history of diabetes mellitus
7. low socioeconomic status
8. prior preeclampsia history
9. family history of hypertension / preeclampsia

These become 21 fixed-order encoded features.

## Interpretation

The interface intentionally uses the term **AI Model Score**, not “diagnostic
probability.” The manuscript reports cohort-level underprediction on locked
temporal validation. Therefore the score is presented for research
risk-prioritization simulation and should not be treated as calibrated absolute
individual clinical risk.

The primary research threshold is fixed at 0.50.

## macOS note

If XGBoost reports an OpenMP / `libomp` error, activate the conda environment
and run:

```bash
conda install -c conda-forge libomp -y
```
