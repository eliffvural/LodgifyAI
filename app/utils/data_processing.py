# data_preprocessing.py

import pandas as pd

def preprocess_input_data(data):
    """
    Kullanıcı girişlerini modelin beklediği formatta işler.
    """
    # Örnek: Numerik dönüşümler
    data["Havuz"] = data["Havuz"].apply(lambda x: 1 if x == "Evet" else 0)
    data["WiFi"] = data["WiFi"].apply(lambda x: 1 if x == "Evet" else 0)
    data["Kahvaltı"] = data["Kahvaltı"].apply(lambda x: 1 if x == "Evet" else 0)
    return data
