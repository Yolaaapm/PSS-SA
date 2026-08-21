from django.core.management.base import BaseCommand
from catalog.models import Course

class Command(BaseCommand):
    help = "Seed initial demo data for catalog app"

    def handle(self, *args, **options):
        course, created = Course.objects.get_or_create(
            code="PSS01",
            defaults={
                "title": "Pemrograman Sisi Server",
                "description": "Backend development using Django",
            },
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"Created course: {course.code}"))
        else:
            self.stdout.write(self.style.WARNING(f"Course {course.code} already exists"))

        self.stdout.write(self.style.SUCCESS("Demo data ready"))