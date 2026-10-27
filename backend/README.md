# Backend - Sistem Operasional UMKM

Backend adalah REST API FastAPI untuk sistem manajemen operasional dan
pencatatan finansial UMKM. Aplikasi menggunakan pola MVC, SQLModel sebagai
ORM, MySQL sebagai database relasional, Pydantic untuk validasi request, serta
session dan CSRF token untuk keamanan akses.

> **Status:** README ini menjadi panduan setup backend. Sesuaikan nama modul
> pada perintah jika struktur implementasi akhir berbeda.

## Teknologi

- Python 3.11 atau lebih baru
- FastAPI
- Uvicorn
- SQLModel
- SQLAlchemy dan PyMySQL
- Pydantic Settings
- Passlib atau pwdlib untuk hashing password
- Session middleware
- MySQL 8.0 atau lebih baru

## Struktur folder

Struktur backend mengikuti pola MVC. Controller menangani request dan response,
service berisi aturan bisnis, model merepresentasikan tabel database, sedangkan
schema menangani validasi data masuk dan keluar.

```text
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Entry point FastAPI dan konfigurasi middleware
│   ├── config.py               # Pengaturan aplikasi dari environment
│   ├── database.py             # Engine, session, dan koneksi MySQL
│   ├── dependencies.py         # Dependency autentikasi dan database session
│   ├── models/                 # Model SQLModel dan relasi database
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── category.py
│   │   ├── product.py
│   │   └── transaction.py
│   ├── schemas/                # Schema Pydantic untuk validasi API
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── category.py
│   │   ├── product.py
│   │   └── transaction.py
│   ├── controllers/            # Handler endpoint/controller MVC
│   │   ├── __init__.py
│   │   ├── auth_controller.py
│   │   ├── dashboard_controller.py
│   │   ├── category_controller.py
│   │   ├── product_controller.py
│   │   └── transaction_controller.py
│   ├── services/               # Logika bisnis dan operasi database
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── dashboard_service.py
│   │   ├── category_service.py
│   │   ├── product_service.py
│   │   └── transaction_service.py
│   ├── routes/                 # Registrasi dan pengelompokan route API
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── dashboard.py
│   │   ├── categories.py
│   │   ├── products.py
│   │   └── transactions.py
│   ├── middleware/             # Session, CSRF, CORS, dan security headers
│   │   ├── __init__.py
│   │   ├── csrf.py
│   │   └── security.py
│   ├── core/                   # Utility keamanan dan fungsi umum
│   │   ├── __init__.py
│   │   ├── security.py         # Hash password dan verifikasi kredensial
│   │   └── exceptions.py       # Exception handler aplikasi
│   └── seed.py                 # Seed akun admin dan data awal lokal
├── alembic/                    # Migration schema database
│   ├── versions/
│   └── env.py
├── tests/                      # Unit test dan integration test API
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_products.py
│   ├── test_categories.py
│   └── test_transactions.py
├── .env                        # Konfigurasi lokal (jangan di-commit)
├── .env.example                # Template environment tanpa secret
├── .gitignore
├── alembic.ini
├── requirements.txt
└── README.md
```

Alur request secara umum adalah:

```text
Client -> routes -> controllers -> services -> models/database
                    |
                    +-> schemas (validasi request/response)
```

Nama file pada struktur di atas merupakan konvensi yang direkomendasikan.
Apabila implementasi menggunakan nama modul berbeda, perbarui perintah
startup dan dokumentasi endpoint tanpa mengubah pemisahan tanggung jawab MVC.

## Prasyarat

Pasang komponen berikut:

1. Python 3.11+ dan `pip`.
2. MySQL Server 8.0+.
3. Git (opsional).
4. Node.js 20 LTS untuk menjalankan frontend.

Periksa Python:

```bash
python --version
```

## Instalasi di Windows PowerShell

Jalankan dari folder `backend`:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Jika PowerShell menolak aktivasi script, jalankan PowerShell sebagai pengguna
yang sesuai atau gunakan interpreter virtual environment secara langsung:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Instalasi di Linux/macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Menyiapkan database MySQL

Masuk ke MySQL sebagai user yang memiliki hak membuat database:

```sql
CREATE DATABASE umkm_operasional
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

CREATE USER 'umkm_app'@'localhost' IDENTIFIED BY 'ganti-password-lokal';
GRANT ALL PRIVILEGES ON umkm_operasional.* TO 'umkm_app'@'localhost';
FLUSH PRIVILEGES;
```

Jangan memakai user `root` pada konfigurasi aplikasi.

## Konfigurasi environment

Buat file `.env` di folder `backend`:

```env
APP_NAME=UMKM Operational API
ENVIRONMENT=development
SECRET_KEY=ganti-dengan-secret-random-minimal-32-karakter
CSRF_SECRET_KEY=ganti-dengan-secret-csrf-random-minimal-32-karakter
DATABASE_URL=mysql+pymysql://umkm_app:ganti-password-lokal@127.0.0.1:3306/umkm_operasional
FRONTEND_URL=http://localhost:5173
SESSION_COOKIE_NAME=umkm_session
SESSION_COOKIE_SECURE=false
SESSION_COOKIE_SAMESITE=lax
```

Generate secret yang aman, misalnya:

```powershell
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Jalankan perintah tersebut dua kali dan gunakan hasil yang berbeda untuk
`SECRET_KEY` dan `CSRF_SECRET_KEY`. File `.env` tidak boleh dimasukkan ke
version control.

## Menjalankan backend

Dengan virtual environment aktif:

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

API tersedia pada:

```text
http://localhost:8000
```

Dokumentasi interaktif tersedia pada:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Migrasi dan seed data

Jalankan migrasi sesuai tooling yang digunakan project, contohnya:

```bash
alembic upgrade head
python -m app.seed
```

Jika project menggunakan `SQLModel.metadata.create_all()` untuk development,
jalankan command seed yang disediakan setelah tabel dibuat. Jangan memakai
`create_all()` sebagai pengganti migration pada production.

## Informasi akses login lokal

Seed akun administrator lokal:

```text
Email   : admin@umkm.local
Password: Admin123!
Peran   : admin
```

Jika seed belum dijalankan, buat akun melalui:

```text
POST http://localhost:8000/api/auth/register
```

Password harus disimpan dalam bentuk hash, bukan plaintext. Ganti password
akun seed sebelum aplikasi digunakan di luar komputer lokal.

## Endpoint utama

### Autentikasi

```text
POST /api/auth/register
POST /api/auth/login
POST /api/auth/logout
GET  /api/auth/me
```

### Dashboard

```text
GET /api/dashboard/summary
```

### Resource CRUD

```text
GET    /api/products
POST   /api/products
GET    /api/products/{id}
PUT    /api/products/{id}
DELETE /api/products/{id}

GET    /api/categories
POST   /api/categories
GET    /api/categories/{id}
PUT    /api/categories/{id}
DELETE /api/categories/{id}

GET    /api/transactions
POST   /api/transactions
GET    /api/transactions/{id}
PUT    /api/transactions/{id}
DELETE /api/transactions/{id}
```

## Skema data minimum

Database minimal memiliki tabel berelasi berikut:

- `users`: identitas, role, dan kredensial ter-hash.
- `categories`: kategori produk milik pengguna.
- `products`: produk yang merujuk ke kategori dan pemiliknya.
- `transactions`: pemasukan/pengeluaran yang merujuk ke pengguna dan produk.

Relasi utamanya:

```text
users      1 ──── N categories
categories 1 ──── N products
users      1 ──── N products
users      1 ──── N transactions
products   1 ──── N transactions
```

## Keamanan yang wajib dipertahankan

1. Gunakan SQLModel/SQLAlchemy expression dan parameter binding; jangan
   menyusun SQL dari string input pengguna.
2. Validasi semua request menggunakan model Pydantic/SQLModel, termasuk angka
   non-negatif, enum tipe transaksi, panjang string, dan foreign key.
3. Hash password dengan algoritma modern dan verifikasi menggunakan helper
   library, bukan perbandingan plaintext.
4. Gunakan session cookie `HttpOnly`, `SameSite=Lax` atau lebih ketat, serta
   `Secure=true` pada HTTPS.
5. Lindungi request mutasi (`POST`, `PUT`, `PATCH`, `DELETE`) dengan CSRF
   token dan tolak token yang hilang atau tidak valid.
6. Escape output pada frontend dan jangan merender input pengguna sebagai HTML
   mentah. Sanitasi hanya sebagai lapisan tambahan, bukan pengganti escaping.
7. Batasi CORS hanya ke origin frontend yang dikenal, bukan wildcard ketika
   credentials aktif.
8. Jangan mencatat password, session secret, CSRF token, atau cookie ke log.

## Pengujian dan pemeriksaan

Contoh perintah yang diharapkan tersedia:

```bash
pytest
```

Pemeriksaan endpoint sederhana:

```bash
curl http://localhost:8000/health
```

Pastikan endpoint health mengembalikan status sukses, login menghasilkan
session yang valid, dan endpoint CRUD menolak request tanpa autentikasi/CSRF
sesuai kebijakan aplikasi.

## Troubleshooting

### `Can't connect to MySQL server`

Pastikan service MySQL aktif, port `3306` terbuka, database sudah dibuat, dan
`DATABASE_URL` memakai password serta nama database yang benar.

### `ModuleNotFoundError`

Pastikan virtual environment aktif dan dependency terpasang:

```bash
python -m pip install -r requirements.txt
```

### Frontend terkena CORS

Pastikan `FRONTEND_URL=http://localhost:5173`, backend mengizinkan credentials,
dan frontend mengirim request menggunakan cookie sesi.
