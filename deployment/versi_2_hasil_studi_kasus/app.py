"""Aplikasi Streamlit untuk pembelajaran inferensi Praktikum 08.
Model dari Praktikum 07, bukan model baru. Tidak untuk keputusan klinis.
Jalankan: python -m streamlit run deployment/versi_2_hasil_studi_kasus/app.py
"""
from pathlib import Path
import json
import hashlib
import joblib
import pandas as pd
import sklearn
import streamlit as st

BASE = Path(__file__).resolve().parent
MODEL_FILE = BASE / 'models' / 'pe_workshop_pipeline.joblib'
CARD_FILE = BASE / 'models' / 'model_card.json'
EXAMPLE_FILE = BASE / 'data' / 'contoh_input.csv'

st.set_page_config(page_title='Praktikum 08 | Inferensi PE', page_icon='📘', layout='centered')
st.title('Praktikum 08 — Inferensi Model')
st.caption('Demo pendidikan: klasifikasi label PE dengan model Decision Tree hasil Praktikum 06–07.')
st.warning('Bukan alat diagnosis, skrining, atau pengambilan keputusan klinis. Gunakan input sintetis untuk latihan.')

if not MODEL_FILE.is_file() or not CARD_FILE.is_file():
    st.error('Artefak Praktikum 07 belum ditemukan. Ekstrak paket ZIP lengkap terlebih dahulu.')
    st.stop()
try:
    card = json.loads(CARD_FILE.read_text(encoding='utf-8'))
except (OSError, ValueError) as exc:
    st.error(f'Model card tidak dapat dibaca: {exc}')
    st.stop()
if card.get('sklearn_version') != sklearn.__version__:
    st.error('Versi scikit-learn saat ini tidak sama dengan versi pelatihan model. Gunakan environment yang sesuai; jangan memuat model tidak kompatibel.')
    st.stop()

@st.cache_resource
def load_model(path: str, sha256: str):
    # File joblib harus berasal dari paket yang tepercaya. Deserialisasi berisiko untuk berkas tak dikenal.
    return joblib.load(path)

sha = hashlib.sha256(MODEL_FILE.read_bytes()).hexdigest()
try:
    model = load_model(str(MODEL_FILE), sha)
except Exception as exc:
    st.error(f'Model gagal dimuat: {exc}')
    st.stop()

FEATURES = list(card['input_features'])
cat_columns = list(model.named_steps['preprocess'].transformers_[1][2])
encoder = model.named_steps['preprocess'].named_transformers_['cat'].named_steps['onehot']
choices = {col: list(cats) for col, cats in zip(cat_columns, encoder.categories_)}
assert len(FEATURES) == 8 and list(model.feature_names_in_) == FEATURES

with st.expander('Kontrak input dan asal model'):
    st.write('Fitur input:', FEATURES)
    st.write('Model:', card['model_type'])
    st.write('Parameter:', card['hyperparameters'])
    st.write('SHA-256:', sha)
    st.caption('Skor predict_proba tidak terkalibrasi, sehingga bukan peluang kejadian PE pada individu.')

st.subheader('Formulir input sintetis')
st.caption('Batas input numerik mengikuti kisaran yang terlihat dalam dataset pelatihan, bukan batas atau pedoman klinis.')
with st.form('form_sintetis'):
    usia = st.number_input('Usia (tahun)', min_value=13, max_value=43, value=24, step=1)
    paritas = st.number_input('Paritas (jumlah)', min_value=0, max_value=6, value=0, step=1)
    jarak = st.selectbox('Jarak kelahiran', choices['JARAK KELAHIRAN'], index=choices['JARAK KELAHIRAN'].index('anak pertama'))
    hip = st.selectbox('Riwayat hipertensi', choices['RIW HIPERTENSI'])
    obes = st.selectbox('Obesitas', choices['OBESITAS'])
    dm = st.selectbox('Riwayat DM', choices['RIW DM'])
    keluarga = st.selectbox('Riwayat hipertensi/PE dalam keluarga', choices['RIW HIPERTENSI/PE DALAM KELUARGA'])
    sosek = st.selectbox('Status sosial ekonomi', choices['SOSEK RENDAH'])
    submit = st.form_submit_button('Jalankan inferensi contoh', type='primary')

if submit:
    row = pd.DataFrame([{
        'USIA': float(usia), 'PARITAS': float(paritas),
        'JARAK KELAHIRAN': jarak, 'RIW HIPERTENSI': hip,
        'OBESITAS': obes, 'RIW DM': dm,
        'RIW HIPERTENSI/PE DALAM KELUARGA': keluarga,
        'SOSEK RENDAH': sosek
    }])[FEATURES]
    pred = int(model.predict(row)[0])
    i_positive = list(model.classes_).index(1)
    score = float(model.predict_proba(row)[0, i_positive])
    st.subheader('Keluaran teknis model')
    st.write('Label prediksi:', 'PE (kode 1)' if pred == 1 else 'Non PE (kode 0)')
    st.metric('Skor model untuk label PE (tidak dikalibrasi)', f'{score:.3f}')
    st.dataframe(row, use_container_width=True)
    st.info('Perubahan skor pada contoh sintetis bukan bukti sebab-akibat, bukan estimasi risiko individual, dan bukan anjuran medis.')

with st.expander('Verifikasi menggunakan contoh dari Praktikum 07'):
    if EXAMPLE_FILE.is_file():
        sample = pd.read_csv(EXAMPLE_FILE)[FEATURES]
        z = sample.copy()
        z['kelas_prediksi'] = model.predict(sample)
        z['skor_model_PE'] = model.predict_proba(sample)[:, list(model.classes_).index(1)]
        st.dataframe(z, use_container_width=True)
    else:
        st.info('contoh_input.csv tidak ditemukan.')

with st.expander('Batasan dan evaluasi model (test Praktikum 06)'):
    st.json(card['test_metrics'])
    st.write('10 kasus berlabel positif pada test; tidak ada validasi eksternal atau audit independensi pasien.')
    st.write('Aplikasi workshop ini berbeda dengan aplikasi riset XGBoost pada paket asal; evaluasi keduanya tidak dapat dipertukarkan.')
