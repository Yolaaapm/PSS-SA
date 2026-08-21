from django.contrib import admin
from .models import Course, Lesson, Student, Enrollment

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("code", "title", "is_active")
    search_fields = ("code", "title")
    list_filter = ("is_active",)

admin.site.register(Lesson)
admin.site.register(Student)
admin.site.register(Enrollment)