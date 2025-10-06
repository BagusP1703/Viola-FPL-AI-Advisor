import requests
import sqlite3

def ambil_dan_simpan_data(nama_db='fpl_data.db'):
    """Mengambil data FPL dari API dan menyimpannya ke database SQLite."""
    
    # 1. Ambil data utama dari API (pemain, tim, gameweek)
    url_bootstrap = "https://fantasy.premierleague.com/api/bootstrap-static/"
    try:
        response = requests.get(url_bootstrap)
        response.raise_for_status()
        data = response.json()
        print("✅ Data utama (pemain, tim, dll) dari API FPL berhasil diambil.")
    except requests.exceptions.RequestException as e:
        print(f"❌ Gagal mengambil data utama dari API: {e}")
        return

    # 2. Hubungkan ke database dan masukkan data
    koneksi = None # Inisialisasi koneksi
    try:
        koneksi = sqlite3.connect(nama_db)
        kursor = koneksi.cursor()
        print(f"Berhasil terhubung ke database '{nama_db}'.")

        # 3. Masukkan data teams
        teams_data = data['teams']
        kursor.executemany("""
        INSERT OR REPLACE INTO teams (id, name, short_name, form) 
        VALUES (:id, :name, :short_name, :form)
        """, teams_data)
        print(f"-> {len(teams_data)} data tim berhasil dimasukkan/diperbarui.")

        # 4. Masukkan data players
        players_data = []
        for p in data['elements']:
            players_data.append({
                'id': p['id'],
                'first_name': p['first_name'],
                'second_name': p['second_name'],
                'web_name': p['web_name'],
                'price': p['now_cost'] / 10.0,
                'position': {1: 'GKP', 2: 'DEF', 3: 'MID', 4: 'FWD'}[p['element_type']],
                'form': p['form'],
                'team_id': p['team']
            })
        
        kursor.executemany("""
        INSERT OR REPLACE INTO players (id, first_name, second_name, web_name, price, position, form, team_id)
        VALUES (:id, :first_name, :second_name, :web_name, :price, :position, :form, :team_id)
        """, players_data)
        print(f"-> {len(players_data)} data pemain berhasil dimasukkan/diperbarui.")
        
        # 5. Masukkan data gameweeks
        gameweeks_data = data['events']
        kursor.executemany("""
        INSERT OR REPLACE INTO gameweeks (id, name, deadline_time, is_current, finished)
        VALUES (:id, :name, :deadline_time, :is_current, :finished)
        """, gameweeks_data)
        print(f"-> {len(gameweeks_data)} data gameweek berhasil dimasukkan/diperbarui.")

        # --- PERBAIKAN UNTUK FIXTURES DIMULAI DI SINI ---
        
        # 6. Ambil data fixtures dari API terpisah
        url_fixtures = "https://fantasy.premierleague.com/api/fixtures/" # <-- URL BARU khusus fixtures
        print("✅ Mengambil data jadwal pertandingan...")
        response_fixtures = requests.get(url_fixtures)
        response_fixtures.raise_for_status()
        fixtures_data = response_fixtures.json() # <-- Variabel baru untuk menampung data fixtures
        
        # 7. Masukkan data fixtures ke database
        kursor.executemany("""
        INSERT OR REPLACE INTO fixtures (id, gameweek, finished, team_h, team_a, team_h_score, team_a_score, team_h_difficulty, team_a_difficulty)
        VALUES (:id, :event, :finished, :team_h, :team_a , :team_h_score, :team_a_score, :team_h_difficulty, :team_a_difficulty)
        """, fixtures_data) # <-- Gunakan variabel fixtures_data yang baru
        print(f"-> {len(fixtures_data)} data jadwal pertandingan berhasil dimasukkan/diperbarui.")

        # Simpan perubahan (commit)
        koneksi.commit()
        print("✅ Semua perubahan telah disimpan ke database.")

    except requests.exceptions.RequestException as e:
        print(f"❌ Gagal mengambil data fixtures dari API: {e}")
    except sqlite3.Error as e:
        print(f"❌ Terjadi error database: {e}")
    finally:
        if koneksi:
            koneksi.close()
            print("Koneksi database ditutup.")

if __name__ == '__main__':
    ambil_dan_simpan_data()