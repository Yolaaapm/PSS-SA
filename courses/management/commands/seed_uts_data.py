from django.core.management.base import BaseCommand
from courses.models import Course, Lesson

class Command(BaseCommand):
    help = "Seed minimal 20 Courses dan 100 Lessons untuk UTS"

    def handle(self, *args, **kwargs):
        Lesson.objects.all().delete()
        Course.objects.all().delete()

        courses_to_create = []
        for i in range(1, 26):
            courses_to_create.append(
                Course(
                    code=f"CRS{i:03d}",
                    title=f"Pemrograman Web & Backend Tingkat {i}",
                    description=f"Deskripsi materi komprehensif untuk course modul ke-{i}",
                    is_active=True if i % 4 != 0 else False
                )
            )
        created_courses = Course.objects.bulk_create(courses_to_create)

        lessons_to_create = []
        for course in created_courses:
            for l_num in range(1, 6):
                lessons_to_create.append(
                    Lesson(
                        course=course,
                        title=f"Materi {l_num}: Sub-topik Bahasan Modul {course.code}",
                        content=f"Konten detail perkuliahan sub-topik {l_num}",
                        order=l_num
                    )
                )
        Lesson.objects.bulk_create(lessons_to_create)

        self.stdout.write(self.style.SUCCESS(
            f"Seeding berhasil: {Course.objects.count()} Courses & {Lesson.objects.count()} Lessons telah dibuat."
        ))