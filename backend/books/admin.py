from django.contrib import admin
from .models import Book, BookPage, BookQuiz, BookQuizQuestion, BookQuizAttempt, BookQuizAttemptAnswer

class BookPageInline(admin.TabularInline):
    model = BookPage
    extra = 0

class BookQuizInline(admin.StackedInline):
    model = BookQuiz
    extra = 0

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "topic", "grade_level", "lexile", "category", "child", "created_at")
    search_fields = ("title", "topic", "child__name")
    list_filter = ("grade_level", "lexile", "category", "created_at")
    inlines = [BookPageInline, BookQuizInline]

@admin.register(BookPage)
class BookPageAdmin(admin.ModelAdmin):
    list_display = ("id", "book", "order", "text", "image")
    search_fields = ("book__title", "text")
    list_filter = ("book",)

class BookQuizQuestionInline(admin.TabularInline):
    model = BookQuizQuestion
    extra = 0

@admin.register(BookQuiz)
class BookQuizAdmin(admin.ModelAdmin):
    list_display = ("id", "book", "created_for_child", "created_at")
    search_fields = ("book__title", "created_for_child__name")
    inlines = [BookQuizQuestionInline]

@admin.register(BookQuizQuestion)
class BookQuizQuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "quiz", "question", "type", "order")
    search_fields = ("question", "quiz__book__title")
    list_filter = ("type",)

@admin.register(BookQuizAttempt)
class BookQuizAttemptAdmin(admin.ModelAdmin):
    list_display = ("id", "quiz", "child", "score", "passed", "created_at", "completed_at")
    search_fields = ("quiz__book__title", "child__name")
    list_filter = ("passed", "created_at")

@admin.register(BookQuizAttemptAnswer)
class BookQuizAttemptAnswerAdmin(admin.ModelAdmin):
    list_display = ("id", "attempt", "question", "answer", "is_correct")
    search_fields = ("attempt__quiz__book__title", "question__question", "answer")
    list_filter = ("is_correct",)
