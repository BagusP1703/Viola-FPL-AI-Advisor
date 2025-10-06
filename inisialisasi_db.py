import sqlite3

def buat_database(nama_db='fpl_data.db'):
    """Fungsi untuk membuat file database dan tabel-tabelnya."""
    try:
        koneksi = sqlite3.connect(nama_db)
        kursor = koneksi.cursor()
        print(f"Database '{nama_db}' berhasil dibuat/terhubung.")

        # ... (kode tabel teams, players, gameweeks tetap sama) ...
        kursor.execute("""
        CREATE TABLE IF NOT EXISTS teams (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            short_name TEXT NOT NULL,
            form REAL
        )""")
        
        kursor.execute("""
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY,
            first_name TEXT,
            second_name TEXT,
            web_name TEXT NOT NULL,
            price REAL NOT NULL,
            position TEXT NOT NULL,
            form REAL,
            team_id INTEGER,
            FOREIGN KEY (team_id) REFERENCES teams (id)
        )""")
        
        kursor.execute("""
        CREATE TABLE IF NOT EXISTS gameweeks (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            deadline_time TEXT NOT NULL,
            is_current BOOLEAN, -- <-- TAMBAHKAN INI
            finished BOOLEAN    -- <-- TAMBAHKAN INI
        )""")

        # --- TAMBAHAN BARU ---
        # Perintah SQL untuk membuat tabel statistik_pemain
        kursor.execute("""
        CREATE TABLE IF NOT EXISTS statistik_pemain (
            understat_id INTEGER PRIMARY KEY,
            player_name TEXT NOT NULL,
            team_title TEXT NOT NULL,
            games INTEGER,
            time INTEGER,
            goals INTEGER,
            xG REAL,
            assists INTEGER,
            xA REAL,
            shots INTEGER,
            key_passes INTEGER,
            npg INTEGER,
            npxG REAL,
            xGChain REAL,
            xGBuildup REAL
        )""")
        print("Tabel 'statistik_pemain' berhasil dibuat.")

        # Di dalam file inisialisasi_db.py, tambahkan di akhir fungsi
        kursor.execute("""
        CREATE TABLE IF NOT EXISTS fixtures (
        id INTEGER PRIMARY KEY,
        gameweek INTEGER,
        finished BOOLEAN,
        team_h INTEGER,
        team_a INTEGER,
        team_h_score INTEGER,
        team_a_score INTEGER,
        team_h_difficulty INTEGER,
        team_a_difficulty INTEGER
        )""")
        print("Tabel 'fixtures' berhasil dibuat.")

    except sqlite3.Error as e:
        print(f"Terjadi error: {e}")
    finally:
        if koneksi:
            koneksi.close()
            print("Koneksi database ditutup.")

if __name__ == '__main__':
    buat_database()