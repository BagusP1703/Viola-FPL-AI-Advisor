import sqlite3

NAMA_DB = 'fpl_data.db'

# Tambahkan fungsi baru ini di dalam file toolkit_fpl.py

def hitung_form_tim(team_id, gameweek_sekarang, rentang_laga=5):
    """
    Menghitung total poin (W=3,D=1,L=0) sebuah tim dari beberapa laga terakhir.
    """
    if not gameweek_sekarang:
        return 0

    # Ambil 'rentang_laga' terakhir yang sudah selesai untuk tim ini
    kueri = """
    SELECT team_h, team_a, team_h_score, team_a_score
    FROM fixtures
    WHERE (team_h = :team_id OR team_a = :team_id) 
      AND finished = 1 
      AND gameweek < :gameweek_sekarang
    ORDER BY gameweek DESC
    LIMIT :rentang_laga
    """
    
    params = {
        'team_id': team_id,
        'gameweek_sekarang': gameweek_sekarang,
        'rentang_laga': rentang_laga
    }

    laga_terakhir = _jalankan_kueri(kueri, params)
    
    if not laga_terakhir:
        return 0

    poin_form = 0
    for laga in laga_terakhir:
        if laga['team_h'] == team_id: # Jika tim bermain di kandang
            if laga['team_h_score'] > laga['team_a_score']:
                poin_form += 3 # Menang
            elif laga['team_h_score'] == laga['team_a_score']:
                poin_form += 1 # Seri
        else: # Jika tim bermain tandang
            if laga['team_a_score'] > laga['team_h_score']:
                poin_form += 3 # Menang
            elif laga['team_a_score'] == laga['team_h_score']:
                poin_form += 1 # Seri
    
    return poin_form

def _jalankan_kueri(kueri, params=None):
    """
    Fungsi internal untuk koneksi dan eksekusi kueri.
    Mengembalikan hasil sebagai list of dictionaries.
    """
    try:
        koneksi = sqlite3.connect(NAMA_DB)
        # Mengubah cara baris dikembalikan, dari tuple menjadi seperti dictionary
        koneksi.row_factory = sqlite3.Row 
        kursor = koneksi.cursor()
        
        if params:
            kursor.execute(kueri, params)
        else:
            kursor.execute(kueri)
            
        hasil_mentah = kursor.fetchall()
        # Mengubah hasil menjadi list of dicts yang bersih
        hasil_bersih = [dict(baris) for baris in hasil_mentah]
        return hasil_bersih

    except sqlite3.Error as e:
        print(f"❌ Terjadi error database: {e}")
        return []
    finally:
        if koneksi:
            koneksi.close()

# --- Kumpulan Fungsi Toolkit ---

def get_semua_tim():
    """Mengambil semua tim dari database."""
    kueri = "SELECT * FROM teams ORDER BY name;"
    return _jalankan_kueri(kueri)

# Ganti fungsi get_pemain_berdasarkan_posisi di toolkit_fpl.py

# Ganti fungsi get_pemain_berdasarkan_posisi di toolkit_fpl.py

# Di dalam file toolkit_fpl.py

def get_pemain_berdasarkan_posisi(posisi):
    """
    Mengambil pemain berdasarkan posisi, digabungkan dengan statistik
    dan DIURUTKAN BERDASARKAN XG TERTINGGI.
    """
    if posisi.upper() not in ['GKP', 'DEF', 'MID', 'FWD']:
        print(f"Posisi '{posisi}' tidak valid.")
        return []
    
    # Kueri ini sekarang menjadi sumber kecerdasan untuk algoritma kita
    kueri = """
    SELECT
        p.web_name,
        p.price,
        s.xG
    FROM
        players AS p
    JOIN
        teams AS t ON p.team_id = t.id
    JOIN
        statistik_pemain AS s ON t.name = s.team_title AND s.player_name LIKE '%' || p.second_name || '%'
    WHERE
        p.position = ? AND p.price > 0 AND s.xG > 0
    ORDER BY
        s.xG DESC;
    """
    return _jalankan_kueri(kueri, (posisi.upper(),))

# Tambahkan fungsi baru ini di dalam file toolkit_fpl.py

def get_pemain_berdasarkan_value(posisi):
    """
    Mengambil pemain berdasarkan posisi, diurutkan berdasarkan
    "Value Score" tertinggi (xG / harga).
    """
    if posisi.upper() not in ['GKP', 'DEF', 'MID', 'FWD']:
        print(f"Posisi '{posisi}' tidak valid.")
        return []
    
    # Kueri ini menghitung kolom 'value_score' secara virtual
    # dan mengurutkan berdasarkan itu.
    kueri = """
    SELECT
        p.web_name,
        p.price,
        s.xG,
        -- Menghitung Value Score, hindari pembagian dengan nol
        CASE 
            WHEN p.price > 0 THEN s.xG / p.price 
            ELSE 0 
        END AS value_score
    FROM
        players AS p
    JOIN
        teams AS t ON p.team_id = t.id
    JOIN
        statistik_pemain AS s ON t.name = s.team_title AND s.player_name LIKE '%' || p.second_name || '%'
    WHERE
        p.position = ?
    ORDER BY
        value_score DESC;
    """
    return _jalankan_kueri(kueri, (posisi.upper(),))

def get_pemain_berdasarkan_tim(nama_pendek_tim):
    """
    Mengambil semua pemain dari sebuah tim berdasarkan short_name tim.
    """
    kueri = """
    SELECT p.web_name, p.position, p.price
    FROM players AS p
    JOIN teams AS t ON p.team_id = t.id
    WHERE t.short_name = ?;
    """
    return _jalankan_kueri(kueri, (nama_pendek_tim.upper(),))

def get_pemain_berdasarkan_nama(nama_web):
    """
    Mencari satu pemain berdasarkan web_name nya.
    """
    kueri = "SELECT * FROM players WHERE web_name = ?;"
    hasil = _jalankan_kueri(kueri, (nama_web,))
    # Mengembalikan dictionary pemain pertama jika ditemukan, jika tidak None
    return hasil[0] if hasil else None

def get_pemain_berdasarkan_rentang_harga(min_harga, maks_harga):
    """
    Mengambil semua pemain dengan harga dalam rentang tertentu.
    Harga disimpan di DB dalam satuan float (contoh: 5.0, 6.5, 12.5).
    """
    kueri = """
    SELECT web_name, position, price
    FROM players
    WHERE price BETWEEN ? AND ?
    ORDER BY price DESC;
    """
    return _jalankan_kueri(kueri, (min_harga, maks_harga))

# Tambahkan dua fungsi baru ini di dalam file toolkit_fpl.py

# Di dalam file toolkit_fpl.py, ganti fungsi ini

def get_gameweek_sekarang():
    """Mencari gameweek yang sedang aktif atau yang akan datang."""
    # Prioritas 1: Cari gameweek yang sedang berjalan (is_current = 1)
    kueri_current = "SELECT id FROM gameweeks WHERE is_current = 1;"
    hasil = _jalankan_kueri(kueri_current)
    if hasil:
        return hasil[0]['id']
    
    # Prioritas 2: Jika tidak ada, cari gameweek pertama yang belum selesai
    kueri_next = "SELECT id FROM gameweeks WHERE finished = 0 ORDER BY id ASC LIMIT 1;"
    hasil = _jalankan_kueri(kueri_next)
    return hasil[0]['id'] if hasil else None

def get_kesulitan_jadwal(team_id, gameweek_sekarang, jumlah_laga=3):
    """
    Menghitung rata-rata skor kesulitan (FDR) untuk beberapa laga ke depan.
    """
    if not gameweek_sekarang:
        return 5.0 # Kembalikan skor kesulitan maksimal jika tidak bisa menentukan gameweek

    kueri = """
    SELECT team_h, team_h_difficulty, team_a_difficulty
    FROM fixtures
    WHERE (team_h = :team_id OR team_a = :team_id) AND gameweek BETWEEN :gw_start AND :gw_end
    ORDER BY gameweek
    LIMIT :limit
    """
    
    params = {
        'team_id': team_id,
        'gw_start': gameweek_sekarang + 1,
        'gw_end': gameweek_sekarang + jumlah_laga - 1,
        'limit': jumlah_laga
    }

    jadwal = _jalankan_kueri(kueri, params)
    
    if not jadwal:
        return 5.0 # Asumsikan jadwal sulit jika tidak ditemukan

    total_kesulitan = 0
    for laga in jadwal:
        if laga['team_h'] == team_id:
            total_kesulitan += laga['team_h_difficulty']
        else:
            total_kesulitan += laga['team_a_difficulty']
            
    return total_kesulitan / len(jadwal)

# Tambahkan fungsi baru ini di dalam file toolkit_fpl.py

def get_pemain_untuk_analisis():
    """
    Mengambil daftar semua pemain dengan data form mereka dan form timnya.
    Menggunakan COALESCE untuk menangani nilai NULL pada form.
    """
    kueri = """
    SELECT
        p.id,
        p.web_name,
        p.position,
        p.price,
        COALESCE(p.form, 0.0) AS player_form, -- Jika form NULL, anggap 0
        t.name AS team_name,
        COALESCE(t.form, 0.0) AS team_form,   -- Jika form NULL, anggap 0
        p.team_id
    FROM
        players AS p
    JOIN
        teams AS t ON p.team_id = t.id
    """
    return _jalankan_kueri(kueri)