from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from catalog.models import Course, Lesson

class Command(BaseCommand):
    help = "Generate large dataset for performance benchmarking"

    def handle(self, *args, **options):
        self.stdout.write("Generating performance dataset...")

        # 1. Buat Dosen / Lecturer
        lecturer, _ = User.objects.get_or_create(
            username="dosen_demo",
            defaults={"first_name": "Pak", "last_name": "Dosen"}
        )

        # 2. Bulk create 10.000 Course
        courses_batch = [
            Course(
                code=f"CRS{i:05d}",
                title=f"Course {i}",
                lecturer=lecturer,
                is_active=(i % 5 != 0)
            )
            for i in range(1, 10001)
        ]
        Course.objects.bulk_create(courses_batch, batch_size=1000)
        self.stdout.write(self.style.SUCCESS("10,000 courses created successfully."))

        # 3. Bulk create Lesson untuk 100 course pertama (untuk testing reverse FK)
        first_100_courses = Course.objects.all()[:100]
        lessons_batch = []
        for course in first_100_courses:
            for order in range(1, 4):  # 3 lesson per course
                lessons_batch.append(
                    Lesson(
                        course=course,
                        title=f"Lesson {order} of {course.code}",
                        order=order
                    )
                )
        Lesson.objects.bulk_create(lessons_batch, batch_size=500)
        self.stdout.write(self.style.SUCCESS("Demo lessons created successfully."))