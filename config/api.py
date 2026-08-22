from ninja import NinjaAPI
from courses.api import router as courses_router

api = NinjaAPI(title="Mini Course Management API", version="1.0")
api.add_router("/courses/", courses_router)