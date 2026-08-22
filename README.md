# UTS Pemrograman Sisi Server - Mini Course Management API

Repository ini berisi implementasi backend RESTful API untuk pengelolaan entitas **Course** dan **Lesson** menggunakan framework Django dan Django Ninja. Sistem dilengkapi dengan containerization Docker, optimasi database ORM, serta automated unit testing.

---

## Identitas Mahasiswa

- **Nama Lengkap:** Fiola Putri Monika
- **NIM:** A11.2023.15413
- **Mata Kuliah:** Pemrograman Sisi Server (PSS)
- **Topik Ujian:** Ujian Tengah Semester (Take-Home Mini Project)

---

## 1. Analisis dan Desain Backend (Soal 1)

### A. Diagram Arsitektur Sistem

```text
+-------------------------------------------------------------+
|              Client Layer (Browser / Swagger / Postman)      |
+-------------------------------------------------------------+
                          |
                  HTTP Request / JSON
                          v
+-------------------------------------------------------------+
|          REST API Router Layer (Django Ninja)               |
|  - Request Validation (Pydantic Schemas)                    |
|  - URL Routing & Serialization                              |
|  - Auto-generated Interactive OpenAPI Docs                  |
+-------------------------------------------------------------+
                          |
                    Validated Data
                          v
+-------------------------------------------------------------+
|          Backend Application Layer (Django Framework)       |
|  - Business Logic & Filtering Engine                        |
|  - Database Abstraction via Django ORM                      |
|  - Query Optimization (prefetch_related)                    |
+-------------------------------------------------------------+
                          |
                      SQL Queries
                          v
+-------------------------------------------------------------+
|                 Database Layer (SQLite)                     |
|  - Relational Schema (Courses & Lessons Tables)             |
|  - Foreign Key Constraints & Data Integrity                 |
+-------------------------------------------------------------+
```

### B. Hubungan Resource & Fungsi Komponen

- **Relasi Antar Entitas:** Hubungan One-to-Many (`1 Course -> Many Lessons`). Satu Course dapat memiliki banyak Lesson terurut (`order`), dan penghapusan Course akan menerapkan `CASCADE` ke seluruh Lesson terkait.
- **Client Layer:** Mengirim HTTP requests (GET, POST, PATCH, DELETE) dengan payload terstruktur.
- **Django Ninja (API Router):** Melakukan parsing request, validasi schema via Pydantic (`CourseIn`, `CourseUpdate`), otentikasi/status handling, dan serialisasi respon (`CourseOut`, `CourseWithLessonsOut`).
- **Django ORM (Application Layer):** Mengelola transaksi data, agregasi (`Count`), pencarian teks, dan memetakan model Python ke query relasional SQL.
- **Database (Storage Layer):** Menyimpan entitas secara persisten dan menjamin integritas data (uniqueness constraint pada `code`).

---

## 2. Environment & Repository Structure (Soal 2)

### Informasi Environment

- **Python:** 3.14.7
- **Virtual Environment:** `.venv`
- **Git Version:** 2.55.0
- **Docker Engine / Compose:** WSL 2 Backend
- **Framework Utama:** Django 6.1, Django Ninja

### Struktur Direktori Project

```text
uts-pss-sa/
├── config/
│   ├── __init__.py
│   ├── api.py              # Inisialisasi NinjaAPI & Router Mounting
│   ├── asgi.py
│   ├── settings.py         # Django Settings & INSTALLED_APPS
│   ├── urls.py             # Root URL Patterns
│   └── wsgi.py
├── courses/
│   ├── management/
│   │   └── commands/
│   │       └── seed_uts_data.py   # Seeder 25 Courses & 125 Lessons
│   ├── migrations/
│   ├── api.py               # REST API Endpoint Logic & Router
│   ├── benchmark_query.py   # Script Uji N+1 Query Optimization
│   ├── models.py            # Relational Models (Course & Lesson)
│   ├── schemas.py           # Pydantic Schemas Input & Output
│   └── tests.py             # Automated API Unit Tests
├── .dockerignore
├── .gitignore
├── compose.yaml              # Docker Compose Configuration
├── Dockerfile                # Multi-stage Containerization
├── manage.py
├── requirements.txt
└── README.md
```

---

## 3. Docker Containerization & Analisis (Soal 3)

### A. Panduan Menjalankan Container

**Build dan jalankan container:**

```bash
docker compose up -d --build
```

**Eksekusi migrasi & data seeder di dalam container:**

```bash
docker compose exec web python manage.py migrate
docker compose exec web python manage.py seed_uts_data
```

**Menghentikan container:**

```bash
docker compose down
```

### B. Analisis Docker Containerization

**Pertanyaan:** Mengapa aplikasi yang berjalan normal menggunakan `python manage.py runserver` belum tentu langsung berjalan ketika dipindahkan ke container?

**Jawaban:**

1. **Host IP Binding (0.0.0.0 vs 127.0.0.1):** Secara lokal, `runserver` mengikat alamat `127.0.0.1` (loopback) yang hanya bisa diakses dari internal host. Di dalam container Docker, server harus mengikat `0.0.0.0` agar port yang diexpose dapat dijangkau oleh mesin host di luar container.
2. **Environment & Dependency Isolation:** Mesin lokal memiliki package global dan cache interpreter yang mungkin tidak tertulis di `requirements.txt`. Ketika berpindah ke container Linux minimal (slim image), missing dependency atau perbedaan arsitektur OS dapat memicu runtime failure.
3. **Volume Mapping & I/O File Permissions:** Berkas database SQLite atau direktori static files memerlukan hak akses baca/tulis yang tepat antara user container dan sistem file OS host.

---

## 4. Django Models & ORM Validation (Soal 4)

### Ringkasan Skema Model

- **Course Model:** `id` (PK), `code` (CharField, Unique), `title` (CharField), `description` (TextField), `is_active` (BooleanField, default=True).
- **Lesson Model:** `id` (PK), `course` (FK ke Course via `related_name="lessons"`), `title` (CharField), `content` (TextField), `order` (PositiveIntegerField).

### Bukti Validasi Django ORM via Shell

Berdasarkan pengujian pada dataset (25 Courses dan 125 Lessons):

| Query ORM | Hasil |
|---|---|
| `Course.objects.filter(is_active=True).count()` | 19 Course aktif |
| `Course.objects.filter(title__icontains="Backend").count()` | 25 record ditemukan |
| `Lesson.objects.filter(course=c1)` | 5 Materi terdaftar pada CRS001 |
| `Course.objects.annotate(total_lessons=Count("lessons"))` | Berhasil mengagregasi 5 lessons per course |

---

## 5. Query Analysis & Optimization (Soal 5)

### A. Hasil Uji Benchmark Script (`benchmark_query.py`)

| Versi Endpoint / Pendekatan | Teknik Eksekusi | Total SQL Queries Dijalankan | Efisiensi |
|---|---|---|---|
| Versi A (Before / Unoptimized) | Standard Lazy Loading QuerySet | 26 Queries (1 + 25) | Baseline (N+1 Issue) |
| Versi B (After / Optimized) | `prefetch_related("lessons")` | 2 Queries (1 Course + 1 Lesson) | ~92,3% Reduksi Query |

### B. Analisis Masalah N+1 Query

**Pertanyaan:** Mengapa N+1 query dapat menjadi masalah serius ketika jumlah data bertambah besar?

**Jawaban:**

Problem N+1 terjadi ketika backend melakukan 1 query awal untuk mengambil N data induk, kemudian mengeksekusi N kali query tambahan ke database untuk mengambil data relasi anak saat proses iterasi/serialisasi JSON. Jika terdapat 10.000 records, aplikasi akan mengeksekusi 10.001 query SQL round-trip ke database engine. Hal ini menimbulkan latensi jaringan kumulatif, menguras connection pool database, meningkatkan beban CPU server, dan menyebabkan bottleneck response time secara signifikan. Optimasi `prefetch_related()` menyelesaikan masalah ini secara deterministik dengan hanya mengeksekusi 2 query SQL terlepas dari berapapun jumlah datanya.

---

## 6. Dokumentasi REST API Django Ninja (Soal 6)

Interactive OpenAPI / Swagger Documentation dapat diakses pada alamat:

- **Swagger UI:** `http://localhost:8000/api/docs`
- **OpenAPI Schema JSON:** `http://localhost:8000/api/openapi.json`

### Daftar Endpoint API

| Method | URL Path | Status Response | Deskripsi & Parameter |
|---|---|---|---|
| GET | `/api/courses/` | 200 OK | Mengambil list courses dengan query param `search`, `active`, dan pagination (`limit`, `offset`). |
| POST | `/api/courses/` | 201 Created, 400 Bad Request, 422 Unprocessable | Menambahkan course baru dengan validasi schema Pydantic. |
| GET | `/api/courses/{course_id}` | 200 OK, 404 Not Found | Mengambil detail spesifik course berdasarkan ID. |
| PATCH | `/api/courses/{course_id}` | 200 OK, 404 Not Found | Memperbarui sebagian atribut course (`title`, `description`, `is_active`). |
| DELETE | `/api/courses/{course_id}` | 204 No Content, 404 Not Found | Menghapus record course secara permanen dari database. |
| GET | `/api/courses/courses-unoptimized` | 200 OK | Endpoint demonstrasi data course + lessons (Versi A - N+1 Query). |
| GET | `/api/courses/courses-optimized` | 200 OK | Endpoint demonstrasi data course + lessons (Versi B - prefetch_related). |

---

## 7. API Testing & Analisis (Soal 7)

### A. Menjalankan Automated Tests

Jalankan perintah unit testing Django berikut:

```bash
python manage.py test courses
```

**Hasil:** `Ran 4 tests in 0.067s - OK` (Semua test berhasil dilewati).

### B. Analisis Automated Testing

**Pertanyaan:** Jika endpoint berhasil ketika dicoba melalui Swagger, mengapa automated testing masih diperlukan?

**Jawaban:**

1. **Pencegahan Regresi Kode (Regression Prevention):** Pengujian manual via Swagger hanya memvalidasi fungsionalitas saat itu. Automated testing memastikan bahwa penambahan fitur atau refactoring logic di kemudian hari tidak merusak fungsi yang sudah ada.
2. **Efisiensi Pengujian Kompleks (Edge Cases):** Menguji ratusan skenario validasi, status error (400, 404, 422), dan payload abnormal secara manual sangat lambat serta rentan kelalaian manusia (human error). Automated test dapat memverifikasi seluruh skenario dalam hitungan milidetik.
3. **Standar Integrasi CI/CD:** Automated test dapat diotomatisasi dalam pipeline Continuous Integration (seperti GitHub Actions) untuk mencegah bug lolos ke lingkungan production.

---

## Referensi & Catatan AI

- **Dokumentasi Resmi:** Django Framework Documentation, Django Ninja & Pydantic Documentation.
- **Penggunaan AI:** Google Gemini digunakan sebagai asisten dalam mendesain arsitektur schema, benchmark N+1 query analysis context, dan penyusunan struktur automated testing. Seluruh kode telah dipahami, divalidasi, dan diuji secara independen.