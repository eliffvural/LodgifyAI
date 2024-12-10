import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os

# Çalışma dizinini alın
current_dir = os.path.dirname(__file__)
model_path = os.path.join(current_dir, "../models/eniyi.joblib")

# Modeli yükle
model = joblib.load(model_path)

# Başlık
st.title("Airbnb Fiyat Tahmini Uygulaması")

# Kullanıcı girdileri
oda_sayisi = st.sidebar.slider("Oda Sayısı", 1, 10, 3)
kisi_sayisi = st.sidebar.slider("Kişi Sayısı", 1, 15, 4)
wifi = st.sidebar.selectbox("WiFi Var mı?", ["Hayır", "Evet"])
havuz = st.sidebar.selectbox("Havuz Var mı?", ["Hayır", "Evet"])
kahvalti = st.sidebar.selectbox("Kahvaltı Var mı?", ["Hayır", "Evet"])
ev_tipi = st.sidebar.selectbox("Ev Tipi", ["oda", "daire", "villa"])
konum = st.sidebar.selectbox("Konum", ["kırsal", "şehir merkezi"])

# Tahmin için veri
data = {
    "Oda Sayısı": oda_sayisi,
    "Kişi Sayısı": kisi_sayisi,
    "WiFi": 1 if wifi == "Evet" else 0,
    "Havuz": 1 if havuz == "Evet" else 0,
    "Kahvaltı": 1 if kahvalti == "Evet" else 0,
    "Ev Tipi_daire": 1 if ev_tipi == "daire" else 0,
    "Ev Tipi_villa": 1 if ev_tipi == "villa" else 0,
    "Konum_şehir merkezi": 1 if konum == "şehir merkezi" else 0,
}

# Özellikleri modelin beklediği sırada düzenle
input_data = pd.DataFrame([data])
input_data = input_data.reindex(columns=model.feature_names_in_, fill_value=0)

# Tahmin yap
tahmin = model.predict(input_data)
st.write(f"Tahmini Günlük Fiyat: {tahmin[0]:.2f} TL")

