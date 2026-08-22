from typing import Optional
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from ninja import Router
from ninja.pagination import paginate
from .models import Course, Lesson
from .schemas import (
    CourseIn, CourseOut, CourseUpdate,
    LessonIn, LessonOut, LessonUpdate
)

router = Router(tags=["Courses"])

@router.get("/hello")
def hello(request):
    return {"message": "Hello REST API"}

# GET Collection dengan Search, Filter & Pagination (Bagian 8, 15, 16)
@router.get("/", response=list[CourseOut])
@paginate
def list_courses(
    request,
    search: Optional[str] = None,
    active: Optional[bool] = None,
):
    qs = Course.objects.all()
    if search:
        qs = qs.filter(title__icontains=search)
    if active is not None:
        qs = qs.filter(is_active=active)
    return qs.order_by("id")

# GET Detail & 404 Handling (Bagian 9)
@router.get("/{course_id}", response=CourseOut)
def get_course(request, course_id: int):
    return get_object_or_404(Course, id=course_id)

# POST & Duplicate Code Error 400 (Bagian 10, 11, 12)
@router.post("/", response={201: CourseOut, 400: dict})
def create_course(request, payload: CourseIn):
    try:
        course = Course.objects.create(
            code=payload.code,
            title=payload.title,
            description=payload.description,
        )
        return 201, course
    except IntegrityError:
        return 400, {"detail": "Course code already exists"}

# PATCH / Partial Update (Bagian 13)
@router.patch("/{course_id}", response=CourseOut)
def update_course(request, course_id: int, payload: CourseUpdate):
    course = get_object_or_404(Course, id=course_id)
    data = payload.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(course, field, value)
    course.save()
    return course

# DELETE / 204 No Content (Bagian 14)
@router.delete("/{course_id}", response={204: None})
def delete_course(request, course_id: int):
    course = get_object_or_404(Course, id=course_id)
    course.delete()
    return 204, None

@router.get("/lessons/", response=list[LessonOut])

@paginate
def list_lessons(request, course_id: Optional[int] = None):
    qs = Lesson.objects.select_related("course").all()
    if course_id:
        qs = qs.filter(course_id=course_id)
    return qs.order_by("order")

@router.get("/lessons/{lesson_id}", response=LessonOut)
def get_lesson(request, lesson_id: int):
    return get_object_or_404(Lesson, id=lesson_id)

@router.post("/lessons/", response={201: LessonOut, 404: dict})
def create_lesson(request, payload: LessonIn):
    course = Course.objects.filter(id=payload.course_id).first()
    if not course:
        return 404, {"detail": "Course not found"}
    lesson = Lesson.objects.create(
        course=course,
        title=payload.title,
        content=payload.content,
        order=payload.order,
    )
    return 201, lesson

@router.patch("/lessons/{lesson_id}", response=LessonOut)
def update_lesson(request, lesson_id: int, payload: LessonUpdate):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    data = payload.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(lesson, field, value)
    lesson.save()
    return lesson

@router.delete("/lessons/{lesson_id}", response={204: None})
def delete_lesson(request, lesson_id: int):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    lesson.delete()
    return 204, None