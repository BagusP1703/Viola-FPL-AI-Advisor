import requests
from bs4 import BeautifulSoup
import re
import json
import sqlite3

# --- Bagian 1: Scraper (Tidak ada perubahan) ---
def ambil_data_pemain_understat():
    """Mengambil data mentah pemain dari halaman utama liga di Understat."""
    url = "https://understat.com/league/EPL"
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'lxml')
        scripts = soup.find_all('script')
        players_data_string = None
        for script in scripts:
            if script.string and 'var playersData' in script.string:
                players_data_string = script.string
                break
        if not players_data_string: return None
        match = re.search(r"JSON\.parse\('(.+?)'\)", players_data_string)
        if not match: return None
        json_string = match.group(1).encode().decode('unicode_escape')
        data_pemain = json.loads(json_string)
        print(f"✅ Berhasil mengambil data statistik untuk {len(data_pemain)} pemain dari Understat.")
        return data_pemain
    except requests.exceptions.RequestException as e:
        print(f"❌ Gagal mengambil halaman: {e}")
        return None

# --- Bagian 2: Penyimpanan ke Database (Perbaikan di sini) ---
def simpan_data_statistik(data_pemain, nama_db='fpl_data.db'):
    """Menyimpan data statistik pemain ke dalam tabel statistik_pemain."""
    if not data_pemain:
        print("Tidak ada data untuk disimpan.")
        return
    
    try:
        koneksi = sqlite3.connect(nama_db)
        kursor = koneksi.cursor()

        # **SINKRONISASI DATA**: Kita akan menyiapkan 15 item data per pemain
        data_untuk_db = []
        for p in data_pemain:
            data_untuk_db.append((
                p['id'], p['player_name'], p['team_title'], p['games'], p['time'], 
                p['goals'], p['xG'], p['assists'], p['xA'], p['shots'], 
                p['key_passes'], p['npg'], p['npxG'], p['xGChain'], p['xGBuildup']
            )) # <-- Pastikan ada 15 item di sini

        # **SINKRONISASI Kueri**: Kueri INSERT kita juga harus menyebutkan 15 kolom dan 15 placeholder '?'
        kursor.executemany("""
        INSERT OR REPLACE INTO statistik_pemain (
            understat_id, player_name, team_title, games, time, goals, xG, assists, xA, 
            shots, key_passes, npg, npxG, xGChain, xGBuildup
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, data_untuk_db)

        koneksi.commit()
        print(f"✅ Berhasil menyimpan/memperbarui {len(data_untuk_db)} baris ke tabel 'statistik_pemain'.")

    except sqlite3.Error as e:
        print(f"❌ Terjadi error database: {e}")
    finally:
        if koneksi:
            koneksi.close()

# --- Bagian 3: Eksekusi (Tidak ada perubahan) ---
if __name__ == '__main__':
    data_statistik = ambil_data_pemain_understat()
    simpan_data_statistik(data_statistik)

# --- Bagian 3: Fungsi Utama untuk Eksekusi ---
def jalankan_update_statistik_lengkap():
    """Fungsi utama untuk menjalankan seluruh proses update statistik."""
    print("Memulai update data statistik dari Understat...")
    data_statistik = ambil_data_pemain_understat()
    simpan_data_statistik(data_statistik)
    print("Update data statistik selesai.")

# Jalankan fungsi utama hanya jika file ini dieksekusi langsung
if __name__ == '__main__':
    jalankan_update_statistik_lengkap()