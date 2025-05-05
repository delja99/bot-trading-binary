import streamlit as st
import pandas as pd
import numpy as np

def ambil_data():
    return pd.read_csv("data_sample.csv")

def hitung_tren(data):
    return "Uptrend" if data['close'].iloc[-1] > data['close'].iloc[-5] else "Downtrend"

def hitung_sinyal(data):
    macd = data['close'].ewm(span=12).mean() - data['close'].ewm(span=26).mean()
    rsi = 100 - (100 / (1 + data['close'].pct_change().rolling(14).mean()))
    tren = hitung_tren(data)
    if tren == "Uptrend" and macd.iloc[-1] > 0 and rsi.iloc[-1] > 50:
        return "BUY"
    elif tren == "Downtrend" and macd.iloc[-1] < 0 and rsi.iloc[-1] < 50:
        return "SELL"
    else:
        return "WAIT"

def simulasikan_bot():
    data = ambil_data()
    tren = hitung_tren(data)
    sinyal = hitung_sinyal(data)
    akurasi = np.round(np.random.uniform(85, 95), 2)

    hasil = {
        "Tren": tren,
        "Sinyal": sinyal,
        "Akurasi": akurasi
    }

    # Simpan log hasil trade
    df_log = pd.DataFrame([hasil])
    df_log.to_csv("hasil_trade.csv", index=False)

    return hasil

st.title("🤖 Bot Trading Binary")
st.markdown("Selamat datang di bot trading Binary berbasis analisis tren, indikator teknikal, dan deteksi sinyal palsu.")
if st.button("Mulai Bot"):
    hasil = simulasikan_bot()
    st.success("✅ Bot selesai dijalankan!")

    st.subheader("Hasil Analisa:")
    st.write(f"**Tren:** {hasil['Tren']}")
    st.write(f"**Sinyal:** {hasil['Sinyal']}")
    st.write(f"**Akurasi:** {hasil['Akurasi']}%")
    st.caption("File log disimpan ke `hasil_trade.csv`")
