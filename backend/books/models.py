from django.db import models
from django.conf import settings

class Book(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    topic = models.CharField(max_length=255, null=True, blank=True)
    grade_level = models.IntegerField(null=True, blank=True)
    lexile = models.IntegerField(null=True, blank=True)
    category = models.CharField(max_length=128, null=True, blank=True)
    child = models.ForeignKey('quizzes.Child', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class BookPage(models.Model):
    book = models.ForeignKey(Book, related_name='pages', on_delete=models.CASCADE)
    text = models.TextField()
    image = models.ImageField(upload_to='book_images/', null=True, blank=True)
    order = models.PositiveIntegerField()

class BookQuiz(models.Model):
    book = models.OneToOneField(Book, related_name='quiz', on_delete=models.CASCADE)
    created_for_child = models.ForeignKey('quizzes.Child', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class BookQuizQuestion(models.Model):
    quiz = models.ForeignKey(BookQuiz, related_name='questions', on_delete=models.CASCADE)
    question = models.TextField()
    type = models.CharField(max_length=32, choices=(('multiple_choice','Multiple Choice'),('true_false','True/False')))
    options = models.JSONField(default=list, blank=True)
    answer = models.CharField(max_length=255)
    explanation = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=1)

class BookQuizAttempt(models.Model):
    quiz = models.ForeignKey(BookQuiz, on_delete=models.CASCADE)
    child = models.ForeignKey('quizzes.Child', on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    passed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

class BookQuizAttemptAnswer(models.Model):
    attempt = models.ForeignKey(BookQuizAttempt, related_name='answers', on_delete=models.CASCADE)
    question = models.ForeignKey(BookQuizQuestion, on_delete=models.CASCADE)
    answer = models.CharField(max_length=255)
    is_correct = models.BooleanField()
