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