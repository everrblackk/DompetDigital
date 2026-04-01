# DompetDigital

Aplikasi personal finance sederhana berbasis WebUI (Python + HTML/CSS/JS) untuk mencatat pemasukan dan pengeluaran secara real-time.

## Fitur Utama
- Catat transaksi: deskripsi, nominal, tipe transaksi, dan kategori.
- Format nominal otomatis ke Rupiah pada input (`Rp100.000`).
- Saldo total diperbarui real-time setelah transaksi disimpan.
- Riwayat transaksi terbaru ditampilkan di tabel.
- Ringkasan kategori ditampilkan dengan chart doughnut (Chart.js).
- Data tersimpan lokal ke `data.json` (persist antar restart aplikasi).

## Tech Stack
- Backend: Python + `webui2`
- Frontend: HTML, CSS, JavaScript
- Chart: Chart.js (CDN)
- Penyimpanan: file JSON lokal (`data.json`)

## Struktur Proyek
- `main.py` - logika backend, validasi, state, dan IPC ke frontend.
- `index.html` - antarmuka aplikasi dan interaksi frontend.
- `data.json` - data transaksi lokal (dibuat otomatis saat app berjalan).

## Cara Menjalankan
1. Buat virtual environment:
   ```bash
   python -m venv .venv
   ```
2. Aktifkan virtual environment:
   ```bash
   source .venv/bin/activate
   ```
3. Install dependency:
   ```bash
   pip install --upgrade pip
   pip install webui2
   ```
4. Jalankan aplikasi:
   ```bash
   python main.py
   ```

## Alur Singkat
1. User isi form transaksi di UI.
2. Frontend kirim payload JSON ke fungsi Python `simpan_transaksi`.
3. Backend validasi, hitung saldo, update agregasi + riwayat, lalu simpan ke `data.json`.
4. Backend kirim state terbaru ke frontend untuk update saldo, chart, dan tabel tanpa refresh.

## Validasi Data
- Deskripsi wajib diisi.
- Nominal harus angka bulat positif.
- Tipe transaksi harus valid: `Pemasukan` / `Pengeluaran`.
- Kategori detail harus sesuai tipe transaksi.

## Catatan
- Aplikasi ini adalah prototipe lokal untuk kebutuhan tugas Mobile Apps.
- Belum menggunakan database server dan autentikasi pengguna.
