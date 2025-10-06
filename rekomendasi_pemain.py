from toolkit_fpl import (
    get_pemain_untuk_analisis, 
    get_kesulitan_jadwal, 
    get_gameweek_sekarang,
    hitung_form_tim
)
import pandas as pd

# --- KONFIGURASI STRATEGI (BOBOT) ---
# Anda bisa mengubah angka-angka ini untuk menyesuaikan strategi AI
BOBOT_FORM_PEMAIN = 0.5  # 50%
BOBOT_FORM_TIM = 0.3     # 30%
BOBOT_JADWAL = 0.2       # 20%

def hitung_rekomendasi():
    """
    Menghitung 'Master Score' untuk semua pemain dan memberikan rekomendasi.
    """
    print("Menganalisis data, mohon tunggu...")
    
    # 1. Dapatkan data dasar
    gameweek_sekarang = get_gameweek_sekarang()
    semua_pemain = get_pemain_untuk_analisis()

    print(f"DEBUG: Ditemukan {len(semua_pemain)} pemain yang memenuhi kriteria awal.")
    
    daftar_rekomendasi = []
    
    # 2. Loop melalui setiap pemain untuk menghitung skor mereka
    for pemain in semua_pemain:

        # PANGGILAN BARU: Hitung form tim secara manual
        skor_form_tim = hitung_form_tim(pemain['team_id'], gameweek_sekarang, 5)

        # Ambil skor kesulitan jadwal untuk tim pemain ini
        skor_jadwal = get_kesulitan_jadwal(pemain['team_id'], gameweek_sekarang, 3)
        
        # 3. Hitung Master Score menggunakan formula berbobot
        master_score = (BOBOT_FORM_PEMAIN * pemain['player_form']) + \
                       (BOBOT_FORM_TIM * skor_form_tim) - \
                       (BOBOT_JADWAL * skor_jadwal)
        
        daftar_rekomendasi.append({
            'Nama': pemain['web_name'],
            'Tim': pemain['team_name'],
            'Posisi': pemain['position'],
            'Harga': pemain['price'],
            'FormPemain': round(pemain['player_form'], 2),
            'FormTim': skor_form_tim,
            'SkorJadwal': round(skor_jadwal, 2),
            'MasterScore': round(master_score, 2)
        })
        
    # 4. Urutkan pemain berdasarkan Master Score tertinggi
    daftar_rekomendasi.sort(key=lambda x: x['MasterScore'], reverse=True)
    
    return daftar_rekomendasi

if __name__ == '__main__':
    rekomendasi = hitung_rekomendasi()
    
    df = pd.DataFrame(rekomendasi)
    
    print("\n--- 🔥 Top 20 Rekomendasi Pemain Saat Ini ---")
    print(df.head(20).to_string(index=False))