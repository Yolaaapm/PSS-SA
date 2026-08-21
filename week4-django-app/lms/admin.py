from django.contrib import admin
from .models import LMSCourse, Enrollment, Lesson, Assignment, Submission

@admin.register(LMSCourse)
class LMSCourseAdmin(admin.ModelAdmin):
    list_display = ("code", "title", "lecturer", "status")
    search_fields = ("code", "title")
    list_filter = ("status",)

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "deadline")
    list_filter = ("course",)

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("assignment", "student", "submitted_at", "grade")
    list_filter = ("assignment__course",)

admin.site.register(Enrollment)
admin.site.register(Lesson)