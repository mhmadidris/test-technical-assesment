# Project Test Back

Repositori ini terdiri dari dua layanan utama:

1. **flask-data**: Layanan Flask yang menyediakan data customer dari file JSON.
2. **flask-ingestion**: Layanan FastAPI (Uvicorn) untuk proses ingesti data.

---

## 1. flask-data (Flask)

Layanan ini berjalan di port **5000** dan menyajikan data dari `data/customers.json`.

### Cara Menjalankan:

1. Masuk ke direktori:
   ```bash
   cd flask-data
   ```
2. Buat dan aktifkan Virtual Environment (jika belum):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Instal dependensi:
   ```bash
   pip install -r requirements.txt
   pip install "marshmallow<4.0.0" # Diperlukan untuk kompatibilitas
   ```
4. Jalankan aplikasi:
   ```bash
   python run.py
   ```
5. Akses API:
   - Base URL: `http://localhost:5000/api/v1/customers/`

---

## 2. flask-ingestion (FastAPI)

Layanan ini menggunakan FastAPI dan berjalan di port **8000** secara default.

### Cara Menjalankan:

1. Masuk ke direktori:
   ```bash
   cd flask-ingestion
   ```
2. Siapkan Environment:
   Pastikan `pipenv` sudah terinstal, lalu jalankan:
   ```bash
   pip install pipenv
   pipenv install
   pipenv shell
   ```
3. Konfigurasi `.env`:
   ```bash
   cp .env.example .env
   # Edit file .env sesuai kebutuhan
   ```
4. Jalankan Migrasi Database (jika ada):
   ```bash
   alembic upgrade head
   ```
5. Jalankan aplikasi:
   ```bash
   uvicorn main:app --reload
   ```
6. Akses API:
   - Base URL: `http://localhost:8000/api/v1`
   - Dokumentasi Swagger: `http://localhost:8000/docs`

---

## Struktur Proyek

```text
.
├── flask-data/           # Flask API (Port 5000)
│   ├── app/              # Logika aplikasi & routes
│   └── data/             # Sumber data JSON
└── flask-ingestion/      # FastAPI Service (Port 8000)
    ├── app/              # Router, Models, Services
    └── migrations/       # Database migrations (Alembic)
```
