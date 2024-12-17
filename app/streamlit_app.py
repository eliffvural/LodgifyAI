import streamlit as st
import pandas as pd
import joblib
import os
import base64

# Base64 formatına resmi dönüştüren fonksiyon
def get_base64_image(file_path):
    with open(file_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

# Görsel yolu
current_dir = os.path.dirname(__file__)
image_path = os.path.join(current_dir, "image_blurred.png")
image_base64 = get_base64_image(image_path)

# Model yükleme
model_path = os.path.join(current_dir, "../models/eniyi.joblib")
model = joblib.load(model_path)

# Sayfa düzeni
st.set_page_config(layout="wide", page_title="Airbnb Fiyat Tahmini", page_icon="🏠")

# CSS ile arka plan ve genel düzenleme
st.markdown(f"""
    <style>
        
    
        /* Arka plan resmi */
        .stApp {{
            background: url("data:image/png;base64,{image_base64}") no-repeat center center fixed;
            background-size: cover;
        }}
        

        /* Ana blok kutusu (beyaz alan) */
        .block-container {{
            background: rgba(255, 255, 255, 0.4); /* Şeffaf beyaz */
            padding: 20px; /* İç boşluğu azalttım */
            border-radius: 12px;
            box-shadow: 0 8px 12px rgba(0, 0, 0, 0.3);
            margin: 200px auto; /* Dış boşluğu azalttım */
            max-width: 80%; /* Beyaz alan genişliğini daralttım */
        }}

        /* Sol sütun başlıkları */
        h2 {{
            text-align: center;
            color: #222222; /* Daha koyu bir renk */
            font-size: 22px; /* Yazı boyutunu küçülttüm */
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }}

        /* Sağ sütun başlığı */
        h1 {{
            color: #2C3E50; /* Daha koyu mavi tonu */
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
            font-size: 28px; /* Başlık boyutunu küçülttüm */
            margin-top: 200px;
            text-align: center;
        }}

        /* Buton stilleri */
.stButton > button {{
    background: linear-gradient(135deg, #4CAF50, #388E3C); /* Hafif degrade renk */
    color: white;
    font-size: 14px; /* Yazı boyutu */
    font-weight: bold;
    border: none;
    border-radius: 12px; /* Daha yuvarlak köşeler */
    height: 45px;
    width: 200px; /* Genişlik ayarı */
    margin: 10px auto; /* Ortalamak için */
    display: block;
    cursor: pointer;
    letter-spacing: 1px; /* Harf arası boşluk */
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2); /* Hafif gölge */
    transition: all 0.3s ease; /* Geçiş efekti */
}}

.stButton > button:hover {{
    background: linear-gradient(135deg, #45a049, #2E7D32); /* Hover'da farklı degrade */
    transform: scale(1.07); /* Biraz büyüme efekti */
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3); /* Daha yoğun gölge */
}}

.stButton > button:active {{
    transform: scale(1); /* Tıklanırken eski haline dönme */
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}}


        /* Giriş kutuları */
        .stSelectbox, .stNumberInput {{
            margin-bottom: 6px; /* Aralıkları azalttım */
            font-size: 14px; /* Yazı boyutunu küçülttüm */
        }}
    </style>
""", unsafe_allow_html=True)


# Sol ve sağ sütunlar düzeni
col1, col2 = st.columns([1, 2])

# Sol sütun: Kullanıcı girişleri
with col1:
    st.markdown("## 🏠 Ev Özelliklerini Girin")
    ev_tipi = st.selectbox("🏠 Ev Tipi", ["oda", "daire", "villa"])
    konum = st.selectbox("📍 Konum", ["şehir merkezi", "kırsal"])
    oda_sayisi = st.number_input("🛏️ Oda Sayısı", min_value=1, max_value=10, value=3, step=1)
    kisi_sayisi = st.number_input("👨‍👩‍👧‍👦 Kişi Sayısı", min_value=1, max_value=15, value=4, step=1)
    havuz = st.selectbox("🏊 Havuz Var mı?", ["Hayır", "Evet"])
    wifi = st.selectbox("📶 WiFi Var mı?", ["Hayır", "Evet"])
    kahvalti = st.selectbox("☕ Kahvaltı Var mı?", ["Hayır", "Evet"])

# Sağ sütun: Tahmin sonucu
with col2:
    st.markdown("""
    <h1 style="text-align: center; margin-top: 250px;">
        📊 Airbnb Fiyat Tahmini Uygulaması
    </h1>
""", unsafe_allow_html=True)
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

    # Eksik özellikleri sıfırla
    input_data = pd.DataFrame([data])
    feature_names = model.feature_names_in_
    input_data = input_data.reindex(columns=feature_names, fill_value=0)

    # Tahmin yapma
    if st.button("Fiyat Tahmin Et"):
        tahmin = model.predict(input_data)
        st.markdown(f"""
            <h3 style="text-align: center; margin-top: 20px;">
                💰 Tahmini Günlük Fiyat: <strong>{tahmin[0]:.2f} TL</strong>
            </h3>
        """, unsafe_allow_html=True)
  

