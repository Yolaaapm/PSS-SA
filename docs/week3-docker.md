# Dokumentasi Docker Containerization - Week 3

**Nama:** Fiola Putri Monika  
**NIM:** A11.2023.15413  

---

## Ringkasan Konsep & Implementasi

1. **Dockerfile:** 
   Menggunakan base image `python:3.12-slim` untuk membuat custom image yang efisien. Server dijalankan pada host `0.0.0.0` port `8000` agar dapat diakses dari luar container.

2. **Docker Compose & Networking:**
   Mengorkestrasi dua service utama: `app` (Python backend) dan `db` (PostgreSQL 17). Aplikasi terhubung ke database menggunakan hostname service `db` dalam network bawaan Compose.

3. **Persistent Data & Volume:**
   Menggunakan *named volume* `postgres_data` yang dipetakan ke `/var/lib/postgresql/data` pada container database. Hal ini memastikan data PostgreSQL tetap tersimpan meskipun container di-restart atau dihentikan (`docker compose down`).

4. **Environment Variables:**
   Credential dan konfigurasi database diinjeksi via file `.env` secara aman tanpa menanam credential permanen pada source code.