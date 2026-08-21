from django.contrib import admin
from .models import Category, Book, Member, Borrowing

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "isbn", "category", "is_available")
    search_fields = ("title", "isbn", "author")
    list_filter = ("is_available", "category")

admin.site.register(Category)
admin.site.register(Member)
admin.site.register(Borrowing)