# Program Klasifikasi Tingkat Keterlambatan Pengiriman E-Commerce dan Ringkasan Kinerja Kurir Berdasarkan Data Pengiriman

**Mini Project Pemrograman Komputer — Kelompok 3C**
Laboratorium Sistem Informasi dan Keputusan
Departemen Teknik Industri, Fakultas Teknik, Universitas Andalas (2026)

## Anggota Kelompok 3C

* Farhan Raditya Ramadhan (2610932034)
* Ghani Sakha Favian (2610931023)
* Muhammad Raziq Zoelend (2610932042)
* Nabila Putri Ramadhani (2610931031)

Asisten Pembimbing: Anisha Nur Aprilia
Dosen Pengampu: Dr. Asmuliardi Muluk, S.T., M.T.

## Deskripsi Program

Program berbasis terminal ini membaca data pengiriman e-commerce dari file CSV (50.000 baris), memvalidasi kelayakan setiap baris data, lalu menyediakan empat menu analisis: melihat dataset per halaman, mengecek risiko keterlambatan berdasarkan kombinasi cuaca dan metode pengiriman (`Rendah`, `Sedang`, `Tinggi`), merekomendasikan kurir terbaik, serta meringkas kinerja dan peringkat kurir. Perhitungan skor menggunakan pembobotan AHP. Program diawali dengan registrasi dan login akun sederhana.

## File Utama dalam Repositori

* `analisis_pengiriman_ecommerce.py` — Kode utama program Python.
* `E-commerce_Delivery_Shipping_Data_2026.csv` — Dataset pengiriman e-commerce (50.000 baris, delimiter `,`). Sumber: [Kaggle](https://www.kaggle.com/datasets/datascikhan/e-commerce-delivery-and-shipping-data-2026).
* `Laporan_Mini_Project_3C.docx` — Laporan mini project.
* `README.md` — Dokumentasi panduan penggunaan program.

## Cara Menjalankan Program

1. Pastikan Python 3 terpasang di perangkat.
2. Letakkan file kode program dan file CSV dalam satu folder yang sama.
3. Jalankan program dari terminal di folder proyek:

```
python analisis_pengiriman_ecommerce.py
```

4. Buat username dan password, lalu login. Setelah itu pilih menu 0-4 pada Menu Utama:

| No | Menu |
|---|---|
| 1 | Lihat Dataset |
| 2 | Cek Risiko Keterlambatan |
| 3 | Saran Kurir |
| 4 | Kinerja Kurir |
| 0 | Keluar |
