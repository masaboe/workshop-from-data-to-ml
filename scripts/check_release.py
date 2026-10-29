#!/usr/bin/env python3
"""Smoke test RC1. Aman untuk dijalankan: tidak melatih/menyimpan model."""
from pathlib import Path
import argparse
import ast
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = [
    'praktikum/notebooks/01_Python_dan_Eksplorasi_Data_Modul.ipynb',
    'praktikum/notebooks/02_Input_Space_dan_Feature_Space_Modul.ipynb',
    'praktikum/notebooks/03_Preprocessing_Data_Modul.ipynb',
    'praktikum/notebooks/04_Klasifikasi_KNN_Modul.ipynb',
    'studi_kasus/notebooks/05_Memahami_dan_Membersihkan_Data_PE_Modul.ipynb',
    'studi_kasus/notebooks/06_Pipeline_dan_Evaluasi_PE_Modul.ipynb',
    'studi_kasus/notebooks/07_Ekspor_Model_dan_Hasil_Modul.ipynb',
    'deployment/Notebook_08/08_Inferensi_dan_Streamlit_Modul.ipynb',
    'praktikum/notebooks/09_Pengayaan_Klasifikasi_Teks_Modul.ipynb',
]
FILES = [
    'README.md', 'requirements.txt',
    'Modul_From_Data_to_Machine_Learning_Buku_Ajar_Lengkap.docx',
    'praktikum/data/Tab.csv', 'praktikum/data/Data.csv',
    'praktikum/data/Social_Network_Ads.csv',
    'praktikum/data/Dataset_Sentimen_Emosi.csv',
    'praktikum/data/fruits.png',
    'studi_kasus/data/asli/dataKasus-1.xlsx',
    'studi_kasus/data/hasil/data_bersih.csv',
    'studi_kasus/hasil/laporan_praktikum06.json',
    'studi_kasus/model/pe_workshop_pipeline.joblib',
    'studi_kasus/model/model_card.json',
    'deployment/versi_2_hasil_studi_kasus/app.py',
    'deployment/versi_2_hasil_studi_kasus/models/pe_workshop_pipeline.joblib',
    'deployment/versi_2_hasil_studi_kasus/models/model_card.json',
    'deployment/versi_2_hasil_studi_kasus/data/contoh_input.csv',
]

def sha256(path):
    digest=hashlib.sha256()
    with open(path,'rb') as stream:
        for block in iter(lambda:stream.read(2**20),b''):
            digest.update(block)
    return digest.hexdigest()

def check():
    errors=[]
    for rel in FILES + NOTEBOOKS:
        if not (ROOT/rel).is_file(): errors.append(f'Berkas wajib tidak ditemukan: {rel}')
    if errors: return errors

    for rel in NOTEBOOKS:
        try:
            nb=json.loads((ROOT/rel).read_text(encoding='utf-8'))
            assert nb.get('nbformat')==4 and nb.get('cells')
            assert any(c.get('cell_type')=='code' for c in nb['cells'])
        except Exception as exc:errors.append(f'Notebook tidak valid {rel}: {exc}')

    for p in (ROOT/'deployment').rglob('*.py'):
        try:ast.parse(p.read_text(encoding='utf-8'),filename=str(p))
        except Exception as exc:errors.append(f'Python syntax error {p.relative_to(ROOT)}: {exc}')
    for p in (ROOT/'studi_kasus/python').rglob('*.py'):
        try:ast.parse(p.read_text(encoding='utf-8'),filename=str(p))
        except Exception as exc:errors.append(f'Python syntax error {p.relative_to(ROOT)}: {exc}')

    model_a=ROOT/'studi_kasus/model/pe_workshop_pipeline.joblib'
    model_b=ROOT/'deployment/versi_2_hasil_studi_kasus/models/pe_workshop_pipeline.joblib'
    card_a=ROOT/'studi_kasus/model/model_card.json'
    card_b=ROOT/'deployment/versi_2_hasil_studi_kasus/models/model_card.json'
    if sha256(model_a)!=sha256(model_b):errors.append('Model sumber 07 dan deployment 08 tidak identik')
    if sha256(card_a)!=sha256(card_b):errors.append('Model card sumber 07 dan deployment 08 tidak identik')
    card=json.loads(card_b.read_text(encoding='utf-8'))
    version=card.get('sklearn_version')
    if version!='1.7.1':errors.append(f'Versi model card tidak terduga: {version}')
    deps_main=(ROOT/'requirements.txt').read_text()
    deps_deploy=(ROOT/'deployment/versi_2_hasil_studi_kasus/requirements.txt').read_text()
    for loc,txt in [('root',deps_main),('deployment v2',deps_deploy)]:
        if f'scikit-learn=={version}' not in txt:errors.append(f'Requirements {loc} berbeda dari model card: {version}')
    if len(card.get('input_features',[]))!=8:errors.append('Jumlah fitur model card bukan delapan')
    return errors

def runtime_check():
    import sklearn
    import joblib
    import pandas as pd
    import numpy as np
    base=ROOT/'deployment/versi_2_hasil_studi_kasus'
    card=json.loads((base/'models/model_card.json').read_text(encoding='utf-8'))
    if sklearn.__version__!=card['sklearn_version']:
        raise RuntimeError(
            f"Versi lingkungan {sklearn.__version__} != model card {card['sklearn_version']}; "
            'hindari memuat pickle lintas versi. Aktifkan environment Python 3.10 dan pip install -r requirements.txt.'
        )
    model=joblib.load(base/'models/pe_workshop_pipeline.joblib')
    X=pd.read_csv(base/'data/contoh_input.csv').loc[:,card['input_features']]
    assert list(model.feature_names_in_)==card['input_features']
    assert len(X)==3
    pred=model.predict(X)
    scores=model.predict_proba(X)[:,list(model.classes_).index(1)]
    assert len(pred)==len(scores)==3 and np.isfinite(scores).all()
    assert (scores>=0).all() and (scores<=1).all()
    print('PASS RUNTIME: model, versi, prediksi dan skor untuk 3 contoh.')

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--runtime',action='store_true',help='Periksa joblib (harus sesuai versi model)')
    args=parser.parse_args()
    problems=check()
    if problems:
        for problem in problems: print('FAIL:',problem)
        sys.exit(1)
    print(f'PASS STRUKTUR: {len(NOTEBOOKS)} notebook, artefak PE, requirements, sintaks.')
    if args.runtime:
        try:runtime_check()
        except Exception as exc:
            print('FAIL RUNTIME:',exc)
            sys.exit(1)
    print('RC1 smoke checks selesai.')
