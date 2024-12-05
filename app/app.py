import streamlit as st
import joblib
import pandas as pd

from utils.data_preprocessing import preprocess_input_data
from utils.model_utils import load_model

# Model Yükleme
MODEL_PATH = "model/eniyi.joblib"
model = load_model(MODEL_PATH)

# Uygulama Başlığı
st.title("Airbnb Fiyat Tahmin Uygulaması")

# Kullanıcı Girişi
ev_tipi = st.selectbox("Ev Tipi", ["Apartman", "Villa", "Müstakil Ev"])
konum = st.selectbox("Konum", ["Şehir Merkezi", "Sahil Kenarı", "Kırsal"])
oda_sayisi = st.slider("Oda Sayısı", 1, 10, 3)
konaklama_kapasitesi = st.slider("Konaklayabilecek Kişi Sayısı", 1, 15, 4)
havuz = st.checkbox("Havuz")
wifi = st.checkbox("WiFi")
kahvalti = st.checkbox("Kahvaltı")

if st.button("Tahmin Et"):
    # Giriş Verisini Hazırlama
    user_input = pd.DataFrame({
        "Ev Tipi": [ev_tipi],
        "Konum": [konum],
        "Oda Sayısı": [oda_sayisi],
        "Konaklayabilecek Kişi Sayısı": [konaklama_kapasitesi],
        "Havuz": [havuz],
        "WiFi": [wifi],
        "Kahvaltı": [kahvalti]
    })

    # Veri Ön İşleme
    processed_input = preprocess_input_data(user_input)

    # Tahmin Yapma
    tahmin = model.predict(processed_input)

    # Sonuç Gösterme
    st.success(f"Tahmini Fiyat: {tahmin[0]:.2f} TL")
