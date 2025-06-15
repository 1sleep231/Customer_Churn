# =================================================================
# SCRIPT UNTUK MEMBUAT ASET PREPROCESSOR YANG PASTI BENAR
# File: prepare_assets.py
# =================================================================

# 1. Import library yang dibutuhkan
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
import joblib

print("Memulai proses persiapan aset...")

# 2. Muat data mentah
# !!! PENTING: GANTI 'nama_file_data_asli.csv' DENGAN NAMA FILE DATA ANDA !!!
try:
    df = pd.read_csv('Churn_Modelling.csv') # GANTI NAMA FILE DI SINI
    print("Data mentah berhasil dimuat.")
except FileNotFoundError:
    print("Error: Ganti 'nama_file_data_asli.csv' dengan nama file data Anda yang benar.")
    print("Pastikan file data tersebut ada di folder yang sama dengan script ini.")
    exit() # Keluar jika file tidak ditemukan

# 3. Lakukan semua langkah preprocessing PERSIS seperti di notebook

# Menghapus kolom yang tidak relevan.
# Saya tambahkan beberapa kolom ID umum lainnya untuk berjaga-jaga.
features_to_remove = [
    'RowNumber', 'CustomerId', 'Surname', # Kolom ID
    'Tenure', 'HasCrCard', 'EstimatedSalary' # Fitur yang Anda hapus
]
df = df.drop(columns=features_to_remove, errors='ignore') # errors='ignore' agar tidak error jika kolom sudah tidak ada
print("Fitur tidak relevan telah dihapus.")

# Encoding 'Geography'
geo_map = {'France': 0, 'Spain': 0, 'Germany': 1}
df['Geography'] = df['Geography'].map(geo_map)
print("Fitur 'Geography' telah di-encode.")

# --- Bagian Paling Penting ---

# Encoding 'Gender'
# Kita buat objek BARU dan langsung kita FIT pada seluruh data Gender.
# Ini aman dilakukan karena tujuannya hanya untuk menyimpan mapping ('Male' -> 1, 'Female' -> 0)
le_gender = LabelEncoder()
le_gender.fit(df['Gender']) # Cukup .fit() di sini
print("LabelEncoder untuk 'Gender' berhasil di-fit.")

# Scaling fitur numerik
# Kita buat objek BARU dan FIT pada data yang sesuai.
scaler = StandardScaler()
scl_columns = ['CreditScore', 'Age', 'Balance']
scaler.fit(df[scl_columns]) # Cukup .fit() di sini
print("StandardScaler berhasil di-fit.")

# 4. Simpan semua objek yang sudah di-fit
joblib.dump(le_gender, 'label_encoder_gender.pkl')
joblib.dump(scaler, 'scaler.pkl')

print("\n--- PROSES SELESAI ---")
print("File 'label_encoder_gender.pkl' dan 'scaler.pkl' telah berhasil dibuat/diperbarui dengan benar.")
print("Sekarang Anda bisa menjalankan aplikasi Flask Anda.")