# Frontend - Sistem Operasional UMKM

Frontend aplikasi ini menyediakan antarmuka Vue.js untuk pencatatan penghasilan,
pengeluaran, produk, kategori, transaksi, autentikasi pengguna, dan dashboard
ringkasan finansial.

## Teknologi

- Vue 3
- Vite
- Vue Router
- Pinia
- Fetch API
- Node.js 22 atau lebih baru

## Prasyarat

Pastikan perangkat lokal sudah memiliki:

1. Node.js 22 atau lebih baru.
2. npm 10 atau lebih baru.
3. Backend FastAPI berjalan pada `http://localhost:8000` saat development.
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
VITE_API_BASE_URL=/api
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

Pada mode development, Vite meneruskan request `/api` ke
`http://localhost:8000` melalui proxy di `vite.config.ts`. Pada production,
frontend tidak membutuhkan server terpisah karena hasil build disajikan oleh
FastAPI dari folder `dist/`.

## Build dan preview production

```bash
npm run build
npm run preview
```

Hasil build berada di folder `dist/`. Dalam deployment satu service, folder
tersebut harus berada di `frontend/dist` agar dapat disajikan oleh FastAPI.
Perintah `preview` hanya digunakan untuk memeriksa hasil build secara lokal,
bukan sebagai server production.

## Deployment bersama FastAPI

Dari root project, gunakan [Dockerfile](../Dockerfile):

```bash
docker build -t umkm-operasional .
docker run --env-file backend/.env -p 8000:8000 umkm-operasional
```

Docker membuild Vue dengan `npm run build`, menyalin `frontend/dist` ke image
backend, lalu menjalankan FastAPI sebagai satu service. FastAPI menyajikan API
pada `/api` dan aplikasi Vue pada route lainnya.

## Struktur frontend

```text
src/
├── router/           # Route Vue dan navigation guard autentikasi
├── services/         # Fetch API client, CSRF, dan error handling
├── stores/           # State autentikasi Pinia
├── views/            # Login, register, dashboard, dan CRUD
├── styles.css        # Style global
├── types.ts          # Type TypeScript API
├── App.vue           # Layout aplikasi dan navigasi
└── main.ts           # Bootstrap Vue dan Pinia
```

Route utama yang digunakan:

| Route           | Akses  | Keterangan                                  |
| --------------- | ------ | ------------------------------------------- |
| `/login`        | Publik | Login pengguna                              |
| `/register`     | Publik | Registrasi pengguna                         |
| `/dashboard`    | Login  | Ringkasan pemasukan, pengeluaran, dan saldo |
| `/products`     | Login  | CRUD produk                                 |
| `/categories`   | Login  | CRUD kategori                               |
| `/transactions` | Login  | CRUD transaksi                              |

Pada form transaksi, produk wajib dipilih terlebih dahulu. Field jumlah berarti
jumlah unit produk, catatan bersifat opsional, pemasukan berarti produk terjual
sehingga mengurangi stok, dan pengeluaran berarti pengadaan/restock sehingga
menambah stok. Riwayat transaksi menampilkan nominal uang berdasarkan harga
produk dan jumlah unit. Halaman Produk dan Transaksi menyediakan filter yang
diteruskan ke endpoint backend.

Saat mencatat pemasukan/penjualan, jumlah unit tidak boleh melebihi stok
produk yang tersedia. Validasi ini diterapkan di frontend dan backend.

## Informasi akses login lokal

Gunakan akun seed berikut untuk pengujian lokal:

```text
Email   : admin@umkm.com
Password: Admin123!
Peran   : admin
```

Akun ini harus dibuat oleh seed/migration backend. Jika backend belum memiliki
seed akun, lakukan registrasi melalui `/register` atau buat akun menggunakan
endpoint registrasi backend. Jangan gunakan password ini pada lingkungan
staging atau production.

## Integrasi API

Frontend membaca base URL dari `VITE_API_BASE_URL`. Nilai production yang
digunakan adalah `/api`, sehingga API dan frontend menggunakan origin yang
sama. Endpoint yang diharapkan:

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

Fetch API mengirim cookie sesi dengan `credentials: 'include'`. Untuk request
yang mengubah data, API client mengirim token CSRF melalui header
`X-CSRF-Token`.

## Troubleshooting

### Gagal terhubung ke API

1. Pastikan backend berjalan di `http://localhost:8000` saat development.
2. Periksa nilai `VITE_API_BASE_URL`.
3. Pada development, pastikan proxy Vite mengarah ke backend.
4. Setelah mengubah `.env`, hentikan dan jalankan ulang Vite.

### Login terkena error CORS atau cookie tidak tersimpan

Pastikan request fetch menggunakan `credentials: 'include'`, backend
mengizinkan credentials, dan frontend serta API memakai origin yang sama pada
production.

## Perintah npm yang disarankan

```bash
npm run dev       # Development server
npm run build     # Validasi type/build production
npm run preview   # Preview hasil build
```
