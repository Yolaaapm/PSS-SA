# Arsitektur Sistem - Simple LMS Backend (Week 2)

**Nama:** Fiola Putri Monika  
**NIM:** A11.2023.15413  

---

## 1. Pilihan Arsitektur: Modular Monolith
Aplikasi menggunakan pola **Modular Monolith** sebagai baseline. Alasan memilih pola ini adalah operasional yang lebih sederhana untuk tim, tidak memerlukan overhead jaringan antar-service seperti pada Microservices, serta kode tetap terstruktur rapi berdasarkan pemisahan modul.

---

## 2. Diagram Alur Sistem
```text
+-------------------+
| Browser / Client  |
+---------+---------+
          | HTTP Request
          v
+---------------------------------------------------+
|                  Python Backend                   |
|                                                   |
|  [Courses]    [Students]   [Assignments]          |
|              [Enrollments]                        |
+---------------------------------------------------+