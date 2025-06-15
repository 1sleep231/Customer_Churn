from flask import Flask, render_template, request
import joblib
import pandas as pd
import numpy as np

# Inisialisasi aplikasi Flask
app = Flask(__name__)

# Muat (load) model dan objek preprocessor yang telah disimpan
model = joblib.load('best_model.pkl')
le_gender = joblib.load('label_encoder_gender.pkl')
scaler = joblib.load('scaler.pkl')

# --- DEFINISIKAN ULANG VARIABEL SESUAI KONDISI AKHIR NOTEBOOK ANDA ---

# Definisikan pemetaan untuk Geography
geo_map = {'France': 0, 'Spain': 0, 'Germany': 1}

# Definisikan kolom yang di-scaling (tanpa fitur yang dihapus)
scl_columns = ['CreditScore', 'Age', 'Balance']

# Definisikan URUTAN AKHIR SEMUA FITUR yang digunakan model
# (tanpa fitur yang dihapus)
final_feature_order = [
    'CreditScore', 'Geography', 'Gender', 'Age', 
    'Balance', 'NumOfProducts', 'IsActiveMember'
]
# --------------------------------------------------------------------


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # 1. Mengambil data input dari form (hanya fitur yang relevan)
    input_data = {
        'CreditScore': [int(request.form['credit_score'])],
        'Geography': [request.form['geography']],
        'Gender': [request.form['gender']],
        'Age': [int(request.form['age'])],
        'Balance': [float(request.form['balance'])],
        'NumOfProducts': [int(request.form['num_of_products'])],
        'IsActiveMember': [int(request.form['is_active_member'])],
    }
    
    # 2. Membuat DataFrame dari data input
    input_df = pd.DataFrame(input_data)
    
    # 3. Preprocessing data input (SAMA PERSIS seperti saat training)
    
    # Terapkan pemetaan manual untuk 'Geography'
    input_df['Geography'] = input_df['Geography'].map(geo_map)
    
    # Terapkan LabelEncoder untuk 'Gender'
    input_df['Gender'] = le_gender.transform(input_df['Gender'])
    
    # Scaling fitur numerik tertentu
    input_df[scl_columns] = scaler.transform(input_df[scl_columns])
    
    # Pastikan urutan kolom sudah benar sebelum prediksi
    final_input_df = input_df[final_feature_order]
    
    # 4. Melakukan prediksi
    churn_probability = model.predict_proba(final_input_df)[0][1]
    
    # 5. Menyiapkan hasil untuk ditampilkan
    prediction_text = f'Probabilitas Pelanggan Akan Churn: {churn_probability * 100:.2f}%'
    
    if churn_probability > 0.5:
        recommendation = 'Rekomendasi: Pelanggan ini berisiko tinggi! Pertimbangkan untuk program retensi.'
    else:
        recommendation = 'Rekomendasi: Pelanggan ini berisiko rendah.'
        
    return render_template('index.html', prediction_text=prediction_text, recommendation_text=recommendation)
        
if __name__ == '__main__':
    app.run(debug=True)