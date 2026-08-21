from django.db import models

class CourseQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)

    def search(self, keyword):
        return self.filter(title__icontains=keyword)


class Course(models.Model):
    code = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    objects = CourseQuerySet.as_manager()

    def __str__(self):
        return f"{self.code} {self.title}"


class Lesson(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="lessons",
    )
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.title


class Student(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name


class Enrollment(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="enrollments",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="enrollments",
    )
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["student", "course"],
                name="unique_student_course_enrollment",
            )
        ]