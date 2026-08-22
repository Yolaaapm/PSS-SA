import os
import sys
from pathlib import Path

# Menambahkan root project ke sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django
django.setup()

from django.test.utils import CaptureQueriesContext
from django.db import connection
from courses.models import Course

def run_benchmark():
    # Versi A: Tanpa Optimasi (N+1 Problem)
    with CaptureQueriesContext(connection) as ctx_a:
        courses_a = list(Course.objects.all())
        for c in courses_a:
            _ = list(c.lessons.all())
    queries_a = len(ctx_a)

    # Versi B: Dengan Optimasi prefetch_related
    with CaptureQueriesContext(connection) as ctx_b:
        courses_b = list(Course.objects.prefetch_related("lessons").all())
        for c in courses_b:
            _ = list(c.lessons.all())
    queries_b = len(ctx_b)

    print("=== HASIL ANALISIS QUERY ===")
    print(f"Versi A (Before / Tanpa Optimasi): {queries_a} Queries")
    print(f"Versi B (After / prefetch_related): {queries_b} Queries")

if __name__ == "__main__":
    run_benchmark()