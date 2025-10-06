import sqlite3

def jalankan_kueri(kueri, params=None):
    """
    Menjalankan sebuah kueri SELECT dan mengembalikan hasilnya.
    """
    try:
        koneksi = sqlite3.connect('fpl_data.db')
        koneksi.row_factory = sqlite3.Row 
        kursor = koneksi.cursor()
        
        if params:
            kursor.execute(kueri, params)
        else:
            kursor.execute(kueri)
            
        hasil_mentah = kursor.fetchall()
        hasil_bersih = [dict(baris) for baris in hasil_mentah]
        return hasil_bersih

    except sqlite3.Error as e:
        print(f"❌ Terjadi error database: {e}")
        return []
    finally:
        if koneksi:
            koneksi.close()

def cetak_hasil(judul, hasil):
    """Mencetak hasil kueri dalam format yang rapi."""
    print(f"\n--- {judul} ---")
    if not hasil:
        print("Tidak ada data yang ditemukan.")
        return
    
    headers = hasil[0].keys()
    print(" | ".join(f"{h:<15}" for h in headers)) # Atur lebar kolom
    print("-" * (18 * len(headers)))
    
    for baris in hasil:
        print(" | ".join(f"{str(v):<15}" for v in baris.values()))

if __name__ == '__main__':
    # Kueri gabungan yang akurat
    kueri_join = """
    SELECT
        p.web_name,
        p.price,
        s.xG,
        s.team_title AS team
    FROM
        players AS p
    JOIN
        teams AS t ON p.team_id = t.id
    JOIN
        statistik_pemain AS s ON t.name = s.team_title AND s.player_name LIKE '%' || p.second_name || '%'
    WHERE
        p.price > 0 AND s.xG > 0
    ORDER BY
        s.xG DESC
    LIMIT 15;
    """
    hasil_join = jalankan_kueri(kueri_join)
    cetak_hasil("Top 15 Pemain Berdasarkan xG (Data Gabungan Akurat)", hasil_join)