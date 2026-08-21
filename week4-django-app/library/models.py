from django.db import models

class BookQuerySet(models.QuerySet):
    def available(self):
        return self.filter(is_available=True)


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Book(models.Model):
    isbn = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=200)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="books",
    )
    author = models.CharField(max_length=150)
    is_available = models.BooleanField(default=True)

    objects = BookQuerySet.as_manager()

    def __str__(self):
        return f"{self.title} ({self.isbn})"


class Member(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Borrowing(models.Model):
    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name="borrowings",
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="borrowings",
    )
    borrowed_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()
    is_returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.member.name} borrowed {self.book.title}"