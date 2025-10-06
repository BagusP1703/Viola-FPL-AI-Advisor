import streamlit as st
import pandas as pd
from rekomendasi_pemain import hitung_rekomendasi # Impor fungsi 'otak' kita

# --- Konfigurasi Halaman ---
st.set_page_config(
    page_title="Viola FPL AI Advisor",
    page_icon="⚽",
    layout="wide"
)

# --- Tampilan Aplikasi ---
st.title("⚽ Viola FPL AI Advisor")
st.write("""
Selamat datang di partner AI FPL Anda. Aplikasi ini menganalisis ribuan data poin
untuk memberikan rekomendasi pemain terbaik berdasarkan: **Form Pemain, Form Tim, dan Jadwal Pertandingan.**
""")

# Tombol untuk menjalankan analisis
if st.button("🚀 Jalankan Analisis & Beri Saya Rekomendasi!"):
    
    # Tampilkan pesan loading saat AI bekerja
    with st.spinner("AI sedang menganalisis data, mohon tunggu..."):
        # Panggil fungsi inti dari skrip rekomendasi kita
        rekomendasi_data = hitung_rekomendasi()
        
        # Ubah hasil menjadi DataFrame pandas
        df = pd.DataFrame(rekomendasi_data)
    
    st.success("Analisis selesai! Berikut adalah top 30 pemain yang direkomendasikan:")
    
    # Tampilkan tabel data yang interaktif
    st.dataframe(df.head(30))
    
    # Tambahkan sedikit analisis tambahan
    st.subheader("Pemain 'Value' Terbaik (MasterScore > 5)")
    best_value = df[df['MasterScore'] > 5.0]
    st.dataframe(best_value)