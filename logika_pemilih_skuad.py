# Impor toolkit kita untuk mengakses data
from toolkit_fpl import get_pemain_berdasarkan_posisi
from toolkit_fpl import get_pemain_berdasarkan_value 
import json

# --- ATURAN DAN KONFIGURASI ---
BUDGET_TOTAL = 50.0
FORMASI = {
    'GKP': 1,
    'DEF': 2,
    'MID': 2,
    'FWD': 1
}

def pilih_skuad_greedy():
    """
    Memilih skuad berdasarkan algoritma 'Greedy'.
    Memilih pemain termahal di setiap posisi sesuai budget.
    """
    sisa_budget = BUDGET_TOTAL
    skuad_terpilih = []

    print(f"--- Memulai Pemilihan Skuad dengan Budget £{BUDGET_TOTAL}m ---")

    # Iterasi melalui setiap posisi dalam formasi
    for posisi, jumlah_dibutuhkan in FORMASI.items():

        print(f"\n-> Mencari {jumlah_dibutuhkan} pemain untuk posisi {posisi}...")

        # Ambil semua pemain di posisi tersebut, sudah terurut dari yang termahal
        kandidat_pemain = get_pemain_berdasarkan_value(posisi)

        pemain_terpilih_posisi_ini = 0
        # Iterasi melalui kandidat untuk mencari yang harganya pas
        for kandidat in kandidat_pemain:
            # Cek apakah budget masih cukup
            if sisa_budget >= kandidat['price']:
                # Jika cukup, "beli" pemain ini
                skuad_terpilih.append(kandidat)
                sisa_budget -= kandidat['price']
                pemain_terpilih_posisi_ini += 1

                print(f"  [+] Terpilih: {kandidat['web_name']} (£{kandidat['price']}m). Sisa budget: £{sisa_budget:.1f}m")

                # Jika jumlah untuk posisi ini sudah terpenuhi, lanjut ke posisi berikutnya
                if pemain_terpilih_posisi_ini == jumlah_dibutuhkan:
                    break

        # Jika setelah loop selesai tapi pemain kurang, berarti gagal
        if pemain_terpilih_posisi_ini < jumlah_dibutuhkan:
            print(f"  [!] Gagal menemukan {jumlah_dibutuhkan} pemain untuk posisi {posisi} dengan sisa budget.")

    return skuad_terpilih, sisa_budget


if __name__ == '__main__':
    skuad_final, sisa_budget_final = pilih_skuad_greedy()

    print("\n--- ✅ Pemilihan Skuad Selesai ---")
    print("Skuad Terpilih:")
    # Menggunakan json.dumps untuk cetak rapi
    print(json.dumps(skuad_final, indent=2))
    print(f"\nTotal Pemain: {len(skuad_final)}")
    print(f"Sisa Budget: £{sisa_budget_final:.1f}m")