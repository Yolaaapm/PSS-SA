from django.test import TestCase
from ninja.testing import TestClient
from config.api import api
from courses.models import Course

client = TestClient(api)

class CourseAPITests(TestCase):
    def setUp(self):
        self.course = Course.objects.create(
            code="UTS01",
            title="Django Ninja Core",
            description="Testing API",
            is_active=True
        )

    # 1. Happy-path GET
    def test_get_course_detail_success(self):
        response = client.get(f"/courses/{self.course.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["code"], "UTS01")

    # 2. Happy-path POST
    def test_create_course_success(self):
        response = client.post(
            "/courses/",
            json={"code": "UTS02", "title": "Advanced Web Service", "description": "Desc"}
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["code"], "UTS02")

    # 3. Invalid Input (Code < 3 karakter -> 422 Unprocessable Entity)
    def test_create_course_invalid_code_returns_422(self):
        response = client.post(
            "/courses/",
            json={"code": "AB", "title": "Short Code"}
        )
        self.assertEqual(response.status_code, 422)

    # 4. Resource Not Found (404)
    def test_get_course_not_found_returns_404(self):
        response = client.get("/courses/99999")
        self.assertEqual(response.status_code, 404)