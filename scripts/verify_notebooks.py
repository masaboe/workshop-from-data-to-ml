#!/usr/bin/env python3
"""Verifikasi semua notebook dari 01 sampai 09 pada salinan temporer; tidak menimpa model sumber."""
from pathlib import Path
import tempfile
import shutil
import sys
import time
import nbformat
from nbclient import NotebookClient

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
 'praktikum/notebooks/09_Pengayaan_Klasifikasi_Teks_Modul.ipynb'
]
with tempfile.TemporaryDirectory(prefix='ml-workshop-test-') as temp:
    test_root=Path(temp)/'Workshop_From_Data_to_ML'
    shutil.copytree(ROOT,test_root,ignore=shutil.ignore_patterns('.venv','__pycache__','.ipynb_checkpoints','.git'))
    for relative_path in NOTEBOOKS:
        started=time.monotonic()
        try:
            nb=nbformat.read(test_root/relative_path,as_version=4)
            NotebookClient(nb,timeout=240,kernel_name='python3',resources={'metadata':{'path':str(test_root)}}).execute()
            print(f'PASS {relative_path} ({time.monotonic()-started:.1f}s)',flush=True)
        except Exception as exc:
            print(f'FAIL {relative_path}: {exc}',file=sys.stderr,flush=True)
            sys.exit(1)
print('PASS: semua 9 notebook berhasil dieksekusi pada salinan temporer.')
