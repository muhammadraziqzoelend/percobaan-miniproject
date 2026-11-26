import csv

NAMA_FILE_CSV = "E-commerce_Delivery_Shipping_Data_2026.csv"

DAFTAR_CUACA = ["Rain", "Clear", "Cloudy", "Storm", "Snow", "Extreme Heat"]
DAFTAR_METODE = ["Economy", "Standard", "Express", "Same Day", "International"]
DAFTAR_KURIR = ["BlueRoute", "EagleCourier", "FastTrack Logistics", "GlobalExpress",
                "ParcelPro", "PrimeDelivery", "SpeedyCargo", "SwiftShip"]
DAFTAR_STATUS = ["Delivered", "Delayed", "In Transit", "Failed Delivery"]
KOLOM_WAJIB = ["order_id", "order_date", "delivery_delay_days", "shipping_cost_usd",
               "customer_rating", "weather_condition", "shipping_method", "carrier",
               "delivery_status"]

DAFTAR_MENU = [(1, "Risiko Keterlambatan", "Cuaca terburuk & prediksi risiko telat"),
               (2, "Saran Kurir", "Rekomendasi kurir terbaik"),
               (3, "Kinerja Kurir", "Skor & peringkat ketepatan kurir"),
               (0, "Keluar", "Menutup program")]

BOBOT_CUACA = 0.75
BOBOT_METODE = 0.25
SARAN_RISIKO = {
    "Rendah": "Gunakan estimasi pengiriman biasa.",
    "Sedang": "Tambahkan 1 hari pada estimasi pengiriman.",
    "Tinggi": "Tambahkan 1-2 hari pada estimasi, atau tunggu cuaca membaik.",
}

BOBOT_KECEPATAN = 0.637
BOBOT_RATING = 0.258
BOBOT_ONGKIR = 0.105

POIN_TEPAT_WAKTU = 1.0
POIN_TELAT_1_2_HARI = 0.582
POIN_TELAT_3_HARI_LEBIH = 0.109

LEBAR = 72
GARIS = "=" * LEBAR


def judul(teks):
    print(f"\n{GARIS}\n{teks:^{LEBAR}}\n{GARIS}")


def tabel(kepala, baris, rata=None, caption=None):
    rata = (rata or "").ljust(len(kepala), "<")
    isi = [[str(sel) for sel in satu_baris] for satu_baris in baris]

    lebar_kolom = []
    for i in range(len(kepala)):
        terlebar = len(kepala[i])
        for satu_baris in isi:
            terlebar = max(terlebar, len(satu_baris[i]))
        lebar_kolom.append(terlebar)

    pemisah = "+" + "+".join("-" * (w + 2) for w in lebar_kolom) + "+"
    print("\n" + caption if caption else "")
    print(pemisah)
    print("| " + " | ".join(f"{kepala[i]:^{lebar_kolom[i]}}" for i in range(len(kepala))) + " |")
    print(pemisah)
    for satu_baris in isi:
        print("| " + " | ".join(f"{satu_baris[i]:{rata[i]}{lebar_kolom[i]}}"
                                for i in range(len(kepala))) + " |")
    print(pemisah)


def minta(jenis, pesan=None, pilihan=None, minimum=None, maksimum=None, caption=None):
    if jenis == "pilih":
        tabel(["No", "Pilihan"], [(i + 1, pilihan[i]) for i in range(len(pilihan))],
              "^<", caption=caption)
        minimum, maksimum = 1, len(pilihan)
        if pesan is None:
            pesan = f"Ketik nomor pilihan ({minimum}-{maksimum}), lalu tekan Enter: "

    while True:
        teks = input(pesan).strip().replace(",", ".")
        if jenis == "angka":
            valid = teks.replace(".", "", 1).isdecimal()
        else:
            valid = teks.isdecimal()

        if valid:
            angka = float(teks) if jenis == "angka" else int(teks)
            if angka >= minimum and (maksimum is None or angka <= maksimum):
                return pilihan[angka - 1] if jenis == "pilih" else angka

        satuan = {"pilih": "nomor", "bulat": "angka bulat", "angka": "angka"}[jenis]
        rentang = f"{minimum:g} sampai {maksimum:g}" if maksimum is not None else f"{minimum:g} atau lebih"
        contoh = " Contoh: 3 atau 3.5" if jenis == "angka" else ""
        print(f"[!] Masukkan {satuan} {rentang}.{contoh}")


def tingkat_risiko(indeks):
    return "Rendah" if indeks < 40 else "Sedang" if indeks <= 60 else "Tinggi"


class Akun:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def cek_login(self, username, password):
        return username == self.username and password == self.password


def cetak_cover():
    anggota = [("Farhan Raditya Ramadhan", "2610932034"),
               ("Ghani Sakha Favian", "2610931023"),
               ("Muhammad Raziq Zoelend", "2610932042"),
               ("Nabila Putri Ramadhani", "2610931031")]
    isi_cover = ["TUGAS MINI PROJECT", "KELOMPOK 3 C", "", "PEMROGRAMAN KOMPUTER", "",
                 "Program Klasifikasi Tingkat Keterlambatan Pengiriman E-Commerce",
                 "dan Ringkasan Kinerja Kurir Berdasarkan Data Pengiriman", "",
                 "Anggota:"]
    isi_cover += [f"{nama:<26}({nim})" for nama, nim in anggota]
    isi_cover += ["", "Asisten Pembimbing : Anisha Nur Aprilia",
                  "Dosen Pengampu     : Dr. Asmuliardi Muluk, S.T., M.T.", "",
                  "LABORATORIUM SISTEM INFORMASI DAN KEPUTUSAN",
                  "DEPARTEMEN TEKNIK INDUSTRI - FAKULTAS TEKNIK",
                  "UNIVERSITAS ANDALAS 2026"]
    print()
    for teks in isi_cover:
        print(f"{teks:^{LEBAR}}")


def registrasi():
    judul("LANGKAH 1 DARI 2 : REGISTRASI AKUN")
    print("Buat akun baru untuk menggunakan program ini.")
    print("Akun hanya berlaku selama program berjalan, jadi Anda perlu")
    print("registrasi dan login lagi setiap kali program dijalankan.\n")

    username = input(f"{'Buat username':<22}: ").strip().lower()
    password = input(f"{'Buat password':<22}: ")

    akun = Akun(username, password)
    print(f"\n[OK] Registrasi berhasil. Akun '{akun.username}' telah dibuat.")
    return akun


def login(akun):
    judul("LANGKAH 2 DARI 2 : LOGIN")
    print("Masuk menggunakan username dan password yang baru Anda buat.\n")

    while True:
        username = input(f"{'Username':<22}: ").strip().lower()
        password = input(f"{'Password':<22}: ")
        if akun.cek_login(username, password):
            break
        print("[!] Username atau password salah. Silakan coba lagi.\n")
    print(f"\n[OK] Login berhasil. Selamat datang, {akun.username}!")


def cek_baris(baris):
    for kolom in KOLOM_WAJIB:
        if not baris[kolom] or not baris[kolom].strip():
            return f"Kolom {kolom} kosong"
        baris[kolom] = baris[kolom].strip()

    bagian = baris["order_date"].split("-")
    if len(bagian) != 3 or len(bagian[0]) != 4 or len(bagian[1]) != 2 or len(bagian[2]) != 2:
        return "Format tanggal harus tahun-bulan-hari (contoh 2026-11-25)"
    if not (bagian[0].isdecimal() and bagian[1].isdecimal() and bagian[2].isdecimal()):
        return "Tanggal harus berisi angka"

    tahun, bulan, hari = int(bagian[0]), int(bagian[1]), int(bagian[2])
    hari_per_bulan = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if tahun % 400 == 0 or (tahun % 4 == 0 and tahun % 100 != 0):
        hari_per_bulan[1] = 29
    if tahun < 1 or not 1 <= bulan <= 12:
        return "Tahun atau bulan pada tanggal salah"
    if not 1 <= hari <= hari_per_bulan[bulan - 1]:
        return "Hari pada tanggal salah"

    if not baris["delivery_delay_days"].isdecimal():
        return "delivery_delay_days harus bilangan bulat 0 atau lebih"
    for kolom in ["shipping_cost_usd", "customer_rating"]:
        if not baris[kolom].replace(".", "", 1).isdecimal():
            return f"{kolom} harus berupa angka 0 atau lebih"

    if not 1 <= float(baris["customer_rating"]) <= 5:
        return "customer_rating harus antara 1 dan 5"
    if baris["weather_condition"] not in DAFTAR_CUACA or baris["shipping_method"] not in DAFTAR_METODE:
        return "weather_condition atau shipping_method tidak dikenal"
    if baris["carrier"] not in DAFTAR_KURIR or baris["delivery_status"] not in DAFTAR_STATUS:
        return "carrier atau delivery_status tidak dikenal"
    return ""


def baca_data():
    data = []
    terkirim = []
    salah = []
    total_baris = 0

    with open(NAMA_FILE_CSV, "r", newline="", encoding="utf-8-sig") as file:
        pembaca = csv.DictReader(file)
        kolom_kurang = [kolom for kolom in KOLOM_WAJIB if kolom not in (pembaca.fieldnames or [])]
        if kolom_kurang:
            print("\n[X] Kolom wajib tidak ditemukan: " + ", ".join(kolom_kurang))
            exit()

        for nomor, baris in enumerate(pembaca, 2):
            total_baris += 1
            alasan = cek_baris(baris)
            if alasan:
                salah.append((nomor, alasan))
                continue

            baris["hari_telat"] = int(baris["delivery_delay_days"])
            baris["shipping_cost_usd"] = float(baris["shipping_cost_usd"])
            baris["customer_rating"] = float(baris["customer_rating"])
            data.append(baris)
            if baris["delivery_status"] == "Delivered":
                terkirim.append(baris)

    return data, terkirim, salah, total_baris


def menu_risiko(data):
    judul("MENU 1 : RISIKO KETERLAMBATAN")
    print("Pilih cuaca dan metode kirim yang ingin diperiksa, lalu tentukan")
    print("berapa kombinasi cuaca dan metode dengan risiko tertinggi yang ditampilkan.")
    cuaca_pilihan = minta("pilih", pilihan=DAFTAR_CUACA, caption="Daftar kondisi cuaca")
    metode_pilihan = minta("pilih", pilihan=DAFTAR_METODE, caption="Daftar metode kirim")
    jumlah_kombinasi = len(DAFTAR_CUACA) * len(DAFTAR_METODE)
    jumlah_tampil = minta(
        "bulat", minimum=1, maksimum=jumlah_kombinasi,
        pesan=f"\nTampilkan berapa kombinasi berisiko tertinggi? (1-{jumlah_kombinasi}, contoh 10): ")

    total_cuaca = {c: 0 for c in DAFTAR_CUACA}
    telat_cuaca = {c: 0 for c in DAFTAR_CUACA}
    total_metode = {m: 0 for m in DAFTAR_METODE}
    telat_metode = {m: 0 for m in DAFTAR_METODE}
    kombinasi = {}
    for baris in data:
        c = baris["weather_condition"]
        m = baris["shipping_method"]
        hari = baris["hari_telat"]
        if (c, m) not in kombinasi:
            kombinasi[(c, m)] = [0, 0, 0]
        total_cuaca[c] += 1
        total_metode[m] += 1
        kombinasi[(c, m)][0] += 1
        if hari > 0:
            telat_cuaca[c] += 1
            telat_metode[m] += 1
            kombinasi[(c, m)][1] += 1
            kombinasi[(c, m)][2] += hari

    urutan_risiko = []
    for (c, m), (jumlah, jml_telat, total_hari) in kombinasi.items():
        p_cuaca = 100 * telat_cuaca[c] / total_cuaca[c]
        p_metode = 100 * telat_metode[m] / total_metode[m]
        indeks = BOBOT_CUACA * p_cuaca + BOBOT_METODE * p_metode
        rata_telat = total_hari / jml_telat if jml_telat else 0
        urutan_risiko.append((indeks, c, m, jumlah, 100 * jml_telat / jumlah,
                              rata_telat, p_cuaca, p_metode))
    urutan_risiko.sort(reverse=True)

    terpilih = None
    for posisi, baris_risiko in enumerate(urutan_risiko, 1):
        if baris_risiko[1] == cuaca_pilihan and baris_risiko[2] == metode_pilihan:
            terpilih = baris_risiko
            posisi_terpilih = posisi
    if terpilih is None:
        print("\n[!] Tidak ada pesanan dengan kombinasi cuaca dan metode kirim yang Anda pilih.")
    else:
        indeks, c, m, jumlah, persen_telat, rata_telat, p_cuaca, p_metode = terpilih
        tingkat = tingkat_risiko(indeks)
        tabel(["Keterangan", "Hasil"],
              [("Cuaca yang dipilih", c),
               ("Metode kirim yang dipilih", m),
               ("Jumlah pesanan serupa", f"{jumlah} pesanan"),
               ("Pesanan serupa yang terlambat", f"{persen_telat:.1f}%"),
               ("Rata-rata telat (hanya yang terlambat)", f"{rata_telat:.1f} hari"),
               ("Persentase telat pada cuaca ini", f"{p_cuaca:.1f}%"),
               ("Persentase telat pada metode ini", f"{p_metode:.1f}%"),
               ("Indeks risiko", f"{indeks:.1f}%"),
               ("Tingkat risiko", tingkat),
               ("Peringkat risiko", f"{posisi_terpilih} dari {len(urutan_risiko)} kombinasi"),
               ("Saran", SARAN_RISIKO[tingkat])],
              "<<", caption="HASIL ANALISIS RISIKO KETERLAMBATAN")

    baris_tabel = []
    for urutan, (indeks, c, m, jumlah, persen_telat, rata_telat, _, _) in enumerate(urutan_risiko[:jumlah_tampil], 1):
        baris_tabel.append((urutan, c, m, jumlah, f"{persen_telat:.1f}%",
                            f"{rata_telat:.1f}", f"{indeks:.1f}%", tingkat_risiko(indeks)))
    tabel(["No", "Cuaca", "Metode Kirim", "Pesanan", "Terlambat",
           "Rata-rata Telat (hari)", "Indeks Risiko", "Tingkat"],
          baris_tabel, "^<<>>>><",
          caption=f"{len(baris_tabel)} KOMBINASI CUACA & METODE DENGAN RISIKO TERTINGGI")
    print("\nCatatan : Indeks risiko = 75% x (persentase telat pada cuaca)")
    print("                       + 25% x (persentase telat pada metode kirim).")
    print("Skala   : di bawah 40% = Rendah | 40%-60% = Sedang | di atas 60% = Tinggi")


def menu_saran(terkirim):
    judul("MENU 2 : SARAN KURIR")
    print("Tentukan metode kirim, syarat minimal kurir, dan jumlah kurir yang ditampilkan.")
    metode_pilihan = minta("pilih", pilihan=DAFTAR_METODE, caption="Daftar metode kirim")
    print()
    batas = minta(
        "angka", minimum=0,
        pesan="Maksimal rata-rata keterlambatan yang diterima (hari, contoh 1 atau 1.5): ")
    minimal = minta(
        "angka", minimum=1, maksimum=5,
        pesan="Minimal rata-rata rating pelanggan (angka 1 sampai 5, contoh 4): ")
    jumlah_tampil = minta(
        "bulat", minimum=1, maksimum=len(DAFTAR_KURIR),
        pesan=f"Tampilkan berapa kurir teratas? (1-{len(DAFTAR_KURIR)}, contoh 3): ")

    rata_hari = {}
    rata_rating = {}
    rata_ongkir = {}
    for nama in DAFTAR_KURIR:
        jumlah = total_hari = total_rating = total_ongkir = 0
        for baris in terkirim:
            if baris["carrier"] == nama and baris["shipping_method"] == metode_pilihan:
                jumlah += 1
                total_hari += baris["hari_telat"]
                total_rating += baris["customer_rating"]
                total_ongkir += baris["shipping_cost_usd"]
        if jumlah > 0:
            hari = total_hari / jumlah
            rating = total_rating / jumlah
            if hari <= batas and rating >= minimal:
                rata_hari[nama] = hari
                rata_rating[nama] = rating
                rata_ongkir[nama] = total_ongkir / jumlah

    if not rata_hari:
        print("\n[!] Tidak ada kurir yang memenuhi syarat Anda.")
        print("    Coba naikkan batas keterlambatan atau turunkan minimal rating.")
        return

    min_hari = min(rata_hari.values())
    max_rating = max(rata_rating.values())
    min_ongkir = min(rata_ongkir.values())
    hasil = []
    for nama in rata_hari:
        hari = rata_hari[nama]
        rating = rata_rating[nama]
        ongkir = rata_ongkir[nama]
        nilai_hari = min_hari / hari if hari > 0 else 1
        nilai_ongkir = min_ongkir / ongkir if ongkir > 0 else 1
        skor = (BOBOT_KECEPATAN * nilai_hari
                + BOBOT_RATING * rating / max_rating
                + BOBOT_ONGKIR * nilai_ongkir)
        hasil.append((skor, nama, hari, rating, ongkir))
    hasil.sort(reverse=True)

    baris_tabel = []
    for urutan, (skor, nama, hari, rating, ongkir) in enumerate(hasil[:jumlah_tampil], 1):
        baris_tabel.append((urutan, nama, f"{skor:.2f}", f"{hari:.2f}",
                            f"{rating:.2f}", f"{ongkir:.2f}"))
    tabel(["Peringkat", "Kurir", "Skor", "Rata-rata Telat (hari)", "Rating", "Ongkir (USD)"],
          baris_tabel, "^<>>>>",
          caption=f"{len(baris_tabel)} KURIR TERBAIK - Metode {metode_pilihan} "
                  f"(telat maks. {batas:g} hari, rating min. {minimal:g})")
    print(f"\nCatatan : {len(hasil)} kurir memenuhi syarat.")
    print("          Skor makin tinggi makin baik (bobot: kecepatan 63,7% | rating 25,8% | ongkir 10,5%).")


def menu_kinerja(terkirim):
    judul("MENU 3 : KINERJA KURIR")
    print("Pilih satu kurir, lalu tentukan berapa kurir teratas yang ditampilkan di peringkat.")
    kurir_pilihan = minta("pilih", pilihan=DAFTAR_KURIR, caption="Daftar kurir")
    jumlah_tampil = minta(
        "bulat", minimum=1, maksimum=len(DAFTAR_KURIR),
        pesan=f"\nTampilkan berapa kurir teratas di peringkat? (1-{len(DAFTAR_KURIR)}, contoh 5): ")

    kinerja = {}
    for nama in DAFTAR_KURIR:
        hari = [baris["hari_telat"] for baris in terkirim if baris["carrier"] == nama]
        if hari:
            n = len(hari)
            tepat = hari.count(0)
            ringan = hari.count(1) + hari.count(2)
            lama = n - tepat - ringan
            poin = (POIN_TEPAT_WAKTU * tepat
                    + POIN_TELAT_1_2_HARI * ringan
                    + POIN_TELAT_3_HARI_LEBIH * lama)
            kinerja[nama] = (n, tepat, ringan, lama, 100 * poin / n)

    if kurir_pilihan not in kinerja:
        print(f"\n[!] Kurir {kurir_pilihan} belum memiliki pesanan terkirim.")
        return

    n, tepat, ringan, lama, skor = kinerja[kurir_pilihan]
    tabel(["Kategori Pengiriman", "Jumlah", "Persentase"],
          [("Tepat waktu", tepat, f"{100 * tepat / n:.1f}%"),
           ("Telat 1-2 hari", ringan, f"{100 * ringan / n:.1f}%"),
           ("Telat 3 hari atau lebih", lama, f"{100 * lama / n:.1f}%"),
           ("Total terkirim", n, "100.0%")],
          "<>>", caption=f"KINERJA KURIR : {kurir_pilihan}")

    urutan_skor = []
    for nama, nilai in kinerja.items():
        peringkat = 1
        for lain in kinerja.values():
            if lain[4] > nilai[4]:
                peringkat += 1
        urutan_skor.append((nilai[4], nama, nilai[0], peringkat))
    urutan_skor.sort(reverse=True)

    baris_tabel = []
    for skor_kurir, nama, total, peringkat in urutan_skor[:jumlah_tampil]:
        tanda = "<-- dipilih" if nama == kurir_pilihan else ""
        baris_tabel.append((peringkat, nama, total, f"{skor_kurir:.1f}", tanda))
    for skor_kurir, nama, total, peringkat in urutan_skor:
        if nama == kurir_pilihan:
            peringkat_pilihan = peringkat
    tabel(["Peringkat", "Kurir", "Total Terkirim", "Skor (0-100)", ""],
          baris_tabel, "^<>><",
          caption=f"{len(baris_tabel)} KURIR TERATAS BERDASARKAN SKOR")
    print(f"\nHasil  : {kurir_pilihan} memiliki skor {skor:.1f}/100 "
          f"dan berada di peringkat {peringkat_pilihan} dari {len(DAFTAR_KURIR)} kurir.")
    print("Catatan: Skor makin tinggi berarti kurir makin sering mengirim tepat waktu.")


try:
    try:
        open(NAMA_FILE_CSV, "r", encoding="utf-8-sig").close()
    except FileNotFoundError:
        print(f"\n[X] File '{NAMA_FILE_CSV}' tidak ditemukan.")
        print("    Letakkan file tersebut di folder yang sama dengan program ini,")
        print("    lalu jalankan ulang program.")
        exit()

    cetak_cover()
    akun = registrasi()
    login(akun)

    judul("MEMBACA DATA PENGIRIMAN")
    print(f"Membaca file {NAMA_FILE_CSV} ... mohon tunggu.")
    data, terkirim, salah, total_baris = baca_data()

    if not data:
        print("\n[X] Tidak ada baris data yang valid di dalam file.")
        exit()

    tabel(["Keterangan", "Jumlah"],
          [("Total baris data dibaca", total_baris),
           ("Baris valid", len(data)),
           ("Baris tidak valid (tidak dipakai)", len(salah)),
           ("Pesanan berstatus Delivered", len(terkirim))],
          "<>", caption="RINGKASAN PEMBACAAN DATA")
    if salah:
        tabel(["Baris di CSV", "Alasan Tidak Valid"], salah[:10], "><",
              caption="BARIS TIDAK VALID (maksimal 10 ditampilkan)")

    while True:
        judul("MENU UTAMA")
        tabel(["No", "Menu", "Keterangan"], DAFTAR_MENU, "^<<")
        pilihan = minta("bulat", "Ketik nomor menu (0-3), lalu tekan Enter: ", minimum=0, maksimum=3)

        if pilihan == 1:
            menu_risiko(data)
        elif pilihan == 2:
            menu_saran(terkirim)
        elif pilihan == 3:
            menu_kinerja(terkirim)
        else:
            break

    print(f"\nTerima kasih telah menggunakan program ini, {akun.username}.")

except (KeyboardInterrupt, EOFError):
    print("\n\nProgram dihentikan oleh pengguna.")
