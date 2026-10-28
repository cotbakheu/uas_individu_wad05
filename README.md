# UMKM Pro

Aplikasi full-stack untuk manajemen operasional dan keuangan UMKM. Frontend
menggunakan Vue 3 dan backend menggunakan FastAPI, SQLModel, serta MySQL.
Pada production, frontend dibuild di dalam Docker image dan disajikan oleh
FastAPI dalam satu service.

## Demo deployment

Aplikasi production tersedia di:

<https://uas-individu-wad05.onrender.com/>

Halaman API:

- Health check: <https://uas-individu-wad05.onrender.com/health>
- Swagger UI: <https://uas-individu-wad05.onrender.com/docs>

## Prasyarat komputer lokal

Install Git, Node.js 22+, Python 3.12+, `uv`, dan Docker Desktop jika ingin
menguji image production. MySQL 8 dapat digunakan untuk development; SQLite
tersedia sebagai fallback sederhana.

```bash
git --version
node --version
npm --version
python --version
uv --version
docker --version
```

## Instalasi dan menjalankan backend

```bash
cd backend
uv sync
```

Salin `.env.example` menjadi `.env`. Untuk development dengan SQLite:

```env
APP_NAME=UMKM Pro API
ENVIRONMENT=development
SECRET_KEY=local-secret-key-minimal-32-characters
CSRF_SECRET_KEY=local-csrf-secret-key-minimal-32-characters
DATABASE_URL=sqlite:///./umkm_local.db
FRONTEND_URL=http://localhost:5173
SESSION_COOKIE_NAME=umkm_session
SESSION_COOKIE_SECURE=false
SESSION_COOKIE_SAMESITE=lax
```

Untuk MySQL lokal, gunakan format:

```env
DATABASE_URL=mysql+pymysql://umkm_app:password@127.0.0.1:3306/umkm_operasional
```

Jalankan backend dari folder `backend`:

```bash
uv run uvicorn app.main:app --app-dir src --reload --host 127.0.0.1 --port 8000
```

Backend tersedia di <http://localhost:8000>. Tabel dibuat otomatis dengan
`SQLModel.metadata.create_all(engine)`. Project ini belum menggunakan Alembic.
Untuk membuat akun administrator dan kategori awal:

```bash
uv run python -m app.database.seed
```

## Instalasi dan menjalankan frontend

Buka terminal baru dari root repository:

```bash
cd frontend
npm install
```

Buat `frontend/.env`:

```env
VITE_API_BASE_URL=/api
```

Jalankan frontend:

```bash
npm run dev
```

Buka <http://localhost:5173>. Vite meneruskan request `/api` ke backend pada
`http://localhost:8000`.

Build production frontend:

```bash
npm run build
```

## Menjalankan aplikasi melalui Docker

Jalankan dari root repository, yaitu folder yang berisi `Dockerfile`:

```bash
docker build -t umkm-pro-local .
docker run --rm --name umkm-pro-local --env-file ./backend/.env -p 8000:8000 umkm-pro-local
```

Buka <http://localhost:8000/>. FastAPI akan menyajikan frontend Vue, asset
`/assets`, route SPA, dan API `/api` dari origin yang sama.

Test container:

```bash
curl http://localhost:8000/health
```

Pada PowerShell gunakan `curl.exe` jika diperlukan:

```powershell
curl.exe http://localhost:8000/health
```

## Informasi akses login

Akun administrator dari seed:

```text
Email   : admin@umkm.com
Password: Admin123!
Peran   : admin
```

Jalankan seed sebelum memakai akun tersebut. Jangan gunakan password default
untuk pengguna production; ganti dengan password yang kuat. Jika seed belum
dijalankan, akun dapat dibuat melalui halaman `/register`.

## Aturan transaksi

- Produk wajib dipilih.
- `amount` adalah jumlah unit produk.
- `income` berarti produk terjual: stok berkurang dan uang masuk.
- `expense` berarti pengadaan/restock: stok bertambah dan uang keluar.
- Penjualan melebihi stok ditolak oleh backend dan dibatasi di frontend.
- Riwayat transaksi menampilkan nominal `harga produk x jumlah unit`.

## Deploy ke Render

Buat **Web Service** baru di Render dan hubungkan repository. Pilih:

```text
Environment     : Docker
Dockerfile path : Dockerfile
Docker context  : root repository
```

Biarkan Build Command dan Start Command kosong karena keduanya sudah diatur
oleh Dockerfile. Dockerfile membuild Vue, menginstal backend dari
`pyproject.toml` dan `uv.lock`, lalu menjalankan Uvicorn pada `0.0.0.0:$PORT`.

Tambahkan environment variables berikut di Render:

```env
APP_NAME=UMKM Pro API
ENVIRONMENT=production
SECRET_KEY=<secret-random-panjang>
CSRF_SECRET_KEY=<secret-random-berbeda>
DATABASE_URL=mysql+pymysql://username:password@host:3306/database_name
FRONTEND_URL=https://uas-individu-wad05.onrender.com
SESSION_COOKIE_NAME=umkm_session
SESSION_COOKIE_SECURE=true
SESSION_COOKIE_SAMESITE=lax
```

`FRONTEND_URL` harus sama dengan URL publik Render tanpa trailing slash:

```text
https://uas-individu-wad05.onrender.com
```

Pastikan MySQL production dapat menerima koneksi dari Render dan gunakan user
database khusus aplikasi, bukan `root`. Setelah deploy, uji:

```text
https://uas-individu-wad05.onrender.com/health
https://uas-individu-wad05.onrender.com/
https://uas-individu-wad05.onrender.com/docs
```

Untuk deployment Docker, `requirements.txt` tidak diperlukan karena dependency
backend dibaca dari `pyproject.toml` dan `uv.lock`.

## Struktur repository

```text
.
├── Dockerfile
├── README.md
├── frontend/
│   ├── src/
│   ├── package.json
│   └── README.md
└── backend/
    ├── src/app/
    ├── pyproject.toml
    ├── uv.lock
    └── README.md
```

Dokumentasi khusus tersedia pada [frontend/README.md](frontend/README.md) dan
[backend/README.md](backend/README.md).
