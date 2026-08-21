from django.test import TestCase
from django.db.utils import IntegrityError
from catalog.models import Course

class CourseModelTest(TestCase):
    def test_course_code_must_be_unique(self):
        Course.objects.create(code="PSS01", title="Backend")
        with self.assertRaises(IntegrityError):
            Course.objects.create(code="PSS01", title="Duplicate")