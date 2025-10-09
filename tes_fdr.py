import sqlite3

# ================================
# KONFIGURASI
# ================================
DB_PATH = "fpl_data.db"   # Ganti sesuai file database kamu
GAMEWEEK_SEKARANG = 8
JUMLAH_LAGA = 3

TEAM_IDS = [4, 13, 20]  # contoh: Arsenal=1, Liverpool=13, Man City=20


# ================================
# Fungsi ambil fixture & hitung FDR
# ================================
def get_jadwal_tim(conn, team_id, gameweek_sekarang, jumlah_laga=3):
    """
    Ambil daftar fixture untuk tim tertentu dalam rentang jumlah_laga ke depan.
    """
    q = """
    SELECT gameweek, team_h, team_a, team_h_difficulty, team_a_difficulty
    FROM fixtures
    WHERE (team_h = :team_id OR team_a = :team_id)
      AND gameweek BETWEEN :gw_start AND :gw_end
    ORDER BY gameweek
    LIMIT :limit
    """

    params = {
        'team_id': team_id,
        'gw_start': gameweek_sekarang,
        'gw_end': gameweek_sekarang + jumlah_laga - 1,
        'limit': jumlah_laga
    }

    cur = conn.execute(q, params)
    return cur.fetchall()


def hitung_rata_fdr(jadwal, team_id):
    total = 0
    for row in jadwal:
        gw, team_h, team_a, diff_h, diff_a = row
        if team_h == team_id:
            total += diff_h
        else:
            total += diff_a
    return total / len(jadwal) if jadwal else 5.0


# ================================
# Fungsi utama
# ================================
def main():
    conn = sqlite3.connect(DB_PATH)

    print("------------------------------------------------------------")
    print(f"Pembuktian Perhitungan FDR dari GW {GAMEWEEK_SEKARANG} selama {JUMLAH_LAGA} laga ke depan\n")

    for team_id in TEAM_IDS:
        jadwal = get_jadwal_tim(conn, team_id, GAMEWEEK_SEKARANG, JUMLAH_LAGA)
        if not jadwal:
            print(f"Team ID {team_id}: Tidak ada data fixture ditemukan")
            continue

        print(f"=== Team ID {team_id} ===")
        total = 0

        for row in jadwal:
            gw, team_h, team_a, diff_h, diff_a = row
            if team_h == team_id:
                lokasi = "Home"
                fdr = diff_h
                lawan = team_a
            else:
                lokasi = "Away"
                fdr = diff_a
                lawan = team_h

            total += fdr
            print(f"GW {gw:<2} | {lokasi:<4} vs Team {lawan:<2} | FDR: {fdr}")

        rata = total / len(jadwal)
        print(f"Rata-rata FDR: {rata:.2f}\n")

    conn.close()


if __name__ == "__main__":
    main()
