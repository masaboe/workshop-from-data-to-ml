# From Data to Machine Learning with Python

**Workshop Machine Learning dengan Python — GitHub Release Candidate v1.0.0-rc1**

Repositori ini berisi **9 notebook praktikum berurutan**, dataset contoh, buku ajar, model hasil pelatihan, dan contoh aplikasi Streamlit. Notebook dan kode pembelajaran dari paket yang telah diuji pemiliknya **dipertahankan tanpa perubahan** pada RC1.

> **Mulai cepat:** gunakan Python **3.10** dan environment yang sama untuk Praktikum **01–09**, khususnya **05 → 06 → 07 → 08**. Artefak bawaan untuk aplikasi Streamlit versi 2 dicatat menggunakan **scikit-learn 1.7.1**. Jangan menjalankan `studi_kasus/python/pe_workflow.py` untuk membangun ulang model final: skrip lama tersebut menggunakan konfigurasi Decision Tree yang berbeda dari model final hasil CV pada Notebook 06–07.

## 1. Peta pembelajaran

| No. | Materi | Output yang dipelajari | Lokasi notebook |
|---|---|---|---|
| 01 | Python dan eksplorasi data | NumPy, Pandas, inspeksi dataset, visualisasi | `praktikum/notebooks/01_Python_dan_Eksplorasi_Data_Modul.ipynb` |
| 02 | Input Space dan Feature Space | One-Hot Encoding, TF-IDF, representasi RGB | `praktikum/notebooks/02_Input_Space_dan_Feature_Space_Modul.ipynb` |
| 03 | Data Preprocessing | Audit, imputasi, scaling, pipeline, data leakage | `praktikum/notebooks/03_Preprocessing_Data_Modul.ipynb` |
| 04 | Klasifikasi KNN | Jarak, pemilihan k, baseline, cross-validation, evaluasi | `praktikum/notebooks/04_Klasifikasi_KNN_Modul.ipynb` |
| 05 | Memahami & membersihkan data PE | Data understanding, definisi label, cleaning | `studi_kasus/notebooks/05_Memahami_dan_Membersihkan_Data_PE_Modul.ipynb` |
| 06 | Pipeline dan evaluasi PE | Decision Tree, CV train, holdout test, metrik | `studi_kasus/notebooks/06_Pipeline_dan_Evaluasi_PE_Modul.ipynb` |
| 07 | Ekspor model dan hasil | Model `.joblib`, model card, checksum, consistency check | `studi_kasus/notebooks/07_Ekspor_Model_dan_Hasil_Modul.ipynb` |
| 08 | Inferensi dan Streamlit | Muat model dari 07, prediksi, validasi input, aplikasi web | `deployment/Notebook_08/08_Inferensi_dan_Streamlit_Modul.ipynb` |
| 09 | Pengayaan klasifikasi teks | TF-IDF + Multinomial Naive Bayes, evaluasi | `praktikum/notebooks/09_Pengayaan_Klasifikasi_Teks_Modul.ipynb` |

**Alur wajib:** 01 → 02 → 03 → 04 → **05 → 06 → 07 → 08**. Notebook 09 merupakan pengayaan setelah memahami TF-IDF (02) dan klasifikasi (04). Buku ajar: [`Modul_From_Data_to_Machine_Learning_Buku_Ajar_Lengkap.docx`](Modul_From_Data_to_Machine_Learning_Buku_Ajar_Lengkap.docx).

## 2. Instalasi sekali pada folder utama

Clone atau unduh ZIP repository, ekstrak, lalu buka terminal pada direktori yang berisi `README.md` dan `requirements.txt`.

**Windows (PowerShell; Python 3.10 sudah terpasang):**

```powershell
py -3.10 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m jupyter lab
```

**macOS / Linux (Python 3.10 sudah terpasang):**

```bash
python3.10 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m jupyter lab
```

Jika menggunakan Jupyter dari instalasi terpisah, pilih kernel yang menunjuk `.venv` ini. Dari notebook, periksa:

```python
import sys, sklearn
print('Interpreter:', sys.executable)
print('Scikit-learn:', sklearn.__version__)  # 1.7.1
```

`requirements.txt` di root merupakan **satu file utama**. Requirements di `deployment/versi_2_hasil_studi_kasus/` hanya untuk aplikasi itu dan telah diselaraskan ke scikit-learn 1.7.1. Jangan memakai requirements `deployment/versi_1_Contoh/` untuk praktikum utama.

## 3. Menjalankan notebook

1. Buka notebook sesuai urutan pada tabel §1, pilih kernel `.venv`.
2. Gunakan **Kernel → Restart & Run All** pada tiap notebook.
3. Periksa tabel, grafik, jawaban, serta keluaran `praktikum/hasil/`, `studi_kasus/hasil/`, atau `hasil_praktikum08/`.
4. Pada rangkaian PE jalankan **05 → 06 → 07** sebelum menjalankan **08** jika ingin menghasilkan ulang model dengan environment Anda.
5. Notebook 07 menyimpan salinan `.joblib` dan `model_card.json` ke `studi_kasus/model/` **serta** `deployment/versi_2_hasil_studi_kasus/models/`. Kedua artefak harus berasal dari pelatihan yang sama.

**Boleh langsung ke 08?** Ya, bila menggunakan artefak bawaan yang telah diuji pada versi scikit-learn sesuai `model_card.json` (1.7.1). Jika versi tidak cocok, jangan mengedit `model_card.json` secara manual; gunakan environment yang sesuai atau ulang 06→07 dan kemudian 08.

> **Peringatan hasil tersimpan:** menjalankan notebook 05–07 akan menulis ulang file hasil dan model lokal. Ini disengaja untuk latihan. Jika ingin mempertahankan snapshot hasil yang disertakan, buat salinan repository sebelum `Run All`.

## 4. Struktur direktori

```text
Workshop_From_Data_to_ML/
├── README.md
├── requirements.txt
├── Modul_From_Data_to_Machine_Learning_Buku_Ajar_Lengkap.docx
├── praktikum/
│   ├── data/                  # Dataset untuk 01–04 dan 09
│   ├── notebooks/             # Notebook 01–04 dan 09
│   └── hasil/                 # Artefak contoh praktikum
├── studi_kasus/
│   ├── data/asli/             # Dataset contoh PE
│   ├── data/hasil/            # Data cleaning dan split
│   ├── notebooks/             # Notebook 05–07
│   ├── model/                 # Model final dan model card
│   ├── python/                # pe_workflow.py (helper sumber, model default lama)
│   └── hasil/                 # Laporan 06–07
├── deployment/
│   ├── Notebook_08/           # Notebook 08
│   ├── versi_2_hasil_studi_kasus/  # Streamlit dari model 07 (utama)
│   └── versi_1_Contoh/       # XGBoost sumber, environment TERPISAH
├── hasil_praktikum08/
├── scripts/                   # Pemeriksaan RC1
└── .github/workflows/         # CI dasar
```

## 5. Menjalankan aplikasi Streamlit (versi 2)

Setelah berhasil memuat model lewat notebook 08, dari **root repository**:

```bash
python -m streamlit run deployment/versi_2_hasil_studi_kasus/app.py
```

Masukkan data contoh dari `deployment/versi_2_hasil_studi_kasus/data/contoh_input.csv` dan bandingkan output dengan notebook 08. Bila model diekspor ulang, **restart** proses Streamlit agar cache model diperbarui. Model hanya untuk pendidikan, bukan keputusan klinis.

**Deployment versi 1** adalah aplikasi XGBoost sumber dengan kontrak fitur dan environment berbeda. Untuk mencoba, ikuti [`deployment/versi_1_Contoh/README.md`](deployment/versi_1_Contoh/README.md) dan `environment.yml` di folder tersebut. Jangan campur bobot, angka evaluasi, atau requirements dengan versi 2.

## 6. Pemeriksaan paket (RC1)

Pemeriksaan file, dependensi dan kontrak artefak (tidak melatih model):

```bash
python scripts/check_release.py
```

Jika environment sama dengan versi model bawaan (scikit-learn 1.7.1), lakukan pemeriksaan inferensi:

```bash
python scripts/check_release.py --runtime
```

GitHub Actions menjalankan pemeriksaan tersebut secara otomatis pada Python 3.10 dan dependensi root. Dokumentasi perubahan RC1: [`docs/RELEASE_RC1.md`](docs/RELEASE_RC1.md). Hasil audit: [`docs/VALIDASI_RC1.md`](docs/VALIDASI_RC1.md). Pengujian notebook 01–09 otomatis tersedia lewat **Actions → Full notebook verification → Run workflow**.

## 7. Masalah umum

| Masalah | Langkah pengecekan |
|---|---|
| `ModuleNotFoundError` | Cek kernel notebook, jalankan `python -m pip install -r requirements.txt` pada `.venv` aktif. |
| Model 1.7.1 tetapi environment 1.8.0 | Cocokkan sklearn dengan `model_card.json` atau ekspor ulang model 07; jangan paksa `joblib.load`. |
| `FileNotFoundError` | Pastikan repo diekstrak utuh, jangan memindahkan notebook dari foldernya tanpa dataset. |
| Hasil Streamlit berbeda dari notebook | Periksa model + model card, delapan nama fitur, dan restart cache/app. |
| Skrip `pe_workflow.py` menghasilkan model lain | Skrip helper sumber menggunakan Decision Tree parameter tetap; gunakan **Notebook 06 → 07** sebagai sumber artefak final. |
| Label PE sedikit | Baca confusion matrix dan recall kelas positif; accuracy saja tidak cukup. |

## 8. Penggunaan dan sumber bahan

Semua contoh klasifikasi PE adalah **demonstrasi pendidikan**, bukan sistem diagnosis, penilaian risiko klinis, atau alat keputusan medis. Dataset contoh dinyatakan aman untuk dibagikan oleh penyedia paket; pengguna ulang tetap perlu memperhatikan hak dan sumber data/komponen pihak ketiga. Repository publik tidak otomatis memberi izin penggunaan ulang seluruh materi. Lisensi menyeluruh belum dinyatakan pada RC1 dan dapat ditambahkan pemilik sebelum rilis final.

Sumber teknis: [scikit-learn model persistence](https://scikit-learn.org/stable/model_persistence.html), [scikit-learn pipelines](https://scikit-learn.org/stable/modules/compose.html), [Streamlit run](https://docs.streamlit.io/develop/api-reference/cli/run).
