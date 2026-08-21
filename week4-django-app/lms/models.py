from django.db import models
from django.conf import settings

class CourseQuerySet(models.QuerySet):
    def active(self):
        return self.filter(status="PUBLISHED")


class LMSCourse(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        PUBLISHED = "PUBLISHED", "Published"
        ARCHIVED = "ARCHIVED", "Archived"

    code = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    lecturer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="teaching_courses",
        limit_choices_to={"role": "LECTURER"},
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    objects = CourseQuerySet.as_manager()

    class Meta:
        verbose_name = "LMS Course"
        verbose_name_plural = "LMS Courses"

    def __str__(self):
        return f"{self.code} - {self.title}"


class Enrollment(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="course_enrollments",
        limit_choices_to={"role": "STUDENT"},
    )
    course = models.ForeignKey(
        LMSCourse,
        on_delete=models.CASCADE,
        related_name="enrollments",
    )
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["student", "course"],
                name="unique_lms_student_course_enrollment",
            )
        ]

    def __str__(self):
        return f"{self.student.username} -> {self.course.code}"


class Lesson(models.Model):
    course = models.ForeignKey(
        LMSCourse,
        on_delete=models.CASCADE,
        related_name="lessons",
    )
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.course.code} - Lesson {self.order}: {self.title}"


class Assignment(models.Model):
    course = models.ForeignKey(
        LMSCourse,
        on_delete=models.CASCADE,
        related_name="assignments",
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    deadline = models.DateTimeField()

    def __str__(self):
        return f"{self.course.code} - Assignment: {self.title}"


class Submission(models.Model):
    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name="submissions",
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="submissions",
        limit_choices_to={"role": "STUDENT"},
    )
    content = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    grade = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["assignment", "student"],
                name="unique_student_assignment_submission",
            )
        ]

    def __str__(self):
        return f"Submission by {self.student.username} on {self.assignment.title}"