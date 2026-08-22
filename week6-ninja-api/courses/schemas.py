from typing import Optional
from ninja import Schema
from pydantic import field_validator

class CourseOut(Schema):
    id: int
    code: str
    title: str
    description: str
    is_active: bool

class CourseIn(Schema):
    code: str
    title: str
    description: str = ""

    @field_validator("code")
    @classmethod
    def validate_code(cls, value: str):
        value = value.strip().upper()
        if len(value) < 3:
            raise ValueError("Course code minimal 3 karakter")
        return value

class CourseUpdate(Schema):
    title: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

class LessonIn(Schema):
    course_id: int
    title: str
    content: str = ""
    order: int = 1

class LessonUpdate(Schema):
    title: Optional[str] = None
    content: Optional[str] = None
    order: Optional[int] = None

class LessonOut(Schema):
    id: int
    course_id: int
    title: str
    content: str
    order: int