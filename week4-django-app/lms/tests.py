from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from lms.models import LMSCourse, Enrollment, Assignment, Submission

User = get_user_model()

class LMSModelTest(TestCase):
    def setUp(self):
        self.lecturer = User.objects.create_user(
            username="dosen1",
            password="Password123!",
            role=User.Role.LECTURER
        )
        self.student = User.objects.create_user(
            username="mhs1",
            password="Password123!",
            role=User.Role.STUDENT
        )
        self.course = LMSCourse.objects.create(
            code="CS101",
            title="Intro to Computer Science",
            lecturer=self.lecturer,
            status=LMSCourse.Status.PUBLISHED
        )

    def test_unique_enrollment_constraint(self):
        Enrollment.objects.create(student=self.student, course=self.course)
        with self.assertRaises(IntegrityError):
            Enrollment.objects.create(student=self.student, course=self.course)

    def test_unique_submission_constraint(self):
        assignment = Assignment.objects.create(
            course=self.course,
            title="Tugas 1",
            deadline=timezone.now() + timezone.timedelta(days=7)
        )
        Submission.objects.create(
            assignment=assignment,
            student=self.student,
            content="Link Github Repo"
        )
        with self.assertRaises(IntegrityError):
            Submission.objects.create(
                assignment=assignment,
                student=self.student,
                content="Duplikat Submission"
            )