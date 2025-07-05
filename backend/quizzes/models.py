from django.db import models
from lessons.models import LessonText
from users.models import User


class Quiz(models.Model):
    lesson = models.ForeignKey(LessonText, on_delete=models.CASCADE)
    link_slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField()
    type = models.CharField(choices=[('mcq', 'MCQ'), ('tf', 'True/False')], max_length=3)
    options = models.JSONField()
    answer = models.CharField(max_length=100)

class Child(models.Model):
    GRADE_CHOICES = [
        ('K', 'Kinder'),
        ('1', 'Grade 1'),
        ('2', 'Grade 2'),
        ('3', 'Grade 3'),
        ('4', 'Grade 4'),
        ('5', 'Grade 5'),
        ('6', 'Grade 6'),
    ]
    parent = models.ForeignKey('users.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField(null=True, blank=True)
    grade_level = models.CharField(max_length=2, choices=GRADE_CHOICES, default='3')
    tokens = models.IntegerField(default=0)
    avatar = models.CharField(default="default.png", max_length=255)
    background = models.CharField(default="default.jpg", max_length=255)


class Attempt(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    passed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)


class AttemptAnswer(models.Model):
    attempt = models.ForeignKey(Attempt, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=100)
    is_correct = models.BooleanField()


class Feedback(models.Model):
    attempt = models.OneToOneField(Attempt, on_delete=models.CASCADE, related_name="quiz_feedback")
    ai_review = models.TextField()
