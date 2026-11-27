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

DAFTAR_MENU = [(1, "Lihat Dataset", "Menampilkan data pengirima per halaman"),
               (2, "Cek Risiko Keterlambatan", "Prediksi risiko telat faktor cuaca dan metode"),
               (3, "Saran Kurir", "Rekomendasi kurir terbaik"),
               (4, "Kinerja Kurir", "Peringkat kinerja kurir"),
               (0, "Keluar", "Menutup program")]

BARIS_PER_HALAMAN = 20

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
            pesan = f"Silakan ketik nomor pilihan Anda ({minimum}-{maksimum}), lalu tekan Enter: "

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
        print(f"Maaf, input Anda belum sesuai. Silakan masukkan {satuan} {rentang}.{contoh}")


def tingkat_risiko(indeks):
    return "Rendah" if indeks < 40 else "Sedang" if indeks <= 60 else "Tinggi"


class Akun:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def cek_login(self, username, password):
        return username == self.username and password == self.password


class Kurir:
    def __init__(self, nama, pesanan):
        self.nama = nama
        self.pesanan = pesanan
        self.total = len(pesanan)
        hari = [p["hari_telat"] for p in pesanan]
        self.tepat = hari.count(0)
        self.ringan = hari.count(1) + hari.count(2)
        self.lama = self.total - self.tepat - self.ringan
        poin = (POIN_TEPAT_WAKTU * self.tepat
                + POIN_TELAT_1_2_HARI * self.ringan
                + POIN_TELAT_3_HARI_LEBIH * self.lama)
        self.skor = 100 * poin / self.total if self.total else 0

    def rata(self, kolom):
        return sum(p[kolom] for p in self.pesanan) / self.total


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
    print("Selamat datang! Sebelum mulai, silakan buat akun Anda terlebih dahulu.")
    print()

    username = input("Silakan buat username Anda : ").strip().lower()
    password = input("Silakan buat password Anda : ")

    akun = Akun(username, password)
    print(f"\nAkun '{akun.username}' berhasil dibuat. Sekarang, silakan masuk ya.")
    return akun


def login(akun):
    judul("LANGKAH 2 DARI 2 : LOGIN")
    print("Silakan masuk dengan username dan password yang tadi Anda buat.\n")

    while True:
        username = input("Username Anda : ").strip().lower()
        password = input("Password Anda : ")
        if akun.cek_login(username, password):
            break
        print("Maaf, username atau password Anda belum sesuai. Silakan coba lagi.\n")
    print(f"\nBerhasil masuk. Halo, {akun.username}! Senang bertemu dengan Anda.")


class Dataset:
    def __init__(self, nama_file):
        self.nama_file = nama_file
        self.data = []
        self.terkirim = []
        self.salah = []
        self.total_baris = 0

    @staticmethod
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

    def baca(self):
        with open(self.nama_file, "r", newline="", encoding="utf-8-sig") as file:
            pembaca = csv.DictReader(file)
            kolom_kurang = [kolom for kolom in KOLOM_WAJIB if kolom not in (pembaca.fieldnames or [])]
            if kolom_kurang:
                print("\nMaaf, file Anda belum memiliki kolom wajib berikut: " + ", ".join(kolom_kurang))
                print("Silakan lengkapi kolomnya, lalu jalankan program ini lagi.")
                exit()

            for nomor, baris in enumerate(pembaca, 2):
                self.total_baris += 1
                alasan = self.cek_baris(baris)
                if alasan:
                    self.salah.append((nomor, alasan))
                    continue

                baris["hari_telat"] = int(baris["delivery_delay_days"])
                baris["shipping_cost_usd"] = float(baris["shipping_cost_usd"])
                baris["customer_rating"] = float(baris["customer_rating"])
                self.data.append(baris)
                if baris["delivery_status"] == "Delivered":
                    self.terkirim.append(baris)

    def ringkasan(self):
        tabel(["Keterangan", "Jumlah"],
              [("Total baris data dibaca", self.total_baris),
               ("Baris valid", len(self.data)),
               ("Baris tidak valid (tidak dipakai)", len(self.salah)),
               ("Pesanan berstatus Delivered", len(self.terkirim))],
              "<>", caption="RINGKASAN PEMBACAAN DATA")
        if self.salah:
            tabel(["Baris di CSV", "Alasan Tidak Valid"], self.salah[:10], "><",
                  caption="BARIS TIDAK VALID (maksimal 10 ditampilkan)")


def menu_dataset(data):
    judul("MENU 1 : LIHAT DATASET")
    total_halaman = (len(data) + BARIS_PER_HALAMAN - 1) // BARIS_PER_HALAMAN
    print(f"Di sini Anda bisa melihat seluruh data pengiriman, {BARIS_PER_HALAMAN} baris untuk setiap halaman.")
    print("Hanya baris data yang valid yang akan ditampilkan.")

    halaman = 1
    while True:
        awal = (halaman - 1) * BARIS_PER_HALAMAN
        akhir = min(awal + BARIS_PER_HALAMAN, len(data))
        baris_tabel = []
        for nomor, baris in enumerate(data[awal:akhir], awal + 1):
            baris_tabel.append((nomor, baris["order_id"], baris["order_date"],
                                baris["hari_telat"], f"{baris['shipping_cost_usd']:.2f}",
                                f"{baris['customer_rating']:g}", baris["weather_condition"],
                                baris["shipping_method"], baris["carrier"],
                                baris["delivery_status"]))
        tabel(["No", "ID Order", "Tanggal", "Telat (hr)", "Ongkir ($)", "Rating",
               "Cuaca", "Metode Kirim", "Kurir", "Status"],
              baris_tabel, "><<>>><<<<",
              caption=f"HALAMAN {halaman} DARI {total_halaman} "
                      f"(menampilkan baris {awal + 1} sampai {akhir} dari {len(data)} baris)")

        halaman = minta(
            "bulat", minimum=0, maksimum=total_halaman,
            pesan=f"\nHalaman berapa yang ingin Anda buka? (1-{total_halaman}), "
                  f"atau ketik 0 untuk kembali ke menu utama: ")
        if halaman == 0:
            return


def menu_risiko(data):
    judul("MENU 2 : RISIKO KETERLAMBATAN")
    print("Di sini Anda bisa memeriksa seberapa besar risiko pengiriman Anda terlambat.")
    print("Silakan pilih cuaca dan metode kirim yang ingin Anda periksa, lalu tentukan")
    print("berapa banyak kombinasi berisiko tertinggi yang ingin Anda lihat.")
    cuaca_pilihan = minta("pilih", pilihan=DAFTAR_CUACA, caption="Daftar kondisi cuaca")
    metode_pilihan = minta("pilih", pilihan=DAFTAR_METODE, caption="Daftar metode kirim")
    jumlah_kombinasi = len(DAFTAR_CUACA) * len(DAFTAR_METODE)
    jumlah_tampil = minta(
        "bulat", minimum=1, maksimum=jumlah_kombinasi,
        pesan=f"\nBerapa kombinasi berisiko tertinggi yang ingin Anda lihat? "
              f"(1-{jumlah_kombinasi}, contoh 10): ")

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
        print("\nMaaf, tidak ada pesanan dengan kombinasi cuaca dan metode kirim yang Anda pilih.")
    else:
        indeks, c, m, jumlah, persen_telat, rata_telat, p_cuaca, p_metode = terpilih
        tingkat = tingkat_risiko(indeks)
        tabel(["Keterangan", "Hasil"],
              [("Cuaca yang Anda pilih", c),
               ("Metode kirim yang Anda pilih", m),
               ("Jumlah pesanan serupa", f"{jumlah} pesanan"),
               ("Pesanan serupa yang terlambat", f"{persen_telat:.1f}%"),
               ("Rata-rata telat (hanya yang terlambat)", f"{rata_telat:.1f} hari"),
               ("Persentase telat pada cuaca ini", f"{p_cuaca:.1f}%"),
               ("Persentase telat pada metode ini", f"{p_metode:.1f}%"),
               ("Skor AHP (indeks risiko)", f"{indeks:.1f}%"),
               ("Tingkat risiko", tingkat),
               ("Peringkat risiko", f"{posisi_terpilih} dari {len(urutan_risiko)} kombinasi"),
               ("Saran untuk Anda", SARAN_RISIKO[tingkat])],
              "<<", caption="HASIL ANALISIS RISIKO KETERLAMBATAN")

    baris_tabel = []
    for urutan, (indeks, c, m, jumlah, persen_telat, rata_telat, _, _) in enumerate(urutan_risiko[:jumlah_tampil], 1):
        baris_tabel.append((urutan, c, m, jumlah, f"{persen_telat:.1f}%",
                            f"{rata_telat:.1f}", f"{indeks:.1f}%", tingkat_risiko(indeks)))
    tabel(["No", "Cuaca", "Metode Kirim", "Jumlah", "% Telat",
           "Telat (hr)", "Skor AHP", "Tingkat"],
          baris_tabel, "^<<>>>><",
          caption=f"{len(baris_tabel)} KOMBINASI CUACA & METODE DENGAN RISIKO TERTINGGI")


def menu_saran(terkirim):
    judul("MENU 3 : SARAN KURIR")
    print("Di sini saya akan membantu Anda memilih kurir terbaik. Silakan pilih metode")
    print("kirim, tentukan syarat minimal untuk kurirnya, lalu pilih berapa kurir yang ingin Anda lihat.")
    metode_pilihan = minta("pilih", pilihan=DAFTAR_METODE, caption="Daftar metode kirim")
    print()
    batas = minta(
        "angka", minimum=0,
        pesan="Berapa hari rata-rata keterlambatan maksimal yang masih Anda terima? (contoh 1 atau 1.5): ")
    minimal = minta(
        "angka", minimum=1, maksimum=5,
        pesan="Berapa rata-rata rating pelanggan minimal yang Anda inginkan? (angka 1 sampai 5, contoh 4): ")
    jumlah_tampil = minta(
        "bulat", minimum=1, maksimum=len(DAFTAR_KURIR),
        pesan=f"Berapa kurir teratas yang ingin Anda lihat? (1-{len(DAFTAR_KURIR)}, contoh 3): ")

    kandidat = []
    for nama in DAFTAR_KURIR:
        k = Kurir(nama, [b for b in terkirim if b["carrier"] == nama and b["shipping_method"] == metode_pilihan])
        if k.total and k.rata("hari_telat") <= batas and k.rata("customer_rating") >= minimal:
            kandidat.append(k)

    if not kandidat:
        print("\nMaaf, belum ada kurir yang memenuhi syarat Anda.")
        print("Coba naikkan batas keterlambatan atau turunkan minimal rating ya.")
        return

    min_hari = min(k.rata("hari_telat") for k in kandidat)
    max_rating = max(k.rata("customer_rating") for k in kandidat)
    min_ongkir = min(k.rata("shipping_cost_usd") for k in kandidat)
    hasil = []
    for k in kandidat:
        hari, rating, ongkir = k.rata("hari_telat"), k.rata("customer_rating"), k.rata("shipping_cost_usd")
        nilai_hari = min_hari / hari if hari > 0 else 1
        nilai_ongkir = min_ongkir / ongkir if ongkir > 0 else 1
        skor = (BOBOT_KECEPATAN * nilai_hari
                + BOBOT_RATING * rating / max_rating
                + BOBOT_ONGKIR * nilai_ongkir)
        hasil.append((skor, k.nama, hari, rating, ongkir))
    hasil.sort(reverse=True)

    baris_tabel = []
    for urutan, (skor, nama, hari, rating, ongkir) in enumerate(hasil[:jumlah_tampil], 1):
        baris_tabel.append((urutan, nama, f"{skor:.2f}", f"{hari:.2f}",
                            f"{rating:.2f}", f"{ongkir:.2f}"))
    tabel(["Rank", "Kurir", "Skor AHP", "Telat (hr)", "Rating", "Ongkir ($)"],
          baris_tabel, "^<>>>>",
          caption=f"{len(baris_tabel)} KURIR TERBAIK - Metode {metode_pilihan} "
                  f"(telat maks. {batas:g} hari, rating min. {minimal:g})")
    print(f"\nAda {len(hasil)} kurir yang memenuhi syarat Anda.")
    print("Semakin tinggi skor AHP-nya, semakin baik kurirnya (bobot AHP: kecepatan 63,7% | rating 25,8% | ongkir 10,5%).")


def menu_kinerja(terkirim):
    judul("MENU 4 : KINERJA KURIR")
    print("Di sini Anda bisa melihat seberapa sering seorang kurir mengirim tepat waktu.")
    print("Silakan pilih satu kurir, lalu tentukan berapa kurir teratas yang ingin Anda lihat di peringkat.")
    kurir_pilihan = minta("pilih", pilihan=DAFTAR_KURIR, caption="Daftar kurir")
    jumlah_tampil = minta(
        "bulat", minimum=1, maksimum=len(DAFTAR_KURIR),
        pesan=f"\nBerapa kurir teratas yang ingin Anda lihat di peringkat? "
              f"(1-{len(DAFTAR_KURIR)}, contoh 5): ")

    semua = [Kurir(n, [b for b in terkirim if b["carrier"] == n]) for n in DAFTAR_KURIR]
    semua = [k for k in semua if k.total]
    pilih = next((k for k in semua if k.nama == kurir_pilihan), None)
    if pilih is None:
        print(f"\nMaaf, kurir {kurir_pilihan} belum memiliki pesanan yang terkirim.")
        return

    tabel(["Kategori Pengiriman", "Jumlah", "Persen"],
          [("Tepat waktu", pilih.tepat, f"{100 * pilih.tepat / pilih.total:.1f}%"),
           ("Telat 1-2 hari", pilih.ringan, f"{100 * pilih.ringan / pilih.total:.1f}%"),
           ("Telat 3 hari atau lebih", pilih.lama, f"{100 * pilih.lama / pilih.total:.1f}%"),
           ("Total terkirim", pilih.total, "100.0%"),
           ("Skor AHP (0-100)", "-", f"{pilih.skor:.1f}")],
          "<>>", caption=f"KINERJA KURIR : {kurir_pilihan}")

    semua.sort(key=lambda k: k.skor, reverse=True)
    peringkat = {k.nama: 1 + sum(lain.skor > k.skor for lain in semua) for k in semua}
    baris_tabel = [(peringkat[k.nama], k.nama, k.total, f"{k.skor:.1f}",
                    "<-- pilihan Anda" if k is pilih else "") for k in semua[:jumlah_tampil]]
    tabel(["Rank", "Kurir", "Terkirim", "Skor AHP", ""],
          baris_tabel, "^<>><",
          caption=f"{len(baris_tabel)} KURIR TERATAS BERDASARKAN SKOR")
    print(f"\nHasilnya, {kurir_pilihan} memiliki skor AHP {pilih.skor:.1f}/100 "
          f"dan berada di peringkat {peringkat[kurir_pilihan]} dari {len(DAFTAR_KURIR)} kurir.")
    print("Semakin tinggi skor AHP-nya, semakin sering kurir ini mengirim tepat waktu.")

    terbaik = " dan ".join(k.nama for k in semua if peringkat[k.nama] == 1)
    print(f"\nSaran dari program: pilihan terbaik untuk Anda adalah {terbaik}.")

def tanya_lanjut():
    pilihan = minta("pilih", pilihan=["Kembali ke menu utama", "Keluar dari program"],
                    caption="Hasilnya sudah selesai ditampilkan. Apa yang ingin Anda lakukan selanjutnya?")
    return pilihan == "Kembali ke menu utama"


try:
    open(NAMA_FILE_CSV, "r", encoding="utf-8-sig").close()
except FileNotFoundError:
    print(f"\nMaaf, file '{NAMA_FILE_CSV}' tidak ditemukan.")
    print("Silakan letakkan file tersebut di folder yang sama dengan program ini,")
    print("lalu jalankan programnya lagi.")
    exit()

cetak_cover()
akun = registrasi()
login(akun)

judul("MEMBACA DATA PENGIRIMAN")
print(f"Sebentar ya, saya sedang membaca file {NAMA_FILE_CSV} ...")
dataset = Dataset(NAMA_FILE_CSV)
dataset.baca()

if not dataset.data:
    print("\nMaaf, saya tidak menemukan satu pun baris data yang valid di dalam file Anda,")
    print("jadi program tidak bisa dilanjutkan.")
    exit()

print("Selesai! Berikut ringkasan data yang berhasil saya baca.")
dataset.ringkasan()

while True:
    judul("MENU UTAMA")
    print("Apa yang ingin Anda lakukan sekarang?")
    tabel(["No", "Menu", "Keterangan"], DAFTAR_MENU, "^<<")
    pilihan = minta("bulat", "Silakan pilih menu (0-4), lalu tekan Enter: ", minimum=0, maksimum=4)

    if pilihan == 1:
        menu_dataset(dataset.data)
    elif pilihan == 2:
        menu_risiko(dataset.data)
    elif pilihan == 3:
        menu_saran(dataset.terkirim)
    elif pilihan == 4:
        menu_kinerja(dataset.terkirim)
    else:
        break

    if pilihan in (2, 3, 4) and not tanya_lanjut():
        break

print(f"\nTerima kasih sudah menggunakan program ini, {akun.username}. Sampai jumpa!")