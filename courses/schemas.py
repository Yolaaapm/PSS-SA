from typing import Optional
from ninja import Schema
from pydantic import field_validator

class LessonOut(Schema):
    id: int
    course_id: int
    title: str
    content: str
    order: int

class CourseOut(Schema):
    id: int
    code: str
    title: str
    description: str
    is_active: bool

class CourseWithLessonsOut(Schema):
    id: int
    code: str
    title: str
    description: str
    is_active: bool
    lessons: list[LessonOut]

class CourseIn(Schema):
    code: str
    title: str
    description: str = ""

    @field_validator("code")
    @classmethod
    def validate_code(cls, value: str):
        val = value.strip().upper()
        if len(val) < 3:
            raise ValueError("Code minimal 3 karakter")
        return val

class CourseUpdate(Schema):
    title: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None