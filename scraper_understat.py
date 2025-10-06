import requests
from bs4 import BeautifulSoup
import re
import json

def ambil_data_pemain_understat():
    """
    Mengambil data mentah pemain dari halaman utama liga di Understat.
    """
    # URL halaman utama statistik EPL di Understat
    url = "https://understat.com/league/EPL"

    try:
        # 1. Ambil konten halaman web
        response = requests.get(url)
        response.raise_for_status()
        print("✅ Berhasil mengambil konten halaman Understat.")

        # 2. Gunakan BeautifulSoup untuk mem-parsing HTML
        soup = BeautifulSoup(response.content, 'lxml')

        # 3. Cari semua tag <script>
        scripts = soup.find_all('script')

        # 4. Cari tag <script> yang berisi data pemain (playersData)
        players_data_string = None
        for script in scripts:
            # Kita cari teks di dalam script yang cocok dengan pola 'var playersData'
            if script.string and 'var playersData' in script.string:
                players_data_string = script.string
                break

        if not players_data_string:
            print("❌ Tidak dapat menemukan variabel 'playersData' di dalam script.")
            return None

        print("✅ Berhasil menemukan blok data pemain (playersData).")

        # 5. Ekstrak JSON dari string JavaScript menggunakan Regular Expression
        # Pola ini mencari teks yang diawali dengan JSON.parse('...')
        match = re.search(r"JSON\.parse\('(.+?)'\)", players_data_string)
        if not match:
            print("❌ Tidak dapat mengekstrak JSON dari string.")
            return None

        # String JSON mentah, perlu decoding
        json_string = match.group(1).encode().decode('unicode_escape')

        # 6. Ubah string JSON menjadi objek Python (list of dictionaries)
        data_pemain = json.loads(json_string)
        print(f"✅ Berhasil mengurai data untuk {len(data_pemain)} pemain.")

        return data_pemain

    except requests.exceptions.RequestException as e:
        print(f"❌ Gagal mengambil halaman: {e}")
        return None

if __name__ == '__main__':
    data = ambil_data_pemain_understat()

    if data:
        # Tampilkan data 3 pemain pertama sebagai sampel
        print("\n--- CONTOH DATA 3 PEMAIN PERTAMA ---")
        print(json.dumps(data[:3], indent=2))