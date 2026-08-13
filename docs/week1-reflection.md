# Refleksi Praktikum Minggu 1 - Pemrograman Sisi Server

**Nama:** Fiola Putri Monika  
**NIM:** A11.2023.15413  

---

### 1. Apa perbedaan frontend dan backend dalam konteks aplikasi web?
- **Frontend:** Bagian antarmuka aplikasi yang berjalan di browser/client, bertugas menampilkan UI/UX, menangani interaksi pengguna, dan mengirim request ke server.
- **Backend:** Bagian logika bisnis yang berjalan di sisi server, bertugas mengolah logika, memproses request, mengelola database, keamanan, dan mengembalikan response.

### 2. Apa yang dimaksud request dan response?
- **Request:** Pesan yang dikirim oleh client (browser) ke server untuk meminta data atau menjalankan perintah (misal: GET, POST).
- **Response:** Pesan balasan dari server ke client yang berisi status code (misal: 200 OK, 404 Not Found) dan payload data (misal: JSON/HTML).

### 3. Mengapa endpoint yang tidak tersedia sebaiknya menghasilkan 404?
Agar client/browser mengetahui secara pasti bahwa resource atau URL yang diminta tidak ditemukan di server, sehingga penanganan error pada sisi aplikasi client dapat dilakukan secara standar dan tepat.

### 4. Apa manfaat virtual environment?
Untuk mengisolasi dependensi dan package Python dari lingkungan global, sehingga proyek tidak bentrok dengan versi library proyek lain dan konfigurasi aplikasi menjadi reproducible (mudah direplikasi).

### 5. Apa perbedaan `git add` dan `git commit`?
- **`git add`:** Memindahkan perubahan file dari working directory ke staging area (persiapan).
- **`git commit`:** Menyimpan snapshot permanen dari file-file yang ada di staging area ke riwayat/repository lokal beserta pesan commit.

### 6. Mengapa secret tidak boleh disimpan di GitHub?
Karena credential seperti password, API key, dan secret key yang berada di repository publik dapat diekspos dan disalahgunakan oleh pihak tidak bertanggung jawab, yang mengancam keamanan data dan server aplikasi.

### 7. Apa manfaat Docker bagi reproducibility walaupun belum digunakan penuh pada minggu 1?
Docker memastikan lingkungan aplikasi (OS, dependency, environment) berjalan secara konsisten dan identik di komputer mana pun (baik komputer pengembang, penguji, maupun server produksi).

### 8. Bagaimana konsep mini backend tadi akan berkembang ketika menggunakan Django/Django Ninja?
Penanganan routing, parsing JSON, validasi data, serta pembacaan database akan ditangani secara otomatis dan terstruktur oleh framework (menggunakan ORM dan Schema/Pydantic), tidak lagi menggunakan logika kondisional manual seperti pada `http.server` bawaan.