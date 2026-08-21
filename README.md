# Week 1 Backend Practice - Pemrograman Sisi Server

## Identitas Mahasiswa
- **Nama:** Fiola Putri Monika
- **NIM:** A11.2023.15413
- **Kelompok/Kelas:** Pemrograman Sisi Server-Semester Antara (A11.64707)

---

## Informasi Environment
- **Python:** 3.14.7
- **Virtual Environment:** `.venv`
- **Git:** 2.55.0
- **IDE:** Visual Studio Code
- **Docker Desktop:** Status Pending 

### Ringkasan
- Menyiapkan environment pengembangan backend (Python, Virtualenv, Git, VS Code).
- Membuat HTTP Server sederhana dari nol menggunakan pustaka bawaan Python `http.server`[cite: 1].
- Mengimplementasikan routing dasar, pengembalian respon berformat JSON, serta penanganan status code HTTP (200 OK & 404 Not Found)[cite: 1].

## Cara Menjalankan Project

1. **Aktifkan Virtual Environment:**
   ```cmd
   .venv\Scripts\activate.bat

## Week 2: Architectural Patterns & Refactoring Modular Monolith

## Ringkasan
- Menganalisis pola arsitektur backend (Monolithic, Microservices, Event-Driven, Serverless).  
- Menerapkan pola Modular Monolith sebagai arsitektur baseline Simple LMS Backend.  
- Melakukan refactoring kode dari satu file server.py menjadi struktur terisolasi per domain di dalam folder modules/ (courses.py, students.py, assignments.py, enrollments.py).  
- Merancang Module Boundary dan Entity Relationship Diagram (ERD) awal Simple LMS.  

## Cara Menjalankan Project

1. **Aktifkan Virtual Environment:**
   ```cmd
   .venv\Scripts\activate.bat
   python server.py

## Week 3: Docker Containerization & Multi-Container Setup

## Ringkasan Kegiatan
- Pemahaman konsep dasar kontainerisasi (Image, Container, Dockerfile, Volume, dan Network).
- Pembuatan custom Docker image menggunakan base image python:3.12-slim.
- Penyusunan konfigurasi compose.yaml untuk mengorkestrasi multi-container (Aplikasi Python Backend & Database PostgreSQL 17).
- Penerapan Persistent Volume (postgres_data) agar data PostgreSQL tetap tersimpan saat container di-restart.
- Pengelolaan konfigurasi environment variable secara aman menggunakan file .env dan .env.example.

## Cara Menjalankan Stack (Week 3)
## (Dijalankan setelah Docker Desktop aktif)

1. **Jalankan Multi-Container Stack:**
    ```cmd
    docker compose up --build -d

2. **Cek Status Container:**
    ```cmd
    docker compose ps

3. **Uji Endpoint Health Check Database:**
    ```cmd
    http://localhost:8000/health

4. **Hentikan Stack:**
    ```cmd
    docker compose down

# Modul 4: Django Models & ORM (Week 4)

## Fitur & Implementasi
- **Guided Labs (Catalog & Users App)**:
  - Implementasi model `Course`, `Lesson`, `Student`, dan intermediate model `Enrollment`.
  - Custom `User` model dengan role-based authentication (`ADMIN`, `LECTURER`, `STUDENT`).
  - Custom QuerySet & Manager (`active()`, `search()`).
  - Django Admin configuration & Management Command (`seed_demo`).
- **Mini Challenge (Library Domain)**:
  - Model `Category`, `Book`, `Member`, dan `Borrowing`.
  - ISBN uniqueness constraint & Custom QuerySet `.available()`.
- **Capstone Milestone 4 (Core LMS Models)**:
  - Model `LMSCourse`, `Lesson`, `Enrollment`, `Assignment`, dan `Submission`.
  - Unique constraints pada relasi enrollment dan submission.
  - Automated Unit Tests (5/5 tests passed).

## Menjalankan Unit Tests
```cmd
python manage.py test