from django.test import TestCase
from ninja.testing import TestClient
from config.api import api
from courses.models import Course, Lesson

client = TestClient(api)

class CourseApiTest(TestCase):
    def setUp(self):
        self.course = Course.objects.create(
            code="API01",
            title="REST API Initial",
            description="Init description",
            is_active=True
        )

    def test_create_course_success(self):
        response = client.post(
            "/courses/",
            json={
                "code": "API02",
                "title": "REST API Development",
                "description": "Practice",
            },
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["code"], "API02")

    def test_create_course_duplicate_code_returns_400(self):
        response = client.post(
            "/courses/",
            json={
                "code": "API01",
                "title": "Duplicate API",
                "description": "Duplicate",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("already exists", response.json()["detail"])

    def test_get_course_detail_success(self):
        response = client.get(f"/courses/{self.course.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["code"], "API01")

    def test_get_course_not_found_returns_404(self):
        response = client.get("/courses/99999")
        self.assertEqual(response.status_code, 404)

    def test_patch_course_partial_update(self):
        response = client.patch(
            f"/courses/{self.course.id}",
            json={"title": "Updated Title Only"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], "Updated Title Only")

    def test_delete_course_returns_204(self):
        response = client.delete(f"/courses/{self.course.id}")
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Course.objects.filter(id=self.course.id).exists())


class LessonApiTest(TestCase):
    def setUp(self):
        self.course = Course.objects.create(
            code="API03",
            title="Django Testing Course",
            description="Testing lesson relationship"
        )
        self.lesson = Lesson.objects.create(
            course=self.course,
            title="Lesson 1: Intro",
            content="Content of lesson 1",
            order=1
        )

    def test_create_lesson_success(self):
        response = client.post(
            "/courses/lessons/",
            json={
                "course_id": self.course.id,
                "title": "Lesson 2: Advanced",
                "content": "Content of lesson 2",
                "order": 2
            }
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["title"], "Lesson 2: Advanced")

    def test_create_lesson_invalid_course_returns_404(self):
        response = client.post(
            "/courses/lessons/",
            json={
                "course_id": 9999,
                "title": "Invalid Lesson",
                "content": "No parent course",
                "order": 1
            }
        )
        self.assertEqual(response.status_code, 404)

    def test_get_lessons_filter_by_course(self):
        response = client.get(f"/courses/lessons/?course_id={self.course.id}")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json()["items"]) >= 1)

    def test_delete_lesson_returns_204(self):
        response = client.delete(f"/courses/lessons/{self.lesson.id}")
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Lesson.objects.filter(id=self.lesson.id).exists())