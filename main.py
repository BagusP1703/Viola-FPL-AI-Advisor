# Impor fungsi-fungsi spesifik dari toolkit kita
from toolkit_fpl import (
    get_semua_tim, 
    get_pemain_berdasarkan_posisi, 
    get_pemain_berdasarkan_tim,
    get_pemain_berdasarkan_nama,
    get_pemain_berdasarkan_rentang_harga
)
import json

def cetak_rapi(data):
    """Mencetak list of dictionaries dengan format JSON yang rapi."""
    if data:
        print(json.dumps(data, indent=2))
    else:
        print("Tidak ada data ditemukan.")

if __name__ == '__main__':
    print("--- 🚀 MENJALANKAN FPL TOOLKIT 🚀 ---")

    print("\n[INFO] Mengambil 5 striker teratas berdasarkan harga...")
    striker_termahal = get_pemain_berdasarkan_posisi("FWD")[:5] # Ambil 5 pertama
    cetak_rapi(striker_termahal)

    print("\n[INFO] Mencari semua pemain dari Man Utd (MUN)...")
    pemain_mu = get_pemain_berdasarkan_tim("MUN")
    cetak_rapi(pemain_mu)

    print("\n[INFO] Mencari detail pemain 'Saka'...")
    detail_saka = get_pemain_berdasarkan_nama("Saka")
    cetak_rapi(detail_saka)
    
    if detail_saka:
        print(f"\n[ANALISIS] Harga {detail_saka['web_name']} saat ini adalah £{detail_saka['price']}m.")

    print("\n[INFO] Mencari pemain dengan harga antara £5.0m - £7.0m...")
    pemain_midrange = get_pemain_berdasarkan_rentang_harga(5.0, 7.0)
    cetak_rapi(pemain_midrange[:10])