import csv

cuaca = ["Rain", "Clear", "Cloudy", "Storm", "Snow", "Extreme Heat"]
metode = ["Economy", "Standard", "Express", "Same Day", "International"]
kurir = ["BlueRoute", "EagleCourier", "FastTrack Logistics", "GlobalExpress", "ParcelPro", "PrimeDelivery", "SpeedyCargo", "SwiftShip"]
status = ["Delivered", "Delayed", "In Transit", "Failed Delivery"]
kolom_wajib = ["order_id", "order_date", "delivery_delay_days", "shipping_cost_usd", "customer_rating", "weather_condition", "shipping_method", "carrier", "delivery_status"]


def cek_kolom(judul):
    lengkap = True
    for kolom in kolom_wajib:
        if kolom not in judul:
            print("Kolom yang kurang:", kolom)
            lengkap = False
    return lengkap


def cek_data(baris):
    for kolom in kolom_wajib:
        if not baris[kolom] or not baris[kolom].strip():
            return kolom + " kosong"
        baris[kolom] = baris[kolom].strip()

    tanggal = baris["order_date"].split("-")
    if len(tanggal) != 3:
        return "Format tanggal harus tahun-bulan-hari"
    tahun, bulan, hari = tanggal
    if len(tahun) != 4 or len(bulan) != 2 or len(hari) != 2:
        return "Format tanggal harus tahun-bulan-hari"
    if not tahun.isdecimal() or not bulan.isdecimal() or not hari.isdecimal():
        return "Tanggal harus berisi angka"

    tahun, bulan, hari = int(tahun), int(bulan), int(hari)
    if tahun < 1 or not 1 <= bulan <= 12:
        return "Tahun atau bulan salah"
    hari_per_bulan = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if tahun % 400 == 0 or (tahun % 4 == 0 and tahun % 100 != 0):
        hari_per_bulan[1] = 29
    if not 1 <= hari <= hari_per_bulan[bulan - 1]:
        return "Hari pada tanggal salah"

    if not baris["delivery_delay_days"].isdecimal():
        return "Hari terlambat harus bilangan bulat mulai dari 0"
    for kolom in ["shipping_cost_usd", "customer_rating"]:
        if not baris[kolom].replace(".", "", 1).isdecimal():
            return kolom + " harus berupa angka positif atau nol"

    hari = int(baris["delivery_delay_days"])
    ongkir = float(baris["shipping_cost_usd"])
    rating = float(baris["customer_rating"])
    if not 1 <= rating <= 5:
        return "Rating harus antara 1 dan 5"
    if baris["weather_condition"] not in cuaca or baris["shipping_method"] not in metode:
        return "Cuaca atau metode kirim tidak dikenal"
    if baris["carrier"] not in kurir or baris["delivery_status"] not in status:
        return "Kurir atau status pengiriman tidak dikenal"

    baris["hari"] = hari
    baris["shipping_cost_usd"] = ongkir
    baris["customer_rating"] = rating
    return ""


def pilih(judul, daftar):
    print("\n" + judul)
    pilihan = {}
    for i in range(len(daftar)):
        pilihan[str(i + 1)] = daftar[i]
        print(i + 1, daftar[i])

    while True:
        nomor = input("Pilih nomor: ").strip()
        if nomor in pilihan:
            return pilihan[nomor]
        print("Nomor tidak ada di daftar.")


data = []
salah = []
terkirim = []

with open("E-commerce_Delivery_Shipping_Data_2026.csv", "r") as file:
    pembaca = csv.DictReader(file)
    if cek_kolom(pembaca.fieldnames or []):
        for nomor, baris in enumerate(pembaca, 2):
            alasan = cek_data(baris)
            if alasan:
                salah.append((nomor, alasan))
                continue

            data.append(baris)
            if baris["delivery_status"] == "Delivered":
                terkirim.append(baris)

        print("Data valid:", len(data), "| Data tidak valid:", len(salah))
        for nomor, alasan in salah[:10]:
            print("Baris", nomor, "-", alasan)

while data:
    print("\n1. Risiko terlambat\n2. Saran kurir\n3. Kinerja kurir\n0. Keluar")
    menu = input("Pilih menu: ").strip()

    if menu == "0":
        break

    elif menu == "1":
        cuaca_pilihan = pilih("Cuaca", cuaca)
        layanan = pilih("Metode kirim", metode)
        hari_cuaca = []
        hari_metode = []
        serupa = []
        telat = []

        for baris in data:
            cocok_cuaca = baris["weather_condition"] == cuaca_pilihan
            cocok_metode = baris["shipping_method"] == layanan
            hari = baris["hari"]
            if cocok_cuaca:
                hari_cuaca.append(hari)
            if cocok_metode:
                hari_metode.append(hari)
            if cocok_cuaca and cocok_metode:
                serupa.append(hari)
                if hari > 0:
                    telat.append(hari)

        if not serupa:
            print("Tidak ada pesanan serupa.")
            continue

        p_cuaca = 100 * (len(hari_cuaca) - hari_cuaca.count(0)) / len(hari_cuaca)
        p_metode = 100 * (len(hari_metode) - hari_metode.count(0)) / len(hari_metode)
        indeks = 0.75 * p_cuaca + 0.25 * p_metode
        rata_telat = 0
        if telat:
            rata_telat = sum(telat) / len(telat)

        print(f"\nPesanan serupa: {len(serupa)} | Terlambat: {100 * len(telat) / len(serupa):.1f}%")
        print(f"Rata-rata untuk yang terlambat: {rata_telat:.1f} hari")
        print(f"Cuaca: {p_cuaca:.1f}% | Metode: {p_metode:.1f}% | Indeks: {indeks:.1f}%")

        if indeks < 40:
            print("Rendah. Gunakan estimasi biasa.")
        elif indeks <= 60:
            print("Sedang. Tambahkan 1 hari.")
        else:
            print("Tinggi. Tambahkan 1–2 hari atau tunggu cuaca membaik.")

    elif menu == "2":
        layanan = pilih("Metode kirim", metode)

        batas = input("Maksimal rata-rata terlambat (hari): ").strip()
        minimal = input("Minimal rating (1–5): ").strip()
        if not batas.replace(".", "", 1).isdecimal() or not minimal.replace(".", "", 1).isdecimal():
            print("Masukkan angka, misalnya 3 atau 3.5.")
            continue

        batas = float(batas)
        minimal = float(minimal)
        if not 1 <= minimal <= 5:
            print("Rating harus antara 1 dan 5.")
            continue

        rata_hari = {}
        rata_rating = {}
        rata_ongkir = {}
        for nama in kurir:
            jumlah = total_hari = total_rating = total_ongkir = 0
            for baris in terkirim:
                if baris["carrier"] == nama and baris["shipping_method"] == layanan:
                    jumlah += 1
                    total_hari += baris["hari"]
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
            print("Tidak ada kurir yang memenuhi syarat.")
            continue

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
            skor = 0.637 * nilai_hari + 0.258 * rating / max_rating + 0.105 * nilai_ongkir
            hasil.append((skor, nama, hari, rating, ongkir))

        hasil.sort(reverse=True)
        print("\nRekomendasi kurir")
        for skor, nama, hari, rating, ongkir in hasil[:3]:
            print(f"{nama}: skor {skor:.2f}, telat {hari:.2f} hari, rating {rating:.2f}, ongkir ${ongkir:.1f}")

    elif menu == "3":
        pilihan = pilih("Kurir", kurir)
        skor_kurir = {}

        for nama in kurir:
            hari = []
            for baris in terkirim:
                if baris["carrier"] == nama:
                    hari.append(baris["hari"])

            if hari:
                tepat = hari.count(0)
                ringan = hari.count(1) + hari.count(2)
                sedang = len(hari) - tepat - ringan
                n = len(hari)
                skor_kurir[nama] = 100 * (0.309 * tepat + 0.109 * (n - ringan) + 0.582 * (n - sedang)) / n

                if nama == pilihan:
                    print("\nTotal terkirim:", n)
                    print(f"Tepat waktu: {tepat} ({100 * tepat / n:.1f}%)")
                    print(f"Telat 1–2 hari: {ringan} ({100 * ringan / n:.1f}%)")
                    print(f"Telat 3 hari atau lebih: {sedang} ({100 * sedang / n:.1f}%)")

        if pilihan in skor_kurir:
            skor = skor_kurir[pilihan]
            peringkat = 1
            for nilai in skor_kurir.values():
                if nilai > skor:
                    peringkat += 1
            print(f"Skor: {skor:.1f}/100 | Peringkat: {peringkat} dari {len(kurir)}")
        else:
            print("Kurir ini belum memiliki pesanan terkirim.")
    else:
        print("Pilih menu 0 sampai 3.")
