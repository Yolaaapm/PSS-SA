from typing import Optional
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from ninja import Router
from ninja.pagination import paginate
from .models import Course, Lesson
from .schemas import CourseIn, CourseOut, CourseUpdate, CourseWithLessonsOut

router = Router(tags=["Courses"])

# SOAL 5: QUERY OPTIMIZATION BENCHMARK
# Versi A: QuerySet Biasa (N+1 Query Issue)
@router.get("/courses-unoptimized", response=list[CourseWithLessonsOut])
def list_courses_unoptimized(request):
    courses = list(Course.objects.all())
    return courses

# Versi B: Optimized Query (prefetch_related)
@router.get("/courses-optimized", response=list[CourseWithLessonsOut])
def list_courses_optimized(request):
    courses = list(Course.objects.prefetch_related("lessons").all())
    return courses


# SOAL 6: CRUD COURSE REST API
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

@router.get("/{course_id}", response=CourseOut)
def get_course(request, course_id: int):
    return get_object_or_404(Course, id=course_id)

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

@router.patch("/{course_id}", response=CourseOut)
def update_course(request, course_id: int, payload: CourseUpdate):
    course = get_object_or_404(Course, id=course_id)
    data = payload.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(course, field, value)
    course.save()
    return course

@router.delete("/{course_id}", response={204: None})
def delete_course(request, course_id: int):
    course = get_object_or_404(Course, id=course_id)
    course.delete()
    return 204, None