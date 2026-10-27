# Frontend - Sistem Operasional UMKM

Frontend aplikasi ini menyediakan antarmuka Vue.js untuk pencatatan penghasilan,
pengeluaran, produk, kategori, transaksi, autentikasi pengguna, dan dashboard
ringkasan finansial.

> **Status:** README ini menjadi panduan setup frontend. Pastikan implementasi
> Vue.js dan API backend sudah tersedia sebelum menjalankan perintah di bawah.

## Teknologi

- Vue 3
- Vite
- Vue Router
- Pinia
- Axios
- Node.js 20 LTS atau lebih baru

## Prasyarat

Pastikan perangkat lokal sudah memiliki:

1. Node.js 20 LTS atau lebih baru.
2. npm 10 atau lebih baru.
3. Backend FastAPI berjalan pada `http://localhost:8000`.
4. Browser modern seperti Chrome, Edge, atau Firefox.

Periksa versi yang terpasang:

```bash
node --version
npm --version
```

## Instalasi

Jalankan perintah berikut dari folder `frontend`:

```bash
npm install
```

Buat file `.env` di folder `frontend`:

```env
VITE_API_BASE_URL=http://localhost:8000/api
```

Jangan commit file `.env` jika berisi konfigurasi khusus mesin lokal atau
credential.

## Menjalankan dalam mode development

```bash
npm run dev
```

Buka URL yang ditampilkan Vite, biasanya:

```text
http://localhost:5173
```

Jika frontend dijalankan pada port lain, pastikan URL tersebut terdaftar pada
konfigurasi CORS backend.

## Build dan preview production

```bash
npm run build
npm run preview
```

Hasil build berada di folder `dist/`. Perintah `preview` hanya digunakan untuk
memeriksa hasil build secara lokal, bukan sebagai server production.

## Struktur halaman yang direncanakan

```text
src/
├── assets/           # Gambar dan stylesheet
├── components/       # Komponen UI yang dapat digunakan ulang
├── layouts/          # Layout publik dan layout aplikasi
├── router/           # Definisi route dan navigation guard
├── stores/           # State autentikasi dan data aplikasi (Pinia)
├── services/         # Konfigurasi Axios dan pemanggilan API
├── views/            # Halaman login, dashboard, dan CRUD
└── App.vue
```

Route utama yang digunakan:

| Route | Akses | Keterangan |
|---|---|---|
| `/login` | Publik | Login pengguna |
| `/register` | Publik | Registrasi pengguna |
| `/dashboard` | Login | Ringkasan pemasukan, pengeluaran, dan saldo |
| `/products` | Login | CRUD produk |
| `/categories` | Login | CRUD kategori |
| `/transactions` | Login | CRUD transaksi |

## Informasi akses login lokal

Gunakan akun seed berikut untuk pengujian lokal:

```text
Email   : admin@umkm.local
Password: Admin123!
Peran   : admin
```

Akun ini harus dibuat oleh seed/migration backend. Jika backend belum memiliki
seed akun, lakukan registrasi melalui `/register` atau buat akun menggunakan
endpoint registrasi backend. Jangan gunakan password ini pada lingkungan
staging atau production.

## Integrasi API

Frontend membaca base URL dari `VITE_API_BASE_URL`. Endpoint yang diharapkan:

```text
POST   /api/auth/register
POST   /api/auth/login
POST   /api/auth/logout
GET    /api/auth/me

GET    /api/dashboard/summary
GET    /api/products
POST   /api/products
GET    /api/products/{id}
PUT    /api/products/{id}
DELETE /api/products/{id}

GET    /api/categories
POST   /api/categories
PUT    /api/categories/{id}
DELETE /api/categories/{id}

GET    /api/transactions
POST   /api/transactions
PUT    /api/transactions/{id}
DELETE /api/transactions/{id}
```

Axios harus mengirim cookie sesi secara konsisten (`withCredentials: true`).
Untuk request yang mengubah data, frontend juga harus mengirim token CSRF
sesuai mekanisme yang disediakan backend, misalnya header `X-CSRF-Token`.

## Troubleshooting

### Gagal terhubung ke API

1. Pastikan backend berjalan di `http://localhost:8000`.
2. Periksa nilai `VITE_API_BASE_URL`.
3. Pastikan CORS backend mengizinkan `http://localhost:5173`.
4. Setelah mengubah `.env`, hentikan dan jalankan ulang Vite.

### Login terkena error CORS atau cookie tidak tersimpan

Pastikan request Axios menggunakan `withCredentials: true`, backend
mengizinkan credentials, dan frontend tidak mengakses API melalui hostname
yang berbeda dari konfigurasi cookie backend.

## Perintah npm yang disarankan

```bash
npm run dev       # Development server
npm run build     # Validasi type/build production
npm run preview   # Preview hasil build
```

