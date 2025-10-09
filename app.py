import streamlit as st
import pandas as pd
import time

# Impor fungsi 'otak' dan fungsi 'update' kita
from rekomendasi_pemain import hitung_rekomendasi
from ambil_data import ambil_dan_simpan_data
from update_statistik import jalankan_update_statistik_lengkap

# --- Konfigurasi Halaman ---
st.set_page_config(
    page_title="Viola FPL AI Advisor",
    page_icon="⚽",
    layout="wide"
)

# --- Sidebar (Panel Samping) ---
with st.sidebar:
    st.header("⚙️ Opsi")
    st.write("Data diperbarui secara manual. Klik tombol di bawah jika Anda ingin mengambil data terbaru dari server FPL dan Understat.")
    
    # Tombol untuk me-refresh data
    if st.button("🔄 Refresh Data Database"):
        
        # Tampilkan pesan loading saat proses berjalan
        with st.spinner("Mengambil data FPL terbaru... (Langkah 1/2)"):
            try:
                ambil_dan_simpan_data() # Menjalankan skrip ambil_data.py
                st.success("Data FPL berhasil diperbarui!")
            except Exception as e:
                st.error(f"Gagal memperbarui data FPL: {e}")

        with st.spinner("Mengambil data statistik Understat... (Langkah 2/2)"):
            try:
                jalankan_update_statistik_lengkap() # Menjalankan skrip update_statistik.py
                st.success("Data statistik berhasil diperbarui!")
            except Exception as e:
                st.error(f"Gagal memperbarui data statistik: {e}")
        
        st.info("Refresh selesai! Silakan jalankan analisis untuk melihat data terbaru.")
    
    # 🧹 Tombol untuk membersihkan cache
    if st.button("🧹 Bersihkan Cache"):
        st.cache_data.clear()
        st.cache_resource.clear()
        st.success("Cache sudah dibersihkan!")
# --- Tampilan Utama Aplikasi ---
st.title("⚽ Viola FPL AI Advisor")
st.write("""
Selamat datang di partner AI FPL Anda. Aplikasi ini menganalisis ribuan data poin
untuk memberikan rekomendasi pemain terbaik berdasarkan: **Form Pemain, Form Tim, dan Jadwal Pertandingan.**
""")

if 'rekomendasi_df' not in st.session_state:
    st.session_state.rekomendasi_df = pd.DataFrame()

# Tombol untuk menjalankan analisis
if st.button("🚀 Jalankan Analisis & Beri Saya Rekomendasi!"):
    with st.spinner("AI sedang menganalisis data, mohon tunggu..."):
        rekomendasi_data = hitung_rekomendasi()
        df = pd.DataFrame(rekomendasi_data)
        st.session_state.rekomendasi_df = df # Simpan hasil di session state
    
    st.success("Analisis selesai!")

# Selalu tampilkan hasil terakhir jika ada
if not st.session_state.rekomendasi_df.empty:
    df_hasil = st.session_state.rekomendasi_df
    st.subheader("🔥 Top 30 Rekomendasi Pemain")
    st.dataframe(df_hasil.head(30))
    
    st.subheader("💎 Pemain 'Value' Terbaik (MasterScore > 4)")
    best_value = df_hasil[df_hasil['MasterScore'] > 4.0]
    st.dataframe(best_value)