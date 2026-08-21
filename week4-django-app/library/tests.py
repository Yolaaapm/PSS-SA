from django.test import TestCase
from django.db.utils import IntegrityError
from library.models import Category, Book

class LibraryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Computer Science")

    def test_isbn_must_be_unique(self):
        Book.objects.create(
            isbn="978-602-001",
            title="Python Advanced",
            category=self.category,
            author="John Doe"
        )
        with self.assertRaises(IntegrityError):
            Book.objects.create(
                isbn="978-602-001",
                title="Duplicate ISBN Book",
                category=self.category,
                author="Jane Doe"
            )

    def test_book_available_queryset(self):
        Book.objects.create(
            isbn="978-001",
            title="Book Available",
            category=self.category,
            is_available=True
        )
        Book.objects.create(
            isbn="978-002",
            title="Book Borrowed",
            category=self.category,
            is_available=False
        )
        available_books = Book.objects.available()
        self.assertEqual(available_books.count(), 1)
        self.assertEqual(available_books.first().isbn, "978-001")