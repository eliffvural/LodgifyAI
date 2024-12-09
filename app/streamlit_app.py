import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Modeli yükle
model = joblib.load("../models/eniyi.joblib")

# Başlık
st.title("Airbnb Fiyat Tahmini Uygulaması")

# Kullanıcıdan giriş al
st.sidebar.header("Ev Özelliklerini Girin")
ev_tipi = st.sidebar.selectbox("Ev Tipi", ["oda", "daire", "villa"])
konum = st.sidebar.selectbox("Konum", ["şehir merkezi", "kırsal"])
oda_sayisi = st.sidebar.slider("Oda Sayısı", 1, 10, 3)
kisi_sayisi = st.sidebar.slider("Kişi Sayısı", 1, 15, 4)
havuz = st.sidebar.selectbox("Havuz Var mı?", ["Hayır", "Evet"])
wifi = st.sidebar.selectbox("WiFi Var mı?", ["Hayır", "Evet"])
kahvalti = st.sidebar.selectbox("Kahvaltı Var mı?", ["Hayır", "Evet"])

# Girdi verilerini işleme
data = {
    "Oda Sayısı": oda_sayisi,
    "Kişi Sayısı": kisi_sayisi,
    "Havuz": 1 if havuz == "Evet" else 0,
    "WiFi": 1 if wifi == "Evet" else 0,
    "Kahvaltı": 1 if kahvalti == "Evet" else 0,
    "Ev Tipi_daire": 1 if ev_tipi == "daire" else 0,
    "Ev Tipi_villa": 1 if ev_tipi == "villa" else 0,
    "Konum_şehir merkezi": 1 if konum == "şehir merkezi" else 0,
}

input_data = pd.DataFrame([data])

# Tahmin yap
if st.button("Tahmin Et"):
    tahmin = model.predict(input_data)
    st.write(f"Tahmini Günlük Fiyat: {tahmin[0]:.2f} TL")
