# Backend - Sistem Operasional UMKM

Backend adalah REST API FastAPI untuk sistem manajemen operasional dan
pencatatan finansial UMKM. Aplikasi menggunakan pola MVC, SQLModel sebagai
ORM, MySQL sebagai database relasional, Pydantic untuk validasi request, serta
session dan CSRF token untuk keamanan akses.

Backend saat ini menggunakan SQLModel untuk membuat tabel secara otomatis saat
aplikasi mulai. Alembic belum dikonfigurasi pada project ini, sehingga belum
ada migration versioning.

## Teknologi

- Python 3.12 atau lebih baru
- FastAPI
- Uvicorn
- SQLModel
- SQLAlchemy dan PyMySQL
- Pydantic Settings
- bcrypt untuk hashing password
- Session middleware
- MySQL 8.0 atau lebih baru

## Struktur folder

Struktur backend mengikuti pola MVC. Route menangani request dan response,
service berisi aturan bisnis, model merepresentasikan tabel database, sedangkan
schema menangani validasi data masuk dan keluar.

```text
backend/
├── src/
│   └── app/
│       ├── __init__.py
│       ├── main.py             # Entry point FastAPI dan static frontend
│       ├── core/               # Config, dependencies, dan security
│       │   ├── __init__.py
│       │   ├── config.py
│       │   ├── dependencies.py
│       │   └── security.py
│       ├── database/            # Koneksi database dan seed data
│       │   ├── __init__.py
│       │   ├── database.py
│       │   └── seed.py
│       ├── models/              # Model SQLModel dan relasi database
│       │   ├── __init__.py
│       │   ├── user.py
│       │   ├── category.py
│       │   ├── product.py
│       │   └── transaction.py
│       ├── schemas/             # Schema Pydantic untuk validasi API
│       │   ├── __init__.py
│       │   ├── auth.py
│       │   ├── category.py
│       │   ├── product.py
│       │   └── transaction.py
│       ├── routes/              # Endpoint API per modul
│       │   ├── __init__.py
│       │   ├── auth.py
│       │   ├── users.py
│       │   ├── dashboard.py
│       │   ├── categories.py
│       │   ├── products.py
│       │   └── transactions.py
│       ├── services/            # Logika bisnis per modul
│       │   ├── __init__.py
│       │   ├── auth.py
│       │   ├── users.py
│       │   ├── dashboard.py
│       │   ├── categories.py
│       │   ├── products.py
│       │   ├── transactions.py
│       │   └── common.py
│       └── middleware/          # Session, CSRF, dan middleware keamanan
│           └── csrf.py
├── .env                        # Konfigurasi lokal (jangan di-commit)
├── .env.example                # Template environment tanpa secret
├── .gitignore
├── pyproject.toml
├── uv.lock
├── umkm_local.db               # SQLite lokal jika digunakan
└── README.md
```

Alur request secara umum adalah:

```text
Client -> routes -> services -> models/database
             |
             +-> schemas (validasi request/response)
```

Nama file pada struktur di atas merupakan struktur yang digunakan project.
`routes` menerima request per modul (`auth`, `users`, `categories`, `products`,
`transactions`, dan `dashboard`), `services` menjalankan aturan bisnis per modul,
`models`
merepresentasikan tabel, `schemas` memvalidasi payload, `database` mengelola
koneksi/seed, dan `core` menyediakan konfigurasi serta dependency bersama.

## Prasyarat

Pasang komponen berikut:

1. Python 3.12+.
2. MySQL Server 8.0+.
3. `uv`.
4. Git (opsional).

Periksa Python:

```bash
python --version
uv --version
```

## Instalasi di Windows PowerShell

Jalankan dari folder `backend`:

```powershell
uv sync
```

`uv sync` akan membuat atau memperbarui virtual environment `.venv`
berdasarkan `pyproject.toml` dan `uv.lock`.

## Instalasi di Linux/macOS

```bash
uv sync
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

Untuk development tanpa MySQL, gunakan fallback SQLite berikut:

```env
DATABASE_URL=sqlite:///./umkm_local.db
```

File SQLite tersebut dibuat di folder `backend` dan hanya ditujukan untuk
development lokal.

Saat menggunakan driver PyMySQL, jangan meneruskan `ssl-mode` sebagai query
parameter yang tidak diproses. Backend menormalisasi `ssl-mode` atau
`ssl_mode` sebelum membuat engine: nilai `FALSE` dihapus, sedangkan
`REQUIRED`, `verify_ca`, dan `verify_identity` mengaktifkan SSL dasar. Untuk
production, gunakan sertifikat TLS dari provider database jika diwajibkan.

Generate secret yang aman, misalnya:

```powershell
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Jalankan perintah tersebut dua kali dan gunakan hasil yang berbeda untuk
`SECRET_KEY` dan `CSRF_SECRET_KEY`. File `.env` tidak boleh dimasukkan ke
version control.

## Menjalankan backend

Jalankan dari folder `backend`:

```bash
uv run uvicorn app.main:app --app-dir src --reload --host 127.0.0.1 --port 8000
```

Atau gunakan FastAPI CLI. Karena source code menggunakan layout `src/`, jalankan
perintah ini dari folder `backend`:

```bash
uv run fastapi dev src/app/main.py
```

Entrypoint `app.main:app` juga sudah disimpan pada bagian `[tool.fastapi]` di
`pyproject.toml`, sehingga setelah dependency project terpasang perintah berikut
juga dapat digunakan:

```bash
uv run fastapi dev
```

Jangan menjalankan `fastapi dev` dari folder `backend/src/app`. Jalankan dari
root folder `backend` agar konfigurasi `pyproject.toml` dan environment project
ditemukan dengan benar.

API tersedia pada:

```text
http://localhost:8000
```

Dokumentasi interaktif tersedia pada:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

Saat frontend sudah dibuild, FastAPI juga menyajikan `frontend/dist` pada
origin yang sama. Route `/api/*` tetap digunakan untuk REST API, sedangkan
route Vue seperti `/`, `/login`, dan `/dashboard` dikembalikan ke `index.html`
agar Vue Router berfungsi setelah refresh halaman.

## Deployment satu platform

Root project menyediakan [Dockerfile](../Dockerfile) untuk membuild Vue dan
menjalankan hasil build tersebut melalui FastAPI dalam satu service. Jalankan
command Docker dari root repository, bukan dari folder `backend`:

```bash
docker build -t umkm-operasional .
docker run --env-file backend/.env -p 8000:8000 umkm-operasional
```

Dockerfile akan:

1. Menginstal dependency dan membuild frontend Vue.
2. Menginstal dependency Python backend menggunakan `uv`.
3. Menyalin `frontend/dist` ke image backend.
4. Menjalankan Uvicorn pada `0.0.0.0` dan port dari environment `PORT`.

Untuk production, gunakan konfigurasi frontend berikut saat build:

```env
VITE_API_BASE_URL=/api
```

Backend mendeteksi folder `frontend/dist` secara otomatis. Jika folder tersebut
tidak ada, route frontend mengembalikan `Frontend build not found`; API tetap
dapat digunakan.

## Pembuatan tabel dan seed data

Project saat ini belum menggunakan Alembic. Tabel dibuat melalui
`SQLModel.metadata.create_all(engine)` ketika aplikasi mulai, dan juga ketika
seed dijalankan.

Jalankan seed dari folder `backend`:

```bash
uv run python -m app.database.seed
```

Seed membuat tabel `users`, `categories`, `products`, dan `transactions` jika
belum ada, lalu membuat akun administrator serta kategori awal.

Jika model database berubah, `create_all()` hanya membuat tabel yang belum ada;
ia tidak mengubah atau menghapus kolom pada tabel yang sudah ada. Untuk
perubahan schema production, Alembic perlu ditambahkan dan dikonfigurasi pada
fase berikutnya. Karena itu, `alembic upgrade head` belum dapat digunakan pada
project ini.

## Informasi akses login lokal

Seed akun administrator lokal:

```text
Email   : admin@umkm.com
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
GET    /api/products?search=kopi&category_id=1&min_stock=0&max_stock=100
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
GET    /api/transactions?type=income&product_id=1&search=penjualan&date_from=2026-01-01&date_to=2026-12-31
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
- `transactions`: pemasukan/pengeluaran berbasis jumlah unit produk yang merujuk
  ke pengguna dan produk.

Relasi utamanya:

```text
users      1 ──── N categories
categories 1 ──── N products
users      1 ──── N products
users      1 ──── N transactions
products   1 ──── N transactions
```

Pada transaksi, `amount` berarti jumlah unit produk dan `product_id` wajib
diisi. Transaksi `income` berarti produk terjual sehingga mengurangi stok,
sedangkan `expense` berarti pengadaan/restock sehingga menambah stok.
Response transaksi juga menyediakan `total_amount`, yaitu nilai uang dari
`harga_produk * amount`. Pengeluaran ditolak jika stok tidak mencukupi. Nilai finansial
dashboard dihitung dari `product.price * transaction.amount`.

## Keamanan yang wajib dipertahankan

1. Gunakan SQLModel/SQLAlchemy expression dan parameter binding; jangan
   menyusun SQL dari string input pengguna.
2. Validasi semua request menggunakan model Pydantic/SQLModel, termasuk angka
   non-negatif, enum tipe transaksi, panjang string, dan foreign key.
3. Hash password menggunakan bcrypt dan verifikasi menggunakan helper library,
   bukan perbandingan plaintext. Password dibatasi maksimal 72 byte UTF-8 oleh
   batasan bcrypt.
4. Gunakan session cookie `HttpOnly`, `SameSite=Lax` atau lebih ketat, serta
   `Secure=true` pada HTTPS.
5. Lindungi request mutasi (`POST`, `PUT`, `PATCH`, `DELETE`) dengan CSRF
   token dan tolak token yang hilang atau tidak valid.
6. Escape output pada frontend dan jangan merender input pengguna sebagai HTML
   mentah. Sanitasi hanya sebagai lapisan tambahan, bukan pengganti escaping.
7. Batasi CORS hanya ke origin frontend yang dikenal, bukan wildcard ketika
   credentials aktif.
8. Jangan mencatat password, session secret, CSRF token, atau cookie ke log.

## Pemeriksaan manual

Pemeriksaan endpoint sederhana:

```bash
curl http://localhost:8000/health
```

Endpoint tersebut seharusnya mengembalikan:

```json
{ "status": "ok" }
```

Project ini belum menyediakan file test otomatis. Validasi sementara dilakukan
melalui Swagger UI pada `http://localhost:8000/docs` dan pemeriksaan endpoint
secara manual.

## Troubleshooting

### `Can't connect to MySQL server`

Pastikan service MySQL aktif, port `3306` terbuka, database sudah dibuat, dan
`DATABASE_URL` memakai password serta nama database yang benar.

### `ModuleNotFoundError`

Pastikan command dijalankan dari folder `backend` dan dependency telah
disinkronkan:

```bash
uv sync
uv run python -m app.database.seed
```

### Frontend terkena CORS

Pastikan `FRONTEND_URL=http://localhost:5173`, backend mengizinkan credentials,
dan frontend mengirim request menggunakan cookie sesi.
